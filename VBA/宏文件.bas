Sub main()
    Dim tim1 As Date: tim1 = Timer
    Application.ScreenUpdating = False '关闭屏幕刷新
    Application.DisplayAlerts = False '关闭提示
    On Error Resume Next '忽略错误
    '***************************************************************************
    Dim Destination As Worksheet
    'Set Destination  = Application.ActiveWorkbook().Worksheets(1) '指定目标工作表
    Set Destination = ActiveSheet '指定当前表为目标工作表
    Dim 差旅签批
    差旅签批 = Destination.UsedRange

    Dim fileToOpen
    fileToOpen = Application.GetOpenFilename("Excel文件 (*.xl*), *.xl*", , "请选择Excel文件", , False)
    Dim bok As Workbook, source As Worksheet
    Set bok = Workbooks.Open(fileToOpen)

    Dim sheetarr()
    sheetname = "机票订单"

    Set source = bok.Sheets(sheetname) '指定源工作表
    '删除行
    source.Rows(source.Range("a1048576").End(xlUp).Row + 1 & ":1048576").Delete
    '删除列
    'source.Columns(iCol & ":16383").Delete
    source.Columns(Split(source.Cells(1, source.Cells(1, 16383).End(xlToLeft).Column + 1).Address, "$")(1) & ":XFD").Delete

    Dim 订单记录
    订单记录 = source.UsedRange
    ReDim Preserve 订单记录(1 To UBound(订单记录, 1), 1 To UBound(订单记录, 2) + 1) '保留源数据,只改列+1
    'MsgBox 订单记录(2, 2) & "X" & source.UsedRange.Columns.Count & "X" & source.UsedRange.Rows.Count

    For i = 2 To UBound(订单记录, 1) '遍历数组arr1的每一行
        For j = 2 To UBound(差旅签批, 1)
            'MsgBox 差旅签批(j, 1)
            If 差旅签批(j, 1) = 订单记录(i, 6) Then
                'MsgBox 差旅签批(j, 1)
                If 差旅签批(j, 3) < 订单记录(i, 3) Then
                    If 差旅签批(j, 4) > 订单记录(i, 3) Then
                        'MsgBox 差旅签批(j, 5)
                        订单记录(i, UBound(订单记录, 2)) = 差旅签批(j, 5)
                    End If
                End If
            End If
        Next j
    Next i
    source.Cells(1, 1).Resize(UBound(订单记录, 1), UBound(订单记录, 2)) = 订单记录
    'WorksheetFunction.Transpose (订单记录) '将数组转置后存入工作表区域
    bok.Close
    Set bok = Nothing
    Set source = Nothing



    '***************************************************************************
    Err.Clear: On Error GoTo 0 '恢复错误捕捉
    Application.DisplayAlerts = True '开启提示
    Application.ScreenUpdating = True '开启屏幕刷新
    'MsgBox Format((Timer - tim1) * 1000, "程序执行时间为：0.00毫秒"), 64, "时间统计"
End Sub

Sub 批量删除中间空行空列(oWK)
    'QQ:1722187970,微信:xycgenius,公众号:水星excel
    With oWK
        iRow = .Range("a1048576").End(xlUp).Row
        iCol = .Cells(1, 16383).End(xlToLeft).Column
        '逆序删除行
        For i = iRow To 1 Step -1
            If Excel.Application.WorksheetFunction.CountA(.Range("a" & i).EntireRow) = 0 Then
                .Range("a" & i).EntireRow.Delete
            End If
        Next i
        '逆序删除列
        For i = iCol To 1 Step -1
            If Excel.Application.WorksheetFunction.CountA(.Cells(1, i).EntireColumn) = 0 Then
                .Cells(1, i).EntireColumn.Delete
            End If
        Next i
    End With
End Sub

Sub 批量删除结尾空行空列(oWK)
    With oWK
        iRow = .Range("a1048576").End(xlUp).Row
        iCol = .Cells(1, 16383).End(xlToLeft).Column
        '删除行
        For i = 1048576 To iRow + 1 Step -1
            Rows(i).Delete
        Next i

        '删除列
        For j = 16383 To iCol + 1 Step -1
            Columns(j).Delete
        Next j
    End With
End Sub

Sub 删除所有空行(oWK)
    Dim R As Long, RR As Long, i As Long, Counter As Long
    Dim LastRow As Long '真正最后使用过的单元格行号
    R = oWK.UsedRange.Rows.Count '使用过的行数
    RR = oWK.UsedRange.Rows(1).Row '使用过的单元格区域首行行号
    LastRow = R + RR - 1
    Application.ScreenUpdating = False '关闭屏幕刷新
    For i = LastRow To 1 Step -1
        If Application.WorksheetFunction.CountA(Rows(i)) = 0 Then '如果是空行，那么
            oWK.Rows(i).Delete '删除
            Counter = Counter + 1 '计算空行数量
        End If
    Next i
    Application.ScreenUpdating = True '开启屏幕刷新
    MsgBox Counter & " 空行已删除"
End Sub

Function 创建并写入文件(path, filename, texts)
    Set fso = CreateObject("Scripting.FileSystemObject") '创建文件需要使用Scripting.FileSystemObject对象
    Set myTxt = fso.CreateTextFile(filename:=path & "\" & filename, OverWrite:=True) '使用CreateTextFile创建文件
    myTxt.Write texts
    myTxt.Close
End Function

Function 检查并创建文件夹(strFullPath)
    Dim resFolder
    resFolder = Dir(strFullPath, vbDirectory)   '判断路径是否存在
    '如果不存在，就新建一个
    If resFolder = "" Then
        MkDir (strFullPath)
    End If
End Function

