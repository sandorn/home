Option Explicit

' ============================================================
' 酒店数据汇总.vbs
' 功能：汇总伯豪瑞廷、重庆瑞尔的营销活动数据和业务指标
' 数据源：活动量文件夹下的 xlsx 文件 + 经营报表文件夹下的 xlsx 文件
' 结果写入：【2026年4月】经营数据.et 的"酒店类"工作表
'
' 提取数字逻辑：在源文件中创建辅助区域（从AE列开始），
' 用Excel公式提取每个单元格中的首个连续数字，然后用公式汇总。
' ============================================================

' ---- 常量定义 ----
Private Const TARGET_SHEET_NAME As String = "酒店类"
Private Const ACTIVITY_FOLDER As String = "活动量"
Private Const REPORT_FOLDER As String = "经营报表"

' 源文件名
Private Const BHRT_SOURCE_FILE As String = "伯豪瑞廷.xlsx"
Private Const CQRER_SOURCE_FILE As String = "重庆瑞尔.xlsx"

' 源工作表名
Private Const ACTIVITY_SHEET_NAME As String = "酒店类"
Private Const REPORT_SHEET_NAME As String = "指标统计"

' ---- 营销活动 ----
' 目标结果区域：A1:D5
' A列=类别, B列=项目, C列=伯豪瑞廷, D列=重庆瑞尔
Private Const TARGET_COL_BHRT As Long = 3 ' C列
Private Const TARGET_COL_CQRER As Long = 4 ' D列

' 伯豪瑞廷营销活动行分组（在12:23范围内）
' 投放数量：12-14行（官微、抖音、OTA）
' 受众数量：15-17行（官微、抖音、OTA）
' 成交数量：18-20行（官微、抖音、OTA）
Private Const BHRT_PUT_ROW1 As Long = 12 ' 投放数量-官微
Private Const BHRT_PUT_ROW2 As Long = 13 ' 投放数量-抖音
Private Const BHRT_PUT_ROW3 As Long = 14 ' 投放数量-OTA
Private Const BHRT_AUD_ROW1 As Long = 15 ' 受众数量-官微
Private Const BHRT_AUD_ROW2 As Long = 16 ' 受众数量-抖音
Private Const BHRT_AUD_ROW3 As Long = 17 ' 受众数量-OTA
Private Const BHRT_DEAL_ROW1 As Long = 18 ' 成交数量-官微
Private Const BHRT_DEAL_ROW2 As Long = 19 ' 成交数量-抖音
Private Const BHRT_DEAL_ROW3 As Long = 20 ' 成交数量-OTA

' 重庆瑞尔营销活动行号
Private Const CQRER_PUT_ROW As Long = 12 ' 投放数量
Private Const CQRER_AUD_ROW As Long = 13 ' 受众数量
Private Const CQRER_DEAL_ROW As Long = 14 ' 成交数量

' ---- 业务指标 ----
' 目标结果区域：E1:K13
Private Const TARGET_OTA_COL_BHRT As Long = 6 ' F列（伯豪瑞廷OTA）
Private Const TARGET_OTA_COL_CQRER As Long = 7 ' G列（重庆瑞尔OTA）
Private Const TARGET_OCC_COL_BHRT As Long = 10 ' J列（伯豪瑞廷入住率）
Private Const TARGET_OCC_COL_CQRER As Long = 11 ' K列（重庆瑞尔入住率）
Private Const TARGET_MONTH_START_ROW As Long = 2 ' 1月所在行（第2行）

' 填写页配置
Private Const CONFIG_SHEET_NAME As String = "填写页"
Private Const MONTH_NUMBER_CELL As String = "A2"

' 经营报表中指标行号
Private Const REPORT_ROW_OCCUPANCY As Long = 15 ' 月均入住率
Private Const REPORT_ROW_OTA_RATING As Long = 17 ' OTA网络评价

' 辅助区域起始列（AE列 = 第31列）
Private Const AUX_START_COL As Long = 31

' ============================================================
' 主入口
' ============================================================
Public Sub 酒店数据汇总()
    Dim prevScreenUpdating As Boolean
    Dim prevCalculation As XlCalculation
    Dim prevEnableEvents As Boolean
    Dim wsTarget As Worksheet
    Dim sourceFolderPath As String
    Dim reportFolderPath As String

    prevScreenUpdating = Application.ScreenUpdating
    prevCalculation = Application.Calculation
    prevEnableEvents = Application.EnableEvents

    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False

     On Error Goto ErrorHandler

    ' 获取目标工作表
    Set wsTarget = GetTargetWorksheet()
    If wsTarget Is Nothing Then
        MsgBox "目标工作表 '" & TARGET_SHEET_NAME & "' 不存在！", vbCritical
        Goto Cleanup
    End If

    ' 构建文件夹路径
    sourceFolderPath = ThisWorkbook.path & "\" & ACTIVITY_FOLDER & "\"
    reportFolderPath = ThisWorkbook.path & "\" & REPORT_FOLDER & "\"

    ' 检查文件夹是否存在
    If Dir(sourceFolderPath, vbDirectory) = "" Then
        MsgBox "活动量文件夹不存在: " & sourceFolderPath, vbCritical
        Goto Cleanup
    End If
    If Dir(reportFolderPath, vbDirectory) = "" Then
        MsgBox "经营报表文件夹不存在: " & reportFolderPath, vbCritical
        Goto Cleanup
    End If

    ' ==========================================
    ' 第一部分：营销活动数据汇总
    ' ==========================================
    Application.StatusBar = "正在处理营销活动数据..."

    ' 处理伯豪瑞廷营销活动
    ProcessActivityBHRT sourceFolderPath, wsTarget

    ' 处理重庆瑞尔营销活动
    ProcessActivityCQRER sourceFolderPath, wsTarget

    ' 写入转化率公式
    WriteConversionRateFormulas wsTarget

    ' ==========================================
    ' 第二部分：业务指标数据汇总
    ' ==========================================
    Application.StatusBar = "正在处理业务指标数据..."

    ' 处理伯豪瑞廷业务指标
    ProcessReportBHRT reportFolderPath, wsTarget

    ' 处理重庆瑞尔业务指标
    ProcessReportCQRER reportFolderPath, wsTarget

    ' 设置格式
    FormatTargetSheet wsTarget

    MsgBox "酒店类数据汇总完成！", vbInformation, "处理完成"

    Cleanup :
    Application.ScreenUpdating = prevScreenUpdating
    Application.Calculation = prevCalculation
    Application.EnableEvents = prevEnableEvents
    Application.StatusBar = False
    Exit Sub

    ErrorHandler :
    MsgBox "处理过程中发生错误: " & Err.Description & vbCrLf & _
        "错误代码: " & Err.Number, vbCritical
    Err.Clear
    Goto Cleanup
End Sub

' ============================================================
' 获取目标工作表
' ============================================================
Private Function GetTargetWorksheet() As Worksheet
    On Error Resume Next
    Set GetTargetWorksheet = ThisWorkbook.Worksheets(TARGET_SHEET_NAME)
    On Error GoTo 0
End Function

' ============================================================
' 从填写页读取报告月份（填写页!A2）
' ============================================================
Private Function GetTargetMonth() As Long
    Dim wsConfig As Worksheet
    Dim v As Variant

    On Error Resume Next
    Set wsConfig = ThisWorkbook.Worksheets(CONFIG_SHEET_NAME)
    On Error GoTo 0

    If wsConfig Is Nothing Then
        GetTargetMonth = GetMonthFromFolderName()
        Exit Function
    End If

    v = wsConfig.Range(MONTH_NUMBER_CELL).Value
    If IsNumeric(v) Then
        GetTargetMonth = CLng(v)
    ElseIf IsDate(v) Then
        GetTargetMonth = Month(CDate(v))
    Else
        GetTargetMonth = GetMonthFromFolderName()
    End If
End Function

' ============================================================
' 从文件夹名解析报告月份（回退方案）
' ============================================================
Private Function GetMonthFromFolderName() As Long
    Dim pathParts As Variant
    Dim folderName As String
    Dim yearPos As Long
    Dim monthPos As Long
    Dim monthStr As String
    Dim i As Long

    pathParts = Split(ThisWorkbook.path, "\")
    folderName = pathParts(UBound(pathParts))

    yearPos = InStr(1, folderName, "年", vbTextCompare)
    If yearPos = 0 Then Goto Fallback

    monthPos = InStr(yearPos + 1, folderName, "月", vbTextCompare)
    If monthPos = 0 Then Goto Fallback

    monthStr = ""
    For i = yearPos + 1 To monthPos - 1
        If IsNumeric(Mid $(folderName, i, 1)) Then
            monthStr = monthStr & Mid $(folderName, i, 1)
        End If
    Next i

    If Len(monthStr) > 0 And IsNumeric(monthStr) Then
        GetMonthFromFolderName = CLng(monthStr)
        Exit Function
    End If

    Fallback :
    GetMonthFromFolderName = Month(Date)
End Function

' ============================================================
' 提取单元格中的首个连续数字（VBA直接计算）
' 处理逻辑：
' 1. 空单元格 → 0
' 2. 数值单元格 → 直接取值
' 3. 文本单元格 → 提取首个连续数字串
'    例如 "直播1736场" → 1736
' 4. 含加号的文本（如 "1+1000"）→ 分别提取各段数字后相加
'    结果 = 1 + 1000 = 1001
' ============================================================
Private Function ExtractNumberFromCell(ByVal cellValue As Variant) As Double
    Dim strVal As String
    Dim parts As Variant
    Dim i As Long
    Dim total As Double
    Dim numStr As String
    Dim j As Long
    Dim ch As String

    ' 空值
    If IsEmpty(cellValue) Then
        ExtractNumberFromCell = 0
        Exit Function
    End If

    ' 错误值
    If IsError(cellValue) Then
        ExtractNumberFromCell = 0
        Exit Function
    End If

    ' 数值
    If IsNumeric(cellValue) Then
        ExtractNumberFromCell = CDbl(cellValue)
        Exit Function
    End If

    ' 文本：检查是否包含加号
    strVal = CStr(cellValue)
    If InStr(1, strVal, "+", vbTextCompare) > 0 Then
        ' 按加号分割，分别提取数字后相加
        parts = Split(strVal, "+")
        total = 0
        For i = 0 To UBound(parts)
            total = total + ExtractSingleNumber(parts(i))
        Next i
        ExtractNumberFromCell = total
    Else
        ' 直接提取首个连续数字
        ExtractNumberFromCell = ExtractSingleNumber(strVal)
    End If
End Function

' 从字符串中提取首个连续数字
Private Function ExtractSingleNumber(ByVal text As String) As Double
    Dim i As Long
    Dim ch As String
    Dim numStr As String
    Dim foundDigit As Boolean
    Dim foundDot As Boolean

    numStr = ""
    foundDigit = False
    foundDot = False

    For i = 1 To Len(text)
        ch = Mid $(text, i, 1)
        If ch >= "0" And ch <= "9" Then
            numStr = numStr & ch
            foundDigit = True
        ElseIf ch = "." And foundDigit And Not foundDot Then
            ' 小数点（仅当已找到数字且尚未出现小数点时）
            numStr = numStr & ch
            foundDot = True
        ElseIf foundDigit Then
            ' 已找到数字后又遇到非数字字符，结束提取
            Exit For
        End If
    Next i

    If Len(numStr) > 0 And IsNumeric(numStr) Then
        ExtractSingleNumber = CDbl(numStr)
    Else
        ExtractSingleNumber = 0
    End If
End Function

' ============================================================
' 在源工作表中创建辅助列（伯豪瑞廷版：连续列）
' 辅助列从 AE列开始，与源数据列一一对应
' 用VBA直接计算提取数字并写入辅助区域
' ============================================================
Private Sub CreateAuxFormulasBHRT(ByVal wsSource As Worksheet, _
        ByVal srcRow As Long, _
        ByVal numMonths As Long)
    ' 伯豪瑞廷达成列：E=5(1月), G=7(2月), I=9(3月), K=11(4月), ...
    ' 辅助列：AE=31(1月), AF=32(2月), AG=33(3月), AH=34(4月), ...
    Dim m As Long
    Dim srcCol As Long
    Dim auxCol As Long
    Dim cellValue As Variant

    For m = 1 To numMonths
        srcCol = 2 * m + 3 ' E=5, G=7, I=9, K=11, ...
        auxCol = AUX_START_COL + (m - 1) ' AE=31, AF=32, AG=33, ...
        cellValue = wsSource.Cells(srcRow, srcCol).Value
        wsSource.Cells(srcRow, auxCol).Value = ExtractNumberFromCell(cellValue)
    Next m
End Sub

' ============================================================
' 在源工作表中创建辅助列（重庆瑞尔版：隔列）
' 辅助列从 AE列开始，与源数据达成列一一对应
' 用VBA直接计算提取数字并写入辅助区域
' ============================================================
Private Sub CreateAuxFormulasCQRER(ByVal wsSource As Worksheet, _
        ByVal srcRow As Long, _
        ByVal numMonths As Long)
    ' 重庆瑞尔达成列：D=4(1月), F=6(2月), H=8(3月), J=10(4月), ...
    ' 辅助列：AE=31(1月), AF=32(2月), AG=33(3月), AH=34(4月), ...
    Dim m As Long
    Dim srcCol As Long
    Dim auxCol As Long
    Dim cellValue As Variant

    For m = 1 To numMonths
        srcCol = 2 * m + 2 ' D=4, F=6, H=8, J=10, ...
        auxCol = AUX_START_COL + (m - 1) ' AE=31, AF=32, AG=33, ...
        cellValue = wsSource.Cells(srcRow, srcCol).Value
        wsSource.Cells(srcRow, auxCol).Value = ExtractNumberFromCell(cellValue)
    Next m
End Sub

' ============================================================
' 计算辅助区域中指定行的合计（VBA直接求和）
' ============================================================
Private Function SumAuxRow(ByVal wsSource As Worksheet, _
        ByVal srcRow As Long, _
        ByVal numMonths As Long) As Double
    Dim total As Double
    Dim m As Long
    Dim auxCol As Long
    Dim cellVal As Variant

    total = 0
    For m = 1 To numMonths
        auxCol = AUX_START_COL + (m - 1)
        cellVal = wsSource.Cells(srcRow, auxCol).Value
        If IsNumeric(cellVal) Then
            total = total + CDbl(cellVal)
        End If
    Next m

    SumAuxRow = total
End Function

' ============================================================
' 处理伯豪瑞廷营销活动数据
' 投放数量：12-14行（官微、抖音、OTA）→ 合计
' 受众数量：15-17行（官微、抖音、OTA）→ 合计
' 成交数量：18-20行（官微、抖音、OTA）→ 合计
' ============================================================
Private Sub ProcessActivityBHRT(ByVal sourceFolderPath As String, _
        ByVal wsTarget As Worksheet)
    Dim sourceFilePath As String
    Dim wbSource As Workbook
    Dim wsSource As Worksheet
    Dim numMonths As Long
    Dim putTotal As Double
    Dim audTotal As Double
    Dim dealTotal As Double

    sourceFilePath = sourceFolderPath & BHRT_SOURCE_FILE
    If Dir(sourceFilePath) = "" Then
        MsgBox "未找到伯豪瑞廷源文件！" & vbCrLf & _
            "文件名应为: " & BHRT_SOURCE_FILE, vbExclamation
        Exit Sub
    End If

    Application.StatusBar = "正在处理: 伯豪瑞廷 营销活动..."

    On Error Resume Next
    Set wbSource = Workbooks.Open(sourceFilePath, ReadOnly : = True)
    If Err.Number <> 0 Then
        MsgBox "无法打开伯豪瑞廷源文件: " & sourceFilePath & vbCrLf & Err.Description, vbCritical
        On Error GoTo 0
        Exit Sub
    End If
    On Error GoTo 0

    Set wsSource = GetActivityWorksheet(wbSource)
    If wsSource Is Nothing Then
        MsgBox "伯豪瑞廷源文件中未找到 '" & ACTIVITY_SHEET_NAME & "' 工作表！", vbExclamation
        wbSource.Close SaveChanges : = False
        Exit Sub
    End If

    numMonths = GetTargetMonth()
    If numMonths < 1 Or numMonths > 12 Then
        MsgBox "无法确定报告月份: " & numMonths, vbCritical
        wbSource.Close SaveChanges : = False
        Exit Sub
    End If

    ' 伯豪瑞廷数据列结构：E=1月达成, G=2月达成, I=3月达成, K=4月达成, ...
    ' 达成列为隔列（计划/达成交替），从E列（第5列）开始
    ' 在辅助区域（AE列开始）创建提取数字的公式
    CreateAuxFormulasBHRT wsSource, BHRT_PUT_ROW1, numMonths
    CreateAuxFormulasBHRT wsSource, BHRT_PUT_ROW2, numMonths
    CreateAuxFormulasBHRT wsSource, BHRT_PUT_ROW3, numMonths
    CreateAuxFormulasBHRT wsSource, BHRT_AUD_ROW1, numMonths
    CreateAuxFormulasBHRT wsSource, BHRT_AUD_ROW2, numMonths
    CreateAuxFormulasBHRT wsSource, BHRT_AUD_ROW3, numMonths
    CreateAuxFormulasBHRT wsSource, BHRT_DEAL_ROW1, numMonths
    CreateAuxFormulasBHRT wsSource, BHRT_DEAL_ROW2, numMonths
    CreateAuxFormulasBHRT wsSource, BHRT_DEAL_ROW3, numMonths

    ' 计算辅助区域合计
    putTotal = SumAuxRow(wsSource, BHRT_PUT_ROW1, numMonths) _
         + SumAuxRow(wsSource, BHRT_PUT_ROW2, numMonths) _
         + SumAuxRow(wsSource, BHRT_PUT_ROW3, numMonths)

    audTotal = SumAuxRow(wsSource, BHRT_AUD_ROW1, numMonths) _
         + SumAuxRow(wsSource, BHRT_AUD_ROW2, numMonths) _
         + SumAuxRow(wsSource, BHRT_AUD_ROW3, numMonths)

    dealTotal = SumAuxRow(wsSource, BHRT_DEAL_ROW1, numMonths) _
         + SumAuxRow(wsSource, BHRT_DEAL_ROW2, numMonths) _
         + SumAuxRow(wsSource, BHRT_DEAL_ROW3, numMonths)

    ' 写入目标
    wsTarget.Cells(2, TARGET_COL_BHRT).Value = putTotal
    wsTarget.Cells(3, TARGET_COL_BHRT).Value = audTotal
    wsTarget.Cells(4, TARGET_COL_BHRT).Value = dealTotal

    wbSource.Close SaveChanges : = False
    Set wbSource = Nothing
    Set wsSource = Nothing
End Sub

' ============================================================
' 处理重庆瑞尔营销活动数据
' 投放数量：第12行（可能包含加法表达式如"1+1000"）
' 受众数量：第13行
' 成交数量：第14行
' ============================================================
Private Sub ProcessActivityCQRER(ByVal sourceFolderPath As String, _
        ByVal wsTarget As Worksheet)
    Dim sourceFilePath As String
    Dim wbSource As Workbook
    Dim wsSource As Worksheet
    Dim numMonths As Long
    Dim putTotal As Double
    Dim audTotal As Double
    Dim dealTotal As Double

    sourceFilePath = sourceFolderPath & CQRER_SOURCE_FILE
    If Dir(sourceFilePath) = "" Then
        MsgBox "未找到重庆瑞尔源文件！" & vbCrLf & _
            "文件名应为: " & CQRER_SOURCE_FILE, vbExclamation
        Exit Sub
    End If

    Application.StatusBar = "正在处理: 重庆瑞尔 营销活动..."

    On Error Resume Next
    Set wbSource = Workbooks.Open(sourceFilePath, ReadOnly : = True)
    If Err.Number <> 0 Then
        MsgBox "无法打开重庆瑞尔源文件: " & sourceFilePath & vbCrLf & Err.Description, vbCritical
        On Error GoTo 0
        Exit Sub
    End If
    On Error GoTo 0

    Set wsSource = GetActivityWorksheet(wbSource)
    If wsSource Is Nothing Then
        MsgBox "重庆瑞尔源文件中未找到 '" & ACTIVITY_SHEET_NAME & "' 工作表！", vbExclamation
        wbSource.Close SaveChanges : = False
        Exit Sub
    End If

    numMonths = GetTargetMonth()
    If numMonths < 1 Or numMonths > 12 Then
        MsgBox "无法确定报告月份: " & numMonths, vbCritical
        wbSource.Close SaveChanges : = False
        Exit Sub
    End If

    ' 重庆瑞尔数据列结构：D=1月达成, F=2月达成, H=3月达成, J=4月达成, ...
    ' 达成列每隔一列（计划/达成交替），从D列（第4列）开始
    ' 在辅助区域（AE列开始）创建提取数字的公式
    CreateAuxFormulasCQRER wsSource, CQRER_PUT_ROW, numMonths
    CreateAuxFormulasCQRER wsSource, CQRER_AUD_ROW, numMonths
    CreateAuxFormulasCQRER wsSource, CQRER_DEAL_ROW, numMonths

    ' 计算辅助区域合计
    putTotal = SumAuxRow(wsSource, CQRER_PUT_ROW, numMonths)
    audTotal = SumAuxRow(wsSource, CQRER_AUD_ROW, numMonths)
    dealTotal = SumAuxRow(wsSource, CQRER_DEAL_ROW, numMonths)

    ' 写入目标
    wsTarget.Cells(2, TARGET_COL_CQRER).Value = putTotal
    wsTarget.Cells(3, TARGET_COL_CQRER).Value = audTotal
    wsTarget.Cells(4, TARGET_COL_CQRER).Value = dealTotal

    wbSource.Close SaveChanges : = False
    Set wbSource = Nothing
    Set wsSource = Nothing
End Sub

' ============================================================
' 获取活动量工作表
' ============================================================
Private Function GetActivityWorksheet(ByVal wb As Workbook) As Worksheet
    On Error Resume Next
    Set GetActivityWorksheet = wb.Worksheets(ACTIVITY_SHEET_NAME)
    On Error GoTo 0
End Function

' ============================================================
' 写入转化率公式
' C5=C4/C3, D5=D4/D3
' ============================================================
Private Sub WriteConversionRateFormulas(ByVal wsTarget As Worksheet)
    wsTarget.Cells(5, TARGET_COL_BHRT).formula = _
        "=" & ColLetter(TARGET_COL_BHRT) & "4/" & ColLetter(TARGET_COL_BHRT) & "3"
    wsTarget.Cells(5, TARGET_COL_CQRER).formula = _
        "=" & ColLetter(TARGET_COL_CQRER) & "4/" & ColLetter(TARGET_COL_CQRER) & "3"

    wsTarget.Cells(5, TARGET_COL_BHRT).NumberFormat = "0.0000%"
    wsTarget.Cells(5, TARGET_COL_CQRER).NumberFormat = "0.0000%"
End Sub

' ============================================================
' 处理伯豪瑞廷业务指标（经营报表）
' 从"指标统计"工作表的第15行（月均入住率）和第17行（OTA网络评价）提取月度数据
' ============================================================
Private Sub ProcessReportBHRT(ByVal reportFolderPath As String, _
        ByVal wsTarget As Worksheet)
    Dim sourceFilePath As String
    Dim wbSource As Workbook
    Dim wsSource As Worksheet
    Dim numMonths As Long
    Dim m As Long
    Dim col As Long
    Dim cellVal As Variant

    sourceFilePath = reportFolderPath & BHRT_SOURCE_FILE
    If Dir(sourceFilePath) = "" Then
        MsgBox "未找到伯豪瑞廷经营报表！" & vbCrLf & _
            "文件名应为: " & BHRT_SOURCE_FILE, vbExclamation
        Exit Sub
    End If

    Application.StatusBar = "正在处理: 伯豪瑞廷 业务指标..."

    On Error Resume Next
    Set wbSource = Workbooks.Open(sourceFilePath, ReadOnly : = True)
    If Err.Number <> 0 Then
        MsgBox "无法打开伯豪瑞廷经营报表: " & sourceFilePath & vbCrLf & Err.Description, vbCritical
        On Error GoTo 0
        Exit Sub
    End If
    On Error GoTo 0

    Set wsSource = GetReportWorksheet(wbSource)
    If wsSource Is Nothing Then
        MsgBox "伯豪瑞廷经营报表中未找到 '" & REPORT_SHEET_NAME & "' 工作表！", vbExclamation
        wbSource.Close SaveChanges : = False
        Exit Sub
    End If

    numMonths = GetTargetMonth()
    If numMonths < 1 Or numMonths > 12 Then
        MsgBox "无法确定报告月份: " & numMonths, vbCritical
        wbSource.Close SaveChanges : = False
        Exit Sub
    End If

    ' 写入月度数据（1月到12月）
    ' 数据列：D=4(1月), E=5(2月), F=6(3月), ...
    For m = 1 To 12
        col = m + 3 ' D=4, E=5, F=6, ...

        ' 月均入住率（第15行）
        If m <= numMonths Then
            cellVal = wsSource.Cells(REPORT_ROW_OCCUPANCY, col).Value
            wsTarget.Cells(TARGET_MONTH_START_ROW + m - 1, TARGET_OCC_COL_BHRT).Value = cellVal
        Else
            wsTarget.Cells(TARGET_MONTH_START_ROW + m - 1, TARGET_OCC_COL_BHRT).Value = CVErr(xlErrNA)
        End If

        ' OTA网络评价（第17行）
        If m <= numMonths Then
            cellVal = wsSource.Cells(REPORT_ROW_OTA_RATING, col).Value
            wsTarget.Cells(TARGET_MONTH_START_ROW + m - 1, TARGET_OTA_COL_BHRT).Value = cellVal
        Else
            wsTarget.Cells(TARGET_MONTH_START_ROW + m - 1, TARGET_OTA_COL_BHRT).Value = CVErr(xlErrNA)
        End If
    Next m

    wbSource.Close SaveChanges : = False
    Set wbSource = Nothing
    Set wsSource = Nothing
End Sub

' ============================================================
' 处理重庆瑞尔业务指标（经营报表）
' ============================================================
Private Sub ProcessReportCQRER(ByVal reportFolderPath As String, _
        ByVal wsTarget As Worksheet)
    Dim sourceFilePath As String
    Dim wbSource As Workbook
    Dim wsSource As Worksheet
    Dim numMonths As Long
    Dim m As Long
    Dim col As Long
    Dim cellVal As Variant

    sourceFilePath = reportFolderPath & CQRER_SOURCE_FILE
    If Dir(sourceFilePath) = "" Then
        MsgBox "未找到重庆瑞尔经营报表！" & vbCrLf & _
            "文件名应为: " & CQRER_SOURCE_FILE, vbExclamation
        Exit Sub
    End If

    Application.StatusBar = "正在处理: 重庆瑞尔 业务指标..."

    On Error Resume Next
    Set wbSource = Workbooks.Open(sourceFilePath, ReadOnly : = True)
    If Err.Number <> 0 Then
        MsgBox "无法打开重庆瑞尔经营报表: " & sourceFilePath & vbCrLf & Err.Description, vbCritical
        On Error GoTo 0
        Exit Sub
    End If
    On Error GoTo 0

    Set wsSource = GetReportWorksheet(wbSource)
    If wsSource Is Nothing Then
        MsgBox "重庆瑞尔经营报表中未找到 '" & REPORT_SHEET_NAME & "' 工作表！", vbExclamation
        wbSource.Close SaveChanges : = False
        Exit Sub
    End If

    numMonths = GetTargetMonth()
    If numMonths < 1 Or numMonths > 12 Then
        MsgBox "无法确定报告月份: " & numMonths, vbCritical
        wbSource.Close SaveChanges : = False
        Exit Sub
    End If

    ' 写入月度数据（1月到12月）
    ' 数据列：D=4(1月), E=5(2月), F=6(3月), ...
    For m = 1 To 12
        col = m + 3 ' D=4, E=5, F=6, ...

        ' 月均入住率（第15行）
        If m <= numMonths Then
            cellVal = wsSource.Cells(REPORT_ROW_OCCUPANCY, col).Value
            wsTarget.Cells(TARGET_MONTH_START_ROW + m - 1, TARGET_OCC_COL_CQRER).Value = cellVal
        Else
            wsTarget.Cells(TARGET_MONTH_START_ROW + m - 1, TARGET_OCC_COL_CQRER).Value = CVErr(xlErrNA)
        End If

        ' OTA网络评价（第17行）
        If m <= numMonths Then
            cellVal = wsSource.Cells(REPORT_ROW_OTA_RATING, col).Value
            wsTarget.Cells(TARGET_MONTH_START_ROW + m - 1, TARGET_OTA_COL_CQRER).Value = cellVal
        Else
            wsTarget.Cells(TARGET_MONTH_START_ROW + m - 1, TARGET_OTA_COL_CQRER).Value = CVErr(xlErrNA)
        End If
    Next m

    wbSource.Close SaveChanges : = False
    Set wbSource = Nothing
    Set wsSource = Nothing
End Sub

' ============================================================
' 获取经营报表工作表
' ============================================================
Private Function GetReportWorksheet(ByVal wb As Workbook) As Worksheet
    On Error Resume Next
    Set GetReportWorksheet = wb.Worksheets(REPORT_SHEET_NAME)
    On Error GoTo 0
End Function

' ============================================================
' 设置目标工作表格式
' ============================================================
Private Sub FormatTargetSheet(ByVal wsTarget As Worksheet)
    With wsTarget.Range("C2:D4")
        .NumberFormat = "#,##0"
    End With
    With wsTarget.Range("F2:G13")
        .NumberFormat = "0.00"
    End With
    With wsTarget.Range("J2:K13")
        .NumberFormat = "0%"
    End With
End Sub

' ============================================================
' 列号转字母
' ============================================================
Private Function ColLetter(ByVal colNum As Long) As String
    ColLetter = Split(Cells(1, colNum).Address(True, False), "$")(0)
End Function