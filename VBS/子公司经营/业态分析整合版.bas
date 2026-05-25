Option Explicit

' ============================================================
' 业态分析整合版 — 一键运行商写、保险、酒店三个业态分析
' 依赖：DeepSeekAPI.bas（需在同一 VBA 项目中）
' ============================================================

' ---- 商写业态配置 ----
Private Const OS_SHEET_NAME As String = "商写类"
Private Const OS_DATA_RANGE As String = "A1:G18" ' 包含商写子公司的运营数据
Private Const OS_RESULT_CELL As String = "L14"
Private Const OS_SYSTEM_PROMPT_CELL As String = "L1"

' ---- 保险业态配置 ----
Private Const INS_SHEET_NAME As String = "保险类"
Private Const INS_DATA_RANGE As String = "F1:H25" ' 包含规模保费和人力两部分数据
Private Const INS_RESULT_CELL As String = "L14"
Private Const INS_SYSTEM_PROMPT_CELL As String = "L1"

' ---- 酒店业态配置 ----
Private Const HTL_SHEET_NAME As String = "酒店类"
Private Const HTL_RANGE_MARKETING As String = "B1:D5" ' 营销活动数据区域
Private Const HTL_RANGE_OTA As String = "E1:G13" ' OTA网络评价数据区域
Private Const HTL_RANGE_OCC As String = "I1:K13" ' 月均入住率数据区域
Private Const HTL_RESULT_CELL As String = "M14"
Private Const HTL_SYSTEM_PROMPT_CELL As String = "M1"

' ============================================================
' === 主入口：运行所有业态分析 ===
' ============================================================

Public Sub 运行所有业态分析()
    Dim apiKey As String
    apiKey = GetApiKey(DEBUG_MODE, "主入口")
    If Len(apiKey) = 0 Then MsgBox "未配置 API Key，请在 ~\.dskey 文件中设置 [EXCEL] 段。", vbExclamation : Exit Sub
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

Public Sub 运行商写业态分析(Optional ByVal apiKey As String = "")
    Dim wsOS As Worksheet, wsConfig As Worksheet, systemMsg As String, dataPrompt As String
    Dim apiResponse As String, analysisResult As String, dataArray As Variant
    Dim prevCalc As XlCalculation, prevScreenUpdating As Boolean, prevEnableEvents As Boolean
    
     On Error Goto ErrorHandler
    Set wsOS = GetTargetWorksheet(OS_SHEET_NAME, True)
    If wsOS Is Nothing Then Exit Sub
    If Len(apiKey) = 0 Then apiKey = GetApiKey(DEBUG_MODE, OS_SHEET_NAME) : If Len(apiKey) = 0 Then MsgBox "未配置 API Key", vbExclamation : Exit Sub
    prevScreenUpdating = Application.ScreenUpdating : prevCalc = Application.Calculation : prevEnableEvents = Application.EnableEvents
    Application.ScreenUpdating = False : Application.Calculation = xlCalculationManual : Application.EnableEvents = False
    
    systemMsg = GetSystemMessage(wsOS, OS_SYSTEM_PROMPT_CELL)
    If Len(systemMsg) = 0 Then MsgBox "系统提示词为空，请在 " & OS_SHEET_NAME & "!" & OS_SYSTEM_PROMPT_CELL & " 单元格中填写。", vbExclamation : Goto Cleanup
    
    dataArray = wsOS.Range(OS_DATA_RANGE).Value
    dataPrompt = "请对以下商写租赁类子公司数据进行客观分析，并按系统提示词指定格式输出。" & vbCrLf & BuildDataPrompt(dataArray)
    Application.StatusBar = "正在分析商写数据..."
    apiResponse = CallDeepSeekAPI(dataPrompt, apiKey, API_BASE_URL, API_MODEL, TEMPERATURE, MAX_TOKENS, API_TIMEOUT_MS, OS_SHEET_NAME, DEBUG_MODE, , systemMsg)
    If Left(apiResponse, 1) = "{" Then analysisResult = ParseAPIResponseSimple(apiResponse) Else analysisResult = apiResponse
    analysisResult = CleanAnalysisResult(analysisResult)
    WriteAnalysisResult wsOS, OS_RESULT_CELL, analysisResult, DEBUG_MODE, OS_SHEET_NAME
    Goto Cleanup
    
    ErrorHandler :
    On Error Resume Next : Application.Calculation = prevCalc : Application.EnableEvents = prevEnableEvents : Application.ScreenUpdating = prevScreenUpdating : Application.StatusBar = False : On Error GoTo 0
    MsgBox "商写业态分析错误: " & Err.Description, vbCritical
    Exit Sub
    Cleanup :
    Application.Calculation = prevCalc : Application.EnableEvents = prevEnableEvents : Application.ScreenUpdating = prevScreenUpdating : Application.StatusBar = False
End Sub

Public Sub 商写业态分析() : 运行商写业态分析 : End Sub

' ============================================================
' === 保险业态分析 ===
' ============================================================

Public Sub 运行保险业态分析(Optional ByVal apiKey As String = "")
    Dim wsIns As Worksheet, wsConfig As Worksheet, systemMsg As String, dataPrompt As String
    Dim apiResponse As String, analysisResult As String, dataArray As Variant, currentMonth As Long
    Dim prevCalc As XlCalculation, prevScreenUpdating As Boolean, prevEnableEvents As Boolean
    
     On Error Goto ErrorHandler
    Set wsIns = GetTargetWorksheet(INS_SHEET_NAME, True)
    If wsIns Is Nothing Then Exit Sub
    If Len(apiKey) = 0 Then apiKey = GetApiKey(DEBUG_MODE, INS_SHEET_NAME) : If Len(apiKey) = 0 Then MsgBox "未配置 API Key", vbExclamation : Exit Sub
    prevScreenUpdating = Application.ScreenUpdating : prevCalc = Application.Calculation : prevEnableEvents = Application.EnableEvents
    Application.ScreenUpdating = False : Application.Calculation = xlCalculationManual : Application.EnableEvents = False
    
    systemMsg = GetSystemMessage(wsIns, INS_SYSTEM_PROMPT_CELL)
    If Len(systemMsg) = 0 Then MsgBox "系统提示词为空，请在 " & INS_SHEET_NAME & "!" & INS_SYSTEM_PROMPT_CELL & " 单元格中填写。", vbExclamation : Goto Cleanup
    
    Set wsConfig = GetConfigWorksheet(CONFIG_SHEET_NAME)
    currentMonth = GetCurrentMonthNumber(wsConfig)
    dataArray = wsIns.Range(INS_DATA_RANGE).Value
    dataPrompt = "以下是两家保险中介类子公司的经营对比数据，请根据系统提示词进行分析，并按指定输出格式给出分析结果。" & vbCrLf & BuildInsuranceDataPrompt(dataArray, currentMonth)
    Application.StatusBar = "正在分析保险数据..."
    apiResponse = CallDeepSeekAPI(dataPrompt, apiKey, API_BASE_URL, API_MODEL, TEMPERATURE, MAX_TOKENS, API_TIMEOUT_MS, INS_SHEET_NAME, DEBUG_MODE, , systemMsg)
    If Left(apiResponse, 1) = "{" Then analysisResult = ParseAPIResponseSimple(apiResponse) Else analysisResult = apiResponse
    analysisResult = CleanAnalysisResult(analysisResult)
    WriteAnalysisResult wsIns, INS_RESULT_CELL, analysisResult, DEBUG_MODE, INS_SHEET_NAME
    Goto Cleanup
    
    ErrorHandler :
    On Error Resume Next : Application.Calculation = prevCalc : Application.EnableEvents = prevEnableEvents : Application.ScreenUpdating = prevScreenUpdating : Application.StatusBar = False : On Error GoTo 0
    MsgBox "保险业态分析错误: " & Err.Description, vbCritical
    Exit Sub
    Cleanup :
    Application.Calculation = prevCalc : Application.EnableEvents = prevEnableEvents : Application.ScreenUpdating = prevScreenUpdating : Application.StatusBar = False
End Sub

Public Sub 保险业态分析() : 运行保险业态分析 : End Sub

' ============================================================
' === 酒店业态分析 ===
' ============================================================

Public Sub 运行酒店业态分析(Optional ByVal apiKey As String = "")
    Dim wsHtl As Worksheet, wsConfig As Worksheet, systemMsg As String, dataPrompt As String
    Dim apiResponse As String, analysisResult As String
    Dim dataMarketing As Variant, dataOTA As Variant, dataOcc As Variant
    Dim prevCalc As XlCalculation, prevScreenUpdating As Boolean, prevEnableEvents As Boolean
    
     On Error Goto ErrorHandler
    Set wsHtl = GetTargetWorksheet(HTL_SHEET_NAME, True)
    If wsHtl Is Nothing Then Exit Sub
    If Len(apiKey) = 0 Then apiKey = GetApiKey(DEBUG_MODE, HTL_SHEET_NAME) : If Len(apiKey) = 0 Then MsgBox "未配置 API Key", vbExclamation : Exit Sub
    prevScreenUpdating = Application.ScreenUpdating : prevCalc = Application.Calculation : prevEnableEvents = Application.EnableEvents
    Application.ScreenUpdating = False : Application.Calculation = xlCalculationManual : Application.EnableEvents = False
    
    systemMsg = GetSystemMessage(wsHtl, HTL_SYSTEM_PROMPT_CELL)
    If Len(systemMsg) = 0 Then MsgBox "系统提示词为空，请在 " & HTL_SHEET_NAME & "!" & HTL_SYSTEM_PROMPT_CELL & " 单元格中填写。", vbExclamation : Goto Cleanup
    
    dataMarketing = wsHtl.Range(HTL_RANGE_MARKETING).Value
    dataOTA = wsHtl.Range(HTL_RANGE_OTA).Value
    dataOcc = wsHtl.Range(HTL_RANGE_OCC).Value
    dataPrompt = "以下是两家酒店子公司的经营数据，包含三个独立区域：" & vbCrLf & vbCrLf & "【区域一：营销活动】" & vbCrLf & BuildDataPrompt(dataMarketing) & vbCrLf & "【区域二：OTA网络评价】" & vbCrLf & BuildDataPrompt(dataOTA) & vbCrLf & "【区域三：月均入住率】" & vbCrLf & BuildDataPrompt(dataOcc) & vbCrLf & "请根据系统提示词进行分析，并按指定输出格式给出分析结果。"
    Application.StatusBar = "正在分析酒店数据..."
    apiResponse = CallDeepSeekAPI(dataPrompt, apiKey, API_BASE_URL, API_MODEL, TEMPERATURE, MAX_TOKENS, API_TIMEOUT_MS, HTL_SHEET_NAME, DEBUG_MODE, , systemMsg)
    If Left(apiResponse, 1) = "{" Then analysisResult = ParseAPIResponseSimple(apiResponse) Else analysisResult = apiResponse
    analysisResult = CleanAnalysisResult(analysisResult)
    WriteAnalysisResult wsHtl, HTL_RESULT_CELL, analysisResult, DEBUG_MODE, HTL_SHEET_NAME
    Goto Cleanup
    
    ErrorHandler :
    On Error Resume Next : Application.Calculation = prevCalc : Application.EnableEvents = prevEnableEvents : Application.ScreenUpdating = prevScreenUpdating : Application.StatusBar = False : On Error GoTo 0
    MsgBox "酒店业态分析错误: " & Err.Description, vbCritical
    Exit Sub
    Cleanup :
    Application.Calculation = prevCalc : Application.EnableEvents = prevEnableEvents : Application.ScreenUpdating = prevScreenUpdating : Application.StatusBar = False
End Sub

Public Sub 酒店业态分析() : 运行酒店业态分析 : End Sub

' ============================================================
' === 保险业态专用函数 ===
' ============================================================

Private Function BuildInsuranceDataPrompt(ByVal dataArray As Variant, ByVal currentMonth As Long) As String
    Dim prompt As String, i As Long, j As Long, rowText As String, colCount As Long
    Dim inScaleSection As Boolean, monthLabel As String, monthNum As Long
    If Not IsArray(dataArray) Then BuildInsuranceDataPrompt = "数据无效" : Exit Function
    colCount = UBound(dataArray, 2) : prompt = "数据表格如下：" & vbCrLf
    For i = 1 To UBound(dataArray, 1)
        If Not IsEmpty(dataArray(i, 1)) Then
            If Trim$(CStr(dataArray(i, 1))) = "规模保费" Then
                inScaleSection = True
            ElseIf Trim$(CStr(dataArray(i, 1))) = "项目" Then
                inScaleSection = False
            End If
        End If
        If inScaleSection And i > 1 Then monthLabel = CStr(dataArray(i, 1)) : monthNum = ParseMonthLabel(monthLabel) : If monthNum > 0 And currentMonth > 0 And monthNum > currentMonth Then Goto NextRow
        rowText = "|"
        For j = 1 To colCount
            If Not IsEmpty(dataArray(i, j)) Then rowText = rowText & " " & CStr(dataArray(i, j)) & " |" Else rowText = rowText & " |"
        Next j
        prompt = prompt & rowText & vbCrLf
        NextRow :
    Next i
    BuildInsuranceDataPrompt = prompt
End Function

Private Function GetCurrentMonthNumber(ByVal wsConfig As Worksheet) As Long
    Dim v As Variant
    If wsConfig Is Nothing Then GetCurrentMonthNumber = 0 : Exit Function
    v = wsConfig.Range(MONTH_NUMBER_CELL).Value
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
    If Len(t) = 0 Then ParseMonthLabel = 0 : Exit Function
    If Right$(t, 1) = "月" Then t = Left$(t, Len(t) - 1)
    If IsNumeric(t) Then ParseMonthLabel = CLng(t) Else ParseMonthLabel = 0
End Function