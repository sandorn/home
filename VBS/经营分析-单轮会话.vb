Option Explicit

' 调试开关：需要查看 Debug.Print 时改为 True
Private Const DEBUG_MODE As Boolean = False

' 添加API配置常量
Private Const API_BASE_URL As String = "https://api.deepseek.com"
Private Const API_KEY As String = "sk-f39ab3c0e58c4592aa80d9a51822366f"
Private Const API_MODEL As String = "deepseek-chat"

' 更好的解析函数，使用更简单的逻辑
Function ParseAPIResponseSimple(apiResponse As String) As String
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

' 修改API调用函数，使用更简单的解析
Function CallDeepSeekAPI(prompt As String) As String
    Dim http As Object
    Dim url As String
    Dim jsonBody As String
    Dim response As String
    Dim escapedPrompt As String
    
    ' 创建HTTP请求对象
    Set http = CreateObject("MSXML2.ServerXMLHTTP.6.0")
    url = API_BASE_URL & "/chat/completions"
    
    ' 正确转义JSON中的特殊字符
    escapedPrompt = prompt
    escapedPrompt = Replace(escapedPrompt, "\", "\\")
    escapedPrompt = Replace(escapedPrompt, """", "\""")
    escapedPrompt = Replace(escapedPrompt, vbCrLf, "\n")
    escapedPrompt = Replace(escapedPrompt, vbTab, "\t")
    
    ' 构建JSON请求体
    jsonBody = "{"
    jsonBody = jsonBody & """model"": """ & API_MODEL & ""","
    jsonBody = jsonBody & """messages"": [{"
    jsonBody = jsonBody & """role"": ""user"","
    jsonBody = jsonBody & """content"": """ & escapedPrompt & """"
    jsonBody = jsonBody & "}],"
    jsonBody = jsonBody & """temperature"": 0.3,"
    jsonBody = jsonBody & """max_tokens"": 2000"
    jsonBody = jsonBody & "}"
    
    ' 调试信息（仅在 DEBUG_MODE=True 时输出）
    If DEBUG_MODE Then
        Debug.Print "发送的JSON前100字符: " & Left(jsonBody, 100)
        Debug.Print "提示词长度: " & Len(prompt)
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
    
    CallDeepSeekAPI = response
End Function

' 修改主要分析函数，使用新的解析方法
Sub GenerateBusinessAnalysis()
    Dim wsConfig As Worksheet
    Dim targetSheetNames As Range
    Dim cell As Range
    Dim wsTarget As Worksheet
    Dim wsData As Variant
    Dim nowmonth As String
    Dim apiResponse As String
    Dim analysisResult As String
    Dim prompt As String
    Dim companyName As String
    Dim prevCalc As XlCalculation
    Dim prevScreenUpdating As Boolean
    Dim prevEnableEvents As Boolean
    
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
                
                ' 构建提示词
                prompt = BuildPrompt(companyName, nowmonth, wsData)
                
                ' 调用DeepSeek API
                apiResponse = CallDeepSeekAPI(prompt)
                
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
    
    ' 恢复应用状态
    Application.Calculation = prevCalc
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating
    
    MsgBox "分析完成！", vbInformation
    Exit Sub
    
ErrorHandler:
    ' 出错时同样恢复应用状态
    On Error Resume Next
    Application.Calculation = prevCalc
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating
    On Error GoTo 0
    MsgBox "错误: " & Err.Description & " (错误代码: " & Err.Number & ")", vbCritical
End Sub

' 更好的JSON构建函数
Function BuildPrompt(sheetName As String, month As String, dataArray As Variant) As String
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
    
    ' 构建完整的提示词（更简洁的版本）
    prompt = "请基于" & sheetName & "公司2025年截止" & month & "的业务数据，生成分析报告。" & vbCrLf & vbCrLf
    prompt = prompt & "数据表头：" & vbCrLf & headerRow & vbCrLf & vbCrLf
    prompt = prompt & "具体数据：" & vbCrLf
    For i = 1 To 4
        prompt = prompt & dataRows(i) & vbCrLf
    Next i
    prompt = prompt & vbCrLf
    prompt = prompt & "要求：" & vbCrLf
    prompt = prompt & "1. 绝对客观，只陈述事实，不使用主观词汇" & vbCrLf
    prompt = prompt & "2. 开头用1-2句话总结最突出特点" & vbCrLf
    prompt = prompt & "3. 基于数据描述关键事实" & vbCrLf & vbCrLf
    prompt = prompt & "格式：" & vbCrLf
    prompt = prompt & "{简洁摘要}" & vbCrLf
    prompt = prompt & "营业收入：{描述}" & vbCrLf
    prompt = prompt & "EBITDA/GOP/扣非利润：{描述}" & vbCrLf
    prompt = prompt & "经营活动净现金流：{描述}" & vbCrLf
    prompt = prompt & "经营支出：{描述}"
    
    Debug.Print "提示词长度: " & Len(prompt)
    BuildPrompt = prompt
End Function


Sub CopyDataFromSource()
    Dim sourcePath As String
    Dim sourceFile As String

    Dim wsConfig As Worksheet
    Dim targetSheetNames As Range
    Dim cell As Range
    Dim targetSheetName As String
    Dim wsTarget As Worksheet
    
    ' 设置配置工作表
    Set wsConfig = ThisWorkbook.Worksheets("填写页")
    
    ' 构建源文件路径
    sourcePath = "C:\Users\Administrator\Documents\子管\2025经营分析\经营报表\"
    
    Application.ScreenUpdating = False
    
    ' 循环处理C2:C10中的每个子公司名称
    Set targetSheetNames = wsConfig.Range("C2:C10")
    For Each cell In targetSheetNames
        If cell.Value <> "" Then
            Dim canProcess As Boolean
            Dim wbSource As Workbook

            canProcess = True
            targetSheetName = cell.Value
            
            ' 构建源文件路径（假设源文件名与子公司名称相同）
            sourceFile = sourcePath & targetSheetName & ".xlsx"
            
            ' 检查源文件是否存在
            If Dir(sourceFile) = "" Then
                MsgBox "源文件不存在: " & sourceFile & "，跳过处理"
                canProcess = False
            End If
            
            ' 检查目标工作表是否存在
            If canProcess Then
                On Error Resume Next
                Set wsTarget = ThisWorkbook.Worksheets(targetSheetName)
                On Error GoTo 0
                
                If wsTarget Is Nothing Then
                    MsgBox "工作表 '" & targetSheetName & "' 不存在，跳过处理"
                    canProcess = False
                End If
            End If
            
            ' 只有在文件和工作表都存在时才执行后续复制逻辑
            If canProcess Then
                ' 打开源工作簿（不可见）
                Set wbSource = Workbooks.Open(sourceFile, ReadOnly:=True)
                
                ' 复制数据到目标工作表的G2:R18
                wbSource.Worksheets("指标统计").Range("D4:O20").Copy
                wsTarget.Range("G2:R18").PasteSpecial Paste:=xlPasteValues
                
                ' 关闭源工作簿
                wbSource.Close SaveChanges:=False
            End If
            
            Set wsTarget = Nothing
        End If
    Next cell
    
    Application.CutCopyMode = False
    Application.ScreenUpdating = True
    
    MsgBox "数据更新完成！"
End Sub
