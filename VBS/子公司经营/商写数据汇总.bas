
Option Explicit

' 常量定义
Private Const SOURCE_SHEET_NAME As String = "写字楼和商业综合体类"
Private Const TARGET_SHEET_NAME As String = "商写类"
Private Const SOURCE_FOLDER As String = "活动量"

' 填写页配置
Private Const CONFIG_SHEET_NAME As String = "填写页"
Private Const MONTH_NUMBER_CELL As String = "A2"

' 源行号常量（写字楼和商业综合体类 sheet）
Private Const ROW_BASE_AREA As Long = 4       ' 期初面积
Private Const ROW_NEW_SIGN As Long = 5        ' 新增签约面积
Private Const ROW_RETREAT As Long = 7         ' 本期退租面积
Private Const ROW_END_AREA As Long = 8        ' 月末面积
Private Const ROW_CH_LEAD As Long = 9         ' 渠道带客
Private Const ROW_CH_DEAL As Long = 10        ' 渠道成交
Private Const ROW_CH_SIGN As Long = 11        ' 渠道签约面积
Private Const ROW_SELF_LEAD As Long = 14      ' 自营带客
Private Const ROW_SELF_DEAL As Long = 15      ' 自营成交
Private Const ROW_SELF_SIGN As Long = 16      ' 自营签约面积
Private Const ROW_EXPIRE As Long = 19         ' 到期面积
Private Const ROW_RENEW As Long = 20          ' 续签面积

' 公司配置：源文件名, 公司名, 目标列号
Private Type CompanyConfig
    sourceFile As String
    companyName As String
    targetCol As Long
End Type

' 主入口
Public Sub 商写数据汇总()
    Dim prevScreenUpdating As Boolean
    Dim prevCalculation As XlCalculation
    Dim prevEnableEvents As Boolean
    Dim sourceFolderPath As String
    Dim wsTarget As Worksheet
    Dim companies(0 To 4) As CompanyConfig
    Dim i As Long

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

    ' B=项目名称, C=3 北京中言, D=4 大连凯丹, E=5 福建钱隆, F=6 春夏秋冬, G=7 重庆宜新
    companies(0).sourceFile = "北京中言.xlsx":  companies(0).companyName = "北京中言":  companies(0).targetCol = 3
    companies(1).sourceFile = "大连凯丹.xlsx":  companies(1).companyName = "大连凯丹":  companies(1).targetCol = 4
    companies(2).sourceFile = "福建钱隆.xlsx":  companies(2).companyName = "福建钱隆":  companies(2).targetCol = 5
    companies(3).sourceFile = "春夏秋冬.xlsx":  companies(3).companyName = "春夏秋冬":  companies(3).targetCol = 6
    companies(4).sourceFile = "重庆宜新.xlsx":  companies(4).companyName = "重庆宜新":  companies(4).targetCol = 7

    For i = 0 To 4
        ProcessCompany sourceFolderPath, companies(i), wsTarget
    Next i

    WriteFormulas wsTarget

    MsgBox "商写数据汇总完成！", vbInformation, "处理完成"

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
                           ByRef config As CompanyConfig, _
                           ByVal wsTarget As Worksheet)
    Dim sourceFilePath As String
    Dim wbSource As Workbook
    Dim wsSource As Worksheet
    Dim numMonths As Long
    Dim lastMonthCol As Long

    sourceFilePath = sourceFolderPath & config.sourceFile
    If Dir(sourceFilePath) = "" Then
        MsgBox "未找到 " & config.companyName & " 的源文件！" & vbCrLf & _
               "文件名应为: " & config.sourceFile, vbExclamation
        Exit Sub
    End If

    Application.StatusBar = "正在处理: " & config.companyName & " ..."

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
        MsgBox config.companyName & " 源文件中未找到 '" & SOURCE_SHEET_NAME & "' 工作表！", vbExclamation
        wbSource.Close SaveChanges:=False
        Exit Sub
    End If

    numMonths = GetTargetMonth()
    If numMonths < 1 Or numMonths > 12 Then
        MsgBox "无法确定报告月份: " & numMonths, vbCritical
        wbSource.Close SaveChanges:=False
        Exit Sub
    End If

    lastMonthCol = 2 * numMonths + 2  ' 报告月达成列

    ' ==========================================
    ' 写入目标
    ' ==========================================

    ' Row 2: 期初面积 = 1月达成(D4)
    wsc config, wsTarget, 2, SafeRead(wsSource, ROW_BASE_AREA, 4)

    ' Row 3: 新增签约面积 YTD
    wsc config, wsTarget, 3, SumAchievementCols(wsSource, ROW_NEW_SIGN, numMonths)

    ' Row 4: 平均租金 = 0
    wsTarget.Cells(4, config.targetCol).Value = 0

    ' Row 5: 本期退租面积 YTD
    wsc config, wsTarget, 5, SumAchievementCols(wsSource, ROW_RETREAT, numMonths)

    ' Row 6: 月末面积 = 最后一个月达成
    wsc config, wsTarget, 6, SafeRead(wsSource, ROW_END_AREA, lastMonthCol)

    ' Row 7: 渠道带客 YTD
    wsc config, wsTarget, 7, SumAchievementCols(wsSource, ROW_CH_LEAD, numMonths)

    ' Row 8: 渠道成交 YTD
    wsc config, wsTarget, 8, SumAchievementCols(wsSource, ROW_CH_DEAL, numMonths)

    ' Row 9: 渠道签约面积 YTD
    wsc config, wsTarget, 9, SumAchievementCols(wsSource, ROW_CH_SIGN, numMonths)

    ' Row 10: 成交周期 = 0
    wsTarget.Cells(10, config.targetCol).Value = 0

    ' Row 12: 自营带客 YTD
    wsc config, wsTarget, 12, SumAchievementCols(wsSource, ROW_SELF_LEAD, numMonths)

    ' Row 13: 自营成交 YTD
    wsc config, wsTarget, 13, SumAchievementCols(wsSource, ROW_SELF_DEAL, numMonths)

    ' Row 14: 自营签约面积 YTD
    wsc config, wsTarget, 14, SumAchievementCols(wsSource, ROW_SELF_SIGN, numMonths)

    ' Row 15: 成交周期 = 0
    wsTarget.Cells(15, config.targetCol).Value = 0

    ' Row 17: 到期面积 YTD
    wsc config, wsTarget, 17, SumAchievementCols(wsSource, ROW_EXPIRE, numMonths)

    ' Row 18: 续签面积 YTD
    wsc config, wsTarget, 18, SumAchievementCols(wsSource, ROW_RENEW, numMonths)

    wbSource.Close SaveChanges:=False
    Set wbSource = Nothing
    Set wsSource = Nothing
End Sub

' 写入数值的简写
Private Sub wsc(ByRef config As CompanyConfig, ByVal wsTarget As Worksheet, ByVal r As Long, ByVal v As Double)
    wsTarget.Cells(r, config.targetCol).Value = v
End Sub

' ============================================================
' 写入转化率公式: 行11=渠道成交/渠道带客, 行16=自营成交/自营带客
' ============================================================
Private Sub WriteFormulas(ByVal wsTarget As Worksheet)
    Dim col As Long

    For col = 3 To 7  ' C=3 到 G=7
        ' 渠道转化率 = 渠道成交 / 渠道带客
        wsTarget.Cells(11, col).Formula = _
            "=" & ColLetter(col) & "8/" & ColLetter(col) & "7"

        ' 自营转化率 = 自营成交 / 自营带客
        wsTarget.Cells(16, col).Formula = _
            "=" & ColLetter(col) & "13/" & ColLetter(col) & "12"
    Next col

    wsTarget.Range("C11:G11").NumberFormat = "0%"
    wsTarget.Range("C16:G16").NumberFormat = "0%"
End Sub

Private Function GetSourceWorksheet(ByVal wb As Workbook) As Worksheet
    On Error Resume Next
    Set GetSourceWorksheet = wb.Worksheets(SOURCE_SHEET_NAME)
    On Error GoTo 0
End Function
