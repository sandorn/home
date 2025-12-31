Option Explicit

' 调试开关：需要查看 Debug.Print 时改为 True
Private Const DEBUG_MODE As Boolean = False

' 添加API配置常量
Private Const API_BASE_URL As String = "https://api.deepseek.com"
Private Const API_KEY As String = "sk-f39ab3c0e58c4592aa80d9a51822366f"
Private Const API_MODEL As String = "deepseek-chat"

' 全局变量用于存储对话历史
Private chatHistory As Object

' 初始化对话历史
Private Sub InitializeChatHistory()
    Set chatHistory = CreateObject("Scripting.Dictionary")
    
    ' 添加系统消息，设定统一的风格和要求
    Dim systemMessage As String
    systemMessage = "你是一个专业的财务分析师，负责分析各子公司的业务数据。" & vbCrLf & _
                   "要求：" & vbCrLf & _
                   "1. 绝对客观，只陈述事实，不使用主观词汇" & vbCrLf & _
                   "2. 开头用1-2句话总结最突出特点" & vbCrLf & _
                   "3. 基于数据描述关键事实" & vbCrLf & _
                   "4. 所有分析保持一致的风格和格式" & vbCrLf & _
                   "5. 每个子公司的分析独立成段" & vbCrLf & vbCrLf & _
                   "格式：" & vbCrLf & _
                   "{简洁摘要}" & vbCrLf & _
                   "营业收入：{描述}" & vbCrLf & _
                   "EBITDA/GOP/扣非利润：{描述}" & vbCrLf & _
                   "经营活动净现金流：{描述}" & vbCrLf & _
                   "经营支出：{描述}" & vbCrLf
    
    ' 存储系统消息
    chatHistory.Add "system", systemMessage
    chatHistory.Add "messages", CreateObject("System.Collections.ArrayList")
End Sub

' 更好的解析函数，使用更简单的逻辑
Private Function ParseAPIResponseSimple(apiResponse As String) As String
    Dim result As String
    Dim startPos As Long
    Dim endPos As Long
    Dim jsonString As String
    
    ' 清理JSON字符串，移除换行和多余空格
    jsonString = Replace(apiResponse, vbCrLf, "")
    jsonString = Replace(jsonString, vbTab, "")
    
    ' 查找content字段的开始
    startPos = InStr(jsonString, """content"":""")
    If startPos = 0 Then
        ParseAPIResponseSimple = "未找到content字段"
        Exit Function
    End If
    
    startPos = startPos + 11  ' """content"":""" 的长度
    
    ' 从startPos开始，查找不在转义序列中的双引号
    Dim i As Long
    Dim escapeMode As Boolean
    
    escapeMode = False
    For i = startPos To Len(jsonString)
        Select Case Mid(jsonString, i, 1)
            Case "\"
                escapeMode = Not escapeMode
            Case """"
                If Not escapeMode Then
                    endPos = i - 1
                    Exit For
                Else
                    escapeMode = False
                End If
            Case Else
                escapeMode = False
        End Select
    Next i
    
    If endPos >= startPos Then
        result = Mid(jsonString, startPos, endPos - startPos + 1)
        ' 处理转义字符
        result = Replace(result, "\""", """")
        result = Replace(result, "\\", "\")
        result = Replace(result, "\n", vbCrLf)
        result = Replace(result, "\t", vbTab)
        result = Replace(result, "\r", "")
        result = Replace(result, "\/", "/")
    End If
    
    If result = "" Then
        result = "解析失败，原始响应: " & Left(apiResponse, 200)
    End If
    
    ParseAPIResponseSimple = result
End Function

' JSON字符串转义函数
Private Function EscapeJSONString(ByVal text As String) As String
    text = Replace(text, "\", "\\")
    text = Replace(text, """", "\""")
    text = Replace(text, vbCrLf, "\n")
    text = Replace(text, vbTab, "\t")
    text = Replace(text, vbBack, "\b")
    text = Replace(text, vbFormFeed, "\f")
    text = Replace(text, vbCr, "\r")
    EscapeJSONString = text
End Function

' 使用对话历史调用API
Private Function CallDeepSeekAPIWithHistory(prompt As String, companyName As String) As String
    Dim http As Object
    Dim url As String
    Dim jsonBody As String
    Dim response As String
    Dim escapedPrompt As String
    Dim messagesList As Object
    Dim i As Long
    
    ' 创建HTTP请求对象
    Set http = CreateObject("MSXML2.ServerXMLHTTP.6.0")
    url = API_BASE_URL & "/chat/completions"
    
    ' 获取消息列表
    Set messagesList = chatHistory("messages")
    
    ' 将新的用户消息添加到历史中
    Dim userMessage As Object
    Set userMessage = CreateObject("Scripting.Dictionary")
    userMessage.Add "role", "user"
    userMessage.Add "content", "请分析" & companyName & "公司2025年截止" & prompt
    
    messagesList.Add userMessage
    
    ' 构建完整的消息数组
    Dim allMessages As String
    allMessages = "["
    
    ' 添加系统消息
    allMessages = allMessages & "{""role"":""system"",""content"":""" & _
                  EscapeJSONString(chatHistory("system")) & """},"
    
    ' 添加所有历史消息
    For i = 0 To messagesList.Count - 1
        Dim msg As Object
        Set msg = messagesList(i)
        allMessages = allMessages & "{""role"":""" & msg("role") & """,""content"":""" & _
                     EscapeJSONString(msg("content")) & """},"
    Next i
    
    ' 移除最后一个逗号并闭合数组
    allMessages = Left(allMessages, Len(allMessages) - 1) & "]"
    
    ' 构建JSON请求体
    jsonBody = "{"
    jsonBody = jsonBody & """model"": """ & API_MODEL & ""","
    jsonBody = jsonBody & """messages"": " & allMessages & ","
    jsonBody = jsonBody & """temperature"": 0.3,"
    jsonBody = jsonBody & """max_tokens"": 2000"
    jsonBody = jsonBody & "}"
    
    ' 调试信息
    If DEBUG_MODE Then
        Debug.Print "发送的JSON前200字符: " & Left(jsonBody, 200)
        Debug.Print "消息数量: " & (messagesList.Count + 1)
    End If
    
    ' 发送API请求
    On Error Resume Next
    With http
        .Open "POST", url, False
        .setRequestHeader "Content-Type", "application/json"
        .setRequestHeader "Authorization", "Bearer " & API_KEY
        .setRequestHeader "Accept", "application/json"
        .send jsonBody
        
        If .Status = 200 Then
            response = .responseText
            If DEBUG_MODE Then Debug.Print "API调用成功，响应长度: " & Len(response)
            
            ' 将助手回复添加到历史中
            Dim assistantMessage As Object
            Set assistantMessage = CreateObject("Scripting.Dictionary")
            assistantMessage.Add "role", "assistant"
            assistantMessage.Add "content", ParseAPIResponseSimple(response)
            
            messagesList.Add assistantMessage
        Else
            response = "API调用失败: " & .Status & " - " & .statusText
            If DEBUG_MODE Then
                Debug.Print response
                If Len(.responseText) > 0 Then
                    Debug.Print "错误详情: " & .responseText
                End If
            End If
        End If
    End With
    
    If Err.Number <> 0 Then
        response = "HTTP请求错误: " & Err.Description
    End If
    
    On Error GoTo 0
    
    CallDeepSeekAPIWithHistory = response
End Function

' 构建数据提示词（不含格式要求）
Private Function BuildDataPrompt(companyName As String, month As String, dataArray As Variant) As String
    Dim prompt As String
    Dim dataStr As String
    Dim i As Long, j As Long
    Dim headerRow As String
    Dim dataRows(1 To 5) As String
    
    ' 构建表头（C1:R1）
    For j = 1 To 16 ' C到R是16列
        If Not IsEmpty(dataArray(1, j)) Then
            headerRow = headerRow & dataArray(1, j) & vbTab
        Else
            headerRow = headerRow & "列" & j & vbTab
        End If
    Next j
    
    ' 构建数据行（C2:R5）
    For i = 2 To 5
        dataRows(i - 1) = "行" & i & ": "
        For j = 1 To 16
            If Not IsEmpty(dataArray(i, j)) Then
                dataRows(i - 1) = dataRows(i - 1) & dataArray(i, j) & vbTab
            Else
                dataRows(i - 1) = dataRows(i - 1) & "空" & vbTab
            End If
        Next j
    Next i
    
    ' 构建数据描述
    prompt = month & "的数据如下：" & vbCrLf & vbCrLf
    prompt = prompt & "数据表头：" & vbCrLf & headerRow & vbCrLf & vbCrLf
    prompt = prompt & "具体数据：" & vbCrLf
    For i = 1 To 4
        prompt = prompt & dataRows(i) & vbCrLf
    Next i
    
    If DEBUG_MODE Then Debug.Print companyName & " - 数据提示词长度: " & Len(prompt)
    
    BuildDataPrompt = prompt
End Function

' 主分析函数，使用对话历史保持一致性
Public Sub GenerateBusinessAnalysis()
    Dim wsConfig As Worksheet
    Dim targetSheetNames As Range
    Dim cell As Range
    Dim wsTarget As Worksheet
    Dim wsData As Variant
    Dim nowmonth As String
    Dim apiResponse As String
    Dim analysisResult As String
    Dim dataPrompt As String
    Dim companyName As String
    Dim prevCalc As XlCalculation
    Dim prevScreenUpdating As Boolean
    Dim prevEnableEvents As Boolean
    
    ' 设置错误处理
    On Error GoTo ErrorHandler
    
    ' 初始化对话历史
    InitializeChatHistory
    
    ' 记录当前应用状态并关闭屏幕更新/事件/自动计算，提高性能
    prevScreenUpdating = Application.ScreenUpdating
    prevCalc = Application.Calculation
    prevEnableEvents = Application.EnableEvents
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False
    
    ' 获取配置信息
    Set wsConfig = ThisWorkbook.Worksheets("填写页")
    Set targetSheetNames = wsConfig.Range("C2:C10")
    nowmonth = wsConfig.Range("A1").Value
    
    ' 循环处理每个子公司
    For Each cell In targetSheetNames
        If cell.Value <> "" Then
            companyName = cell.Value
            
            ' 检查工作表是否存在
            On Error Resume Next
            Set wsTarget = ThisWorkbook.Worksheets(companyName)
            On Error GoTo ErrorHandler
            
            If Not wsTarget Is Nothing Then
                ' 读取数据范围 C1:R5
                wsData = wsTarget.Range("C1:R5").Value
                
                ' 构建数据提示词
                dataPrompt = BuildDataPrompt(companyName, nowmonth, wsData)
                
                ' 调用DeepSeek API（使用对话历史）
                apiResponse = CallDeepSeekAPIWithHistory(dataPrompt, companyName)
                
                ' 解析API响应
                If Left(apiResponse, 5) = "API调用失败" Or _
                   Left(apiResponse, 12) = "HTTP请求错误" Then
                    analysisResult = apiResponse
                Else
                    ' 使用简单解析方法
                    analysisResult = ParseAPIResponseSimple(apiResponse)
                End If
                
                ' 将结果写入C61单元格
                If analysisResult <> "" Then
                    wsTarget.Range("C61").Value = analysisResult
                    wsTarget.Range("C61").WrapText = True
                    wsTarget.Range("C61").RowHeight = 150
                    wsTarget.Columns("C").ColumnWidth = 80  ' 设置合适的列宽
                    
                    ' 添加单元格格式
                    With wsTarget.Range("C61")
                        .HorizontalAlignment = xlLeft
                        .VerticalAlignment = xlTop
                        .Font.Name = "宋体"
                        .Font.Size = 10
                    End With
                    
                    If DEBUG_MODE Then Debug.Print companyName & " - 分析完成，写入C61"
                Else
                    If DEBUG_MODE Then Debug.Print companyName & " - 分析结果为空"
                End If
                
                ' 释放对象
                Set wsTarget = Nothing
            Else
                If DEBUG_MODE Then Debug.Print "未找到工作表: " & companyName
            End If
        End If
    Next cell
    
    ' 清理对话历史
    Set chatHistory = Nothing
    
    ' 恢复应用状态
    Application.Calculation = prevCalc
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating
    
    MsgBox "分析完成！所有公司分析风格保持一致。", vbInformation
    Exit Sub
    
ErrorHandler:
    ' 出错时同样恢复应用状态
    On Error Resume Next
    Set chatHistory = Nothing
    Application.Calculation = prevCalc
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating
    On Error GoTo 0
    MsgBox "错误: " & Err.Description & " (错误代码: " & Err.Number & ")", vbCritical
End Sub

' 清空对话历史的函数（可选）
Public Sub ClearChatHistory()
    If Not chatHistory Is Nothing Then
        Set chatHistory = Nothing
        MsgBox "对话历史已清空。", vbInformation
    Else
        MsgBox "没有活动的对话历史。", vbInformation
    End If
End Sub

