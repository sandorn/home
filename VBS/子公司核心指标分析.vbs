Option Explicit

' 调试开关：需要查看 Debug.Print 时改为 True
Private Const DEBUG_MODE As Boolean = False

' API配置常量 - 建议从外部配置读取敏感信息
Private Const API_BASE_URL As String = "https://api.deepseek.com"
Private Const API_MODEL As String =  "deepseek-chat"    '"deepseek-reasoner"  
Private Const API_TIMEOUT_MS As Long = 30000 ' 请求超时时间（毫秒）
Private Const MAX_TOKENS As Long = 1000
Private Const TEMPERATURE As Double = 0.3

' 工作表数据范围常量
Private Const DATA_RANGE As String = "C1:R5"
Private Const RESULT_CELL As String = "C61"
Private Const CONFIG_SHEET As String = "填写页"
Private Const TARGET_RANGE As String = "C2:C10"
Private Const MONTH_NUMBER_CELL As String = "A2"
Private Const YEAR_CELL As String = "A4"
Private Const API_KEY_CELL As String = "I1"
Private Const SYSTEM_PROMPT_CELL As String = "C20"

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

' 系统消息模板改为从配置表读取（填写页!C20），为空时回退到默认模板
Private Function GetSystemMessage() As String
    Dim wsConfig As Worksheet
    Dim msg As String
    
    Set wsConfig = GetConfigSheet()
    If Not wsConfig Is Nothing Then
        msg = Trim$(CStr(wsConfig.Range(SYSTEM_PROMPT_CELL).Value))
    End If
    
    If Len(msg) = 0 Then
        msg = "### 月度经营数据分析提示词（优化版）" & vbCrLf & vbCrLf & _
              "1. 核心指令" & vbCrLf & _
              "请基于我提供的【公司名称】经营数据（数据单位：万元），参照“客观叙述为主、趋势分析为辅”的风格，形成半页PPT内容。" & vbCrLf & vbCrLf & _
              "2. 数据输入格式" & vbCrLf & _
              "数据以表格形式呈现，包含以下列：" & vbCrLf & _
              "指标、年度目标、实际达成、年度目标达成率、1月、2月、3月、……、12月。" & vbCrLf & _
              "数值均为数字，缺失月份可用空或“-”表示。" & vbCrLf & vbCrLf & _
              "3. 分析要求" & vbCrLf & _
              "- 简洁摘要：用一两句话总结最突出的特点（例如：“收入与利润达成率均过半，但现金流波动较大”）。" & vbCrLf & _
              "- 指标描述：对每个指标分别进行描述，需包含：" & vbCrLf & _
              "  - 累计达成率：与序时进度比较。序时进度根据数据中出现的最大月份计算（例如，若数据仅到2月，序时进度 = 2/12 ≈ 16.67%）。" & vbCrLf & _
              "  - 月度趋势：对已有数据的月份，描述环比变化（上升/下降/平稳），并判断波动是否剧烈（如波动大/平稳/缓慢上升等）。" & vbCrLf & _
              "  - 未发生月份：不进行趋势描述，但累计值基于已有月份计算。" & vbCrLf & _
              "- 表述风格：严格客观，只陈述“是什么”（如达成率XX%，环比上升/下降，累计为负），禁止使用主观色彩强烈的词汇（如崩盘、危机），禁止分析原因或提出行动建议。" & vbCrLf & _
              "- 聚焦数据：所有描述必须基于提供的具体数值，不得额外假设。" & vbCrLf & vbCrLf & _
              "4. 输出格式（严格执行）" & vbCrLf & _
              "第一行直接写摘要内容（1-2句客观陈述），不要输出“[简洁摘要]”或任何方括号占位符。" & vbCrLf & _
              "营业收入：<描述>" & vbCrLf & _
              "EBITDA/扣非利润：<描述>" & vbCrLf & _
              "经营活动净现金流：<描述>" & vbCrLf & _
              "经营支出小计：<描述>"
    End If
    
    GetSystemMessage = msg
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

' 创建HTTP对象（单例模式，但每次调用创建新对象以确保线程安全）
Private Function CreateHTTPObject() As Object
    On Error Resume Next
    Set CreateHTTPObject = CreateObject("MSXML2.ServerXMLHTTP.6.0")
    If Err.Number <> 0 Then
        Err.Clear
        Set CreateHTTPObject = CreateObject("MSXML2.XMLHTTP")
    End If
    On Error GoTo 0
End Function

' 构建JSON请求体（优化字符串拼接）
Private Function BuildJSONRequest(prompt As String) As String
    Dim jsonParts(1 To 5) As String
    
    jsonParts(1) = "{""model"":""" & API_MODEL & ""","
    jsonParts(2) = """messages"":[{""role"":""system"",""content"":""" & EscapeJSONString(GetSystemMessage()) & """},"
    jsonParts(3) = "{""role"":""user"",""content"":""" & EscapeJSONString(prompt) & """}],"
    jsonParts(4) = """temperature"":" & CStr(TEMPERATURE) & ","
    jsonParts(5) = """max_tokens"":" & CStr(MAX_TOKENS) & "}"
    
    BuildJSONRequest = Join(jsonParts, "")
End Function

' 调用DeepSeek API（优化版）
Private Function CallDeepSeekAPI(prompt As String, companyName As String) As String
    Dim http As Object
    Dim url As String
    Dim jsonBody As String
    Dim response As String
    Dim startTime As Double
    Dim apiKey As String
    Dim canSetTimeouts As Boolean
    
    ' 记录开始时间用于超时控制
    startTime = Timer
    
    ' 读取 API Key
    apiKey = GetApiKey()
    If Len(apiKey) = 0 Then
        CallDeepSeekAPI = "错误：未配置 API Key，请在 '" & CONFIG_SHEET & "' 工作表的 " & API_KEY_CELL & " 单元格中填写。"
        Exit Function
    End If
    
    ' 创建HTTP对象
    Set http = CreateHTTPObject()
    If http Is Nothing Then
        CallDeepSeekAPI = "错误：无法创建HTTP对象"
        Exit Function
    End If
    
    url = API_BASE_URL & "/chat/completions"
    jsonBody = BuildJSONRequest(prompt)
    
    If DEBUG_MODE Then
        Debug.Print "[" & companyName & "] 发送请求，长度: " & Len(jsonBody)
    End If
    
    canSetTimeouts = (InStr(1, TypeName(http), "ServerXMLHTTP", vbTextCompare) > 0)
    
    On Error GoTo HttpError
    With http
        .Open "POST", url, False
        .setRequestHeader "Content-Type", "application/json"
        .setRequestHeader "Authorization", "Bearer " & apiKey
        .setRequestHeader "Accept", "application/json"
        
        ' 仅在支持 ServerXMLHTTP 时设置超时时间，避免 XMLHTTP 抛错
        If canSetTimeouts Then
            On Error Resume Next
            .setTimeouts API_TIMEOUT_MS, API_TIMEOUT_MS, API_TIMEOUT_MS, API_TIMEOUT_MS
            Err.Clear
            On Error GoTo HttpError
        End If
        
        .send jsonBody
        If .Status = 200 Then
            response = .responseText
            If DEBUG_MODE Then
                Debug.Print "[" & companyName & "] API响应成功，长度: " & Len(response)
            End If
        Else
            response = "API调用失败: " & .Status & " - " & .statusText
            If DEBUG_MODE Then
                Debug.Print "[" & companyName & "] " & response
                If Len(.responseText) > 0 Then
                    Debug.Print "错误详情: " & Left$(.responseText, 500)
                End If
            End If
        End If
    End With
    
    ' 检查是否超时
    If (Timer - startTime) * 1000 > API_TIMEOUT_MS Then
        If DEBUG_MODE Then Debug.Print "[" & companyName & "] 警告：请求可能超时"
    End If
    
    CallDeepSeekAPI = response
    Exit Function
    
HttpError:
    CallDeepSeekAPI = "HTTP请求错误: " & Err.Description
End Function

' ============================================================================
' 数据准备模块
' ============================================================================

' 构建数据提示词（优化版）
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
    Dim prevWasEmpty As Boolean
    Dim currentLine As String
    
    If Len(result) = 0 Then
        CleanAnalysisResult = ""
        Exit Function
    End If
    
    lines = Split(result, vbCrLf)
    ReDim cleanedLines(0 To UBound(lines))
    lineCount = 0
    
    prevWasEmpty = True
    For i = 0 To UBound(lines)
        currentLine = Trim$(CStr(lines(i)))
        If currentLine = "" Then
            ' 保留单个空行，合并连续空行
            If Not prevWasEmpty Then
                cleanedLines(lineCount) = ""
                lineCount = lineCount + 1
                prevWasEmpty = True
            End If
        Else
            cleanedLines(lineCount) = currentLine
            lineCount = lineCount + 1
            prevWasEmpty = False
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
' 主业务流程
' ============================================================================

' 分析单个公司
Private Function AnalyzeCompany(companyName As String) As Boolean
    Dim wsTarget As Worksheet
    Dim wsData As Variant
    Dim dataPrompt As String
    Dim apiResponse As String
    Dim analysisResult As String
    Dim monthNumber As Long
    Dim monthText As String
    Dim progressPercent As Double
    
    On Error GoTo AnalyzeError
    
    ' 检查工作表是否存在（使用安全方式避免直接抛错）
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
    
    ' 构建提示词（月份/序时进度依赖填写页!A2）
    monthNumber = GetMonthNumberFromConfig()
    If monthNumber >= 1 And monthNumber <= 12 Then
        monthText = MonthNumberToText(monthNumber)
        progressPercent = (monthNumber / 12#) * 100#
    Else
        monthText = "未知"
        progressPercent = 0#
    End If
    
    dataPrompt = "公司名称：" & companyName & vbCrLf & _
                 "年份：" & GetAnalysisYear() & vbCrLf & _
                 "当前月份（按填写页参数）：" & monthText & vbCrLf & _
                 "序时进度：" & Format$(progressPercent, "0.00") & "%" & vbCrLf & _
                 "数据单位：万元" & vbCrLf & _
                 "请按系统提示词要求输出指定格式。" & vbCrLf & _
                 BuildDataPrompt(wsData)
    
    ' 调用API
    apiResponse = CallDeepSeekAPI(dataPrompt, companyName)
    
    ' 解析响应
    If Left(apiResponse, 5) = "API调用失败" Or _
       Left(apiResponse, 12) = "HTTP请求错误" Then
        analysisResult = apiResponse
    Else
        analysisResult = ParseAPIResponseSimple(apiResponse)
    End If
    
    ' 清理结果
    analysisResult = CleanAnalysisResult(analysisResult)
    
    ' 写入结果
    If Len(analysisResult) > 0 Then
        With wsTarget.Range(RESULT_CELL)
            .Value = analysisResult
            .WrapText = True
            .HorizontalAlignment = xlLeft
            .VerticalAlignment = xlTop
        End With
        
        
        If DEBUG_MODE Then Debug.Print companyName & " - 分析完成"
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

' 主分析函数 - 优化版本
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
    
    ' 设置错误处理
    On Error GoTo ErrorHandler
    
    ' 记录当前应用状态并关闭屏幕更新/事件/自动计算，提高性能
    prevScreenUpdating = Application.ScreenUpdating
    prevCalc = Application.Calculation
    prevEnableEvents = Application.EnableEvents
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False
    
    ' 获取配置信息
    Set wsConfig = ThisWorkbook.Worksheets(CONFIG_SHEET)
    Set targetSheetNames = wsConfig.Range(TARGET_RANGE)
    
    ' 统计待处理公司数量
    totalCount = 0
    For Each cell In targetSheetNames
        If Len(Trim(cell.Value)) > 0 Then totalCount = totalCount + 1
    Next cell
    
    If totalCount = 0 Then
        MsgBox "未找到待分析的公司名称，请在填写页C2:C10范围内填写。", vbExclamation
        GoTo Cleanup
    End If
    
    processedCount = 0
    
    ' 循环处理每个子公司
    For Each cell In targetSheetNames
        companyName = Trim(cell.Value)
        If Len(companyName) > 0 Then
            processedCount = processedCount + 1
            
            If AnalyzeCompany(companyName) Then
                If DEBUG_MODE Then Debug.Print "成功分析: " & companyName
            Else
                If DEBUG_MODE Then Debug.Print "分析失败: " & companyName
            End If
        End If
    Next cell
    
Cleanup:
    ' 恢复应用状态
    Application.Calculation = prevCalc
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating
    Application.StatusBar = False
    
    MsgBox "分析完成！共处理 " & processedCount & " 家公司。", vbInformation
    Exit Sub
    
ErrorHandler:
    ' 出错时恢复应用状态
    On Error Resume Next
    Application.Calculation = prevCalc
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating
    Application.StatusBar = False
    On Error GoTo 0
    
    MsgBox "错误: " & Err.Description & " (错误代码: " & Err.Number & ")", vbCritical
End Sub



