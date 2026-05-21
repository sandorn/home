Option Explicit

' 调试开关：需要查看 Debug.Print 时改为 True
Private Const DEBUG_MODE As Boolean = False

' API 配置常量
Private Const API_BASE_URL As String = "https://api.deepseek.com"
Private Const API_MODEL As String =  "deepseek-chat"    '"deepseek-reasoner"  
Private Const API_TIMEOUT_MS As Long = 30000 ' 毫秒
Private Const MAX_TOKENS As Long = 1000
Private Const TEMPERATURE As Double = 0.3

' 工作表与配置常量
Private Const INSURANCE_SHEET As String = "保险类"
Private Const DATA_RANGE As String = "F2:H25"
Private Const RESULT_CELL As String = "L14"
Private Const SYSTEM_PROMPT_CELL As String = "L1"
Private Const API_KEY_FILE As String = "dskey"
Private Const API_KEY_SECTION As String = "EXCEL"
Private Const MONTH_NUMBER_CELL As String = "A2"

' 系统消息从保险类!L1读取，为空时返回空字符串（由调用方处理）
Private Function GetSystemMessage() As String
    Dim wsInsurance As Worksheet
    
    On Error Resume Next
    Set wsInsurance = ThisWorkbook.Worksheets(INSURANCE_SHEET)
    On Error GoTo 0
    If wsInsurance Is Nothing Then
        GetSystemMessage = ""
        Exit Function
    End If
    
    GetSystemMessage = Trim$(CStr(wsInsurance.Range(SYSTEM_PROMPT_CELL).Value))
End Function

' 从 ~/.dskey 文件读取 API Key（EXCEL 段）
Private Function GetApiKey() As String
    Dim filePath As String
    Dim fileNum As Integer
    Dim line As String
    Dim keyPrefix As String
    Dim pos As Long
    
    ' 构建文件路径：~/.dskey
    filePath = Environ("USERPROFILE") & "\." & API_KEY_FILE
    
    ' 检查文件是否存在
    On Error Resume Next
    fileNum = FreeFile
    Open filePath For Input As #fileNum
    If Err.Number <> 0 Then
        If DEBUG_MODE Then Debug.Print "配置错误: 未找到 API Key 文件 '" & filePath & "'"
        GetApiKey = ""
        Exit Function
    End If
    On Error GoTo 0
    
    keyPrefix = API_KEY_SECTION & "="
    
    ' 逐行读取，查找对应段
    Do Until EOF(fileNum)
        Line Input #fileNum, line
        line = Trim$(line)
        ' 跳过空行和注释行
        If Len(line) > 0 And Left$(line, 1) <> "#" Then
            pos = InStr(1, line, keyPrefix, vbTextCompare)
            If pos > 0 Then
                GetApiKey = Trim$(Mid$(line, pos + Len(keyPrefix)))
                Close #fileNum
                Exit Function
            End If
        End If
    Loop
    
    Close #fileNum
    
    If DEBUG_MODE Then Debug.Print "配置错误: 未在 '" & filePath & "' 中找到 [" & API_KEY_SECTION & "] 的 API Key"
    GetApiKey = ""
End Function

' ============================================================================
' JSON 处理模块
' ============================================================================

' JSON 字符串转义
Private Function EscapeJSONString(ByVal text As String) As String
    Dim result As String
    Dim i As Long
    Dim ch As String
    Dim pos As Long
    
    result = Space$(Len(text) * 2)
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

' 简化的 JSON 解析函数 - 提取 content 字段
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
        If inEscape Then
            inEscape = False
        Else
            Select Case Mid$(apiResponse, i, 1)
                Case "\" : inEscape = True
                Case """" : endPos = i - 1 : Exit For
            End Select
        End If
    Next i
    
    If endPos = 0 Then
        ParseAPIResponseSimple = "无法定位content结束位置"
        Exit Function
    End If
    
    result = Mid$(apiResponse, contentStart, endPos - contentStart + 1)
    
    result = Replace(result, "\""", """")
    result = Replace(result, "\n", vbCrLf)
    result = Replace(result, "\t", vbTab)
    result = Replace(result, "\r", "")
    result = Replace(result, "\/", "/")
    result = Replace(result, "\b", vbBack)
    result = Replace(result, "\f", vbFormFeed)
    result = Replace(result, "\\", "\")
    
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

Private Function CallDeepSeekAPI(prompt As String, contextName As String) As String
    Dim http As Object
    Dim url As String
    Dim jsonBody As String
    Dim response As String
    Dim startTime As Double
    Dim apiKey As String
    Dim canSetTimeouts As Boolean
    
    startTime = Timer
    
    apiKey = GetApiKey()
    If Len(apiKey) = 0 Then
        CallDeepSeekAPI = "错误：未配置 API Key，请在 ~\." & API_KEY_FILE & " 文件中设置 [" & API_KEY_SECTION & "] 段。"
        Exit Function
    End If
    
    Set http = CreateHTTPObject()
    If http Is Nothing Then
        CallDeepSeekAPI = "错误：无法创建HTTP对象"
        Exit Function
    End If
    
    url = API_BASE_URL & "/chat/completions"
    jsonBody = BuildJSONRequest(prompt)
    
    If DEBUG_MODE Then
        Debug.Print "[" & contextName & "] 发送请求，长度: " & Len(jsonBody)
    End If
    
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
            If DEBUG_MODE Then
                Debug.Print "[" & contextName & "] API响应成功，长度: " & Len(response)
            End If
        Else
            response = "API调用失败: " & .Status & " - " & .statusText
            If DEBUG_MODE Then
                Debug.Print "[" & contextName & "] " & response
                If Len(.responseText) > 0 Then
                    Debug.Print "错误详情: " & Left$(.responseText, 500)
                End If
            End If
        End If
    End With
    
    If (Timer - startTime) * 1000 > API_TIMEOUT_MS Then
        If DEBUG_MODE Then Debug.Print "[" & contextName & "] 警告：请求可能超时"
    End If
    
    CallDeepSeekAPI = response
    Exit Function
    
HttpError:
    CallDeepSeekAPI = "HTTP请求错误: " & Err.Description
End Function

' ============================================================================
' 数据准备模块
' ============================================================================

Private Function GetCurrentMonthNumber() As Long
    Dim wsCfg As Worksheet
    Dim v As Variant
    
    On Error Resume Next
    Set wsCfg = ThisWorkbook.Worksheets("填写页")
    On Error GoTo 0
    If wsCfg Is Nothing Then
        GetCurrentMonthNumber = 0
        Exit Function
    End If
    
    v = wsCfg.Range(MONTH_NUMBER_CELL).Value
    If IsNumeric(v) Then
        GetCurrentMonthNumber = CLng(v)
    ElseIf IsDate(v) Then
        GetCurrentMonthNumber = Month(CDate(v))
    Else
        GetCurrentMonthNumber = 0
    End If
End Function

Private Function ParseMonthLabel(ByVal label As String) As Long
    Dim t As String
    t = Trim$(label)
    If Len(t) = 0 Then
        ParseMonthLabel = 0
        Exit Function
    End If
    If Right$(t, 1) = "月" Then
        t = Left$(t, Len(t) - 1)
    End If
    If IsNumeric(t) Then
        ParseMonthLabel = CLng(t)
    Else
        ParseMonthLabel = 0
    End If
End Function

Private Function BuildDataPrompt(dataArray As Variant) As String
    Dim prompt As String
    Dim i As Long, j As Long
    Dim rowText As String
    Dim colCount As Long
    Dim inScaleSection As Boolean
    Dim currentMonth As Long
    Dim monthLabel As String
    Dim monthNumber As Long
    
    If Not IsArray(dataArray) Then
        BuildDataPrompt = "数据无效"
        Exit Function
    End If
    
    colCount = UBound(dataArray, 2)
    currentMonth = GetCurrentMonthNumber()
    prompt = "数据表格如下：" & vbCrLf
    
    For i = 1 To UBound(dataArray, 1)
        ' 识别是否进入“规模保费”部分
        If Not IsEmpty(dataArray(i, 1)) Then
            If Trim$(CStr(dataArray(i, 1))) = "规模保费" Then
                inScaleSection = True
            ElseIf Trim$(CStr(dataArray(i, 1))) = "项目" Then
                inScaleSection = False
            End If
        End If
        
        ' 对规模保费部分的月份行做过滤：只保留填写页 A2 及之前的月份
        If inScaleSection And i > 1 Then
            monthLabel = CStr(dataArray(i, 1))
            monthNumber = ParseMonthLabel(monthLabel)
            If monthNumber > 0 And currentMonth > 0 And monthNumber > currentMonth Then
                ' 跳过超过当前月份的行
                GoTo NextRow
            End If
        End If
        
        rowText = "|"
        For j = 1 To colCount
            If Not IsEmpty(dataArray(i, j)) Then
                rowText = rowText & " " & CStr(dataArray(i, j)) & " |"
            Else
                rowText = rowText & " |"
            End If
        Next j
        prompt = prompt & rowText & vbCrLf
NextRow:
    Next i
    
    BuildDataPrompt = prompt
End Function

' 清理分析结果：去掉所有空行
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
    
    lines = Split(result, vbCrLf)
    ReDim cleanedLines(0 To UBound(lines))
    lineCount = 0
    
    For i = 0 To UBound(lines)
        currentLine = Trim$(CStr(lines(i)))
        If currentLine <> "" Then
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
' 主流程：保险业态分析
' ============================================================================

Public Sub 保险业态分析()
    Dim wsInsurance As Worksheet
    Dim wsData As Variant
    Dim dataPrompt As String
    Dim apiResponse As String
    Dim analysisResult As String
    Dim prevCalc As XlCalculation
    Dim prevScreenUpdating As Boolean
    Dim prevEnableEvents As Boolean
    
    On Error GoTo ErrorHandler
    
    ' 获取保险类工作表
    On Error Resume Next
    Set wsInsurance = ThisWorkbook.Worksheets(INSURANCE_SHEET)
    On Error GoTo ErrorHandler
    If wsInsurance Is Nothing Then
        MsgBox "未找到工作表: " & INSURANCE_SHEET, vbCritical
        Exit Sub
    End If
    
    ' 记录当前应用状态并关闭屏幕更新/事件/自动计算，提高性能
    prevScreenUpdating = Application.ScreenUpdating
    prevCalc = Application.Calculation
    prevEnableEvents = Application.EnableEvents
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False
    
    ' 检查系统提示词是否已配置
    Dim systemMsg As String
    systemMsg = GetSystemMessage()
    If Len(systemMsg) = 0 Then
        MsgBox "系统提示词为空，请在 '" & INSURANCE_SHEET & "' 工作表的 " & SYSTEM_PROMPT_CELL & " 单元格中填写分析提示词。", vbExclamation
        GoTo Cleanup
    End If
    
    ' 读取数据区域
    wsData = wsInsurance.Range(DATA_RANGE).Value
    
    ' 构建提示词
    dataPrompt = "以下两家保险中介类子公司的经营对比数据，请根据系统提示词进行分析，并按指定输出格式给出分析结果。" & vbCrLf & _
                 BuildDataPrompt(wsData)
    
    ' 调用 API
    apiResponse = CallDeepSeekAPI(dataPrompt, INSURANCE_SHEET)
    
    ' 解析响应
    If Left(apiResponse, 5) = "API调用失败" Or _
       Left(apiResponse, 12) = "HTTP请求错误" Then
        analysisResult = apiResponse
    Else
        analysisResult = ParseAPIResponseSimple(apiResponse)
    End If
    
    ' 清理结果（去掉空行）
    analysisResult = CleanAnalysisResult(analysisResult)
    
    ' 写入结果到 保险类!L14
    If Len(analysisResult) > 0 Then
        With wsInsurance.Range(RESULT_CELL)
            .Value = analysisResult
            .WrapText = True
            .HorizontalAlignment = xlLeft
            .VerticalAlignment = xlTop
        End With
        
        If DEBUG_MODE Then Debug.Print INSURANCE_SHEET & " - 保险业态分析完成"
    Else
        If DEBUG_MODE Then Debug.Print INSURANCE_SHEET & " - 分析结果为空"
    End If
    
Cleanup:
    Application.Calculation = prevCalc
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating
    Application.StatusBar = False
    Exit Sub
    
ErrorHandler:
    On Error Resume Next
    Application.Calculation = prevCalc
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating
    Application.StatusBar = False
    On Error GoTo 0
    
    MsgBox "保险业态分析错误: " & Err.Description & " (错误代码: " & Err.Number & ")", vbCritical
End Sub
