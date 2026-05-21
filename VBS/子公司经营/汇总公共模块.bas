Option Explicit

' ============================================================
' 汇总公共模块 — 数据汇总脚本的公共函数
' 适用于：保险数据汇总、商写数据汇总、酒店数据汇总
' ============================================================

' ---- 配置常量 ----
Private Const CONFIG_SHEET_NAME As String = "填写页"
Private Const MONTH_NUMBER_CELL As String = "A2"

' ============================================================
' 列号转字母（如 3 → "C"）
' ============================================================
Public Function ColLetter(ByVal colNum As Long) As String
    ColLetter = Split(Cells(1, colNum).Address(True, False), "$")(0)
End Function

' ============================================================
' 从填写页读取报告月份（填写页!A2）
' ============================================================
Public Function GetTargetMonth() As Long
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
' 支持格式如 "2026年4月" → 4
' ============================================================
Public Function GetMonthFromFolderName() As Long
    Dim pathParts As Variant
    Dim folderName As String
    Dim yearPos As Long
    Dim monthPos As Long
    Dim monthStr As String
    Dim i As Long

    pathParts = Split(ThisWorkbook.path, "\")
    folderName = pathParts(UBound(pathParts))

    yearPos = InStr(1, folderName, "年", vbTextCompare)
    If yearPos = 0 Then GoTo Fallback

    monthPos = InStr(yearPos + 1, folderName, "月", vbTextCompare)
    If monthPos = 0 Then GoTo Fallback

    monthStr = ""
    For i = yearPos + 1 To monthPos - 1
        If IsNumeric(Mid$(folderName, i, 1)) Then
            monthStr = monthStr & Mid$(folderName, i, 1)
        End If
    Next i

    If Len(monthStr) > 0 And IsNumeric(monthStr) Then
        GetMonthFromFolderName = CLng(monthStr)
        Exit Function
    End If

Fallback:
    GetMonthFromFolderName = Month(Date)
End Function

' ============================================================
' 安全读取单元格数值，非数字返回 0
' ============================================================
Public Function SafeRead(ByVal ws As Worksheet, ByVal r As Long, ByVal c As Long) As Double
    SafeRead = ParseNumeric(ws.Cells(r, c).Value)
End Function

' ============================================================
' 从单元格值中提取数字（含文本数字解析）
' 如 "1组" → 1, "3.5万" → 3.5
' ============================================================
Public Function ParseNumeric(ByVal v As Variant) As Double
    Dim s As String
    Dim i As Long
    Dim numStr As String

    If IsEmpty(v) Then
        ParseNumeric = 0
        Exit Function
    End If

    If IsNumeric(v) Then
        ParseNumeric = CDbl(v)
        Exit Function
    End If

    s = CStr(v)
    numStr = ""
    For i = 1 To Len(s)
        If IsNumeric(Mid$(s, i, 1)) Or Mid$(s, i, 1) = "." Then
            numStr = numStr & Mid$(s, i, 1)
        End If
    Next i

    If Len(numStr) > 0 And IsNumeric(numStr) Then
        ParseNumeric = CDbl(numStr)
    Else
        ParseNumeric = 0
    End If
End Function

' ============================================================
' 计算指定源行从1月到报告月的达成列之和
' 达成列从 D=4 开始，隔列（D=1月达成, F=2月达成, H=3月达成...）
' ============================================================
Public Function SumAchievementCols(ByVal wsSource As Worksheet, _
                                   ByVal sourceRow As Long, _
                                   ByVal numMonths As Long) As Double
    Dim total As Double
    Dim m As Long
    Dim col As Long

    total = 0
    For m = 1 To numMonths
        col = 2 * m + 2  ' D=4, F=6, H=8, J=10, ...
        total = total + ParseNumeric(wsSource.Cells(sourceRow, col).Value)
    Next m
    SumAchievementCols = total
End Function

' ============================================================
' 解析单元格数字（SafeRead + ParseNumeric 结合版）
' ============================================================
Public Function SafeReadEx(ByVal ws As Worksheet, ByVal r As Long, ByVal c As Long) As Double
    SafeReadEx = ParseNumeric(ws.Cells(r, c).Value)
End Function
