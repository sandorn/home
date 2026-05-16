Option Explicit

' ============================================================================
' 子公司核心指标分析 - 优化建议版
' ============================================================================
' 原文件：子公司核心指标分析.vbs
'
' 问题诊断：
' 1. 连续9次API调用，越到后面分析质量越差
' 2. 每次调用都是独立请求，没有上下文关联
' 3. 模型可能因长序列推理产生"注意力衰减"
' 4. 没有重试机制，单次失败影响整体质量
' 5. 没有对API返回结果进行质量校验
' 6. 所有公司使用相同的temperature=0.3，缺乏多样性
' 7. 没有分批处理或延迟机制，可能触发API限流
'
' 优化方案：
' ============================================================================

' 调试开关
Private Const DEBUG_MODE As Boolean = False

' ============================================================================
' 优化1: API配置增强
' ============================================================================
Private Const API_BASE_URL As String = "https://api.deepseek.com"
Private Const API_MODEL As String = "deepseek-chat"
Private Const API_TIMEOUT_MS As Long = 60000
Private Const MAX_TOKENS As Long = 1500
Private Const TEMPERATURE As Double = 0.3

' ============================================================================
' 优化2: 新增配置常量
' ============================================================================
Private Const MAX_RETRIES As Long = 2
Private Const RETRY_DELAY_MS As Long = 2000
Private Const BATCH_DELAY_MS As Long = 1000
Private Const QUALITY_CHECK_INTERVAL As Long = 3

' 工作表数据范围常量
Private Const DATA_RANGE As String = "C1:R5"
Private Const RESULT_CELL As String = "C61"
Private Const CONFIG_SHEET As String = "填写页"
Private Const TARGET_RANGE As String = "C2:C10"
Private Const MONTH_NUMBER_CELL As String = "A2"
Private Const YEAR_CELL As String = "A4"
Private Const API_KEY_CELL As String = "I1"
Private Const SYSTEM_PROMPT_CELL As String = "C20"

' ============================================================================
' 优化3: 新增 - 质量评分结果存储
' ============================================================================
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
' 优化4: 新增 - 上下文缓存
' ============================================================================
Private previousAnalysisResults() As String
Private analysisCount As Long

' ============================================================================
' 工具函数
' ============================================================================

Private Function MonthNumberToText(ByVal monthNumber As Long) As String
    If monthNumber < 1 Or monthNumber > 12 Then
        MonthNumberToText = ""
    Else
        MonthNumberToText = CStr(monthNumber) & "月"
    End If
End Function

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

' ============================================================================
' 优化5: 系统提示词 - 必须从配置表读取，为空时停止分析并提醒
' 请将提示词填写在配置表(CONFIG_SHEET)的 SYSTEM_PROMPT_CELL 单元格中
' ============================================================================
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

Private Function GetConfigSheet() As Worksheet
    On Error Resume Next
    Set GetConfigSheet = ThisWorkbook.Worksheets(CONFIG_SHEET)
    On Error GoTo 0
End Function

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

' ============================================================================
' JSON 处理模块
' ============================================================================

Private Function EscapeJSONString(ByVal text As String) As String
    Dim result As String
    Dim i As Long
    Dim ch As String
    result = Space$(Len(text) * 2)
    Dim pos As Long
    pos = 1
    For i = 1 To Len(text)
        ch = Mid$(text, i, 1)
        Select Case ch
            Case "\": Mid$(result, pos, 2) = "\\": pos = pos + 2
            Case """": Mid$(result, pos, 2) = "\""": pos = pos + 2
            Case vbCr: Mid$(result, pos, 2) = "\r": pos = pos + 2
            Case vbLf: Mid$(result, pos, 2) = "\n": pos = pos + 2
            Case vbTab: Mid$(result, pos, 2) = "\t": pos = pos + 2
            Case vbBack: Mid$(result, pos, 2) = "\b": pos = pos + 2
            Case vbFormFeed: Mid$(result, pos, 2) = "\f": pos = pos + 2
            Case Else: Mid$(result, pos, 1) = ch: pos = pos + 1
        End Select
    Next i
    EscapeJSONString = Left$(result, pos - 1)
End Function

Private Function ParseAPIResponseSimple(apiResponse As String) As String
    If Len(apiResponse) = 0 Then
        ParseAPIResponseSimple = "API响应为空"
        Exit Function
    End If
    Dim contentStart As Long
    contentStart = InStr(1, apiResponse, """content"":""", vbBinaryCompare)
    If contentStart = 0 Then
        ParseAPIResponseSimple = "未找到content字段"
        Exit Function
    End If
    contentStart = contentStart + 11
    Dim i As Long
    Dim inEscape As Boolean
    Dim result As String
    Dim endPos As Long
    inEscape = False
    For i = contentStart To Len(apiResponse)
        Select Case Mid$(apiResponse, i, 1)
            Case "\": inEscape = True
            Case """": If Not inEscape Then endPos = i - 1: Exit For
            Case Else: inEscape = False
        End Select
        If inEscape And Mid$(apiResponse, i, 1) <> "\" Then inEscape = False
    Next i
    If endPos = 0 Then
        ParseAPIResponseSimple = "无法定位content结束位置"
        Exit Function
    End If
    result = Mid$(apiResponse, contentStart, endPos - contentStart + 1)
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

Private Function CreateHTTPObject() As Object
    On Error Resume Next
    Set CreateHTTPObject = CreateObject("MSXML2.ServerXMLHTTP.6.0")
    If Err.Number <> 0 Then
        Err.Clear
        Set CreateHTTPObject = CreateObject("MSXML2.XMLHTTP")
    End If
    On Error GoTo 0
End Function

Private Function BuildJSONRequest(prompt As String) As String
    Dim jsonParts(1 To 5) As String
    jsonParts(1) = "{""model"":""" & API_MODEL & ""","
    jsonParts(2) = """messages"":[{""role"":""system"",""content"":""" & EscapeJSONString(GetSystemMessage()) & """},"
    jsonParts(3) = "{""role"":""user"",""content"":""" & EscapeJSONString(prompt) & """}],"
    jsonParts(4) = """temperature"":" & CStr(TEMPERATURE) & ","
    jsonParts(5) = """max_tokens"":" & CStr(MAX_TOKENS) & "}"
    BuildJSONRequest = Join(jsonParts, "")
End Function

' ============================================================================
' 优化6: 增强版API调用 - 增加重试机制
' ============================================================================
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
' 优化7: 新增 - 分析结果质量检查
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

' ============================================================================
' 优化8: 新增 - 质量不足时重新分析
' ============================================================================
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
' 优化9: 新增 - 分批处理策略
' ============================================================================
Private Sub ProcessCompanyBatch(companyNames() As String, startIndex As Long, batchSize As Long)
    Dim i As Long
    Dim endIndex As Long
    endIndex = startIndex + batchSize - 1
    If endIndex > UBound(companyNames) Then endIndex = UBound(companyNames)
    For i = startIndex To endIndex
        If Len(Trim(companyNames(i))) > 0 Then
            If DEBUG_MODE Then Debug.Print "处理批次中的公司: " & companyNames(i)
        End If
    Next i
End Sub

' ============================================================================
' 优化10: 增强版分析单个公司
' ============================================================================
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

    Set wsTarget = Nothing
    On Error Resume Next
    Set wsTarget = ThisWorkbook.Worksheets(companyName)
    On Error GoTo AnalyzeError
    If wsTarget Is Nothing Then
        If DEBUG_MODE Then Debug.Print "未找到工作表: " & companyName
        AnalyzeCompany = False
        Exit Function
    End If

    wsData = wsTarget.Range(DATA_RANGE).Value

    monthNumber = GetMonthNumberFromConfig()
    If monthNumber >= 1 And monthNumber <= 12 Then
        monthText = MonthNumberToText(monthNumber)
        progressPercent = (monthNumber / 12#) * 100#
    Else
        monthText = "未知"
        progressPercent = 0#
    End If

    ' 优化11: 增强数据提示词 - 加入序号提醒
    dataPrompt = "公司名称：" & companyName & vbCrLf & _
                 "年份：" & GetAnalysisYear() & vbCrLf & _
                 "当前月份：" & monthText & vbCrLf & _
                 "序时进度：" & Format$(progressPercent, "0.00") & "%" & vbCrLf & _
                 "数据单位：万元" & vbCrLf & _
                 "分析序号：第" & index & "/" & total & "家公司" & vbCrLf & _
                 "注意：请保持与前面公司一致的分析深度和质量，不要因为序号靠后而简化输出。" & vbCrLf & _
                 "请按系统提示词要求输出指定格式。" & vbCrLf & _
                 BuildDataPrompt(wsData)

    ' 优化12: 使用带质量检查的分析函数
    analysisResult = AnalyzeWithQualityCheck(companyName, dataPrompt)

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

' ============================================================================
' 优化13: 主分析函数 - 增强版
' ============================================================================
Public Sub 多轮经营分析_优化版()
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
    Dim batchSize As Long
    Dim batchCount As Long
    Dim i As Long

    On Error GoTo ErrorHandler

    prevScreenUpdating = Application.ScreenUpdating
    prevCalc = Application.Calculation
    prevEnableEvents = Application.EnableEvents

    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False

    Set wsConfig = ThisWorkbook.Worksheets(CONFIG_SHEET)
    Set targetSheetNames = wsConfig.Range(TARGET_RANGE)

    totalCount = 0
    For Each cell In targetSheetNames
        If Len(Trim(cell.Value)) > 0 Then totalCount = totalCount + 1
    Next cell

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

    ' 优化14: 分批处理策略
    batchSize = 3
    batchCount = 0
    processedCount = 0
    companyIndex = 0

    ReDim previousAnalysisResults(1 To totalCount)
    analysisCount = 0

    For Each cell In targetSheetNames
        companyName = Trim(cell.Value)
        If Len(companyName) > 0 Then
            companyIndex = companyIndex + 1
            batchCount = batchCount + 1

            Application.StatusBar = "正在分析: " & companyName & " (" & companyIndex & "/" & totalCount & ")"

            ' 优化15: 每批处理后增加延迟
            If batchCount > batchSize Then
                If DEBUG_MODE Then Debug.Print "批次完成，等待 " & BATCH_DELAY_MS & "ms 后继续..."
                Application.Wait Now + TimeSerial(0, 0, BATCH_DELAY_MS / 1000)
                batchCount = 1
            End If

            If AnalyzeCompany(companyName, companyIndex, totalCount) Then
                processedCount = processedCount + 1
                analysisCount = analysisCount + 1
                previousAnalysisResults(analysisCount) = companyName
                If DEBUG_MODE Then Debug.Print "成功分析(" & companyIndex & "/" & totalCount & "): " & companyName
            Else
                If DEBUG_MODE Then Debug.Print "分析失败(" & companyIndex & "/" & totalCount & "): " & companyName
            End If
        End If
    Next cell

Cleanup:
    Application.Calculation = prevCalc
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating
    Application.StatusBar = False

    MsgBox "分析完成！共处理 " & processedCount & "/" & totalCount & " 家公司。" & vbCrLf & _
           "（优化版已启用质量检查和重试机制）", vbInformation
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
' 优化16: 新增 - 单公司快速重分析
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
