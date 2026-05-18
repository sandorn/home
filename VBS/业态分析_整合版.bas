Option Explicit

' ============================================================
' 业态分析_整合版.vbs
' 功能：整合商写、保险、酒店三个业态分析
' 依赖：VBS_DeepSeekAPI.bas 共享模块
' 原有文件：保留未修改
' ============================================================

' ---- 调试开关 ----
Private Const DEBUG_MODE As Boolean = False

' ---- API 配置常量 ----
Private Const API_BASE_URL As String = "https://api.deepseek.com"
Private Const API_MODEL As String = "deepseek-chat"
Private Const API_TIMEOUT_MS As Long = 30000
Private Const MAX_TOKENS As Long = 1000
Private Const TEMPERATURE As Double = 0.3

' ---- 通用配置 ----
Private Const CONFIG_SHEET_NAME As String = "填写页"
Private Const API_KEY_CELL As String = "I1"
Private Const MONTH_NUMBER_CELL As String = "A2"

' ============================================================
' === 主入口：运行所有业态分析 ===
' ============================================================
Public Sub 运行所有业态分析()
    Dim wsConfig As Worksheet
    Dim apiKey As String
    
    ' 获取配置工作表
    Set wsConfig = VBS_DeepSeekAPI.GetConfigWorksheet(CONFIG_SHEET_NAME)
    If wsConfig Is Nothing Then
        MsgBox "未找到配置工作表：" & CONFIG_SHEET_NAME, vbCritical
        Exit Sub
    End If
    
    ' 读取API Key
    apiKey = VBS_DeepSeekAPI.GetApiKey(wsConfig, API_KEY_CELL, DEBUG_MODE, "主入口")
    If Len(apiKey) = 0 Then
        MsgBox "未配置 API Key，请在 " & CONFIG_SHEET_NAME & "!" & API_KEY_CELL & " 单元格中填写。", vbExclamation
        Exit Sub
    End If
    
    ' 运行各业态分析
    Application.StatusBar = "正在运行所有业态分析..."
    
    运行商写业态分析 apiKey
    运行保险业态分析 apiKey
    运行酒店业态分析 apiKey
    
    Application.StatusBar = False
    MsgBox "所有业态分析完成！", vbInformation, "处理完成"
End Sub

' ============================================================
' === 商写业态分析 ===
' ============================================================
Private Const OS_SHEET_NAME As String = "商写类"
Private Const OS_DATA_RANGE As String = "A1:G18"
Private Const OS_RESULT_CELL As String = "L14"
Private Const OS_SYSTEM_PROMPT_CELL As String = "L1"

Public Sub 运行商写业态分析(Optional ByVal apiKey As String = "")
    Dim wsOS As Worksheet
    Dim wsConfig As Worksheet
    Dim systemMsg As String
    Dim dataPrompt As String
    Dim apiResponse As String
    Dim analysisResult As String
    Dim dataArray As Variant
    Dim prevCalc As XlCalculation
    Dim prevScreenUpdating As Boolean
    Dim prevEnableEvents As Boolean
    
    On Error GoTo ErrorHandler
    
    ' 获取工作表
    Set wsOS = VBS_DeepSeekAPI.GetTargetWorksheet(OS_SHEET_NAME, True)
    If wsOS Is Nothing Then Exit Sub
    
    ' 获取API Key（如果未传入）
    If Len(apiKey) = 0 Then
        Set wsConfig = VBS_DeepSeekAPI.GetConfigWorksheet(CONFIG_SHEET_NAME)
        apiKey = VBS_DeepSeekAPI.GetApiKey(wsConfig, API_KEY_CELL, DEBUG_MODE, OS_SHEET_NAME)
        If Len(apiKey) = 0 Then
            MsgBox "未配置 API Key，请在 " & CONFIG_SHEET_NAME & "!" & API_KEY_CELL & " 单元格中填写。", vbExclamation
            Exit Sub
        End If
    End If
    
    ' 保存并恢复应用状态
    prevScreenUpdating = Application.ScreenUpdating
    prevCalc = Application.Calculation
    prevEnableEvents = Application.EnableEvents
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False
    
    ' 检查系统提示词
    systemMsg = VBS_DeepSeekAPI.GetSystemMessage(wsOS, OS_SYSTEM_PROMPT_CELL)
    If Len(systemMsg) = 0 Then
        MsgBox "系统提示词为空，请在 " & OS_SHEET_NAME & "!" & OS_SYSTEM_PROMPT_CELL & " 单元格中填写。", vbExclamation
        GoTo Cleanup
    End If
    
    ' 读取数据
    dataArray = wsOS.Range(OS_DATA_RANGE).Value
    
    ' 构建提示词
    dataPrompt = "请对以下商写租赁类子公司数据进行客观分析，并按系统提示词指定格式输出。" & vbCrLf & _
                 VBS_DeepSeekAPI.BuildDataPrompt(dataArray)
    
    ' 调用API
    Application.StatusBar = "正在分析商写数据..."
    apiResponse = VBS_DeepSeekAPI.CallDeepSeekAPI( _
        prompt:=dataPrompt, _
        apiKey:=apiKey, _
        apiBaseUrl:=API_BASE_URL, _
        model:=API_MODEL, _
        temperature:=TEMPERATURE, _
        maxTokens:=MAX_TOKENS, _
        timeoutMs:=API_TIMEOUT_MS, _
        contextName:=OS_SHEET_NAME, _
        debugMode:=DEBUG_MODE _
    )
    
    ' 解析响应
    If Left(apiResponse, 5) = "API调用失败" Or Left(apiResponse, 12) = "HTTP请求错误" Then
        analysisResult = apiResponse
    Else
        analysisResult = VBS_DeepSeekAPI.ParseAPIResponseSimple(apiResponse)
    End If
    
    ' 清理并写入结果
    analysisResult = VBS_DeepSeekAPI.CleanAnalysisResult(analysisResult)
    VBS_DeepSeekAPI.WriteAnalysisResult wsOS, OS_RESULT_CELL, analysisResult, DEBUG_MODE, OS_SHEET_NAME
    
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
    MsgBox "商写业态分析错误: " & Err.Description & " (错误代码: " & Err.Number & ")", vbCritical
End Sub

Public Sub 商写业态分析()
    ' 单入口，兼容原有调用方式
    运行商写业态分析
End Sub

' ============================================================
' === 保险业态分析 ===
' ============================================================
Private Const INS_SHEET_NAME As String = "保险类"
Private Const INS_DATA_RANGE As String = "F2:H25"
Private Const INS_RESULT_CELL As String = "L14"
Private Const INS_SYSTEM_PROMPT_CELL As String = "L1"

Public Sub 运行保险业态分析(Optional ByVal apiKey As String = "")
    Dim wsIns As Worksheet
    Dim wsConfig As Worksheet
    Dim systemMsg As String
    Dim dataPrompt As String
    Dim apiResponse As String
    Dim analysisResult As String
    Dim dataArray As Variant
    Dim prevCalc As XlCalculation
    Dim prevScreenUpdating As Boolean
    Dim prevEnableEvents As Boolean
    Dim currentMonth As Long
    
    On Error GoTo ErrorHandler
    
    ' 获取工作表
    Set wsIns = VBS_DeepSeekAPI.GetTargetWorksheet(INS_SHEET_NAME, True)
    If wsIns Is Nothing Then Exit Sub
    
    ' 获取API Key（如果未传入）
    If Len(apiKey) = 0 Then
        Set wsConfig = VBS_DeepSeekAPI.GetConfigWorksheet(CONFIG_SHEET_NAME)
        apiKey = VBS_DeepSeekAPI.GetApiKey(wsConfig, API_KEY_CELL, DEBUG_MODE, INS_SHEET_NAME)
        If Len(apiKey) = 0 Then
            MsgBox "未配置 API Key，请在 " & CONFIG_SHEET_NAME & "!" & API_KEY_CELL & " 单元格中填写。", vbExclamation
            Exit Sub
        End If
    End If
    
    ' 保存并恢复应用状态
    prevScreenUpdating = Application.ScreenUpdating
    prevCalc = Application.Calculation
    prevEnableEvents = Application.EnableEvents
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False
    
    ' 检查系统提示词
    systemMsg = VBS_DeepSeekAPI.GetSystemMessage(wsIns, INS_SYSTEM_PROMPT_CELL)
    If Len(systemMsg) = 0 Then
        MsgBox "系统提示词为空，请在 " & INS_SHEET_NAME & "!" & INS_SYSTEM_PROMPT_CELL & " 单元格中填写。", vbExclamation
        GoTo Cleanup
    End If
    
    ' 获取当前月份
    currentMonth = GetCurrentMonthNumber(wsConfig)
    
    ' 读取数据
    dataArray = wsIns.Range(INS_DATA_RANGE).Value
    
    ' 构建提示词（保险特定：过滤超过当前月份的数据）
    dataPrompt = "以下是两家保险中介类子公司的经营对比数据，请根据系统提示词进行分析，并按指定输出格式给出分析结果。" & vbCrLf & _
                 BuildInsuranceDataPrompt(dataArray, currentMonth)
    
    ' 调用API
    Application.StatusBar = "正在分析保险数据..."
    apiResponse = VBS_DeepSeekAPI.CallDeepSeekAPI( _
        prompt:=dataPrompt, _
        apiKey:=apiKey, _
        apiBaseUrl:=API_BASE_URL, _
        model:=API_MODEL, _
        temperature:=TEMPERATURE, _
        maxTokens:=MAX_TOKENS, _
        timeoutMs:=API_TIMEOUT_MS, _
        contextName:=INS_SHEET_NAME, _
        debugMode:=DEBUG_MODE _
    )
    
    ' 解析响应
    If Left(apiResponse, 5) = "API调用失败" Or Left(apiResponse, 12) = "HTTP请求错误" Then
        analysisResult = apiResponse
    Else
        analysisResult = VBS_DeepSeekAPI.ParseAPIResponseSimple(apiResponse)
    End If
    
    ' 清理并写入结果
    analysisResult = VBS_DeepSeekAPI.CleanAnalysisResult(analysisResult)
    VBS_DeepSeekAPI.WriteAnalysisResult wsIns, INS_RESULT_CELL, analysisResult, DEBUG_MODE, INS_SHEET_NAME
    
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

Public Sub 保险业态分析()
    ' 单入口，兼容原有调用方式
    运行保险业态分析
End Sub

' 保险特定：构建数据提示词（带月份过滤）
Private Function BuildInsuranceDataPrompt(ByVal dataArray As Variant, ByVal currentMonth As Long) As String
    Dim prompt As String
    Dim i As Long, j As Long
    Dim rowText As String
    Dim colCount As Long
    Dim inScaleSection As Boolean
    Dim monthLabel As String
    Dim monthNum As Long
    
    If Not IsArray(dataArray) Then
        BuildInsuranceDataPrompt = "数据无效"
        Exit Function
    End If
    
    colCount = UBound(dataArray, 2)
    prompt = "数据表格如下：" & vbCrLf
    
    For i = 1 To UBound(dataArray, 1)
        ' 识别是否进入"规模保费"部分
        If Not IsEmpty(dataArray(i, 1)) Then
            If Trim$(CStr(dataArray(i, 1))) = "规模保费" Then
                inScaleSection = True
            ElseIf Trim$(CStr(dataArray(i, 1))) = "项目" Then
                inScaleSection = False
            End If
        End If
        
        ' 对规模保费部分的月份行做过滤
        If inScaleSection And i > 1 Then
            monthLabel = CStr(dataArray(i, 1))
            monthNum = ParseMonthLabel(monthLabel)
            If monthNum > 0 And currentMonth > 0 And monthNum > currentMonth Then
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
    
    BuildInsuranceDataPrompt = prompt
End Function

' 保险特定：获取当前月份
Private Function GetCurrentMonthNumber(ByVal wsConfig As Worksheet) As Long
    Dim v As Variant
    
    If wsConfig Is Nothing Then
        GetCurrentMonthNumber = 0
        Exit Function
    End If
    
    v = wsConfig.Range(MONTH_NUMBER_CELL).Value
    If IsNumeric(v) Then
        GetCurrentMonthNumber = CLng(v)
    ElseIf IsDate(v) Then
        GetCurrentMonthNumber = Month(CDate(v))
    Else
        GetCurrentMonthNumber = 0
    End If
End Function

' 保险特定：解析月份标签
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

' ============================================================
' === 酒店业态分析 ===
' ============================================================
Private Const HTL_SHEET_NAME As String = "酒店类"
Private Const HTL_RANGE_MARKETING As String = "B1:D5"
Private Const HTL_RANGE_OTA As String = "E1:G13"
Private Const HTL_RANGE_OCC As String = "I1:K13"
Private Const HTL_RESULT_CELL As String = "M14"
Private Const HTL_SYSTEM_PROMPT_CELL As String = "M1"

Public Sub 运行酒店业态分析(Optional ByVal apiKey As String = "")
    Dim wsHtl As Worksheet
    Dim wsConfig As Worksheet
    Dim systemMsg As String
    Dim dataPrompt As String
    Dim apiResponse As String
    Dim analysisResult As String
    Dim dataMarketing As Variant
    Dim dataOTA As Variant
    Dim dataOcc As Variant
    Dim prevCalc As XlCalculation
    Dim prevScreenUpdating As Boolean
    Dim prevEnableEvents As Boolean
    
    On Error GoTo ErrorHandler
    
    ' 获取工作表
    Set wsHtl = VBS_DeepSeekAPI.GetTargetWorksheet(HTL_SHEET_NAME, True)
    If wsHtl Is Nothing Then Exit Sub
    
    ' 获取API Key（如果未传入）
    If Len(apiKey) = 0 Then
        Set wsConfig = VBS_DeepSeekAPI.GetConfigWorksheet(CONFIG_SHEET_NAME)
        apiKey = VBS_DeepSeekAPI.GetApiKey(wsConfig, API_KEY_CELL, DEBUG_MODE, HTL_SHEET_NAME)
        If Len(apiKey) = 0 Then
            MsgBox "未配置 API Key，请在 " & CONFIG_SHEET_NAME & "!" & API_KEY_CELL & " 单元格中填写。", vbExclamation
            Exit Sub
        End If
    End If
    
    ' 保存并恢复应用状态
    prevScreenUpdating = Application.ScreenUpdating
    prevCalc = Application.Calculation
    prevEnableEvents = Application.EnableEvents
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False
    
    ' 检查系统提示词
    systemMsg = VBS_DeepSeekAPI.GetSystemMessage(wsHtl, HTL_SYSTEM_PROMPT_CELL)
    If Len(systemMsg) = 0 Then
        MsgBox "系统提示词为空，请在 " & HTL_SHEET_NAME & "!" & HTL_SYSTEM_PROMPT_CELL & " 单元格中填写。", vbExclamation
        GoTo Cleanup
    End If
    
    ' 读取数据
    dataMarketing = wsHtl.Range(HTL_RANGE_MARKETING).Value
    dataOTA = wsHtl.Range(HTL_RANGE_OTA).Value
    dataOcc = wsHtl.Range(HTL_RANGE_OCC).Value
    
    ' 构建提示词（酒店特定：三个数据区域）
    dataPrompt = "以下是两家酒店子公司的经营数据，包含三个独立区域：" & vbCrLf & _
                 vbCrLf & _
                 "【区域一：营销活动】" & vbCrLf & _
                 VBS_DeepSeekAPI.BuildDataPrompt(dataMarketing) & vbCrLf & _
                 "【区域二：OTA网络评价】" & vbCrLf & _
                 VBS_DeepSeekAPI.BuildDataPrompt(dataOTA) & vbCrLf & _
                 "【区域三：月均入住率】" & vbCrLf & _
                 VBS_DeepSeekAPI.BuildDataPrompt(dataOcc) & vbCrLf & _
                 "请根据系统提示词进行分析，并按指定输出格式给出分析结果。"
    
    ' 调用API
    Application.StatusBar = "正在分析酒店数据..."
    apiResponse = VBS_DeepSeekAPI.CallDeepSeekAPI( _
        prompt:=dataPrompt, _
        apiKey:=apiKey, _
        apiBaseUrl:=API_BASE_URL, _
        model:=API_MODEL, _
        temperature:=TEMPERATURE, _
        maxTokens:=MAX_TOKENS, _
        timeoutMs:=API_TIMEOUT_MS, _
        contextName:=HTL_SHEET_NAME, _
        debugMode:=DEBUG_MODE _
    )
    
    ' 解析响应
    If Left(apiResponse, 5) = "API调用失败" Or Left(apiResponse, 12) = "HTTP请求错误" Then
        analysisResult = apiResponse
    Else
        analysisResult = VBS_DeepSeekAPI.ParseAPIResponseSimple(apiResponse)
    End If
    
    ' 清理并写入结果
    analysisResult = VBS_DeepSeekAPI.CleanAnalysisResult(analysisResult)
    VBS_DeepSeekAPI.WriteAnalysisResult wsHtl, HTL_RESULT_CELL, analysisResult, DEBUG_MODE, HTL_SHEET_NAME
    
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
    MsgBox "酒店业态分析错误: " & Err.Description & " (错误代码: " & Err.Number & ")", vbCritical
End Sub

Public Sub 酒店业态分析()
    ' 单入口，兼容原有调用方式
    运行酒店业态分析
End Sub

