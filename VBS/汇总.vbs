
Option Explicit

' 常量定义
Private Const SOURCE_WORKSHEET_NAME As String = "指标统计"
Private Const SOURCE_RANGE As String = "D4:O20"
Private Const TARGET_RANGE As String = "G2:R18"
Private Const REPORT_FOLDER_NAME As String = "经营报表"
Private Const CONFIG_SHEET_NAME As String = "填写页"
Private Const COMPANY_RANGE As String = "C2:C10"

' 主函数
Public Sub 数据汇总()
    ' 声明变量
    Dim sourcePath As String
    Dim wsConfig As Worksheet
    Dim targetSheetNames As Range
    Dim companyCount As Long
    Dim processedCount As Long
    Dim errorCount As Long
    Dim companyName As String
    
    ' 记录应用状态
    Dim prevScreenUpdating As Boolean
    Dim prevCalculation As XlCalculation
    Dim prevEnableEvents As Boolean
    
    ' 保存当前应用设置
    prevScreenUpdating = Application.ScreenUpdating
    prevCalculation = Application.Calculation
    prevEnableEvents = Application.EnableEvents
    
    ' 优化性能设置
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False
    
    On Error GoTo ErrorHandler
    
    ' 初始化计数器
    processedCount = 0
    errorCount = 0
    
    ' 获取配置工作表
    Set wsConfig = GetConfigWorksheet
    If wsConfig Is Nothing Then
        MsgBox "配置工作表 '" & CONFIG_SHEET_NAME & "' 不存在！", vbCritical
        GoTo Cleanup
    End If
    
    ' 构建源文件路径
    sourcePath = BuildSourcePath
    If Not ValidateSourcePath(sourcePath) Then
        MsgBox "经营报表文件夹不存在: " & sourcePath, vbCritical
        GoTo Cleanup
    End If
    
    ' 获取公司列表
    Set targetSheetNames = wsConfig.Range(COMPANY_RANGE)
    companyCount = WorksheetFunction.CountA(targetSheetNames)
    
    ' 循环处理每个子公司
    ProcessCompanies targetSheetNames, sourcePath, processedCount, errorCount
    
    ' 显示完成消息
    DisplayCompletionMessage processedCount, errorCount, companyCount
    
Cleanup:
    ' 恢复应用设置
    Application.ScreenUpdating = prevScreenUpdating
    Application.Calculation = prevCalculation
    Application.EnableEvents = prevEnableEvents
    Application.CutCopyMode = False
    
    ' 清理对象变量
    Set wsConfig = Nothing
    Set targetSheetNames = Nothing
    
    Exit Sub
    
ErrorHandler:
    ' 错误处理
    MsgBox "处理过程中发生错误: " & Err.Description & vbCrLf & _
           "错误代码: " & Err.Number, vbCritical
    Err.Clear
    GoTo Cleanup
End Sub

' 获取配置工作表
Private Function GetConfigWorksheet() As Worksheet
    On Error Resume Next
    Set GetConfigWorksheet = ThisWorkbook.Worksheets(CONFIG_SHEET_NAME)
    On Error GoTo 0
End Function

' 构建源文件路径
Private Function BuildSourcePath() As String
    BuildSourcePath = ThisWorkbook.Path & "\" & REPORT_FOLDER_NAME & "\" 
End Function

' 验证源文件路径
Private Function ValidateSourcePath(ByVal path As String) As Boolean
    ValidateSourcePath = (Dir(path, vbDirectory) <> "")
End Function

' 处理所有公司
Private Sub ProcessCompanies(ByVal companyRange As Range, ByVal sourcePath As String, _
                            ByRef processedCount As Long, ByRef errorCount As Long)
    Dim cell As Range
    Dim companyName As String
    Dim currentIndex As Long
    Dim totalCompanies As Long
    
    totalCompanies = WorksheetFunction.CountA(companyRange)
    currentIndex = 0
    
    For Each cell In companyRange
        If cell.Value <> "" Then
            currentIndex = currentIndex + 1
            companyName = cell.Value
            
            ' 显示进度
            UpdateProgress currentIndex, totalCompanies, companyName
            
            ' 处理单个公司
            If ProcessSingleCompany(companyName, sourcePath) Then
                processedCount = processedCount + 1
            Else
                errorCount = errorCount + 1
            End If
        End If
    Next cell
    
    ' 清除状态栏
    Application.StatusBar = False
End Sub

' 处理单个公司
Private Function ProcessSingleCompany(ByVal companyName As String, ByVal sourcePath As String) As Boolean
    Dim sourceFile As String
    Dim wbSource As Workbook
    Dim wsTarget As Worksheet
    
    ProcessSingleCompany = False
    
    ' 构建源文件路径
    sourceFile = sourcePath & companyName & ".xlsx"
    
    ' 检查源文件是否存在
    If Dir(sourceFile) = "" Then
        LogError "源文件不存在: " & sourceFile
        Exit Function
    End If
    
    ' 检查目标工作表是否存在
    Set wsTarget = GetTargetWorksheet(companyName)
    If wsTarget Is Nothing Then
        LogError "工作表 '" & companyName & "' 不存在"
        Exit Function
    End If
    
    ' 复制数据
    On Error Resume Next
    Set wbSource = Workbooks.Open(sourceFile, ReadOnly:=True)
    If Err.Number <> 0 Then
        LogError "无法打开源文件: " & sourceFile & vbCrLf & Err.Description
        On Error GoTo 0
        Exit Function
    End If
    On Error GoTo 0
    
    ' 检查源工作表是否存在
    If Not WorksheetExists(wbSource, SOURCE_WORKSHEET_NAME) Then
        LogError "源工作表 '" & SOURCE_WORKSHEET_NAME & "' 不存在于文件: " & sourceFile
        wbSource.Close SaveChanges:=False
        Exit Function
    End If
    
    ' 复制数据
    On Error Resume Next
    wbSource.Worksheets(SOURCE_WORKSHEET_NAME).Range(SOURCE_RANGE).Copy
    wsTarget.Range(TARGET_RANGE).PasteSpecial Paste:=xlPasteValues
    If Err.Number <> 0 Then
        LogError "复制数据失败: " & Err.Description
        On Error GoTo 0
        wbSource.Close SaveChanges:=False
        Exit Function
    End If
    On Error GoTo 0
    
    ' 关闭源工作簿
    wbSource.Close SaveChanges:=False
    ProcessSingleCompany = True
    
    ' 清理对象变量
    Set wbSource = Nothing
    Set wsTarget = Nothing
End Function

' 获取目标工作表
Private Function GetTargetWorksheet(ByVal sheetName As String) As Worksheet
    On Error Resume Next
    Set GetTargetWorksheet = ThisWorkbook.Worksheets(sheetName)
    On Error GoTo 0
End Function

' 检查工作表是否存在
Private Function WorksheetExists(ByVal wb As Workbook, ByVal sheetName As String) As Boolean
    Dim ws As Worksheet
    On Error Resume Next
    Set ws = wb.Worksheets(sheetName)
    WorksheetExists = Not (ws Is Nothing)
    On Error GoTo 0
    Set ws = Nothing
End Function

' 更新进度
Private Sub UpdateProgress(ByVal current As Long, ByVal total As Long, ByVal companyName As String)
    Application.StatusBar = "正在处理: " & companyName & " (" & current & "/" & total & ")"
    ' 短暂暂停以确保状态更新
    DoEvents
End Sub

' 记录错误
Private Sub LogError(ByVal errorMessage As String)
    ' 可以扩展为写入日志文件
    Debug.Print "错误: " & errorMessage
End Sub

' 显示完成消息
Private Sub DisplayCompletionMessage(ByVal processed As Long, ByVal errors As Long, ByVal total As Long)
    Dim message As String
    
    message = "数据汇总处理完成！" & vbCrLf & vbCrLf
    message = message & "总公司数: " & total & vbCrLf
    message = message & "成功处理: " & processed & vbCrLf
    message = message & "处理失败: " & errors & vbCrLf
    
    If errors > 0 Then
        message = message & vbCrLf & "详细错误信息请查看VBE的立即窗口。"
    End If
    
    MsgBox message, vbInformation, "处理完成"
End Sub
