Option Explicit

' ============================================================
' VBS_DeepSeekAPI.bas - 共享的 DeepSeek API 调用模块
' 功能：为多个业态分析提供统一的 API 调用功能
' ============================================================

' ---- API 配置常量 ----
Private Const DEFAULT_API_BASE_URL As String = "https://api.deepseek.com"
Private Const DEFAULT_API_MODEL As String = "deepseek-chat"
Private Const DEFAULT_TIMEOUT_MS As Long = 30000
Private Const DEFAULT_MAX_TOKENS As Long = 1000
Private Const DEFAULT_TEMPERATURE As Double = 0.3
Private Const CONTENT_PREFIX_LEN As Long = 11  ' Len("""content"":""")

' ---- 错误代码常量 ----
Private Const ERR_API_KEY_MISSING As Long = 1001
Private Const ERR_HTTP_OBJECT_FAILED As Long = 1002
Private Const ERR_API_RESPONSE_INVALID As Long = 1003
Private Const ERR_WORKSHEET_NOT_FOUND As Long = 1004

' ============================================================
' 从指定工作表和单元格读取系统提示词
' ============================================================
Public Function GetSystemMessage(ByVal ws As Worksheet, ByVal cellAddr As String) As String
    If ws Is Nothing Then
        GetSystemMessage = ""
        Exit Function
    End If
    
    GetSystemMessage = Trim$(CStr(ws.Range(cellAddr).Value))
End Function

' ============================================================
' 从配置工作表读取 API Key
' ============================================================
Public Function GetApiKey(ByVal wsConfig As Worksheet, ByVal cellAddr As String, Optional ByVal debugMode As Boolean = False, Optional ByVal contextName As String = "") As String
    If wsConfig Is Nothing Then
        If debugMode Then Debug.Print "[" & contextName & "] 配置错误: 未找到配置工作表"
        GetApiKey = ""
        Exit Function
    End If
    
    GetApiKey = Trim$(CStr(wsConfig.Range(cellAddr).Value))
End Function

' ============================================================
' JSON 字符串转义
' ============================================================
Public Function EscapeJSONString(ByVal text As String) As String
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

' ============================================================
' 简化的 JSON 解析函数 - 提取 content 字段
' ============================================================
Public Function ParseAPIResponseSimple(ByVal apiResponse As String) As String
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
    
    contentStart = contentStart + CONTENT_PREFIX_LEN
    
    Dim i As Long
    Dim inEscape As Boolean
    Dim result As String
    Dim endPos As Long
    
    inEscape = False
    For i = contentStart To Len(apiResponse)
        Select Case Mid$(apiResponse, i, 1)
            Case "\"
                inEscape = True
            Case """"
                If Not inEscape Then
                    endPos = i - 1
                    Exit For
                End If
            Case Else
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

' ============================================================
' 创建 HTTP 对象
' ============================================================
Public Function CreateHTTPObject() As Object
    On Error Resume Next
    Set CreateHTTPObject = CreateObject("MSXML2.ServerXMLHTTP.6.0")
    If Err.Number <> 0 Then
        Err.Clear
        Set CreateHTTPObject = CreateObject("MSXML2.XMLHTTP")
    End If
    On Error GoTo 0
End Function

' ============================================================
' 构建 JSON 请求体
' ============================================================
Public Function BuildJSONRequest( _
    ByVal systemMsg As String, _
    ByVal prompt As String, _
    ByVal model As String, _
    ByVal temperature As Double, _
    ByVal maxTokens As Long _
) As String
    Dim jsonParts(1 To 5) As String
    
    jsonParts(1) = "{""model"":""" & model & ""","
    jsonParts(2) = """messages"":[{""role"":""system"",""content"":""" & EscapeJSONString(systemMsg) & """},"
    jsonParts(3) = "{""role"":""user"",""content"":""" & EscapeJSONString(prompt) & """}],"
    jsonParts(4) = """temperature"":" & CStr(temperature) & ","
    jsonParts(5) = """max_tokens"":" & CStr(maxTokens) & "}"
    
    BuildJSONRequest = Join(jsonParts, "")
End Function

' ============================================================
' 调用 DeepSeek API（带重试机制）
' ============================================================
Public Function CallDeepSeekAPI( _
    ByVal prompt As String, _
    ByVal apiKey As String, _
    Optional ByVal apiBaseUrl As String = DEFAULT_API_BASE_URL, _
    Optional ByVal model As String = DEFAULT_API_MODEL, _
    Optional ByVal temperature As Double = DEFAULT_TEMPERATURE, _
    Optional ByVal maxTokens As Long = DEFAULT_MAX_TOKENS, _
    Optional ByVal timeoutMs As Long = DEFAULT_TIMEOUT_MS, _
    Optional ByVal contextName As String = "", _
    Optional ByVal debugMode As Boolean = False, _
    Optional ByVal maxRetries As Long = 3 _
) As String
    Dim http As Object
    Dim url As String
    Dim jsonBody As String
    Dim response As String
    Dim startTime As Double
    Dim canSetTimeouts As Boolean
    Dim retryCount As Long
    Dim waitTime As Double
    Dim systemMsg As String
    
    If Len(apiKey) = 0 Then
        CallDeepSeekAPI = "错误：未配置 API Key"
        Exit Function
    End If
    
    For retryCount = 1 To maxRetries
        Set http = CreateHTTPObject()
        If http Is Nothing Then
            CallDeepSeekAPI = "错误：无法创建HTTP对象"
            Exit Function
        End If
        
        url = apiBaseUrl & "/chat/completions"
        jsonBody = BuildJSONRequest("", prompt, model, temperature, maxTokens)
        
        If debugMode Then
            Debug.Print "[" & contextName & "] 发送请求，长度: " & Len(jsonBody) & " (重试 #" & retryCount & ")"
        End If
        
        startTime = Timer
        canSetTimeouts = (InStr(1, TypeName(http), "ServerXMLHTTP", vbTextCompare) > 0)
        
        On Error GoTo HttpError
        With http
            .Open "POST", url, False
            .setRequestHeader "Content-Type", "application/json"
            .setRequestHeader "Authorization", "Bearer " & apiKey
            .setRequestHeader "Accept", "application/json"
            
            If canSetTimeouts Then
                On Error Resume Next
                .setTimeouts timeoutMs, timeoutMs, timeoutMs, timeoutMs
                Err.Clear
                On Error GoTo HttpError
            End If
            
            .send jsonBody
            If .Status = 200 Then
                response = .responseText
                If debugMode Then
                    Debug.Print "[" & contextName & "] API响应成功，长度: " & Len(response)
                End If
                Set http = Nothing
                CallDeepSeekAPI = response
                Exit Function
            Else
                response = "API调用失败: " & .Status & " - " & .statusText
                If debugMode Then
                    Debug.Print "[" & contextName & "] " & response
                    If Len(.responseText) > 0 Then
                        Debug.Print "错误详情: " & Left$(.responseText, 500)
                    End If
                End If
            End If
        End With
        
        If (Timer - startTime) * 1000 > timeoutMs Then
            If debugMode Then Debug.Print "[" & contextName & "] 警告：请求可能超时"
        End If
        
        Set http = Nothing
        
        If retryCount < maxRetries Then
            waitTime = 2 ^ retryCount
            If debugMode Then Debug.Print "[" & contextName & "] 等待 " & waitTime & "秒后重试..."
            Application.Wait (Now + TimeValue("0:00:" & CStr(waitTime)))
        End If
    Next retryCount
    
    CallDeepSeekAPI = response
    Exit Function
    
HttpError:
    If Not http Is Nothing Then Set http = Nothing
    CallDeepSeekAPI = "HTTP请求错误: " & Err.Description
End Function

' ============================================================
' 构建数据提示词（通用版）
' ============================================================
Public Function BuildDataPrompt(ByVal dataArray As Variant) As String
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

' ============================================================
' 清理分析结果 - 移除所有空行
' ============================================================
Public Function CleanAnalysisResult(ByVal result As String) As String
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

' ============================================================
' 将分析结果写入工作表
' ============================================================
Public Sub WriteAnalysisResult( _
    ByVal ws As Worksheet, _
    ByVal cellAddr As String, _
    ByVal result As String, _
    Optional ByVal debugMode As Boolean = False, _
    Optional ByVal contextName As String = "" _
)
    If Len(result) > 0 Then
        With ws.Range(cellAddr)
            .Value = result
            .WrapText = True
            .HorizontalAlignment = xlLeft
            .VerticalAlignment = xlTop
        End With
        
        If debugMode Then Debug.Print contextName & " - 业态分析完成"
    Else
        If debugMode Then Debug.Print contextName & " - 分析结果为空"
    End If
End Sub

' ============================================================
' 获取目标工作表（带错误检查）
' ============================================================
Public Function GetTargetWorksheet(ByVal sheetName As String, Optional ByVal showError As Boolean = False) As Worksheet
    On Error Resume Next
    Set GetTargetWorksheet = ThisWorkbook.Worksheets(sheetName)
    On Error GoTo 0
    
    If showError And GetTargetWorksheet Is Nothing Then
        MsgBox "未找到工作表: " & sheetName, vbCritical
    End If
End Function

' ============================================================
' 获取配置工作表
' ============================================================
Public Function GetConfigWorksheet(ByVal sheetName As String) As Worksheet
    On Error Resume Next
    Set GetConfigWorksheet = ThisWorkbook.Worksheets(sheetName)
    On Error GoTo 0
End Function

' ============================================================
' 记录调试信息
' ============================================================
Public Sub LogDebug(ByVal context As String, ByVal message As String, Optional ByVal debugMode As Boolean = False)
    If debugMode Then
        Debug.Print "[" & context & "] " & message
    End If
End Sub

