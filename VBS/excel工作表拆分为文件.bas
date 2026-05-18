' ============================================
' Excel工作表拆分工具 - 优化版
' 功能：将当前工作簿中的所有工作表拆分为单独的Excel文件
' 作者：优化版本
' 日期：2026-02-01
' ============================================

Sub SplitWorksheets()
    ' 声明变量
    Dim wb As Workbook
    Dim ws As Worksheet
    Dim newWb As Workbook
    Dim savePath As String
    Dim wsName As String
    Dim fileExt As String
    Dim fileFormat As XlFileFormat
    Dim sheetCount As Integer
    Dim processedCount As Integer
    Dim startTime As Double
    Dim endTime As Double
    
    ' 记录开始时间（用于性能统计）
    startTime = Timer
    
    ' 初始化计数器
    sheetCount = 0
    processedCount = 0
    
    ' 设置文件格式（默认为.xlsx）
    fileExt = ".xlsx"
    fileFormat = xlOpenXMLWorkbook
    
    On Error GoTo ErrorHandler
    
    ' 获取当前工作簿
    Set wb = ThisWorkbook
    
    ' 验证工作簿是否已保存
    If wb.Path = "" Then
        MsgBox "请先保存工作簿！", vbExclamation
        Exit Sub
    End If
    
    ' 获取保存路径（与原工作簿同目录）
    savePath = wb.Path
    
    ' 验证保存路径是否存在
    If Dir(savePath, vbDirectory) = "" Then
        MsgBox "保存路径不存在：" & savePath, vbCritical
        Exit Sub
    End If
    
    ' 禁用警告和屏幕更新以提高性能
    Application.DisplayAlerts = False
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False
    
    ' 显示进度提示
    Application.StatusBar = "正在准备拆分工作表..."
    
    ' 获取工作表总数
    sheetCount = wb.Worksheets.Count
    
    ' 遍历所有工作表
    For Each ws In wb.Worksheets
        wsName = ws.Name
        processedCount = processedCount + 1
        
        ' 更新进度提示
        Application.StatusBar = "正在处理工作表 " & processedCount & "/" & sheetCount & ": " & wsName
        
        ' 检查工作表名称是否有效（避免无效文件名字符）
        If HasInvalidFileNameChars(wsName) Then
            wsName = CleanFileName(wsName)
        End If
        
        ' 创建新工作簿
        Set newWb = Workbooks.Add
        
        ' 复制当前工作表到新工作簿
        ws.Copy Before:=newWb.Sheets(1)
        
        ' 删除新工作簿中的默认工作表（更高效的方法）
        Application.DisplayAlerts = False
        On Error Resume Next
        newWb.Sheets(2).Delete
        On Error GoTo ErrorHandler
        Application.DisplayAlerts = True
        
        ' 保存新工作簿
        newWb.SaveAs savePath & "\" & wsName & fileExt, fileFormat
        newWb.Close False
        
        ' 释放对象引用
        Set newWb = Nothing
    Next ws
    
    ' 恢复应用程序设置
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    Application.EnableEvents = True
    Application.StatusBar = False
    
    ' 计算处理时间
    endTime = Timer
    
    ' 显示完成消息
    MsgBox "工作表拆分完成！" & vbCrLf & _
           "处理了 " & processedCount & " 个工作表" & vbCrLf & _
           "保存位置：" & savePath & vbCrLf & _
           "耗时：" & Format(endTime - startTime, "0.00") & " 秒", _
           vbInformation, "拆分完成"
    
    Exit Sub
    
ErrorHandler:
    ' 错误处理
    Dim errMsg As String
    errMsg = "错误代码：" & Err.Number & vbCrLf & _
             "错误描述：" & Err.Description & vbCrLf & _
             "发生位置：" & Err.Source
    
    ' 恢复应用程序设置
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    Application.EnableEvents = True
    Application.StatusBar = False
    
    ' 显示错误消息
    MsgBox errMsg, vbCritical, "拆分过程出错"
    
    ' 清理对象变量
    On Error Resume Next
    If Not newWb Is Nothing Then
        newWb.Close False
        Set newWb = Nothing
    End If
    Set ws = Nothing
    Set wb = Nothing
    
    Err.Clear
End Sub

' ============================================
' 辅助函数：检查文件名是否包含无效字符
' ============================================
Private Function HasInvalidFileNameChars(ByVal fileName As String) As Boolean
    Dim invalidChars As String
    Dim i As Integer
    
    ' Windows文件名中不允许的字符
    invalidChars = "\/:*?""<>|"
    
    For i = 1 To Len(invalidChars)
        If InStr(fileName, Mid(invalidChars, i, 1)) > 0 Then
            HasInvalidFileNameChars = True
            Exit Function
        End If
    Next i
    
    HasInvalidFileNameChars = False
End Function

' ============================================
' 辅助函数：清理文件名中的无效字符
' ============================================
Private Function CleanFileName(ByVal fileName As String) As String
    Dim result As String
    Dim i As Integer
    Dim ch As String
    
    result = ""
    
    For i = 1 To Len(fileName)
        ch = Mid(fileName, i, 1)
        Select Case ch
            Case "\", "/", ":", "*", "?", """", "<", ">", "|"
                result = result & "_"  ' 用下划线替换无效字符
            Case Else
                result = result & ch
        End Select
    Next i
    
    ' 移除开头和结尾的空格
    result = Trim(result)
    
    ' 如果结果为空，使用默认名称
    If result = "" Then
        result = "Sheet"
    End If
    
    CleanFileName = result
End Function
