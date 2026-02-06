Option Explicit

' 调试开关：需要查看 Debug.Print 时改为 True
Private Const DEBUG_MODE As Boolean = False

' API配置常量 - 建议从外部配置读取敏感信息
Private Const API_BASE_URL As String = "https://api.deepseek.com"
Private Const API_KEY As String = "sk-e65d2e2442fa4c028951b2bec4dbb510" ' 建议从环境变量或工作表读取
Private Const API_MODEL As String = "deepseek-chat"
Private Const API_TIMEOUT_MS As Long = 30000 ' 请求超时时间（毫秒）
Private Const MAX_TOKENS As Long = 1000
Private Const TEMPERATURE As Double = 0.3

' 工作表数据范围常量
Private Const DATA_RANGE As String = "C1:R5"
Private Const RESULT_CELL As String = "C61"
Private Const CONFIG_SHEET As String = "填写页"
Private Const TARGET_RANGE As String = "C2:C10"
Private Const MONTH_CELL As String = "A1"

' 系统消息模板（避免在每次调用时构建）
Private Const SYSTEM_MESSAGE As String = _
    "你是一个专业的财务分析师，负责分析各子公司的业务数据。" & vbCrLf & _
    "要求：" & vbCrLf & _
    "1. 绝对客观，只陈述事实，不使用主观词汇" & vbCrLf & _
    "2. 开头用1-2句话总结最突出特点" & vbCrLf & _
    "3. 基于数据描述关键事实" & vbCrLf & _
    "4. 所有分析保持一致的风格" & vbCrLf & _
    "请严格按照以下格式输出：" & vbCrLf & _
    "{简洁摘要}" & vbCrLf & _
    "营业收入：{描述}" & vbCrLf & _
    "EBITDA/GOP/扣非利润：{描述}" & vbCrLf & _
    "经营活动净现金流：{描述}" & vbCrLf & _
    "经营支出：{描述}"

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
                inEscape = Not inEscape
            Case """"
                If Not inEscape Then
                    endPos = i - 1
                    Exit For
                Else
                    inEscape = False
                End If
            Case Else
                inEscape = False
        End Select
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
        Set CreateHTTPObject = CreateObject("MSXML2.XMLHTTP")
    End If
    On Error GoTo 0
End Function

' 构建JSON请求体（优化字符串拼接）
Private Function BuildJSONRequest(prompt As String) As String
    Dim jsonParts(1 To 5) As String
    
    jsonParts(1) = "{""model"":""" & API_MODEL & ""","
    jsonParts(2) = """messages"":[{""role"":""system"",""content"":""" & EscapeJSONString(SYSTEM_MESSAGE) & """},"
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
    
    ' 记录开始时间用于超时控制
    startTime = Timer
    
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
    
    On Error Resume Next
    With http
        .Open "POST", url, False
        .setRequestHeader "Content-Type", "application/json"
        .setRequestHeader "Authorization", "Bearer " & API_KEY
        .setRequestHeader "Accept", "application/json"
        .setTimeouts API_TIMEOUT_MS, API_TIMEOUT_MS, API_TIMEOUT_MS, API_TIMEOUT_MS
        .send jsonBody
        
        If Err.Number <> 0 Then
            CallDeepSeekAPI = "HTTP请求错误: " & Err.Description
            Exit Function
        End If
        
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
    On Error GoTo 0
    
    ' 检查是否超时
    If (Timer - startTime) * 1000 > API_TIMEOUT_MS Then
        If DEBUG_MODE Then Debug.Print "[" & companyName & "] 警告：请求可能超时"
    End If
    
    CallDeepSeekAPI = response
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
    
    If Len(result) = 0 Then
        CleanAnalysisResult = ""
        Exit Function
    End If
    
    lines = Split(result, vbCrLf)
    ReDim cleanedLines(0 To UBound(lines))
    lineCount = 0
    
    For i = 0 To UBound(lines)
        If Trim(lines(i)) <> "" Then
            cleanedLines(lineCount) = Trim(lines(i))
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
' 主业务流程
' ============================================================================

' 分析单个公司
Private Function AnalyzeCompany(companyName As String, nowmonth As String) As Boolean
    Dim wsTarget As Worksheet
    Dim wsData As Variant
    Dim dataPrompt As String
    Dim apiResponse As String
    Dim analysisResult As String
    
    On Error GoTo AnalyzeError
    
    ' 检查工作表是否存在
    Set wsTarget = ThisWorkbook.Worksheets(companyName)
    If wsTarget Is Nothing Then
        If DEBUG_MODE Then Debug.Print "未找到工作表: " & companyName
        AnalyzeCompany = False
        Exit Function
    End If
    
    ' 读取数据
    wsData = wsTarget.Range(DATA_RANGE).Value
    
    ' 构建提示词
    dataPrompt = "请分析" & companyName & "公司2025年截止" & nowmonth & "的业务数据。" & vbCrLf & _
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
            .RowHeight = 150
            .HorizontalAlignment = xlLeft
            .VerticalAlignment = xlTop
            .Font.Name = "宋体"
            .Font.Size = 10
        End With
        
        ' 调整列宽
        wsTarget.Columns("C").ColumnWidth = 80
        
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
    Dim nowmonth As String
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
    nowmonth = CStr(wsConfig.Range(MONTH_CELL).Value)
    
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
            ShowProgress processedCount, totalCount, companyName
            
            If AnalyzeCompany(companyName, nowmonth) Then
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

' ============================================================================
' 辅助函数
' ============================================================================

' 显示进度
Private Sub ShowProgress(current As Long, total As Long, companyName As String)
    If total > 1 Then
        Application.StatusBar = "正在分析 " & companyName & " (" & current & "/" & total & ")"
    Else
        Application.StatusBar = "正在分析 " & companyName
    End If
End Sub

' 保持原有接口的函数（空实现）
Public Sub 清空对话历史()
    ' 由于当前版本使用独立调用模式，无需清空历史
    MsgBox "当前版本已优化为独立调用模式，无需清空对话历史。", vbInformation
End Sub