
Option Explicit

' 常量定义
Private Const SOURCE_SHEET_NAME As String = "保险类"
Private Const TARGET_SHEET_NAME As String = "保险类"
Private Const SOURCE_FOLDER As String = "活动量"

' 填写页配置
Private Const CONFIG_SHEET_NAME As String = "填写页"
Private Const MONTH_NUMBER_CELL As String = "A2"

Private Const SHENGTANG_SOURCE_FILE As String = "盛唐融信.xlsx"
Private Const JUNKANG_SOURCE_FILE As String = "君康经纪.xlsx"

' 源行号常量
Private Const ROW_BASE_HR As Long = 4        ' 期初人力
Private Const ROW_HR_IN As Long = 5          ' 当月入职
Private Const ROW_HR_OUT As Long = 6         ' 当月离职
Private Const ROW_OPEN_COUNT As Long = 10    ' 开单人数
Private Const ROW_NEW_PREMIUM As Long = 12   ' 承保新单规模保费
Private Const ROW_QJ_PREMIUM As Long = 13    ' 承保期交规模保费
Private Const ROW_AR_13 As Long = 14         ' 应收13月续期保费
Private Const ROW_RC_13 As Long = 15         ' 实收13月续期保费
Private Const ROW_AR_25 As Long = 16         ' 应收25月续期保费
Private Const ROW_RC_25 As Long = 17         ' 实收25月续期保费
Private Const ROW_POLICIES As Long = 18      ' 承保件数

' 目标汇总列: 盛唐融信→C(3), 君康经纪→D(4)
Private Const SHENGTANG_TARGET_COL As Long = 3
Private Const JUNKANG_TARGET_COL As Long = 4

' 月度规模保费区域: G/H列, 行13=1月..行24=12月
Private Const MONTHLY_SHENGTANG_COL As Long = 7  ' G列
Private Const MONTHLY_JUNKANG_COL As Long = 8    ' H列
Private Const MONTHLY_DATA_START_ROW As Long = 13 ' 1月所在行

' 公式行
Private Const FORMULA_ACTIVITY_ROW As Long = 9    ' 活动率
Private Const FORMULA_AVG_PREMIUM_ROW As Long = 17 ' 件均保费
Private Const FORMULA_PER_CAPITA_ROW As Long = 18  ' 人均保费

' 主入口
Public Sub 保险数据汇总()
    Dim prevScreenUpdating As Boolean
    Dim prevCalculation As XlCalculation
    Dim prevEnableEvents As Boolean
    Dim sourceFolderPath As String
    Dim wsTarget As Worksheet

    prevScreenUpdating = Application.ScreenUpdating
    prevCalculation = Application.Calculation
    prevEnableEvents = Application.EnableEvents

    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False

    On Error GoTo ErrorHandler

    Set wsTarget = GetTargetWorksheet
    If wsTarget Is Nothing Then
        MsgBox "目标工作表 '" & TARGET_SHEET_NAME & "' 不存在！", vbCritical
        GoTo Cleanup
    End If

    sourceFolderPath = ThisWorkbook.path & "\" & SOURCE_FOLDER & "\"
    If Dir(sourceFolderPath, vbDirectory) = "" Then
        MsgBox "活动量文件夹不存在: " & sourceFolderPath, vbCritical
        GoTo Cleanup
    End If

    ProcessCompany sourceFolderPath, SHENGTANG_SOURCE_FILE, "盛唐融信", SHENGTANG_TARGET_COL, MONTHLY_SHENGTANG_COL, wsTarget
    ProcessCompany sourceFolderPath, JUNKANG_SOURCE_FILE, "君康经纪", JUNKANG_TARGET_COL, MONTHLY_JUNKANG_COL, wsTarget

    WriteFormulas wsTarget

    MsgBox "保险类数据汇总完成！", vbInformation, "处理完成"

Cleanup:
    Application.ScreenUpdating = prevScreenUpdating
    Application.Calculation = prevCalculation
    Application.EnableEvents = prevEnableEvents
    Application.StatusBar = False
    Exit Sub

ErrorHandler:
    MsgBox "处理过程中发生错误: " & Err.Description & vbCrLf & _
           "错误代码: " & Err.Number, vbCritical
    Err.Clear
    GoTo Cleanup
End Sub

' 获取目标工作表
Private Function GetTargetWorksheet() As Worksheet
    On Error Resume Next
    Set GetTargetWorksheet = ThisWorkbook.Worksheets(TARGET_SHEET_NAME)
    On Error GoTo 0
End Function

' 处理单个公司的数据
Private Sub ProcessCompany(ByVal sourceFolderPath As String, _
                           ByVal sourceFileName As String, _
                           ByVal companyName As String, _
                           ByVal targetCol As Long, _
                           ByVal monthlyTargetCol As Long, _
                           ByVal wsTarget As Worksheet)
    Dim sourceFilePath As String
    Dim wbSource As Workbook
    Dim wsSource As Worksheet
    Dim numMonths As Long
    Dim baseHR As Double       ' 期初人力(1月达成)
    Dim ytdHRIn As Double      ' YTD入职
    Dim ytdHROut As Double     ' YTD离职
    Dim netAdd As Double       ' 当月净增(计算)
    Dim endHR As Double        ' 月末人力(计算)
    Dim avgHR As Double        ' 平均人力(计算)
    Dim cumIn As Double        ' 逐月累计入职
    Dim cumOut As Double       ' 逐月累计离职
    Dim monthlyEndHR As Double ' 各月月末人力累加
    Dim m As Long
    Dim col As Long

    sourceFilePath = sourceFolderPath & sourceFileName
    If Dir(sourceFilePath) = "" Then
        MsgBox "未找到 " & companyName & " 的源文件！" & vbCrLf & _
               "文件名应为: " & sourceFileName, vbExclamation
        Exit Sub
    End If

    Application.StatusBar = "正在处理: " & companyName & " ..."

    On Error Resume Next
    Set wbSource = Workbooks.Open(sourceFilePath, ReadOnly:=True)
    If Err.Number <> 0 Then
        MsgBox "无法打开源文件: " & sourceFilePath & vbCrLf & Err.Description, vbCritical
        On Error GoTo 0
        Exit Sub
    End If
    On Error GoTo 0

    Set wsSource = GetSourceWorksheet(wbSource)
    If wsSource Is Nothing Then
        MsgBox companyName & " 源文件中未找到 '" & SOURCE_SHEET_NAME & "' 工作表！", vbExclamation
        wbSource.Close SaveChanges:=False
        Exit Sub
    End If

    numMonths = GetTargetMonth()
    If numMonths < 1 Or numMonths > 12 Then
        MsgBox "无法确定报告月份: " & numMonths, vbCritical
        wbSource.Close SaveChanges:=False
        Exit Sub
    End If

    ' ==========================================
    ' 人力部分
    ' ==========================================

    ' 期初人力 = 1月达成
    baseHR = SafeRead(wsSource, ROW_BASE_HR, 4)  ' D4=1月达成

    ' 入职/离职 YTD
    ytdHRIn = SumAchievementCols(wsSource, ROW_HR_IN, numMonths)
    ytdHROut = SumAchievementCols(wsSource, ROW_HR_OUT, numMonths)

    ' 当月净增
    netAdd = ytdHRIn - ytdHROut

    ' 月末人力
    endHR = baseHR + ytdHRIn - ytdHROut

    ' 平均人力: 各月月末人力之和 / 月数
    cumIn = 0
    cumOut = 0
    monthlyEndHR = 0
    For m = 1 To numMonths
        col = 2 * m + 2
        cumIn = cumIn + SafeRead(wsSource, ROW_HR_IN, col)
        cumOut = cumOut + SafeRead(wsSource, ROW_HR_OUT, col)
        monthlyEndHR = monthlyEndHR + (baseHR + cumIn - cumOut)
    Next m
    avgHR = monthlyEndHR / numMonths

    ' 开单人数 YTD
    Dim ytdOpenCount As Double
    ytdOpenCount = SumAchievementCols(wsSource, ROW_OPEN_COUNT, numMonths)

    col = 2 * numMonths + 2  ' 报告月达成列

    ' ==========================================
    ' 写入目标
    ' ==========================================

    ' Row 2: 期初人力
    WriteValue wsTarget, 2, targetCol, baseHR
    ' Row 3: 当月入职
    WriteValue wsTarget, 3, targetCol, ytdHRIn
    ' Row 4: 当月离职
    WriteValue wsTarget, 4, targetCol, ytdHROut
    ' Row 5: 当月净增
    WriteValue wsTarget, 5, targetCol, netAdd
    ' Row 6: 月末人力
    WriteValue wsTarget, 6, targetCol, endHR
    ' Row 7: 平均人力
    WriteValue wsTarget, 7, targetCol, avgHR
    ' Row 8: 开单人数 YTD
    WriteValue wsTarget, 8, targetCol, ytdOpenCount

    ' Row 10: 承保新单规模保费 YTD
    WriteValue wsTarget, 10, targetCol, SumAchievementCols(wsSource, ROW_NEW_PREMIUM, numMonths)
    ' Row 11: 承保期交规模保费 YTD
    WriteValue wsTarget, 11, targetCol, SumAchievementCols(wsSource, ROW_QJ_PREMIUM, numMonths)

    ' Row 12-15: 续期 (当月达成)
    WriteCell wsTarget, 12, targetCol, wsSource.Cells(ROW_AR_13, col).Value
    WriteCell wsTarget, 13, targetCol, wsSource.Cells(ROW_RC_13, col).Value
    WriteCell wsTarget, 14, targetCol, wsSource.Cells(ROW_AR_25, col).Value
    WriteCell wsTarget, 15, targetCol, wsSource.Cells(ROW_RC_25, col).Value

    ' Row 16: 承保件数 YTD
    WriteValue wsTarget, 16, targetCol, SumAchievementCols(wsSource, ROW_POLICIES, numMonths)

    ' ==========================================
    ' 月度规模保费 G/H列 (13=1月..24=12月)
    ' ==========================================
    Dim mth As Long
    Dim premiumCol As Long
    For mth = 1 To 12
        If mth <= numMonths Then
            premiumCol = 2 * mth + 2  ' 达成列
            WriteCell wsTarget, MONTHLY_DATA_START_ROW + mth - 1, monthlyTargetCol, _
                wsSource.Cells(ROW_NEW_PREMIUM, premiumCol).Value
        Else
            wsTarget.Cells(MONTHLY_DATA_START_ROW + mth - 1, monthlyTargetCol).Value = CVErr(xlErrNA)
        End If
    Next mth

    wbSource.Close SaveChanges:=False
    Set wbSource = Nothing
    Set wsSource = Nothing
End Sub

' 获取源工作表
Private Function GetSourceWorksheet(ByVal wb As Workbook) As Worksheet
    On Error Resume Next
    Set GetSourceWorksheet = wb.Worksheets(SOURCE_SHEET_NAME)
    On Error GoTo 0
End Function

' 写入数值（0也写入）
Private Sub WriteValue(ByVal wsTarget As Worksheet, ByVal r As Long, ByVal c As Long, ByVal v As Double)
    wsTarget.Cells(r, c).Value = v
End Sub

' 写入单元格原值（保留空值）
Private Sub WriteCell(ByVal wsTarget As Worksheet, ByVal r As Long, ByVal c As Long, ByVal v As Variant)
    If IsEmpty(v) Then
        wsTarget.Cells(r, c).Value = Empty
    Else
        wsTarget.Cells(r, c).Value = v
    End If
End Sub

' 写入计算公式
Private Sub WriteFormulas(ByVal wsTarget As Worksheet)
    Dim col As Long

    For col = SHENGTANG_TARGET_COL To JUNKANG_TARGET_COL
        ' 活动率 = 开单人数 / 平均人力
        wsTarget.Cells(FORMULA_ACTIVITY_ROW, col).Formula = _
            "=" & ColLetter(col) & "8/" & ColLetter(col) & "7"

        ' 件均保费 = 承保新单规模保费 / 承保件数
        wsTarget.Cells(FORMULA_AVG_PREMIUM_ROW, col).Formula = _
            "=" & ColLetter(col) & "10/" & ColLetter(col) & "16"

        ' 人均保费 = 承保新单规模保费 / 月末人力
        wsTarget.Cells(FORMULA_PER_CAPITA_ROW, col).Formula = _
            "=" & ColLetter(col) & "10/" & ColLetter(col) & "6"
    Next col

    wsTarget.Range("C9:D9").NumberFormat = "0.00%"
    wsTarget.Range("C10:D11").NumberFormat = "#,##0.00"
    wsTarget.Range("C12:D18").NumberFormat = "#,##0.00"
End Sub

