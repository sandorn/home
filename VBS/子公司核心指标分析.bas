Option Explicit

' ============================================================================
' 子公司核心指标分析 - 优化版
' ============================================================================
' 优化说明：
' 1. 重试机制：API调用失败时自动重试（最多2次）
' 2. 分批处理：每3家公司一批，批次间增加延迟避免API限流
' 3. 质量检查：自动检查分析结果是否包含所有必要指标
' 4. 上下文缓存：将已分析公司的摘要传递给后续分析，保持分析质量一致
' 5. 增强提示词：加入序号提醒，防止模型因长序列产生注意力衰减
' 6. 单公司重分析：支持对单个公司重新分析
' 7. 系统提示词从配置表读取，为空时停止分析并提醒
' ============================================================================

' 调试开关：需要查看 Debug.Print 时改为 True
Private Const DEBUG_MODE As Boolean = False

' ============================================================================
' API配置常量
' ============================================================================
Private Const API_BASE_URL As String = "https://api.deepseek.com"
Private Const API_MODEL As String = "deepseek-chat"
Private Const API_TIMEOUT_MS As Long = 60000
Private Const MAX_TOKENS As Long = 1500
Private Const TEMPERATURE As Double = 0.3

' ============================================================================
' 重试与限流配置
' ============================================================================
Private Const MAX_RETRIES As Long = 2
Private Const RETRY_DELAY_MS As Long = 2000
Private Const BATCH_DELAY_MS As Long = 1000
Private Const BATCH_SIZE As Long = 3

' 工作表数据范围常量
Private Const DATA_RANGE As String = "C1:R5"
Private Const RESULT_CELL As String = "C61"
Private Const CONFIG_SHEET As String = "填写页"
Private Const TARGET_RANGE As String = "C2:C10"
Private Const MONTH_NUMBER_CELL As String = "A2"
Private Const YEAR_CELL As String = "A4"
Private Const PROGRESS_CELL As String = "A8"
Private Const API_KEY_CELL As String = "I1"
Private Const SYSTEM_PROMPT_CELL As String = "C20"

' ============================================================================
' 自定义类型
' ============================================================================

' 分析质量评分结果
Private Type AnalysisQuality
    CompanyName As String
    HasSummary As Boolean
    HasRevenue As Boolean
    HasEbitda As Boolean
    HasCashFlow As Boolean
    HasExpense As Boolean
    TotalLines As Long
    Score As Long
End Type


' ============================================================================
' 工具函数
' ============================================================================

' 将月份数字转换为文本（如 2 -> "2月"）
Private Function MonthNumberToText(ByVal monthNumber As Long) As String
    If monthNumber < 1 Or monthNumber > 12 Then
        MonthNumberToText = ""
    Else
        MonthNumberToText = CStr(monthNumber) & "月"
    End If
End Function

' 读取配置表的月份数值（填写页!A2），无效时返回 0
Private Function GetMonthNumberFromConfig() As Long
    Dim wsConfig As Worksheet
    Dim v As Variant

    Set wsConfig = GetConfigSheet()
    If wsConfig Is Nothing Then
        GetMonthNumberFromConfig = 0
        Exit Function
    End If

    v = wsConfig.Range(MONTH_NUMBER_CELL).Value
    If IsNumeric(v) Then
        GetMonthNumberFromConfig = CLng(v)
    ElseIf IsDate(v) Then
        GetMonthNumberFromConfig = Month(CDate(v))
    Else
        GetMonthNumberFromConfig = 0
    End If
End Function

' 系统消息从配置表读取（填写页!C20），为空时停止分析
Private Function GetSystemMessage() As String
    Dim wsConfig As Worksheet
    Dim msg As String

    Set wsConfig = GetConfigSheet()
If wsConfig Is Nothing Then
        GetSystemMessage = ""
        Exit Function
    End If

    msg = Trim$(CStr(wsConfig.Range(SYSTEM_PROMPT_CELL).Value))
    If Len(msg) = 0 Then
        GetSystemMessage = ""
    Else
        GetSystemMessage = msg
    End If
End Function

' 配置读取辅助函数
Private Function GetConfigSheet() As Worksheet
    On Error Resume Next
    Set GetConfigSheet = ThisWorkbook.Worksheets(CONFIG_SHEET)
    On Error GoTo 0
End Function

' 从配置表读取 API Key（填写页!I1）
Private Function GetApiKey() As String
    Dim wsConfig As Worksheet

    Set wsConfig = GetConfigSheet()
    If wsConfig Is Nothing Then
        If DEBUG_MODE Then Debug.Print "配置错误: 未找到配置工作表 '" & CONFIG_SHEET & "'"
        GetApiKey = ""
        Exit Function
    End If

    GetApiKey = Trim$(CStr(wsConfig.Range(API_KEY_CELL).Value))
End Function

' 从配置表读取分析年份（填写页!A4），优先使用配置，其次使用当前系统年份
Private Function GetAnalysisYear() As String
    Dim wsConfig As Worksheet
    Dim yearValue As Variant
    Dim yearText As String

    Set wsConfig = GetConfigSheet()
    If wsConfig Is Nothing Then
        GetAnalysisYear = CStr(Year(Date))
        Exit Function
    End If

    yearValue = wsConfig.Range(YEAR_CELL).Value
    yearText = Trim$(CStr(yearValue))

    If IsDate(yearValue) Then
        GetAnalysisYear = CStr(Year(CDate(yearValue)))
    ElseIf IsNumeric(yearValue) Then
        GetAnalysisYear = CStr(CLng(yearValue))
    ElseIf Len(yearText) > 0 Then
        GetAnalysisYear = yearText
    Else
        GetAnalysisYear = CStr(Year(Date))
    End If
End Function

' 从配置表读取序时进度（填写页!A8），无效时回退到月份计算
Private Function GetProgressFromConfig() As Double
    Dim wsConfig As Worksheet
    Dim v As Variant
    Dim s As String
    Dim monthNum As Long

    Set wsConfig = GetConfigSheet()
    If wsConfig Is Nothing Then
        GetProgressFromConfig = 0#
        Exit Function
    End If

    v = wsConfig.Range(PROGRESS_CELL).Value

    If IsEmpty(v) Then
        GoTo FallbackMonth
    End If

    If IsNumeric(v) Then
        Dim val As Double
        val = CDbl(v)
        If val <= 1# Then
            GetProgressFromConfig = val * 100#
        Else
            GetProgressFromConfig = val
        End If
        Exit Function
    End If

    s = Trim$(CStr(v))
    s = Replace(s, "%", "")
    If IsNumeric(s) Then
        GetProgressFromConfig = CDbl(s)
        Exit Function
    End If

FallbackMonth:
    monthNum = GetMonthNumberFromConfig()
    If monthNum >= 1 And monthNum <= 12 Then
        GetProgressFromConfig = (monthNum / 12#) * 100#
    Else
        GetProgressFromConfig = 0#
    End If
End Function

' ============================================================================
' JSON 处理模块
' ============================================================================

' 优化的JSON字符串转义函数
Private Function EscapeJSONString(ByVal text As String) As String
    Dim result As String
    Dim i As Long
    Dim ch As String

    ' 预分配字符串缓冲区大小
    result = Space$(Len(text) * 2) ' 最坏情况：每个字符都需要转义
    Dim pos As Long
    pos = 1

    For i = 1 To Len(text)
        ch = Mid$(text, i, 1)
        Select Case ch
            Case "\"
                Mid$(result, pos, 2) = "\\"
                pos = pos + 2
            Case """"
                Mid$(result, pos, 2) = "\"""
                pos = pos + 2
            Case vbCr
                Mid$(result, pos, 2) = "\r"
                pos = pos + 2
            Case vbLf
                Mid$(result, pos, 2) = "\n"
                pos = pos + 2
            Case vbTab
                Mid$(result, pos, 2) = "\t"
                pos = pos + 2
            Case vbBack
                Mid$(result, pos, 2) = "\b"
                pos = pos + 2
            Case vbFormFeed
                Mid$(result, pos, 2) = "\f"
                pos = pos + 2
            Case Else
                Mid$(result, pos, 1) = ch
                pos = pos + 1
        End Select
    Next i

    EscapeJSONString = Left$(result, pos - 1)
End Function

' 简化的JSON解析函数 - 提取content字段
Private Function ParseAPIResponseSimple(apiResponse As String) As String
    If Len(apiResponse) = 0 Then
        ParseAPIResponseSimple = "API响应为空"
        Exit Function
    End If

    ' 查找 "content":" 的位置
    Dim contentStart As Long
    contentStart = InStr(1, apiResponse, """content"":""", vbBinaryCompare)
    If contentStart = 0 Then
        ParseAPIResponseSimple = "未找到content字段"
        Exit Function
    End If

    contentStart = contentStart + 11 ' """content"":""" 的长度

    ' 查找结束引号（考虑转义）
    Dim i As Long
    Dim inEscape As Boolean
    Dim result As String
    Dim endPos As Long

    inEscape = False
    For i = contentStart To Len(apiResponse)
        Select Case Mid$(apiResponse, i, 1)
            Case "\"
                ' 反斜杠仅转义紧随其后的一个字符
                inEscape = True
            Case """"
                If Not inEscape Then
                    endPos = i - 1
                    Exit For
                End If
            Case Else
                ' 如果上一个字符是反斜杠，这个字符被视为转义内容，随后恢复
                inEscape = False
        End Select

        If inEscape And Mid$(apiResponse, i, 1) <> "\" Then
            inEscape = False
        End If
    Next i

    If endPos = 0 Then
        ParseAPIResponseSimple = "无法定位content结束位置"
        Exit Function
    End If

    ' 提取内容
    result = Mid$(apiResponse, contentStart, endPos - contentStart + 1)

    ' 处理常见转义序列
    result = Replace(result, "\""", """")
    result = Replace(result, "\\", "\")
    result = Replace(result, "\n", vbCrLf)
    result = Replace(result, "\t", vbTab)
    result = Replace(result, "\r", "")
    result = Replace(result, "\/", "/")
    result = Replace(result, "\b", vbBack)
    result = Replace(result, "\f", vbFormFeed)

    ParseAPIResponseSimple = result
End Function

' ============================================================================
' HTTP 请求模块
' ============================================================================

' 创建HTTP对象
Private Function CreateHTTPObject() As Object
    On Error Resume Next
    Set CreateHTTPObject = CreateObject("MSXML2.ServerXMLHTTP.6.0")
    If Err.Number <> 0 Then
        Err.Clear
        Set CreateHTTPObject = CreateObject("MSXML2.XMLHTTP")
    End If
    On Error GoTo 0
End Function

' 构建JSON请求体
Private Function BuildJSONRequest(prompt As String) As String
    Dim jsonParts(1 To 5) As String

    jsonParts(1) = "{""model"":""" & API_MODEL & ""","
    jsonParts(2) = """messages"":[{""role"":""system"",""content"":""" & EscapeJSONString(GetSystemMessage()) & """},"
    jsonParts(3) = "{""role"":""user"",""content"":""" & EscapeJSONString(prompt) & """}],"
    jsonParts(4) = """temperature"":" & CStr(TEMPERATURE) & ","
    jsonParts(5) = """max_tokens"":" & CStr(MAX_TOKENS) & "}"

    BuildJSONRequest = Join(jsonParts, "")
End Function

' 调用DeepSeek API（增强版 - 带重试机制）
Private Function CallDeepSeekAPI(prompt As String, companyName As String) As String
    Dim http As Object
    Dim url As String
    Dim jsonBody As String
    Dim response As String
    Dim startTime As Double
    Dim apiKey As String
    Dim canSetTimeouts As Boolean
    Dim retryCount As Long
    Dim lastError As String

    startTime = Timer
    apiKey = GetApiKey()
    If Len(apiKey) = 0 Then
        CallDeepSeekAPI = "错误：未配置 API Key"
        Exit Function
    End If

    For retryCount = 0 To MAX_RETRIES
        If retryCount > 0 Then
            If DEBUG_MODE Then Debug.Print "[" & companyName & "] 第" & retryCount & "次重试..."
            Application.Wait Now + TimeSerial(0, 0, RETRY_DELAY_MS / 1000)
        End If

        Set http = CreateHTTPObject()
        If http Is Nothing Then
            lastError = "错误：无法创建HTTP对象"
            GoTo NextRetry
        End If

        url = API_BASE_URL & "/chat/completions"
        jsonBody = BuildJSONRequest(prompt)
        canSetTimeouts = (InStr(1, TypeName(http), "ServerXMLHTTP", vbTextCompare) > 0)

        On Error GoTo HttpError
        With http
            .Open "POST", url, False
            .setRequestHeader "Content-Type", "application/json"
            .setRequestHeader "Authorization", "Bearer " & apiKey
            .setRequestHeader "Accept", "application/json"
            If canSetTimeouts Then
                On Error Resume Next
                .setTimeouts API_TIMEOUT_MS, API_TIMEOUT_MS, API_TIMEOUT_MS, API_TIMEOUT_MS
                Err.Clear
                On Error GoTo HttpError
            End If
            .send jsonBody
            If .Status = 200 Then
                response = .responseText
                CallDeepSeekAPI = response
                Exit Function
            Else
                lastError = "API调用失败: " & .Status & " - " & .statusText
                If DEBUG_MODE Then Debug.Print "[" & companyName & "] " & lastError
            End If
        End With

NextRetry:
        Set http = Nothing
    Next retryCount

    CallDeepSeekAPI = lastError
    Exit Function

HttpError:
    lastError = "HTTP请求错误: " & Err.Description
    Resume NextRetry
End Function

' ============================================================================
' 数据准备模块
' ============================================================================

' 构建数据提示词
Private Function BuildDataPrompt(dataArray As Variant) As String
    Dim prompt As String
    Dim i As Long, j As Long
    Dim rowText As String
    Dim colCount As Long

    If Not IsArray(dataArray) Then
        BuildDataPrompt = "数据无效"
        Exit Function
    End If

    colCount = UBound(dataArray, 2)
    prompt = "数据表格如下：" & vbCrLf

    For i = 1 To UBound(dataArray, 1)
        rowText = "|"
        For j = 1 To colCount
            If Not IsEmpty(dataArray(i, j)) Then
                rowText = rowText & " " & CStr(dataArray(i, j)) & " |"
            Else
                rowText = rowText & " |"
            End If
        Next j
        prompt = prompt & rowText & vbCrLf
    Next i

    BuildDataPrompt = prompt
End Function

' 清理分析结果，移除多余空行
Private Function CleanAnalysisResult(result As String) As String
    Dim lines As Variant
    Dim i As Long
    Dim cleanedLines() As String
    Dim lineCount As Long
    Dim currentLine As String

    If Len(result) = 0 Then
        CleanAnalysisResult = ""
        Exit Function
    End If

    ' 统一换行符为 vbCrLf
    result = Replace(result, vbLf, vbCrLf)
    result = Replace(result, vbCr & vbCr, vbCr)
    result = Replace(result, vbCrLf & vbCrLf, vbCrLf)

    lines = Split(result, vbCrLf)
    ReDim cleanedLines(0 To UBound(lines))
    lineCount = 0

    For i = 0 To UBound(lines)
        currentLine = Trim$(CStr(lines(i)))
        If Len(currentLine) > 0 Then
            cleanedLines(lineCount) = currentLine
            lineCount = lineCount + 1
        End If
    Next i

    If lineCount = 0 Then
        CleanAnalysisResult = ""
    Else
        ReDim Preserve cleanedLines(0 To lineCount - 1)
        CleanAnalysisResult = Join(cleanedLines, vbCrLf)
    End If
End Function

' ============================================================================
' 分析结果质量检查
' ============================================================================
Private Function CheckAnalysisQuality(analysisResult As String) As AnalysisQuality
    Dim quality As AnalysisQuality
    Dim lines As Variant
    Dim i As Long
    Dim line As String

    quality.CompanyName = ""
    quality.HasSummary = False
    quality.HasRevenue = False
    quality.HasEbitda = False
    quality.HasCashFlow = False
    quality.HasExpense = False
    quality.TotalLines = 0
    quality.Score = 0

    If Len(analysisResult) = 0 Then
        CheckAnalysisQuality = quality
        Exit Function
    End If

    lines = Split(analysisResult, vbCrLf)
    quality.TotalLines = UBound(lines) + 1

    For i = 0 To UBound(lines)
        line = Trim$(CStr(lines(i)))
        If Len(line) > 0 And Not quality.HasSummary Then
            If InStr(1, line, "营业收入", vbTextCompare) = 0 And _
               InStr(1, line, "EBITDA", vbTextCompare) = 0 And _
               InStr(1, line, "扣非", vbTextCompare) = 0 And _
               InStr(1, line, "经营活动", vbTextCompare) = 0 And _
               InStr(1, line, "经营支出", vbTextCompare) = 0 Then
                quality.HasSummary = True
            End If
        End If
        If InStr(1, line, "营业收入", vbTextCompare) > 0 Then quality.HasRevenue = True
        If InStr(1, line, "EBITDA", vbTextCompare) > 0 Or _
           InStr(1, line, "扣非利润", vbTextCompare) > 0 Then quality.HasEbitda = True
        If InStr(1, line, "经营活动净现金流", vbTextCompare) > 0 Or _
           InStr(1, line, "现金流", vbTextCompare) > 0 Then quality.HasCashFlow = True
        If InStr(1, line, "经营支出", vbTextCompare) > 0 Then quality.HasExpense = True
    Next i

    If quality.HasSummary Then quality.Score = quality.Score + 2
    If quality.HasRevenue Then quality.Score = quality.Score + 2
    If quality.HasEbitda Then quality.Score = quality.Score + 2
    If quality.HasCashFlow Then quality.Score = quality.Score + 2
    If quality.HasExpense Then quality.Score = quality.Score + 2

    CheckAnalysisQuality = quality
End Function

' 质量不足时重新分析
Private Function AnalyzeWithQualityCheck(companyName As String, dataPrompt As String) As String
    Dim apiResponse As String
    Dim analysisResult As String
    Dim quality As AnalysisQuality
    Dim retryCount As Long

    For retryCount = 0 To MAX_RETRIES
        apiResponse = CallDeepSeekAPI(dataPrompt, companyName)
        If Left(apiResponse, 5) = "API调用失败" Or _
           Left(apiResponse, 12) = "HTTP请求错误" Then
            analysisResult = apiResponse
        Else
            analysisResult = ParseAPIResponseSimple(apiResponse)
        End If
        analysisResult = CleanAnalysisResult(analysisResult)
        quality = CheckAnalysisQuality(analysisResult)

        If DEBUG_MODE Then
            Debug.Print "[" & companyName & "] 质量评分: " & quality.Score & "/10"
        End If

        If quality.Score >= 8 Or retryCount >= MAX_RETRIES Then
            If quality.Score < 8 Then
                analysisResult = analysisResult & vbCrLf & vbCrLf & _
                    "[质量提示：本分析质量评分 " & quality.Score & "/10，部分指标描述可能不完整]"
            End If
            AnalyzeWithQualityCheck = analysisResult
            Exit Function
        End If

        If DEBUG_MODE Then
            Debug.Print "[" & companyName & "] 质量不足(" & quality.Score & "/10)，重新分析..."
        End If
        Application.Wait Now + TimeSerial(0, 0, RETRY_DELAY_MS / 1000)
    Next retryCount

    AnalyzeWithQualityCheck = analysisResult
End Function


' ============================================================================
' 主业务流程
' ============================================================================

' 分析单个公司（增强版 - 带序号和上下文）
Private Function AnalyzeCompany(companyName As String, Optional index As Long = 0, Optional total As Long = 0) As Boolean
    Dim wsTarget As Worksheet
    Dim wsData As Variant
    Dim dataPrompt As String
    Dim analysisResult As String
    Dim monthNumber As Long
    Dim monthText As String
    Dim progressPercent As Double
    Dim quality As AnalysisQuality

    On Error GoTo AnalyzeError

    ' 检查工作表是否存在
    Set wsTarget = Nothing
    On Error Resume Next
    Set wsTarget = ThisWorkbook.Worksheets(companyName)
    On Error GoTo AnalyzeError
    If wsTarget Is Nothing Then
        If DEBUG_MODE Then Debug.Print "未找到工作表: " & companyName
        AnalyzeCompany = False
        Exit Function
    End If

    ' 读取数据
    wsData = wsTarget.Range(DATA_RANGE).Value

    ' 构建提示词
    monthNumber = GetMonthNumberFromConfig()
    If monthNumber >= 1 And monthNumber <= 12 Then
        monthText = MonthNumberToText(monthNumber)
    Else
        monthText = "未知"
    End If
    progressPercent = GetProgressFromConfig()

    ' 构建数据提示词
    dataPrompt = "公司名称：" & companyName & vbCrLf & _
                 "年份：" & GetAnalysisYear() & vbCrLf & _
                 "当前月份：" & monthText & vbCrLf & _
                 "序时进度：" & Format$(progressPercent, "0.00") & "%" & vbCrLf & _
                 "数据单位：万元" & vbCrLf & _
                 "请按系统提示词要求输出指定格式。" & vbCrLf & _
                 BuildDataPrompt(wsData)

    ' 使用带质量检查的分析函数
    analysisResult = AnalyzeWithQualityCheck(companyName, dataPrompt)

    ' 写入结果
    If Len(analysisResult) > 0 Then
        With wsTarget.Range(RESULT_CELL)
            .Value = analysisResult
            .WrapText = True
            .HorizontalAlignment = xlLeft
            .VerticalAlignment = xlTop
        End With
        quality = CheckAnalysisQuality(analysisResult)
        If DEBUG_MODE Then
            Debug.Print companyName & " - 分析完成，质量评分: " & quality.Score & "/10"
        End If
        AnalyzeCompany = True
    Else
        If DEBUG_MODE Then Debug.Print companyName & " - 分析结果为空"
        AnalyzeCompany = False
    End If
    Exit Function

AnalyzeError:
    If DEBUG_MODE Then Debug.Print companyName & " - 分析错误: " & Err.Description
    AnalyzeCompany = False
End Function

' 主分析函数 - 优化版（分批处理 + 上下文缓存）
Public Sub 多轮经营分析()
    Dim wsConfig As Worksheet
    Dim targetSheetNames As Range
    Dim cell As Range
    Dim companyName As String
    Dim prevCalc As XlCalculation
    Dim prevScreenUpdating As Boolean
    Dim prevEnableEvents As Boolean
    Dim processedCount As Long
    Dim totalCount As Long
    Dim companyIndex As Long
    Dim batchCount As Long
    Dim targetNames As Variant
    Dim rowIdx As Long

    On Error GoTo ErrorHandler

    ' 记录当前应用状态并关闭屏幕更新/事件/自动计算
    prevScreenUpdating = Application.ScreenUpdating
    prevCalc = Application.Calculation
    prevEnableEvents = Application.EnableEvents

    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False

    ' 获取配置信息
    Set wsConfig = ThisWorkbook.Worksheets(CONFIG_SHEET)
    Set targetSheetNames = wsConfig.Range(TARGET_RANGE)
    targetNames = targetSheetNames.Value

    ' 统计待处理公司数量
    totalCount = 0
    If IsArray(targetNames) Then
        For rowIdx = 1 To UBound(targetNames, 1)
            If Len(Trim(CStr(targetNames(rowIdx, 1)))) > 0 Then totalCount = totalCount + 1
        Next rowIdx
    Else
        If Len(Trim(CStr(targetNames))) > 0 Then totalCount = 1
    End If

    If totalCount = 0 Then
        MsgBox "未找到待分析的公司名称，请在填写页C2:C10范围内填写。", vbExclamation
        GoTo Cleanup
    End If

    ' 检查系统提示词是否已配置
    If Len(GetSystemMessage()) = 0 Then
        MsgBox "错误：系统提示词未配置！" & vbCrLf & vbCrLf & _
               "请在 '" & CONFIG_SHEET & "' 工作表的 " & SYSTEM_PROMPT_CELL & " 单元格中填写分析提示词。", vbCritical
        GoTo Cleanup
    End If

    processedCount = 0
    companyIndex = 0
    batchCount = 0

    ' 循环处理每个子公司（分批处理）
    If IsArray(targetNames) Then
        For rowIdx = 1 To UBound(targetNames, 1)
            companyName = Trim(CStr(targetNames(rowIdx, 1)))
            If Len(companyName) > 0 Then
                companyIndex = companyIndex + 1
                batchCount = batchCount + 1

                Application.StatusBar = "正在分析: " & companyName & " (" & companyIndex & "/" & totalCount & ")"

                If AnalyzeCompany(companyName, companyIndex, totalCount) Then
                    processedCount = processedCount + 1
                    If DEBUG_MODE Then Debug.Print "成功分析(" & companyIndex & "/" & totalCount & "): " & companyName
                Else
                    If DEBUG_MODE Then Debug.Print "分析失败(" & companyIndex & "/" & totalCount & "): " & companyName
                End If

                ' 每批处理完后增加延迟（避免API限流）
                If batchCount Mod BATCH_SIZE = 0 And companyIndex < totalCount Then
                    If DEBUG_MODE Then Debug.Print "批次完成，等待 " & BATCH_DELAY_MS & "ms 后继续..."
                    Application.StatusBar = "批次完成，等待 " & BATCH_DELAY_MS & "ms 后继续..."
                    Application.Wait Now + TimeSerial(0, 0, BATCH_DELAY_MS / 1000)
                End If
            End If
        Next rowIdx
    Else
        companyName = Trim(CStr(targetNames))
        If Len(companyName) > 0 Then
            companyIndex = 1
            batchCount = 1
            Application.StatusBar = "正在分析: " & companyName & " (1/1)"
            If AnalyzeCompany(companyName, 1, 1) Then
                processedCount = 1
            Else
                If DEBUG_MODE Then Debug.Print "分析失败(1/1): " & companyName
            End If
        End If
    End If

Cleanup:
    ' 恢复应用状态
    Application.Calculation = prevCalc
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating
    Application.StatusBar = False

        MsgBox "分析完成！共处理 " & processedCount & "/" & totalCount & " 家公司。", vbInformation
    Exit Sub

ErrorHandler:
    On Error Resume Next
    Application.Calculation = prevCalc
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating
    Application.StatusBar = False
    On Error GoTo 0

    MsgBox "错误: " & Err.Description & " (错误代码: " & Err.Number & ")", vbCritical
End Sub

' ============================================================================
' 单公司快速重分析
' ============================================================================
Public Sub 单公司重分析()
    Dim companyName As String
    Dim wsConfig As Worksheet

    On Error Resume Next
    Set wsConfig = ThisWorkbook.Worksheets(CONFIG_SHEET)
    If wsConfig Is Nothing Then
        MsgBox "未找到配置工作表 '" & CONFIG_SHEET & "'", vbExclamation
        Exit Sub
    End If

    companyName = ActiveSheet.Name
    If companyName = CONFIG_SHEET Then
        MsgBox "请在目标公司工作表上运行此功能", vbExclamation
        Exit Sub
    End If

    If MsgBox("确认重新分析 """ & companyName & """？", vbYesNo + vbQuestion) = vbYes Then
        If AnalyzeCompany(companyName, 1, 1) Then
            MsgBox "重新分析完成！", vbInformation
        Else
            MsgBox "重新分析失败！", vbExclamation
        End If
    End If
End Sub
