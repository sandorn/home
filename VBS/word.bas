'==============================================================================
' Word 文档自动格式化宏
' 功能：支持普通公文和章节条文档的自动格式化
' 作者：PPA-Universal
'==============================================================================

Option Explicit

'==============================================================================
' 类型定义
'==============================================================================
Private Type StyleConfig
    StyleName As String
    FontName As String
    FontSize As Long
    Alignment As Long
    FirstLineIndentChars As Long
    OutlineLevel As Long
    PageBreakBefore As Boolean
    KeepWithNext As Boolean
    AutoUpdate As Boolean
    BaseStyle As String
    NextStyle As String
    DisableLineHeightGrid As Boolean
End Type

'==============================================================================
' 常量定义
'==============================================================================
Private Const DOC_TYPE_NORMAL = 1      ' 普通公文
Private Const DOC_TYPE_CHAPTER = 2     ' 章节条文档

' 字体常量（如需更换字体，修改此处即可）
Private Const FONT_BODY = "仿宋_GB2312"        ' 正文
Private Const FONT_TITLE1 = "方正小标宋简体"    ' 标题1（一级标题字体）
Private Const FONT_TITLE2 = "黑体"              ' 标题2
Private Const FONT_TITLE3 = "楷体_GB2312"       ' 标题3
Private Const FONT_TABLE = "宋体"               ' 表格
Private Const FONT_SIZE_BODY = 16               ' 正文字号（磅）
Private Const FONT_SIZE_TITLE1 = 22             ' 标题1字号
Private Const FONT_SIZE_TABLE = 12              ' 表格字号
Private Const LINE_SPACING_BODY = 30            ' 正文固定行距（磅）
Private Const LINE_SPACING_TABLE = 14           ' 表格固定行距（磅）

' Undo 记录名称
Private Const UNDO_NAME = "自动排版"

'==============================================================================
' 主入口函数
'==============================================================================

Sub 表格美化()
    '功能：智能表格美化 — 选中表格则处理选中表格，否则处理全部表格
    Dim tbl As Table
    Dim processedCount As Long
    Dim totalCount As Long
    Dim undo As UndoRecord

    totalCount = ActiveDocument.Tables.Count
    If totalCount = 0 Then
        MsgBox "文档中没有表格！", vbExclamation
        Exit Sub
    End If

    On Error GoTo Cleanup
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False

    Set undo = Application.UndoRecord
    undo.StartCustomRecord "表格美化"

    ' 判断是否在表格内或选中了表格区域
    If Selection.Information(wdWithInTable) Or Selection.Tables.Count > 0 Then
        For Each tbl In Selection.Tables
            processedCount = processedCount + 1
            Application.StatusBar = "正在美化表格 " & processedCount & " ..."
            格式化单个表格 tbl
        Next tbl
    Else
        For Each tbl In ActiveDocument.Tables
            processedCount = processedCount + 1
            Application.StatusBar = "正在美化表格 " & processedCount & "/" & totalCount & " ..."
            格式化单个表格 tbl
        Next tbl
    End If

    undo.EndCustomRecord
    Application.StatusBar = False
    MsgBox "表格美化完成！共处理 " & processedCount & " 个表格。", vbInformation

Cleanup:
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
End Sub

Sub 自动格式化文档()
    '功能：自动检测文档类型并格式化（支持 Ctrl+Z 一键撤销）
    On Error GoTo Cleanup
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False

    Dim docType As Integer
    Dim undo As UndoRecord

    ' 开启撤销记录，支持一键撤销所有操作
    Set undo = Application.UndoRecord
    undo.StartCustomRecord UNDO_NAME

    ' === 准备阶段 ===
    Call 初始化公文样式
    If ActiveDocument.Fields.Count > 0 Then Call 去除域代码
    Call 删除超链接
    Call 清理空行
    Call 清理多余空格

    Application.StatusBar = "正在检测文档类型..."
    docType = 检测文档类型()

    Select Case docType
        Case DOC_TYPE_CHAPTER
            Application.StatusBar = "正在格式化章节条文档..."
            Call 识别章节条结构
            MsgBox "已完成章节条文档格式化", vbInformation, "格式化完成"
        Case Else
            Application.StatusBar = "正在格式化普通公文..."
            Call 识别公文标题
            MsgBox "已完成普通公文格式化", vbInformation, "格式化完成"
    End Select

    ' === 收尾阶段 ===
    Dim tbl As Table, tblIdx As Long, tblTotal As Long
    tblTotal = ActiveDocument.Tables.Count
    For Each tbl In ActiveDocument.Tables
        tblIdx = tblIdx + 1
        Application.StatusBar = "正在格式化表格 " & tblIdx & "/" & tblTotal & " ..."
        格式化单个表格 tbl
    Next tbl
    Call 清理多余空格

    Application.StatusBar = "正在清理文档信息..."
    Call 删除个人信息
    Call 移动到文档开头

    undo.EndCustomRecord

Cleanup:
    Application.StatusBar = False
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
End Sub

'==============================================================================
' 文档类型检测
'==============================================================================

Function 检测文档类型() As Integer
    '功能：自动检测文档类型
    '返回：DOC_TYPE_CHAPTER=章节条文档, DOC_TYPE_NORMAL=普通公文
    Dim para As Paragraph
    Dim chapterCount As Integer, articleCount As Integer
    Dim regEx As Object
    
    Set regEx = CreateObject("VBScript.RegExp")
    regEx.IgnoreCase = True
    regEx.Global = False
    
    chapterCount = 0
    articleCount = 0
    
    ' 检测前100段或全部段落
    Dim count As Integer: count = 0
    For Each para In ActiveDocument.Paragraphs
        count = count + 1
        If count > 100 Then Exit For
        
        ' 检测"第X章"
        regEx.Pattern = "第[零〇一二三四五六七八九十百千\d]+章"
        If regEx.Test(para.Range.Text) Then chapterCount = chapterCount + 1
        
        ' 检测"第X条"
        regEx.Pattern = "第[零〇一二三四五六七八九十百千\d]+条"
        If regEx.Test(para.Range.Text) Then articleCount = articleCount + 1
    Next para
    
    ' 如果有章或条的结构，判定为章节条文档
    If chapterCount >= 1 Or articleCount >= 3 Then
        检测文档类型 = DOC_TYPE_CHAPTER
    Else
        检测文档类型 = DOC_TYPE_NORMAL
    End If
    
    Set regEx = Nothing
End Function

'==============================================================================
' 普通公文格式化
'==============================================================================

Private Sub 识别公文标题()
    '功能：识别普通公文中的标题结构，同时将非表格段落设为正文样式
    Dim para As Paragraph
    Dim regEx As Object
    Dim text As String
    Dim isTitle As Boolean
    
    Set regEx = CreateObject("VBScript.RegExp")
    regEx.IgnoreCase = True
    regEx.Global = False
    
    For Each para In ActiveDocument.Paragraphs
        If para.Range.Information(wdWithInTable) Then GoTo NextPara
        
        text = Trim(para.Range.Text)
        isTitle = False
        
        ' 一级标题：一、二、三、...
        regEx.Pattern = "^[一二三四五六七八九十]+[、．.]"
        If regEx.Test(text) Then
            para.Range.Style = ActiveDocument.Styles("标题 2")
            isTitle = True
            GoTo NextPara
        End If
        
        ' 二级标题：（一）（二）（三）...
        regEx.Pattern = "^[（(][一二三四五六七八九十]+[）)]"
        If regEx.Test(text) Then
            para.Range.Style = ActiveDocument.Styles("标题 3")
            isTitle = True
            GoTo NextPara
        End If
        
        ' 三级标题：1. 2. 3. 或 1、2、3、
        regEx.Pattern = "^[0-9]+[、．.]"
        If regEx.Test(text) Then
            para.Range.Style = ActiveDocument.Styles("标题 4")
            isTitle = True
            GoTo NextPara
        End If
        
        ' 四级标题：(1) (2) (3) 或 （1）（2）（3）
        regEx.Pattern = "^[（(][0-9]+[）)]"
        If regEx.Test(text) Then
            para.Range.Style = ActiveDocument.Styles("标题 5")
            isTitle = True
            GoTo NextPara
        End If
        
NextPara:
        ' 非标题的非表格段落统一设为正文
        If Not isTitle Then
            para.Range.Style = ActiveDocument.Styles("正文")
        End If
    Next para
    
    Set regEx = Nothing
End Sub

'==============================================================================
' 章节条文档格式化
'==============================================================================

Private Sub 识别章节条结构()
    '功能：识别章节条结构并设置样式
    ' 主标题→标题1 | 第X编→标题1 | 第X章→标题2(居中) | 第X节→标题3(居中) | 第X条→正文
    Dim para As Paragraph
    Dim regEx As Object
    Dim oRange As Range
    Dim text As String
    Dim m As Long, n As Long
    Dim matchResult As Object
    Dim isHeading As Boolean
    Dim foundMarker As Boolean     ' 是否已遇到第一个章节标记
    Dim titleDone As Boolean       ' 主标题是否已分配
    
    Set regEx = CreateObject("VBScript.RegExp")
    regEx.IgnoreCase = True
    regEx.Global = False
    
    For Each para In ActiveDocument.Paragraphs
        If para.Range.Information(wdWithInTable) Then GoTo NextPara
        
        text = para.Range.Text
        isHeading = False
        
        ' 第X编 - 标题1
        regEx.Pattern = "^[　 ]*(第[零〇一二三四五六七八九十百千\d]+编)[　 ]*"
        If regEx.Test(text) Then
            foundMarker = True
            para.Range.Style = ActiveDocument.Styles("标题 1")
            Set matchResult = regEx.Execute(text)
            If matchResult.Count > 0 Then
                m = matchResult(0).FirstIndex
                n = matchResult(0).Length
                Set oRange = ActiveDocument.Range(para.Range.Start + m, para.Range.Start + m + n)
                oRange.Font.Bold = True
            End If
            isHeading = True
            GoTo NextPara
        End If
        
        ' 第X章 - 标题2（居中）
        regEx.Pattern = "^[　 ]*(第[零〇一二三四五六七八九十百千\d]+章)[　 ]*"
        If regEx.Test(text) Then
            foundMarker = True
            para.Range.Style = ActiveDocument.Styles("标题 2")
            para.Range.ParagraphFormat.Alignment = wdAlignParagraphCenter
            isHeading = True
            GoTo NextPara
        End If
        
        ' 第X节 - 标题3（居中）
        regEx.Pattern = "^[　 ]*(第[零〇一二三四五六七八九十百千\d]+节)[　 ]*"
        If regEx.Test(text) Then
            foundMarker = True
            para.Range.Style = ActiveDocument.Styles("标题 3")
            para.Range.ParagraphFormat.Alignment = wdAlignParagraphCenter
            isHeading = True
            GoTo NextPara
        End If
        
        ' 第X条 - 正文，条号加粗
        regEx.Pattern = "^[　 ]*(第[零〇一二三四五六七八九十百千\d]+条)[　 ]*"
        If regEx.Test(text) Then
            foundMarker = True
            para.Range.Style = ActiveDocument.Styles("正文")
            Set matchResult = regEx.Execute(text)
            If matchResult.Count > 0 Then
                m = matchResult(0).FirstIndex
                n = matchResult(0).Length
                Set oRange = ActiveDocument.Range(para.Range.Start + m, para.Range.Start + m + n)
                oRange.Font.Bold = True
            End If
            isHeading = True
            GoTo NextPara
        End If
        
NextPara:
        If Not isHeading Then
            If Not foundMarker Then
                ' 第一个章节标记之前：首个非空段落 → 标题1，其余 → 正文
                If Not titleDone And Len(Trim(text)) > 1 Then
                    para.Range.Style = ActiveDocument.Styles("标题 1")
                    titleDone = True
                Else
                    para.Range.Style = ActiveDocument.Styles("正文")
                End If
            Else
                para.Range.Style = ActiveDocument.Styles("正文")
            End If
        End If
    Next para
    
    Set regEx = Nothing
End Sub

'==============================================================================
' 样式初始化
'==============================================================================

Private Sub ApplyStyleConfig(cfg As StyleConfig)
    Dim myStyle As Style

    On Error Resume Next
    Set myStyle = ActiveDocument.Styles(cfg.StyleName)
    If Err.Number <> 0 Then
        Err.Clear
        ' 样式不存在则跳过（如"列表段落"在部分文档中不存在）
        Exit Sub
    End If
    On Error GoTo 0

    With myStyle
        .AutomaticallyUpdate = cfg.AutoUpdate
        If Len(cfg.BaseStyle) > 0 Then .BaseStyle = cfg.BaseStyle
        .NextParagraphStyle = cfg.NextStyle
    End With

    With myStyle.Font
        .NameFarEast = cfg.FontName
        .NameAscii = cfg.FontName
        .NameOther = cfg.FontName
        .Name = cfg.FontName
        .Size = cfg.FontSize
        .Bold = False
        .Italic = False
        .Underline = wdUnderlineNone
        .Color = wdColorAutomatic
    End With

    With myStyle.ParagraphFormat
        .LeftIndent = CentimetersToPoints(0)
        .RightIndent = CentimetersToPoints(0)
        .SpaceBefore = 0
        .SpaceAfter = 0
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = LINE_SPACING_BODY
        .Alignment = cfg.Alignment
        .FirstLineIndent = CentimetersToPoints(0)
        .CharacterUnitFirstLineIndent = cfg.FirstLineIndentChars
        .OutlineLevel = cfg.OutlineLevel
        If cfg.PageBreakBefore Then .PageBreakBefore = True
        If cfg.KeepWithNext Then .KeepWithNext = True
        If cfg.DisableLineHeightGrid Then .DisableLineHeightGrid = True
        With .Shading
            .Texture = wdTextureNone
            .BackgroundPatternColor = wdColorAutomatic
        End With
    End With
End Sub

Private Sub 初始化公文样式()
    Dim cfg As StyleConfig

    ' ---- 正文 ----
    cfg.StyleName = "正文": cfg.FontName = FONT_BODY: cfg.FontSize = FONT_SIZE_BODY
    cfg.Alignment = wdAlignParagraphJustify: cfg.FirstLineIndentChars = 2
    cfg.OutlineLevel = wdOutlineLevelBodyText: cfg.PageBreakBefore = False
    cfg.KeepWithNext = False: cfg.AutoUpdate = False
    cfg.BaseStyle = "": cfg.NextStyle = "正文": cfg.DisableLineHeightGrid = True
    ApplyStyleConfig cfg

    ' ---- 标题 1 ----
    cfg.StyleName = "标题 1": cfg.FontName = FONT_TITLE1: cfg.FontSize = FONT_SIZE_TITLE1
    cfg.Alignment = wdAlignParagraphCenter: cfg.FirstLineIndentChars = 0
    cfg.OutlineLevel = wdOutlineLevel1: cfg.PageBreakBefore = True
    cfg.KeepWithNext = False: cfg.AutoUpdate = True
    cfg.BaseStyle = "正文": cfg.NextStyle = "正文": cfg.DisableLineHeightGrid = True
    ApplyStyleConfig cfg

    ' ---- 标题 2 ----
    cfg.StyleName = "标题 2": cfg.FontName = FONT_TITLE2: cfg.FontSize = FONT_SIZE_BODY
    cfg.Alignment = wdAlignParagraphJustify: cfg.FirstLineIndentChars = 2
    cfg.OutlineLevel = wdOutlineLevel2: cfg.PageBreakBefore = False
    cfg.KeepWithNext = True: cfg.AutoUpdate = True
    cfg.BaseStyle = "正文": cfg.NextStyle = "正文": cfg.DisableLineHeightGrid = False
    ApplyStyleConfig cfg

    ' ---- 标题 3 ----
    cfg.StyleName = "标题 3": cfg.FontName = FONT_TITLE3: cfg.FontSize = FONT_SIZE_BODY
    cfg.Alignment = wdAlignParagraphJustify: cfg.FirstLineIndentChars = 2
    cfg.OutlineLevel = wdOutlineLevel3: cfg.PageBreakBefore = False
    cfg.KeepWithNext = True: cfg.AutoUpdate = True
    cfg.BaseStyle = "正文": cfg.NextStyle = "正文": cfg.DisableLineHeightGrid = False
    ApplyStyleConfig cfg

    ' ---- 标题 4 ----
    cfg.StyleName = "标题 4": cfg.FontName = FONT_BODY: cfg.FontSize = FONT_SIZE_BODY
    cfg.Alignment = wdAlignParagraphJustify: cfg.FirstLineIndentChars = 2
    cfg.OutlineLevel = wdOutlineLevel4: cfg.PageBreakBefore = False
    cfg.KeepWithNext = True: cfg.AutoUpdate = True
    cfg.BaseStyle = "正文": cfg.NextStyle = "正文": cfg.DisableLineHeightGrid = False
    ApplyStyleConfig cfg

    ' ---- 标题 5 ----
    cfg.StyleName = "标题 5": cfg.FontName = FONT_BODY: cfg.FontSize = FONT_SIZE_BODY
    cfg.Alignment = wdAlignParagraphJustify: cfg.FirstLineIndentChars = 2
    cfg.OutlineLevel = wdOutlineLevel5: cfg.PageBreakBefore = False
    cfg.KeepWithNext = True: cfg.AutoUpdate = True
    cfg.BaseStyle = "正文": cfg.NextStyle = "正文": cfg.DisableLineHeightGrid = False
    ApplyStyleConfig cfg

    ' ---- 标题 6 ----
    cfg.StyleName = "标题 6": cfg.FontName = FONT_BODY: cfg.FontSize = FONT_SIZE_BODY
    cfg.Alignment = wdAlignParagraphJustify: cfg.FirstLineIndentChars = 2
    cfg.OutlineLevel = wdOutlineLevel6: cfg.PageBreakBefore = False
    cfg.KeepWithNext = True: cfg.AutoUpdate = True
    cfg.BaseStyle = "正文": cfg.NextStyle = "正文": cfg.DisableLineHeightGrid = False
    ApplyStyleConfig cfg

    ' ---- 列表段落 ----
    cfg.StyleName = "列表段落": cfg.FontName = FONT_BODY: cfg.FontSize = FONT_SIZE_BODY
    cfg.Alignment = wdAlignParagraphJustify: cfg.FirstLineIndentChars = 2
    cfg.OutlineLevel = wdOutlineLevelBodyText: cfg.PageBreakBefore = False
    cfg.KeepWithNext = False: cfg.AutoUpdate = True
    cfg.BaseStyle = "正文": cfg.NextStyle = "列表段落": cfg.DisableLineHeightGrid = False
    ApplyStyleConfig cfg
End Sub

'==============================================================================
' 通用格式化功能
'==============================================================================

Sub 清理空行()
    '功能：删除空行（包含空格、全角空格、Tab的行）
    Dim para As Paragraph
    Dim text As String
    Dim regEx As Object
    Dim i As Long
    
    Set regEx = CreateObject("VBScript.RegExp")
    regEx.Pattern = "^[\s　\t\n\r]+$"
    regEx.Global = True
    
    ' 从后向前删除，避免索引问题
    For i = ActiveDocument.Paragraphs.Count To 1 Step -1
        On Error Resume Next
        Set para = ActiveDocument.Paragraphs(i)
        If Err.Number <> 0 Then
            Err.Clear
            GoTo ContinueLoop
        End If
        On Error GoTo 0
        
        text = para.Range.Text
        ' 只剩段落标记的行，或纯空白行
        If Len(text) = 1 Or regEx.Test(text) Then
            para.Range.Delete
        End If
ContinueLoop:
    Next i
    
    Set regEx = Nothing
End Sub

Sub 清理多余空格()
    '功能：清理多余空格（包括全角、半角、Tab等），特别加强段首空格处理
    On Error GoTo Cleanup
    Application.ScreenUpdating = False

    Dim fullSpace As String
    fullSpace = ChrW(12288)  ' 全角空格

    ' === 第一阶段：高效的查找替换 ===
    With ActiveDocument.Content.Find
        .ClearFormatting
        .Replacement.ClearFormatting
        .Forward = True
        .Wrap = wdFindContinue
        .Format = False

        .MatchWildcards = False
        .Text = ChrW(&HA0)
        .Replacement.Text = " "
        .Execute Replace:=wdReplaceAll

        .Text = fullSpace
        .Replacement.Text = " "
        .Execute Replace:=wdReplaceAll

        .MatchWildcards = True
        .Text = "(^13)[ ]{1,}"
        .Replacement.Text = "\1"
        .Execute Replace:=wdReplaceAll

        .Text = "[ ]{1,}(^13)"
        .Replacement.Text = "\1"
        .Execute Replace:=wdReplaceAll

        .Text = "[ ]{2,}"
        .Replacement.Text = " "
        .Execute Replace:=wdReplaceAll

        .Text = "[ ]@(第[零〇一二三四五六七八九十百千0-9]{1,}[编章节条款项目])[ ]@"
        .Replacement.Text = "\1 "
        .Execute Replace:=wdReplaceAll

        .Text = "[ ]@([一二三四五六七八九十]{1,}[、．.])[ ]@"
        .Replacement.Text = "\1"
        .Execute Replace:=wdReplaceAll

        .Text = "[ ]@([（(][一二三四五六七八九十0-9]{1,}[）)])[ ]@"
        .Replacement.Text = "\1"
        .Execute Replace:=wdReplaceAll
    End With

    ' === 第二阶段：精准的段落遍历（处理漏网之鱼） ===
    Dim docRange As Range
    Set docRange = ActiveDocument.Content
    docRange.Collapse Direction:=wdCollapseStart
    Do While docRange.End < ActiveDocument.Content.End
        Dim charText As String
        charText = docRange.Characters(1).Text
        If charText = " " Or charText = vbTab Or charText = fullSpace Or charText = ChrW(&HA0) Then
             docRange.Characters(1).Delete
        Else
            Exit Do
        End If
    Loop

    Dim para As Paragraph
    Dim regEx As Object
    Set regEx = CreateObject("VBScript.RegExp")
    regEx.Pattern = "^[ \t　]+"

    For Each para In ActiveDocument.Paragraphs
        If Not para.Range.Information(wdWithInTable) Then
             Dim txt As String
             txt = para.Range.Text
             If regEx.Test(txt) Then
                 Dim newTxt As String
                 newTxt = regEx.Replace(txt, "")
                 If Len(newTxt) > 0 Then
                    para.Range.Text = newTxt
                 End If
             End If
        End If
    Next para

    Set regEx = Nothing
Cleanup:
    Application.ScreenUpdating = True
End Sub

Private Function 去除域代码() As Long
    '功能：将域代码转换为纯文本，返回处理的域数量
    Dim fld As Field
    For Each fld In ActiveDocument.Fields
        fld.Unlink
        去除域代码 = 去除域代码 + 1
    Next fld
End Function

Private Function 删除超链接() As Long
    '功能：删除所有超链接，返回删除数量
    Dim i As Long
    For i = ActiveDocument.Hyperlinks.Count To 1 Step -1
        ActiveDocument.Hyperlinks(i).Delete
        删除超链接 = 删除超链接 + 1
    Next i
End Function

Private Function 删除个人信息() As Boolean
    '功能：删除文档个人信息，返回是否成功
    On Error Resume Next
    ActiveDocument.RemoveDocumentInformation wdRDIDocumentProperties
    删除个人信息 = (Err.Number = 0)
    On Error GoTo 0
End Function

Private Function 移动到文档开头() As Long
    '功能：将光标移动到文档开头，返回位置
    Selection.HomeKey Unit:=wdStory
    移动到文档开头 = Selection.Start
End Function

'==============================================================================
' 表格格式化
'==============================================================================

Private Sub 格式化单个表格(tbl As Table)
    On Error GoTo ErrHandler

    With tbl
        ' ---- 表格基础设置 ----
        .AutoFitBehavior wdAutoFitContent
        .AutoFitBehavior wdAutoFitWindow
        .AllowAutoFit = False
        .Rows.Alignment = wdAlignRowCenter
        .Rows.WrapAroundText = False

        ' ---- 清除样式 ----
        On Error Resume Next
        .Style = "Normal"
        Err.Clear
        .Range.Style = "正文"
        Err.Clear
        On Error GoTo ErrHandler
        .Shading.Texture = wdTextureNone
        .Range.HighlightColorIndex = wdNoHighlight
        .Shading.BackgroundPatternColor = wdColorAutomatic

        ' ---- 单元格格式 ----
        .Range.Cells.VerticalAlignment = wdAlignVerticalCenter
        .Range.ParagraphFormat.Alignment = wdAlignParagraphCenter

        Dim c As cell, p As Paragraph, ct As String
        Dim cellRegEx As Object
        Set cellRegEx = CreateObject("VBScript.RegExp")
        cellRegEx.Global = True
        cellRegEx.Pattern = "[\r\n \　" & Chr(160) & ChrW(&HA0) & "]+"

        For Each c In .Range.Cells
            ' 用正则一次清除所有空白字符
            ct = cellRegEx.Replace(c.Range.Text, "")
            ct = Trim(ct)
            If Len(ct) > 0 Then
                c.Range.Text = ct
            End If

            With c.Range.ParagraphFormat
                .LeftIndent = 0
                .RightIndent = 0
                .FirstLineIndent = 0
                .CharacterUnitFirstLineIndent = 0
                .CharacterUnitLeftIndent = 0
                .CharacterUnitRightIndent = 0
                .SpaceBefore = 0
                .SpaceAfter = 0
                .LineSpacingRule = wdLineSpaceExactly
                .LineSpacing = LINE_SPACING_TABLE
            End With

            For Each p In c.Range.Paragraphs
                With p.Format
                    .LeftIndent = 0
                    .RightIndent = 0
                    .FirstLineIndent = 0
                    .CharacterUnitFirstLineIndent = 0
                    .CharacterUnitLeftIndent = 0
                    .CharacterUnitRightIndent = 0
                    .SpaceBefore = 0
                    .SpaceAfter = 0
                    .LineSpacingRule = wdLineSpaceExactly
                    .LineSpacing = LINE_SPACING_TABLE
                End With
            Next p

            c.Shading.BackgroundPatternColor = wdColorAutomatic
            c.Shading.Texture = wdTextureNone
        Next c

        Set cellRegEx = Nothing

        ' ---- 行高与边距 ----
        .Rows.HeightRule = wdRowHeightAtLeast
        .Rows.Height = MillimetersToPoints(7)
        .Rows.AllowBreakAcrossPages = True
        .Rows.LeftIndent = 0
        .LeftPadding = MillimetersToPoints(2)
        .RightPadding = MillimetersToPoints(2)
        .TopPadding = 0
        .BottomPadding = 0

        ' ---- 字体与边框 ----
        .Range.Font.Name = FONT_TABLE
        .Range.Font.Size = FONT_SIZE_TABLE
        .Range.Font.Bold = False
        .Range.Font.Color = wdColorBlack

        With .Borders
            .InsideLineStyle = wdLineStyleSingle
            .InsideLineWidth = wdLineWidth025pt
            .OutsideLineStyle = wdLineStyleSingle
            .OutsideLineWidth = wdLineWidth025pt
        End With

        ' ---- 首行特殊处理 ----
        With .Rows.First
            .Height = MillimetersToPoints(8)
            .HeadingFormat = True
            .Range.Font.Bold = True
            .Range.ParagraphFormat.Alignment = wdAlignParagraphCenter
            Dim fc As cell
            For Each fc In .Cells
                fc.Shading.BackgroundPatternColor = RGB(215, 215, 215)
            Next fc
        End With
    End With
    Exit Sub

ErrHandler:
    MsgBox "表格格式化出错！" & vbCrLf & vbCrLf & _
           "错误号: " & Err.Number & vbCrLf & _
           "描述: " & Err.Description, vbCritical, "表格格式化失败"
End Sub

'==============================================================================
' 辅助功能
'==============================================================================

Sub 转换为静态编号()
    '功能：将自动编号转换为静态文本
    Dim myRange As Range
    
    If Selection.Type = wdSelectionIP Then
        Set myRange = ActiveDocument.Content
    Else
        Set myRange = Selection.Range
    End If
    
    myRange.ListFormat.ConvertNumbersToText
    
    ' 替换Tab为空格
    With myRange.Find
        .ClearFormatting
        .Replacement.ClearFormatting
        .Text = "^t"
        .Replacement.Text = " "
        .Forward = True
        .Wrap = wdFindContinue
        .Execute Replace:=wdReplaceAll
    End With
End Sub

Sub 千分位格式化()
    '功能：将数字格式化为千分位格式
    On Error GoTo Cleanup
    Application.ScreenUpdating = False

    Dim rng As Range
    Dim endPos As Long
    Dim originalLen As Long

    If Selection.Type = wdSelectionIP Then
        Set rng = ActiveDocument.Content
        endPos = ActiveDocument.Content.End
    Else
        Set rng = Selection.Range
        endPos = Selection.Range.End
    End If

    With rng.Find
        .ClearFormatting
        .Text = "[0-9]{4,}"
        .MatchWildcards = True

        Do While .Execute
            With .Parent
                If .Start > endPos Then Exit Do
                originalLen = Len(.Text)
                .Text = Format(Val(.Text), "#,##0")
                endPos = endPos + Len(.Text) - originalLen
                .Start = .End
            End With
        Loop
    End With

    Application.ScreenUpdating = True
    Exit Sub

Cleanup:
    Application.ScreenUpdating = True
End Sub

'==============================================================================
' 条目处理
'==============================================================================

Sub 条目加粗()
    '功能：将"第X条"加粗
    On Error GoTo Cleanup
    Application.ScreenUpdating = False

    Dim para As Paragraph
    Dim regEx As Object
    Dim matchResult As Object
    Dim oRange As Range
    Dim m As Long, n As Long

    Set regEx = CreateObject("VBScript.RegExp")
    regEx.Pattern = "^第[^条]+条"
    regEx.Global = False
    regEx.IgnoreCase = False

    For Each para In ActiveDocument.Paragraphs
        Set matchResult = regEx.Execute(para.Range.Text)
        If matchResult.Count > 0 Then
            m = matchResult(0).FirstIndex
            n = matchResult(0).Length
            Set oRange = ActiveDocument.Range(para.Range.Start + m, para.Range.Start + m + n)
            oRange.Font.Bold = True
        End If
    Next para

    Set regEx = Nothing
Cleanup:
    Application.ScreenUpdating = True
End Sub
