'==============================================================================
' Word 文档自动格式化宏
' 功能：支持普通公文和章节条文档的自动格式化
' 作者：PPA-Universal
'==============================================================================

Option Explicit

'==============================================================================
' 常量定义
'==============================================================================
Private Const DOC_TYPE_NORMAL = 1      ' 普通公文
Private Const DOC_TYPE_CHAPTER = 2     ' 章节条文档

'==============================================================================
' 主入口函数
'==============================================================================

Sub 自动格式化文档()
    '功能：自动检测文档类型并格式化
    On Error Resume Next
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    Dim docType As Integer
    
    ' 先执行强力清理空格，确保检测准确且环境干净
    Call 清理多余空格
    
    docType = 检测文档类型()
    
    Select Case docType
        Case DOC_TYPE_CHAPTER
            Call 格式化章节条文档
            MsgBox "已完成章节条文档格式化", vbInformation, "格式化完成"
        Case Else
            Call 格式化普通公文
            MsgBox "已完成普通公文格式化", vbInformation, "格式化完成"
    End Select
    
    Call 删除个人信息
    Call 移动到文档开头
    
    Err.Clear
    On Error GoTo 0
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
End Sub

Sub 格式化为普通公文()
    '功能：强制按普通公文格式化
    On Error Resume Next
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    Call 格式化普通公文
    Call 删除个人信息
    Call 移动到文档开头
    
    Err.Clear
    On Error GoTo 0
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    MsgBox "已完成普通公文格式化", vbInformation, "格式化完成"
End Sub

Sub 格式化为章节条文档()
    '功能：强制按章节条文档格式化
    On Error Resume Next
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    Call 格式化章节条文档
    Call 删除个人信息
    Call 移动到文档开头
    
    Err.Clear
    On Error GoTo 0
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    MsgBox "已完成章节条文档格式化", vbInformation, "格式化完成"
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

Function 格式化普通公文()
    '功能：格式化普通公文
    
    ' 1. 初始化样式
    Call 初始化公文样式
    
    ' 2. 去除域代码
    If ActiveDocument.Fields.Count > 0 Then Call 去除域代码
    
    ' 3. 删除超链接
    Call 删除超链接
    
    ' 4. 清理空行和多余空格（先清理，再设置格式）
    Call 清理空行
    Call 清理多余空格
    
    ' 5. 设置全文基础格式
    Call 设置全文基础格式
    
    ' 6. 再次清理空格（设置格式后可能残留）
    Call 清理多余空格
    
    ' 7. 识别并设置标题样式
    Call 识别公文标题
    
    ' 8. 格式化表格
    Call 格式化所有表格
    
    ' 9. 最后再次强力清理空格，确保万无一失
    Call 清理多余空格
End Function

Function 识别公文标题()
    '功能：识别普通公文中的标题结构
    Dim para As Paragraph
    Dim regEx As Object
    Dim text As String
    
    Set regEx = CreateObject("VBScript.RegExp")
    regEx.IgnoreCase = True
    regEx.Global = False
    
    For Each para In ActiveDocument.Paragraphs
        If para.Range.Information(wdWithInTable) Then GoTo NextPara
        
        text = Trim(para.Range.Text)
        
        ' 一级标题：一、二、三、...
        regEx.Pattern = "^[一二三四五六七八九十]+[、．.]"
        If regEx.Test(text) Then
            para.Range.Style = ActiveDocument.Styles("标题 2")
            GoTo NextPara
        End If
        
        ' 二级标题：（一）（二）（三）...
        regEx.Pattern = "^[（(][一二三四五六七八九十]+[）)]"
        If regEx.Test(text) Then
            para.Range.Style = ActiveDocument.Styles("标题 3")
            GoTo NextPara
        End If
        
        ' 三级标题：1. 2. 3. 或 1、2、3、
        regEx.Pattern = "^[0-9]+[、．.\.]"
        If regEx.Test(text) Then
            para.Range.Style = ActiveDocument.Styles("标题 4")
            GoTo NextPara
        End If
        
        ' 四级标题：(1) (2) (3) 或 （1）（2）（3）
        regEx.Pattern = "^[（(][0-9]+[）)]"
        If regEx.Test(text) Then
            para.Range.Style = ActiveDocument.Styles("标题 5")
            GoTo NextPara
        End If
        
NextPara:
    Next para
    
    Set regEx = Nothing
End Function

'==============================================================================
' 章节条文档格式化
'==============================================================================

Function 格式化章节条文档()
    '功能：格式化章节条文档（法规、规章等）
    
    ' 1. 初始化样式
    Call 初始化公文样式
    
    ' 2. 去除域代码
    If ActiveDocument.Fields.Count > 0 Then Call 去除域代码
    
    ' 3. 删除超链接
    Call 删除超链接
    
    ' 4. 清理空行和多余空格（先清理，再设置格式）
    Call 清理空行
    Call 清理多余空格
    
    ' 5. 设置全文基础格式
    Call 设置全文基础格式
    
    ' 6. 再次清理空格（设置格式后可能残留）
    Call 清理多余空格
    
    ' 7. 识别并设置章节条样式
    Call 识别章节条结构
    
    ' 8. 格式化表格
    Call 格式化所有表格
    
    ' 9. 最后再次强力清理空格，确保万无一失
    Call 清理多余空格
End Function

Function 识别章节条结构()
    '功能：识别章节条结构并设置样式
    Dim para As Paragraph
    Dim regEx As Object
    Dim oRange As Range
    Dim text As String
    Dim m As Long, n As Long
    Dim matchResult As Object
    
    Set regEx = CreateObject("VBScript.RegExp")
    regEx.IgnoreCase = True
    regEx.Global = False
    
    For Each para In ActiveDocument.Paragraphs
        If para.Range.Information(wdWithInTable) Then GoTo NextPara
        
        text = para.Range.Text
        
        ' 第X编（如有）- 标题1
        regEx.Pattern = "^[　 ]*(第[零〇一二三四五六七八九十百千\d]+编)[　 ]*"
        If regEx.Test(text) Then
            para.Range.Style = ActiveDocument.Styles("标题 1")
            ' 加粗编号
            Set matchResult = regEx.Execute(text)
            If matchResult.Count > 0 Then
                m = matchResult(0).FirstIndex
                n = matchResult(0).Length
                Set oRange = ActiveDocument.Range(para.Range.Start + m, para.Range.Start + m + n)
                oRange.Font.Bold = True
            End If
            GoTo NextPara
        End If
        
        ' 第X章 - 标题1
        regEx.Pattern = "^[　 ]*(第[零〇一二三四五六七八九十百千\d]+章)[　 ]*"
        If regEx.Test(text) Then
            para.Range.Style = ActiveDocument.Styles("标题 1")
            para.Range.ParagraphFormat.Alignment = wdAlignParagraphCenter
            GoTo NextPara
        End If
        
        ' 第X节 - 标题2
        regEx.Pattern = "^[　 ]*(第[零〇一二三四五六七八九十百千\d]+节)[　 ]*"
        If regEx.Test(text) Then
            para.Range.Style = ActiveDocument.Styles("标题 2")
            para.Range.ParagraphFormat.Alignment = wdAlignParagraphCenter
            GoTo NextPara
        End If
        
        ' 第X条 - 加粗条号，正文样式
        regEx.Pattern = "^[　 ]*(第[零〇一二三四五六七八九十百千\d]+条)[　 ]*"
        If regEx.Test(text) Then
            para.Range.Style = ActiveDocument.Styles("正文")
            ' 加粗条号
            Set matchResult = regEx.Execute(text)
            If matchResult.Count > 0 Then
                m = matchResult(0).FirstIndex
                n = Len(matchResult(0).SubMatches(0))
                Set oRange = ActiveDocument.Range(para.Range.Start + m, para.Range.Start + m + n + 1)
                oRange.Font.Bold = True
            End If
            GoTo NextPara
        End If
        
NextPara:
    Next para
    
    Set regEx = Nothing
End Function

'==============================================================================
' 样式初始化
'==============================================================================

Function 初始化公文样式()
    '功能：初始化所有公文样式
    Call 设置正文样式
    Call 设置标题1样式
    Call 设置标题2样式
    Call 设置标题3样式
    Call 设置标题4样式
    Call 设置标题5样式
    Call 设置标题6样式
    Call 设置列表段落样式
End Function

Function 设置正文样式()
    Dim myStyle As Style
    Set myStyle = ActiveDocument.Styles("正文")
    
    With myStyle
        .AutomaticallyUpdate = False
        .NextParagraphStyle = "正文"
    End With
    
    With myStyle.Font
        .NameFarEast = "仿宋_GB2312"
        .NameAscii = "仿宋_GB2312"
        .NameOther = "仿宋_GB2312"
        .Name = "仿宋_GB2312"
        .Size = 16
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
        .LineSpacing = 29
        .Alignment = wdAlignParagraphJustify
        .FirstLineIndent = CentimetersToPoints(0)
        .CharacterUnitFirstLineIndent = 2
        .OutlineLevel = wdOutlineLevelBodyText
        .DisableLineHeightGrid = True
        With .Shading
            .Texture = wdTextureNone
            .BackgroundPatternColor = wdColorAutomatic
        End With
    End With
End Function

Function 设置标题1样式()
    Dim myStyle As Style
    Set myStyle = ActiveDocument.Styles("标题 1")
    
    With myStyle
        .AutomaticallyUpdate = True
        .BaseStyle = "正文"
        .NextParagraphStyle = "正文"
    End With
    
    With myStyle.Font
        .NameFarEast = "方正小标宋简体"
        .NameAscii = "方正小标宋简体"
        .Name = "方正小标宋简体"
        .Size = 22
        .Bold = False
        .Color = wdColorAutomatic
    End With
    
    With myStyle.ParagraphFormat
        .SpaceBefore = 0
        .SpaceAfter = 0
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphCenter
        .FirstLineIndent = CentimetersToPoints(0)
        .CharacterUnitFirstLineIndent = 0
        .OutlineLevel = wdOutlineLevel1
        .PageBreakBefore = True
        With .Shading
            .Texture = wdTextureNone
            .BackgroundPatternColor = wdColorAutomatic
        End With
    End With
End Function

Function 设置标题2样式()
    Dim myStyle As Style
    Set myStyle = ActiveDocument.Styles("标题 2")
    
    With myStyle
        .AutomaticallyUpdate = True
        .BaseStyle = "正文"
        .NextParagraphStyle = "正文"
    End With
    
    With myStyle.Font
        .NameFarEast = "黑体"
        .NameAscii = "黑体"
        .NameOther = "黑体"
        .Name = "黑体"
        .Size = 16
        .Bold = False
        .Color = wdColorAutomatic
    End With
    
    With myStyle.ParagraphFormat
        .SpaceBefore = 0
        .SpaceAfter = 0
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphJustify
        .FirstLineIndent = CentimetersToPoints(0)
        .CharacterUnitFirstLineIndent = 2
        .OutlineLevel = wdOutlineLevel2
        .KeepWithNext = True
        With .Shading
            .Texture = wdTextureNone
            .BackgroundPatternColor = wdColorAutomatic
        End With
    End With
End Function

Function 设置标题3样式()
    Dim myStyle As Style
    Set myStyle = ActiveDocument.Styles("标题 3")
    
    With myStyle
        .AutomaticallyUpdate = True
        .BaseStyle = "正文"
        .NextParagraphStyle = "正文"
    End With
    
    With myStyle.Font
        .NameFarEast = "楷体_GB2312"
        .NameAscii = "楷体_GB2312"
        .NameOther = "楷体_GB2312"
        .Name = "楷体_GB2312"
        .Size = 16
        .Bold = False
        .Color = wdColorAutomatic
    End With
    
    With myStyle.ParagraphFormat
        .SpaceBefore = 0
        .SpaceAfter = 0
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphJustify
        .FirstLineIndent = CentimetersToPoints(0)
        .CharacterUnitFirstLineIndent = 2
        .OutlineLevel = wdOutlineLevel3
        .KeepWithNext = True
        With .Shading
            .Texture = wdTextureNone
            .BackgroundPatternColor = wdColorAutomatic
        End With
    End With
End Function

Function 设置标题4样式()
    Dim myStyle As Style
    Set myStyle = ActiveDocument.Styles("标题 4")
    
    With myStyle
        .AutomaticallyUpdate = True
        .BaseStyle = "正文"
        .NextParagraphStyle = "正文"
    End With
    
    With myStyle.Font
        .NameFarEast = "仿宋_GB2312"
        .NameAscii = "仿宋_GB2312"
        .NameOther = "仿宋_GB2312"
        .Name = "仿宋_GB2312"
        .Size = 16
        .Bold = False
        .Color = wdColorAutomatic
    End With
    
    With myStyle.ParagraphFormat
        .SpaceBefore = 0
        .SpaceAfter = 0
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphJustify
        .FirstLineIndent = CentimetersToPoints(0)
        .CharacterUnitFirstLineIndent = 2
        .OutlineLevel = wdOutlineLevel4
        .KeepWithNext = True
        With .Shading
            .Texture = wdTextureNone
            .BackgroundPatternColor = wdColorAutomatic
        End With
    End With
End Function

Function 设置标题5样式()
    Dim myStyle As Style
    Set myStyle = ActiveDocument.Styles("标题 5")
    
    With myStyle
        .AutomaticallyUpdate = True
        .BaseStyle = "正文"
        .NextParagraphStyle = "正文"
    End With
    
    With myStyle.Font
        .NameFarEast = "仿宋_GB2312"
        .NameAscii = "仿宋_GB2312"
        .NameOther = "仿宋_GB2312"
        .Name = "仿宋_GB2312"
        .Size = 16
        .Bold = False
        .Color = wdColorAutomatic
    End With
    
    With myStyle.ParagraphFormat
        .SpaceBefore = 0
        .SpaceAfter = 0
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphJustify
        .FirstLineIndent = CentimetersToPoints(0)
        .CharacterUnitFirstLineIndent = 2
        .OutlineLevel = wdOutlineLevel5
        .KeepWithNext = True
        With .Shading
            .Texture = wdTextureNone
            .BackgroundPatternColor = wdColorAutomatic
        End With
    End With
End Function

Function 设置标题6样式()
    Dim myStyle As Style
    Set myStyle = ActiveDocument.Styles("标题 6")
    
    With myStyle
        .AutomaticallyUpdate = True
        .BaseStyle = "正文"
        .NextParagraphStyle = "正文"
    End With
    
    With myStyle.Font
        .NameFarEast = "仿宋_GB2312"
        .NameAscii = "仿宋_GB2312"
        .NameOther = "仿宋_GB2312"
        .Name = "仿宋_GB2312"
        .Size = 16
        .Bold = False
        .Color = wdColorAutomatic
    End With
    
    With myStyle.ParagraphFormat
        .SpaceBefore = 0
        .SpaceAfter = 0
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphJustify
        .FirstLineIndent = CentimetersToPoints(0)
        .CharacterUnitFirstLineIndent = 2
        .OutlineLevel = wdOutlineLevel6
        .KeepWithNext = True
        With .Shading
            .Texture = wdTextureNone
            .BackgroundPatternColor = wdColorAutomatic
        End With
    End With
End Function

Function 设置列表段落样式()
    Dim myStyle As Style
    Set myStyle = ActiveDocument.Styles("列表段落")
    
    With myStyle
        .AutomaticallyUpdate = True
        .BaseStyle = "正文"
        .NextParagraphStyle = "列表段落"
    End With
    
    With myStyle.Font
        .NameFarEast = "仿宋_GB2312"
        .NameAscii = "仿宋_GB2312"
        .NameOther = "仿宋_GB2312"
        .Name = "仿宋_GB2312"
        .Size = 16
        .Bold = False
        .Color = wdColorAutomatic
    End With
    
    With myStyle.ParagraphFormat
        .SpaceBefore = 0
        .SpaceAfter = 0
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphJustify
        .FirstLineIndent = CentimetersToPoints(0)
        .CharacterUnitFirstLineIndent = 2
        .OutlineLevel = wdOutlineLevelBodyText
        With .Shading
            .Texture = wdTextureNone
            .BackgroundPatternColor = wdColorAutomatic
        End With
    End With
End Function

'==============================================================================
' 通用格式化功能
'==============================================================================

Function 设置全文基础格式()
    '功能：设置全文基础格式为正文样式
    Dim para As Paragraph
    
    For Each para In ActiveDocument.Paragraphs
        If Not para.Range.Information(wdWithInTable) Then
            para.Range.Style = ActiveDocument.Styles("正文")
        End If
    Next para
End Function

Function 清理空行()
    '功能：删除空行（包含空格、全角空格、Tab的行）
    On Error Resume Next
    Dim para As Paragraph
    Dim text As String
    Dim regEx As Object
    
    Set regEx = CreateObject("VBScript.RegExp")
    regEx.Pattern = "^[\s　\t\n\r]+$"
    regEx.Global = True
    
    ' 从后向前删除，避免索引问题
    Dim i As Long
    For i = ActiveDocument.Paragraphs.Count To 1 Step -1
        Set para = ActiveDocument.Paragraphs(i)
        text = para.Range.Text
        ' 只剩段落标记的行
        If Len(text) = 1 Or regEx.Test(text) Then
            para.Range.Delete
        End If
    Next i
    
    Set regEx = Nothing
End Function

Function 清理多余空格()
    '功能：清理多余空格（包括全角、半角、Tab等），特别加强段首空格处理
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
        
        ' 1. 不间断空格 -> 普通空格
        .MatchWildcards = False
        .Text = ChrW(&HA0)
        .Replacement.Text = " "
        .Execute Replace:=wdReplaceAll
        
        ' 2. 全角空格 -> 半角空格
        .Text = fullSpace
        .Replacement.Text = " "
        .Execute Replace:=wdReplaceAll
        
        ' 3. 强力清除段首空格 (通配符: 段落标记后跟空格)
        .MatchWildcards = True
        .Text = "(^13)[ ]{1,}"
        .Replacement.Text = "\1"
        .Execute Replace:=wdReplaceAll
        
        ' 4. 清除行尾空格
        .Text = "[ ]{1,}(^13)"
        .Replacement.Text = "\1"
        .Execute Replace:=wdReplaceAll
        
        ' 5. 合并多个连续空格
        .Text = "[ ]{2,}"
        .Replacement.Text = " "
        .Execute Replace:=wdReplaceAll
        
        ' 6. 针对特定公文结构的空格清理
        ' 章节条前后: " 第二章 " -> "第二章 "
        .Text = "[ ]@(第[零〇一二三四五六七八九十百千0-9]{1,}[编章节条款项目])[ ]@"
        .Replacement.Text = "\1 "
        .Execute Replace:=wdReplaceAll
        
        ' 标题序号前后: " 一、 " -> "一、"
        .Text = "[ ]@([一二三四五六七八九十]{1,}[、．.])[ ]@"
        .Replacement.Text = "\1"
        .Execute Replace:=wdReplaceAll
        
        ' 括号序号前后: " （一） " -> "（一）"
        .Text = "[ ]@([（(][一二三四五六七八九十0-9]{1,}[）)])[ ]@"
        .Replacement.Text = "\1"
        .Execute Replace:=wdReplaceAll
    End With
    
    ' === 第二阶段：精准的段落遍历（处理漏网之鱼） ===
    ' 专门处理文档开头的空格
    Dim docRange As Range
    Set docRange = ActiveDocument.Content
    docRange.Collapse Direction:=wdCollapseStart
    ' 简单循环删除开头的空格字符
    Do While docRange.End < ActiveDocument.Content.End
        Dim charText As String
        charText = docRange.Characters(1).Text
        If charText = " " Or charText = vbTab Or charText = fullSpace Or charText = ChrW(&HA0) Then
             docRange.Characters(1).Delete
        Else
            Exit Do
        End If
    Loop

    ' 遍历所有段落，清理段首残留的空格（特别是Tab等）
    ' 使用正则匹配段首空白
    Dim para As Paragraph
    Dim regEx As Object
    Set regEx = CreateObject("VBScript.RegExp")
    regEx.Pattern = "^[ \t　]+" ' 匹配段首的空格、Tab、全角空格
    
    For Each para In ActiveDocument.Paragraphs
        ' 跳过表格
        If Not para.Range.Information(wdWithInTable) Then
             Dim txt As String
             txt = para.Range.Text
             ' 只有当确实匹配到段首空格时才进行替换，避免不必要的写入
             If regEx.Test(txt) Then
                 Dim newTxt As String
                 newTxt = regEx.Replace(txt, "")
                 ' 确保没有误删整个段落（保留段落标记）
                 If Len(newTxt) > 0 Then
                    para.Range.Text = newTxt
                 End If
             End If
        End If
    Next para
    
    Set regEx = Nothing
    Application.ScreenUpdating = True
End Function

Sub 强力清理段首空格()
    '功能：专门清理段首空格，可作为补充使用
    Call 清理多余空格
    MsgBox "段首空格清理完成", vbInformation
End Sub

Function 去除域代码()
    '功能：将域代码转换为纯文本
    Dim fld As Field
    For Each fld In ActiveDocument.Fields
        fld.Unlink
    Next fld
End Function

Function 删除超链接()
    '功能：删除所有超链接
    Dim i As Long
    For i = ActiveDocument.Hyperlinks.Count To 1 Step -1
        ActiveDocument.Hyperlinks(1).Delete
    Next i
End Function

Function 删除个人信息()
    '功能：删除文档个人信息
    On Error Resume Next
    ActiveDocument.RemoveDocumentInformation wdRDIDocumentProperties
End Function

Function 移动到文档开头()
    '功能：将光标移动到文档开头
    Selection.HomeKey Unit:=wdStory
End Function

'==============================================================================
' 表格格式化
'==============================================================================

Function 格式化所有表格()
    '功能：格式化文档中的所有表格
    Dim tbl As Table
    For Each tbl In ActiveDocument.Tables
        Call 格式化单个表格(tbl)
    Next tbl
End Function

Function 格式化单个表格(tbl As Table)
    '功能：格式化单个表格为网格型
    On Error Resume Next
    
    With tbl
        ' ========== 表格基础设置 ==========
        ' 自动调整（先执行，后续设置可能覆盖）
        .AutoFitBehavior wdAutoFitContent
        .AutoFitBehavior wdAutoFitWindow
        .AllowAutoFit = False              ' 禁用自动调整列宽
        .Rows.Alignment = wdAlignRowCenter ' 表格水平居中
        .Rows.WrapAroundText = False       ' 禁用文字环绕
        
        ' 清除样式干扰
        .Style = "Normal"
        .Range.Style = "正文"
        .Shading.Texture = wdTextureNone
        .Range.HighlightColorIndex = wdNoHighlight
        .Shading.BackgroundPatternColor = wdColorAutomatic
        
        ' ========== 单元格格式设置 ==========
        .Range.Cells.VerticalAlignment = wdAlignVerticalCenter  ' 垂直居中
        .Range.ParagraphFormat.Alignment = wdAlignParagraphCenter ' 水平居中
        
        ' 遍历单元格：清理内容和格式
        Dim cell As cell
        Dim para As Paragraph
        For Each cell In .Range.Cells
            ' 清理单元格内容（去除多余空格和不可见字符）
            With cell.Range
                Dim cellText As String
                cellText = .Text
                ' Word 单元格文本最后有2个字符：Chr(13) + Chr(7)
                cellText = Left(cellText, Len(cellText) - 2)
                cellText = Replace(cellText, vbCr, "")
                cellText = Replace(cellText, vbLf, "")
                cellText = Replace(cellText, vbCrLf, "")
                cellText = Replace(cellText, " ", "")
                cellText = Replace(cellText, "　", "")      ' 全角空格
                cellText = Replace(cellText, Chr(160), "")  ' 不间断空格
                cellText = Replace(cellText, ChrW(&HA0), "")
                cellText = Trim(cellText)
                .Text = cellText
            End With
            
            ' 段落格式（第一层）
            With cell.Range.ParagraphFormat
                .LeftIndent = 0
                .RightIndent = 0
                .FirstLineIndent = 0
                .CharacterUnitFirstLineIndent = 0
                .CharacterUnitLeftIndent = 0
                .CharacterUnitRightIndent = 0
                .SpaceBefore = 0
                .SpaceAfter = 0
                .LineSpacingRule = wdLineSpaceExactly
                .LineSpacing = 14  ' 固定值14磅
            End With
            
            ' 双重保险：遍历单元格内每个段落
            For Each para In cell.Range.Paragraphs
                With para.Format
                    .LeftIndent = 0
                    .RightIndent = 0
                    .FirstLineIndent = 0
                    .CharacterUnitFirstLineIndent = 0
                    .CharacterUnitLeftIndent = 0
                    .CharacterUnitRightIndent = 0
                    .SpaceBefore = 0
                    .SpaceAfter = 0
                    .LineSpacingRule = wdLineSpaceExactly
                    .LineSpacing = 14
                End With
            Next para
            
            ' 清除底纹
            cell.Shading.BackgroundPatternColor = wdColorAutomatic
            cell.Shading.Texture = wdTextureNone
        Next cell
        
        ' ========== 行高与边距设置 ==========
        With .Rows
            .HeightRule = wdRowHeightAtLeast
            .Height = MillimetersToPoints(7)  ' 最小行高7毫米
            .AllowBreakAcrossPages = True     ' 允许跨页断行
            .LeftIndent = 0
        End With
        
        ' 单元格边距
        .LeftPadding = MillimetersToPoints(2)
        .RightPadding = MillimetersToPoints(2)
        .TopPadding = 0
        .BottomPadding = 0
        
        ' ========== 字体与边框设置 ==========
        With .Range.Font
            .Name = "宋体"
            .Size = 12
            .Bold = False
            .Color = wdColorBlack
        End With
        
        With .Borders
            .InsideLineStyle = wdLineStyleSingle
            .InsideLineWidth = wdLineWidth025pt   ' 0.25磅
            .OutsideLineStyle = wdLineStyleSingle
            .OutsideLineWidth = wdLineWidth025pt  ' 0.25磅
        End With
        
        ' ========== 首行特殊处理 ==========
        With .Rows.First
            .Height = MillimetersToPoints(8)  ' 首行行高8毫米
            .HeadingFormat = True             ' 启用标题行格式（跨页重复）
            .Range.Font.Bold = True
            .Range.ParagraphFormat.Alignment = wdAlignParagraphCenter
            ' 设置首行底纹
            Dim firstCell As cell
            For Each firstCell In .Cells
                firstCell.Shading.BackgroundPatternColor = RGB(215, 215, 215)
            Next firstCell
        End With
    End With
End Function

Sub 表格设为网格()
    '功能：将选中表格或所有表格设为网格型
    On Error Resume Next
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    Dim tbl As Table
    Dim inTable As Boolean
    
    inTable = Selection.Information(wdWithInTable)
    
    If inTable Then
        ' 只处理当前表格
        Call 格式化单个表格(Selection.Tables(1))
    Else
        ' 处理所有表格
        Call 格式化所有表格
    End If
    
    Err.Clear
    On Error GoTo 0
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
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
    On Error Resume Next
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
        .Text = "[.0-9]{4,}"
        .MatchWildcards = True
        
        Do While .Execute
            With .Parent
                If .Start > endPos Then Exit Do
                ' 检查是否有多个小数点
                If InStr(.Text, ".") > 0 Then
                    If Len(.Text) - Len(Replace(.Text, ".", "")) > 1 Then
                        .Start = .End
                        GoTo ContinueLoop
                    End If
                End If
                
                originalLen = Len(.Text)
                .Text = Format(Val(.Text), "#,##0.##")
                endPos = endPos + Len(.Text) - originalLen
                .Start = .End
            End With
ContinueLoop:
        Loop
    End With
    
    ' 恢复年份格式
    ActiveDocument.Content.Find.Execute _
        FindText:="(2),([0-9]{3})年", _
        ReplaceWith:="\1\2年", _
        Replace:=wdReplaceAll, _
        MatchWildcards:=True
    
    Application.ScreenUpdating = True
End Sub

Function 统计字符数(ByVal strParent As String, ByVal strPattern As String) As Integer
    '功能：使用正则统计字符串中匹配的数量
    Dim regEx As Object
    Set regEx = CreateObject("VBScript.RegExp")
    
    regEx.Pattern = strPattern
    regEx.Global = True
    regEx.IgnoreCase = True
    
    统计字符数 = regEx.Execute(strParent).Count
    
    Set regEx = Nothing
End Function

Sub 查找替换(ByVal strFind As String, ByVal strReplace As String, _
    Optional ByVal useWildcards As Boolean = False, _
    Optional ByVal wrapMode As Long = 1)
    '功能：执行查找替换
    ' wrapMode: 0=wdFindStop, 1=wdFindContinue
    
    With ActiveDocument.Content.Find
        .ClearFormatting
        .Replacement.ClearFormatting
        .Text = strFind
        .Replacement.Text = strReplace
        .Forward = True
        .Wrap = wrapMode
        .MatchWildcards = useWildcards
        .MatchCase = False
        .MatchWholeWord = False
        .Execute Replace:=wdReplaceAll
    End With
End Sub

'==============================================================================
' 条目处理
'==============================================================================

Sub 条目加粗()
    '功能：将"第X条"加粗
    Application.ScreenUpdating = False
    
    Dim para As Paragraph
    Dim regEx As Object
    Dim matchResult As Object
    Dim oRange As Range
    Dim m As Long, n As Long
    
    Set regEx = CreateObject("VBScript.RegExp")
    regEx.Pattern = "^第[^条]+条"
    regEx.Global = True
    regEx.IgnoreCase = False
    
    For Each para In ActiveDocument.Paragraphs
        Set matchResult = regEx.Execute(para.Range.Text)
        If matchResult.Count > 0 Then
            m = matchResult(0).FirstIndex
            n = matchResult(0).Length
            Set oRange = ActiveDocument.Range(para.Range.Start + m, para.Range.Start + m + n)
            oRange.Bold = True
        End If
    Next para
    
    Set regEx = Nothing
    Application.ScreenUpdating = True
End Sub
