Option Explicit

' ============================================================
' DeepSeekAPI.bas — 公共 API 调用模块
' 为业态分析整合版提供统一的 DeepSeek API 调用功能
' 包含：重试机制、超时中断、统一错误日志
' ============================================================

' ---- 调试开关 ----
Public Const DEBUG_MODE As Boolean = False

' ---- API 配置常量 ----
Public Const API_BASE_URL As String = "https://api.deepseek.com"
Public Const API_MODEL As String = "deepseek-v4-pro"
Public Const API_TIMEOUT_MS As Long = 30000
Public Const MAX_TOKENS As Long = 1000
Public Const TEMPERATURE As Double = 0.3

' ---- 通用配置 ----
Public Const CONFIG_SHEET_NAME As String = "填写页"
Public Const API_KEY_FILE As String = "dskey"
Public Const API_KEY_SECTION As String = "EXCEL"
Public Const MONTH_NUMBER_CELL As String = "A2"

' ---- 内部常量 ----
Private Const CONTENT_PREFIX_LEN As Long = 11
Private Const MAX_RETRIES As Long = 3

' ============================================================
' === 配置读取 ===
' ============================================================

Public Function GetSystemMessage(ByVal ws As Worksheet, ByVal cellAddr As String) As String
    If ws Is Nothing Then
        GetSystemMessage = ""
        Exit Function
    End If
    GetSystemMessage = Trim$(CStr(ws.Range(cellAddr).Value))
End Function

' 从 ~/.dskey 文件读取 API Key（EXCEL 段）
Public Function GetApiKey(Optional ByVal debugMode As Boolean = False, Optional ByVal contextName As String = "") As String
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
        If debugMode Then Debug.Print FormatError(contextName, "配置错误", "未找到 API Key 文件 '" & filePath & "'")
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
    
    If debugMode Then Debug.Print FormatError(contextName, "配置错误", "未在 '" & filePath & "' 中找到 [" & API_KEY_SECTION & "] 的 API Key")
    GetApiKey = ""
End Function

' ============================================================
' === JSON 处理 ===
' ============================================================

Public Function EscapeJSONString(ByVal text As String) As String
    Dim result As String, i As Long, ch As String, pos As Long
    result = Space$(Len(text) * 2)
    pos = 1
    For i = 1 To Len(text)
        ch = Mid$(text, i, 1)
        Select Case ch
            Case "\" : Mid$(result, pos, 2) = "\\" : pos = pos + 2
            Case """" : Mid$(result, pos, 2) = "\""" : pos = pos + 2
            Case vbCr : Mid$(result, pos, 2) = "\r" : pos = pos + 2
            Case vbLf : Mid$(result, pos, 2) = "\n" : pos = pos + 2
            Case vbTab : Mid$(result, pos, 2) = "\t" : pos = pos + 2
            Case vbBack : Mid$(result, pos, 2) = "\b" : pos = pos + 2
            Case vbFormFeed : Mid$(result, pos, 2) = "\f" : pos = pos + 2
            Case Else : Mid$(result, pos, 1) = ch : pos = pos + 1
        End Select
    Next i
    EscapeJSONString = Left$(result, pos - 1)
End Function

Public Function ParseAPIResponseSimple(ByVal apiResponse As String) As String
    Dim contentStart As Long, i As Long, inEscape As Boolean, result As String, endPos As Long
    If Len(apiResponse) = 0 Then ParseAPIResponseSimple = "API响应为空" : Exit Function
    contentStart = InStr(1, apiResponse, """content"":""", vbBinaryCompare)
    If contentStart = 0 Then ParseAPIResponseSimple = "未找到content字段" : Exit Function
    contentStart = contentStart + CONTENT_PREFIX_LEN
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
    If endPos = 0 Then ParseAPIResponseSimple = "无法定位content结束位置" : Exit Function
    result = Mid$(apiResponse, contentStart, endPos - contentStart + 1)
    result = Replace(result, "\""", """")
    result = Replace(result, "\n", vbCrLf) : result = Replace(result, "\t", vbTab)
    result = Replace(result, "\r", "") : result = Replace(result, "\/", "/")
    result = Replace(result, "\b", vbBack) : result = Replace(result, "\f", vbFormFeed)
    result = Replace(result, "\\", "\")
    ParseAPIResponseSimple = result
End Function

' ============================================================
' === HTTP 请求 ===
' ============================================================

Public Function CreateHTTPObject() As Object
    On Error Resume Next
    Set CreateHTTPObject = CreateObject("MSXML2.ServerXMLHTTP.6.0")
    If Err.Number <> 0 Then Err.Clear : Set CreateHTTPObject = CreateObject("MSXML2.XMLHTTP")
    On Error GoTo 0
End Function

Public Function BuildJSONRequest(ByVal systemMsg As String, ByVal prompt As String, ByVal model As String, ByVal temperature As Double, ByVal maxTokens As Long) As String
    BuildJSONRequest = "{""model"":""" & model & """," & """messages"":[{""role"":""system"",""content"":""" & EscapeJSONString(systemMsg) & """}," & "{""role"":""user"",""content"":""" & EscapeJSONString(prompt) & """}]," & """temperature"":" & CStr(temperature) & "," & """max_tokens"":" & CStr(maxTokens) & "}"
End Function

Public Function CallDeepSeekAPI(ByVal prompt As String, ByVal apiKey As String, Optional ByVal apiBaseUrl As String = "https://api.deepseek.com", Optional ByVal model As String = "deepseek-chat", Optional ByVal temperature As Double = 0.3, Optional ByVal maxTokens As Long = 1000, Optional ByVal timeoutMs As Long = 30000, Optional ByVal contextName As String = "", Optional ByVal debugMode As Boolean = False, Optional ByVal maxRetries As Long = 3, Optional ByVal systemMsg As String = "") As String
    Dim http As Object, url As String, jsonBody As String, response As String
    Dim startTime As Double, canSetTimeouts As Boolean, retryCount As Long, waitSec As Long
    Dim statusCode As Long, isRetryable As Boolean, timedOut As Boolean, success As Boolean

    If Len(apiKey) = 0 Then
        CallDeepSeekAPI = FormatError(contextName, "配置错误", "未配置 API Key")
        Exit Function
    End If

    If maxRetries < 1 Then maxRetries = 1

    For retryCount = 1 To maxRetries
        Set http = CreateHTTPObject()
        If http Is Nothing Then
            CallDeepSeekAPI = FormatError(contextName, "网络错误", "无法创建HTTP对象")
            Exit Function
        End If

        url = apiBaseUrl & "/chat/completions"
        jsonBody = BuildJSONRequest(systemMsg, prompt, model, temperature, maxTokens)

        If debugMode Then Debug.Print FormatLog(contextName, "发送请求 (重试 #" & retryCount & ")")

        startTime = Timer
        canSetTimeouts = (InStr(1, TypeName(http), "ServerXMLHTTP", vbTextCompare) > 0)
        timedOut = False : success = False : isRetryable = False

        On Error GoTo HttpError
        With http
            .Open "POST", url, False
            .setRequestHeader "Content-Type", "application/json"
            .setRequestHeader "Authorization", "Bearer " & apiKey
            .setRequestHeader "Accept", "application/json"
            If canSetTimeouts Then On Error Resume Next : .setTimeouts timeoutMs, timeoutMs, timeoutMs, timeoutMs : Err.Clear : On Error GoTo HttpError
            .send jsonBody
            statusCode = .Status

            timedOut = ((Timer - startTime) * 1000 > timeoutMs)
            If timedOut Then
                On Error Resume Next : .Abort : On Error GoTo 0
            ElseIf statusCode = 200 Then
                response = .responseText
                success = True
                If debugMode Then Debug.Print FormatLog(contextName, "API响应成功，长度: " & Len(response))
            Else
                response = "API错误: " & statusCode & " - " & .statusText
                If debugMode And Len(.responseText) > 0 Then Debug.Print FormatLog(contextName, "错误详情: " & Left$(.responseText, 500))
                isRetryable = IsRetryableStatus(statusCode)
            End If
        End With

        Set http = Nothing

        If success Then CallDeepSeekAPI = response : Exit Function

        If timedOut Then
            response = FormatError(contextName, "超时错误", "请求超过 " & CStr(timeoutMs \ 1000) & " 秒未响应")
            isRetryable = True
        End If

        If Not isRetryable Then CallDeepSeekAPI = response : Exit Function

NextIteration:
        If retryCount < maxRetries Then
            waitSec = 2 ^ retryCount
            If debugMode Then Debug.Print FormatLog(contextName, "等待 " & waitSec & " 秒后重试...")
            Application.Wait (Now + TimeValue("0:00:" & CStr(waitSec)))
        End If
    Next retryCount

    CallDeepSeekAPI = response
    Exit Function

HttpError:
    On Error Resume Next : http.Abort : On Error GoTo 0
    Set http = Nothing
    response = FormatError(contextName, "网络错误", Err.Description)
    isRetryable = True
    Resume NextIteration
End Function

Private Function IsRetryableStatus(ByVal statusCode As Long) As Boolean
    Select Case statusCode
        Case 401, 402, 403, 422
            IsRetryableStatus = False
        Case Else
            IsRetryableStatus = True
    End Select
End Function

' ============================================================
' === 数据提示词构建 ===
' ============================================================

Public Function BuildDataPrompt(ByVal dataArray As Variant) As String
    Dim prompt As String, i As Long, j As Long, rowText As String, colCount As Long
    If Not IsArray(dataArray) Then BuildDataPrompt = "数据无效" : Exit Function
    colCount = UBound(dataArray, 2)
    prompt = "数据表格如下：" & vbCrLf
    For i = 1 To UBound(dataArray, 1)
        rowText = "|"
        For j = 1 To colCount
            If Not IsEmpty(dataArray(i, j)) Then rowText = rowText & " " & CStr(dataArray(i, j)) & " |" Else rowText = rowText & " |"
        Next j
        prompt = prompt & rowText & vbCrLf
    Next i
    BuildDataPrompt = prompt
End Function

' ============================================================
' === 结果处理 ===
' ============================================================

Public Function CleanAnalysisResult(ByVal result As String) As String
    Dim lines As Variant, i As Long, cleanedLines() As String, lineCount As Long, currentLine As String
    If Len(result) = 0 Then CleanAnalysisResult = "" : Exit Function
    lines = Split(result, vbCrLf)
    ReDim cleanedLines(0 To UBound(lines))
    lineCount = 0
    For i = 0 To UBound(lines)
        currentLine = Trim$(CStr(lines(i)))
        If currentLine <> "" Then cleanedLines(lineCount) = currentLine : lineCount = lineCount + 1
    Next i
    If lineCount = 0 Then CleanAnalysisResult = "" Else ReDim Preserve cleanedLines(0 To lineCount - 1) : CleanAnalysisResult = Join(cleanedLines, vbCrLf)
End Function

Public Sub WriteAnalysisResult(ByVal ws As Worksheet, ByVal cellAddr As String, ByVal result As String, Optional ByVal debugMode As Boolean = False, Optional ByVal contextName As String = "")
    If Len(result) > 0 Then
        With ws.Range(cellAddr)
            .Value = result : .WrapText = True : .HorizontalAlignment = xlLeft : .VerticalAlignment = xlTop
        End With
        If debugMode Then Debug.Print FormatLog(contextName, "分析结果已写入 " & cellAddr)
    Else
        If debugMode Then Debug.Print FormatLog(contextName, "分析结果为空")
    End If
End Sub

' ============================================================
' === 工作表工具 ===
' ============================================================

Public Function GetTargetWorksheet(ByVal sheetName As String, Optional ByVal showError As Boolean = False) As Worksheet
    On Error Resume Next
    Set GetTargetWorksheet = ThisWorkbook.Worksheets(sheetName)
    On Error GoTo 0
    If showError And GetTargetWorksheet Is Nothing Then MsgBox "未找到工作表: " & sheetName, vbCritical
End Function

Public Function GetConfigWorksheet(ByVal sheetName As String) As Worksheet
    On Error Resume Next
    Set GetConfigWorksheet = ThisWorkbook.Worksheets(sheetName)
    On Error GoTo 0
End Function

' ============================================================
' === 统一错误日志 ===
' ============================================================

Private Function FormatError(ByVal context As String, ByVal category As String, ByVal detail As String) As String
    FormatError = "[" & context & "] " & category & "：" & detail
End Function

Private Function FormatLog(ByVal context As String, ByVal message As String) As String
    If Len(context) > 0 Then
        FormatLog = "[" & context & "] " & message
    Else
        FormatLog = message
    End If
End Function
