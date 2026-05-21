Option Explicit

' ============================================================================
' 子公司核心指标分析 - 依赖 DeepSeekAPI.bas 公共模块
' ============================================================================
' 优化说明：
' 1. 重试机制：API调用失败时自动重试（最多2次）
' 2. 分批处理：每3家公司一批，批次间增加延迟避免API限流
' 3. 质量检查：自动检查分析结果是否包含所有必要指标
' 4. 单公司重分析：支持对单个公司重新分析
' 5. 系统提示词从配置表读取，为空时停止分析并提醒
' 6. JSON/HTTP/数据构建等公共函数统一使用 DeepSeekAPI.bas
' ============================================================================

Private Const DEBUG_MODE As Boolean = False

' ---- API 参数（与 DeepSeekAPI.bas 默认值不同）----
Private Const API_TIMEOUT_MS As Long = 60000
Private Const MAX_TOKENS As Long = 1500
Private Const TEMPERATURE As Double = 0.3

' ---- 重试与限流配置 ----
Private Const MAX_RETRIES As Long = 2
Private Const RETRY_DELAY_MS As Long = 2000
Private Const BATCH_DELAY_MS As Long = 1000
Private Const BATCH_SIZE As Long = 3

' ---- 工作表数据范围常量 ----
Private Const DATA_RANGE As String = "C1:R5"
Private Const RESULT_CELL As String = "C61"
Private Const CONFIG_SHEET As String = "填写页"
Private Const TARGET_RANGE As String = "C2:C10"
Private Const MONTH_NUMBER_CELL As String = "A2"
Private Const YEAR_CELL As String = "A4"
Private Const PROGRESS_CELL As String = "A8"
Private Const SYSTEM_PROMPT_CELL As String = "C20"

' ============================================================================
' 自定义类型
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

Private Function GetProgressFromConfig() As Double
    Dim wsConfig As Worksheet
    Dim v As Variant
    Dim s As String
    Dim monthNum As Long

    Set wsConfig = GetConfigSheet()
    If wsConfig Is Nothing Then
        GetProgressFromConfig = 0#
        Exit Function
    End If

    v = wsConfig.Range(PROGRESS_CELL).Value

    If IsEmpty(v) Then
        GoTo FallbackMonth
    End If

    If IsNumeric(v) Then
        Dim val As Double
        val = CDbl(v)
        If val <= 1# Then
            GetProgressFromConfig = val * 100#
        Else
            GetProgressFromConfig = val
        End If
        Exit Function
    End If

    s = Trim$(CStr(v))
    s = Replace(s, "%", "")
    If IsNumeric(s) Then
        GetProgressFromConfig = CDbl(s)
        Exit Function
    End If

FallbackMonth:
    monthNum = GetMonthNumberFromConfig()
    If monthNum >= 1 And monthNum <= 12 Then
        GetProgressFromConfig = (monthNum / 12#) * 100#
    Else
        GetProgressFromConfig = 0#
    End If
End Function

' ============================================================================
' 分析结果质量检查
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

' 质量不足时重新分析（使用 DeepSeekAPI.bas 公共函数）
Private Function AnalyzeWithQualityCheck(companyName As String, dataPrompt As String, apiKey As String, systemMsg As String) As String
    Dim apiResponse As String
    Dim analysisResult As String
    Dim quality As AnalysisQuality
    Dim retryCount As Long

    For retryCount = 0 To MAX_RETRIES
        ' 调用 DeepSeekAPI.bas 公共函数（内部已含HTTP层重试，此处设为0避免嵌套）
        apiResponse = CallDeepSeekAPI(dataPrompt, apiKey, API_BASE_URL, API_MODEL, TEMPERATURE, MAX_TOKENS, API_TIMEOUT_MS, companyName, DEBUG_MODE, 1, systemMsg)

        If Left(apiResponse, 1) = "{" Then
            analysisResult = ParseAPIResponseSimple(apiResponse)
        Else
            analysisResult = apiResponse
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
' 主业务流程
' ============================================================================

Private Function AnalyzeCompany(companyName As String, Optional index As Long = 0, Optional total As Long = 0, Optional apiKey As String = "", Optional systemMsg As String = "") As Boolean
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
    Else
        monthText = "未知"
    End If
    progressPercent = GetProgressFromConfig()

    ' 使用 DeepSeekAPI.bas 公共函数构建数据提示词
    dataPrompt = "公司名称：" & companyName & vbCrLf & _
                 "年份：" & GetAnalysisYear() & vbCrLf & _
                 "当前月份：" & monthText & vbCrLf & _
                 "序时进度：" & Format$(progressPercent, "0.00") & "%" & vbCrLf & _
                 "数据单位：万元" & vbCrLf & _
                 "请按系统提示词要求输出指定格式。" & vbCrLf & _
                 BuildDataPrompt(wsData)

    analysisResult = AnalyzeWithQualityCheck(companyName, dataPrompt, apiKey, systemMsg)

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

Public Sub 多轮经营分析()
    Dim wsConfig As Worksheet
    Dim targetSheetNames As Range
    Dim companyName As String
    Dim prevCalc As XlCalculation
    Dim prevScreenUpdating As Boolean
    Dim prevEnableEvents As Boolean
    Dim processedCount As Long
    Dim totalCount As Long
    Dim companyIndex As Long
    Dim batchCount As Long
    Dim targetNames As Variant
    Dim rowIdx As Long
    Dim apiKey As String
    Dim systemMsg As String

    On Error GoTo ErrorHandler

    prevScreenUpdating = Application.ScreenUpdating
    prevCalc = Application.Calculation
    prevEnableEvents = Application.EnableEvents

    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False

    Set wsConfig = ThisWorkbook.Worksheets(CONFIG_SHEET)
    Set targetSheetNames = wsConfig.Range(TARGET_RANGE)
    targetNames = targetSheetNames.Value

    totalCount = 0
    If IsArray(targetNames) Then
        For rowIdx = 1 To UBound(targetNames, 1)
            If Len(Trim(CStr(targetNames(rowIdx, 1)))) > 0 Then totalCount = totalCount + 1
        Next rowIdx
    Else
        If Len(Trim(CStr(targetNames))) > 0 Then totalCount = 1
    End If

    If totalCount = 0 Then
        MsgBox "未找到待分析的公司名称，请在填写页C2:C10范围内填写。", vbExclamation
        GoTo Cleanup
    End If

    systemMsg = GetSystemMessage()
    If Len(systemMsg) = 0 Then
        MsgBox "错误：系统提示词未配置！" & vbCrLf & vbCrLf & _
               "请在 '" & CONFIG_SHEET & "' 工作表的 " & SYSTEM_PROMPT_CELL & " 单元格中填写分析提示词。", vbCritical
        GoTo Cleanup
    End If

    ' 使用 DeepSeekAPI.bas 公共函数获取 API Key
    apiKey = GetApiKey(DEBUG_MODE, "核心指标")
    If Len(apiKey) = 0 Then
        MsgBox "未配置 API Key，请在 ~\.dskey 文件中设置 [EXCEL] 段。", vbExclamation
        GoTo Cleanup
    End If

    processedCount = 0
    companyIndex = 0
    batchCount = 0

    If IsArray(targetNames) Then
        For rowIdx = 1 To UBound(targetNames, 1)
            companyName = Trim(CStr(targetNames(rowIdx, 1)))
            If Len(companyName) > 0 Then
                companyIndex = companyIndex + 1
                batchCount = batchCount + 1

                Application.StatusBar = "正在分析: " & companyName & " (" & companyIndex & "/" & totalCount & ")"

                If AnalyzeCompany(companyName, companyIndex, totalCount, apiKey, systemMsg) Then
                    processedCount = processedCount + 1
                    If DEBUG_MODE Then Debug.Print "成功分析(" & companyIndex & "/" & totalCount & "): " & companyName
                Else
                    If DEBUG_MODE Then Debug.Print "分析失败(" & companyIndex & "/" & totalCount & "): " & companyName
                End If

                If batchCount Mod BATCH_SIZE = 0 And companyIndex < totalCount Then
                    If DEBUG_MODE Then Debug.Print "批次完成，等待 " & BATCH_DELAY_MS & "ms 后继续..."
                    Application.StatusBar = "批次完成，等待 " & BATCH_DELAY_MS & "ms 后继续..."
                    Application.Wait Now + TimeSerial(0, 0, BATCH_DELAY_MS / 1000)
                End If
            End If
        Next rowIdx
    Else
        companyName = Trim(CStr(targetNames))
        If Len(companyName) > 0 Then
            companyIndex = 1
            batchCount = 1
            Application.StatusBar = "正在分析: " & companyName & " (1/1)"
            If AnalyzeCompany(companyName, 1, 1, apiKey, systemMsg) Then
                processedCount = 1
            Else
                If DEBUG_MODE Then Debug.Print "分析失败(1/1): " & companyName
            End If
        End If
    End If

Cleanup:
    Application.Calculation = prevCalc
    Application.EnableEvents = prevEnableEvents
    Application.ScreenUpdating = prevScreenUpdating
    Application.StatusBar = False

    MsgBox "分析完成！共处理 " & processedCount & "/" & totalCount & " 家公司。", vbInformation
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
' 单公司快速重分析
' ============================================================================

Public Sub 单公司重分析()
    Dim companyName As String
    Dim wsConfig As Worksheet
    Dim apiKey As String
    Dim systemMsg As String

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

    systemMsg = GetSystemMessage()
    If Len(systemMsg) = 0 Then
        MsgBox "系统提示词未配置，请在 '" & CONFIG_SHEET & "' 工作表的 " & SYSTEM_PROMPT_CELL & " 单元格中填写。", vbExclamation
        Exit Sub
    End If

    apiKey = GetApiKey(DEBUG_MODE, companyName)
    If Len(apiKey) = 0 Then
        MsgBox "未配置 API Key", vbExclamation
        Exit Sub
    End If

    If MsgBox("确认重新分析 """ & companyName & """？", vbYesNo + vbQuestion) = vbYes Then
        If AnalyzeCompany(companyName, 1, 1, apiKey, systemMsg) Then
            MsgBox "重新分析完成！", vbInformation
        Else
            MsgBox "重新分析失败！", vbExclamation
        End If
    End If
End Sub
