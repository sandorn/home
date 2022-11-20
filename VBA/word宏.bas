'/***
 ' @Description  :
 ' @Develop      : VSCode
 ' @Author       : Even.Sand
 ' @Contact      : sandorn@163.com
 ' @Date         : 2021-11-03 17:29:14
 ' @FilePath     : /VBA/word宏.bas
 ' @LastEditTime : 2021-11-03 17:35:45
 ' @Github       : https://github.com/sandorn/home
 '***/
Sub 代码简写()
    '功能：全文查找文字A，全部替换为文字B
    '标准：
    ActiveDocument.Content.Find.Execute FindText:="A", ReplaceWith:="B", Replace:=wdReplaceAll
    '简写：
    ActiveDocument.Content.Find.Execute "A", , , , , , , , , "B", 2
    '------------------------------------------------------------------------------------------------
    '功能：全文查找分页符回车符，全部替换为分页符（勾选<使用通配符>，用括号来分组，第1组用\1表示）
    '标准：
    ActiveDocument.Content.Find.Execute FindText:="(^12)^13", MatchWildcards:=True, ReplaceWith:="\1", Replace:=wdReplaceAll
    '简写：
    ActiveDocument.Content.Find.Execute "(^12)^13", , , 1, , , , , , "\1", 2
    '-------------------------------------------------------------------------------------------------------------------------------
    '功能：选定区域尾部向内缩小1字符
    '标准：
    Selection.MoveEnd unit:=wdCharacter, Count:=-1
    '简写：
    Selection.MoveEnd 1, -1
    '------------------------------------------------------
    '功能：选定区域尾部向外扩展1字符
    '标准：
    Selection.MoveEnd unit:=wdCharacter, Count:=1
    '简写：
    Selection.MoveEnd 1, 1
    '简写：
    Selection.MoveEnd
    '------------------------------------------------------
    '功能：选定区域尾部向外扩展1个段落
    '标准：
    Selection.MoveEnd unit:=wdParagraph, Count:=1
    '简写：
    Selection.MoveEnd 4, 1
    '-----------------------------------------------------
    '功能：选定区域头部向内缩小1字符
    '标准：
    Selection.MoveStart unit:=wdCharacter, Count:=1
    '简写：
    Selection.MoveStart 1, 1
    '简写：
    Selection.MoveStart
    '-----------------------------------------------------
    '功能：选定区域头部向外扩展1字符
    '标准：
    Selection.MoveStart unit:=wdCharacter, Count:=-1
    '简写：
    Selection.MoveStart 1, -1
    '------------------------------------------------------
    '功能：选定区域头部向外扩展1个段落
    '标准：
    Selection.MoveStart unit:=wdParagraph, Count:=-1
    '简写：
    Selection.MoveStart 4, -1
    '------------------------------------------------------

    '--------------------------------------------
    '功能：选定<当前选定内容>的下一段
    '标准：
    Selection.Next(unit:=wdParagraph, Count:=1).Select
    '简写：
    Selection.Next(4, 1).Select
    '------------------------------------------------------------
    '功能：选定<当前选定内容>的上一段
    '标准：
    Selection.Previous(unit:=wdParagraph, Count:=1).Select
    '简写：
    Selection.Previous(4, 1).Select
    '------------------------------------------------------------
    '功能：选定<当前选定内容>的下一字符
    '标准：
    Selection.Next(unit:=wdCharacter, Count:=1).Select
    '简写：
    Selection.Next(1, 1).Select
    '简写：
    Selection.Next.Select
    '------------------------------------------------------
    '功能：选定<当前选定内容>的上一字符
    '标准：
    Selection.Previous(unit:=wdCharacter, Count:=1).Select
    '简写：
    Selection.Previous(1, 1).Select
    '简写：
    Selection.Previous.Select
    '------------------------------------------------------
    '功能：将选定区域折叠为选定区域的开头
    '标准：
    Selection.Collapse Direction:=wdCollapseStart
    '简写：
    Selection.Collapse 1
    '简写：
    Selection.Collapse
    '-----------------------------------------------------
    '功能：将选定内容折叠为选定区域的结尾
    '标准：
    Selection.Collapse Direction:=wdCollapseEnd
    '简写：
    Selection.Collapse 0
    '-----------------------------------------------------
    '功能：判断光标是否在表格中！如果在表格中，则……
    '标准：
    If Selection.Information(wdWithInTable) = True Then:
    '简写：
    If Selection.Information(12) Then:
    '------------------------------------------------------------
    '功能：判断光标是否在表格中！如果不在表格中，则……
    '标准:
    If Selection.Information(wdWithInTable) = False Then:
    '简写：
    If Not Selection.Information(12) Then:
    '------------------------------------------------------------
    '功能：判断选定区域是否为文尾，如果不是文尾，则……
    If Not Selection.End = ActiveDocument.Content.End Then:
    '------------------------------------------------------------
    '功能：判断光标所在段落是否为最后一段，如果不是则……
    If Not Selection.Paragraphs(1).Range.Text = ActiveDocument.Paragraphs.Last.Range.Text Then:
    '--------------------------------------------------------------------------------------------------
    '功能：清除格式（必须先选定部分文字或全文）
    Selection.ClearFormatting
    '-------------------------------------------------
    '功能：删除段落首尾空格（必须先选定部分文字或全文）
    CommandBars.FindControl(ID:=122).Execute
    CommandBars.FindControl(ID:=123).Execute
    '-------------------------------------------------
    '功能：取消首行缩进（两行代码顺序不能颠倒！）
    With Selection.ParagraphFormat
        .CharacterUnitFirstLineIndent = 0
        .FirstLineIndent = CentimetersToPoints(0)
    End With
    '--------------------------------------------------
    '功能：删除表格空行（必须保证空行内没有空格才能应用）
    For Each r In .Rows
        If Len(Replace(Replace(r.Range, vbCr, ""), Chr(7), "")) = 0 Then r.Delete
    Next
End Sub
Function MoveToCurrentLineStart()
    ' 移动光标至当前行首
    Selection.HomeKey unit:=wdLine    '简写:Selection.HomeKey 5
End Function
Function MoveToCurrentLineEnd()
    ' 移动光标至当前行尾
    Selection.EndKey unit:=wdLine    '简写：Selection.EndKey 5
End Function
Function SelectToCurrentLineStart()
    ' 选择从光标至当前行首的内容
    Selection.HomeKey unit:=wdLine, Extend:=wdExtend  '简写：Selection.HomeKey 5, 1
End Function
Function SelectToCurrentLineEnd()
    ' 选择从光标至当前行尾的内容
    Selection.EndKey unit:=wdLine, Extend:=wdExtend  '简写：Selection.EndKey 5, 1
End Function
Function SelectCurrentLine()
    ' 选择当前行
    Selection.HomeKey unit:=wdLine   '简写:Selection.HomeKey 5
    Selection.EndKey unit:=wdLine, Extend:=wdExtend   '简写：Selection.EndKey 5, 1
End Function
Function MoveToDocStart()
    ' 移动光标至文档开始
    Selection.HomeKey unit:=wdStory  '简写：Selection.HomeKey 6
End Function
Function MoveToDocEnd()
    ' 移动光标至文档结尾
    Selection.EndKey unit:=wdStory   '简写：Selection.EndKey 6
End Function
Function SelectToDocStart()
    ' 选定区域向上扩展至文首
    Selection.HomeKey unit:=wdStory, Extend:=wdExtend  '简写：Selection.HomeKey 6, 1
End Function
Function SelectToDocEnd()
    ' 选择从光标至文档结尾的内容
    Selection.EndKey unit:=wdStory, Extend:=wdExtend  '简写：Selection.EndKey 6, 1
End Function
Function SelectDocAll()
    ' 选择文档全部内容
    Selection.WholeStory    '或：ActiveDocument.Select
End Function
Function MoveToCurrentParagraphStart()
    ' 移动光标至当前段落的开始
    Selection.MoveUp unit:=wdParagraph
End Function
Function MoveToCurrentParagraphEnd()
    ' 移动光标至当前段落的结尾
    Selection.MoveDown unit:=wdParagraph
End Function
Function SelectToCurrentParagraphStart()
    ' 选择从光标至当前段落开始的内容
    Selection.MoveUp unit:=wdParagraph, Extend:=wdExtend
End Function
Function SelectToCurrentParagraphEnd()
    ' 选择从光标至当前段落结尾的内容
    Selection.MoveDown unit:=wdParagraph, Extend:=wdExtend
End Function
Function SelectCurrentParagraph()
    ' 选择光标所在段落的内容
    Selection.MoveUp unit:=wdParagraph
    Selection.MoveDown unit:=wdParagraph, Extend:=wdExtend
    '标准：    Selection.Paragraphs(1).Range.Select
    '标准2：   Selection.Expand Unit:=wdParagraph
    '简写：    Selection.Expand 4
End Function
Function DeleteHyperlinks()
    '删除链接
    Dim idx%, a%
    a = ActiveDocument.Hyperlinks.Count
    For idx = 1 To ActiveDocument.Hyperlinks.Count
        ActiveDocument.Hyperlinks(1).Delete
    Next
    MsgBox a & "-->" & ActiveDocument.Hyperlinks.Count
End Function
Function FieUnlink()
    '删除域代码
    Dim a%, Fie As Field
    a = ActiveDocument.Fields.Count
    For Each Fie In ActiveDocument.Fields
        Fie.Unlink
    Next
    MsgBox a & "-->" & ActiveDocument.Fields.Count
End Function
Function FindReplaceChar(ByVal strFind$, ByVal strReplace$, _
        Optional ByVal bWild As Boolean = False, _
        Optional ByVal sBold As Boolean = False, _
        Optional ByVal sRstyle$ = "None", _
        Optional ByVal FindWrap% = wdFindStop, _
        Optional ByVal bByte As Boolean = False, _
        Optional ByVal nReplace% = wdReplaceAll)
    '执行查找替换操作
    With Selection.Find
        .ClearFormatting
        .Text = strFind
        .Forward = True
        .MatchWildcards = bWild '使用通配符复选框
        .Wrap = FindWrap 'wdFindStop:停止,替换选定部分,若没选中则替换至文档末尾
        'wdFindContinue:到达文档末尾时，继续从文档开头进行搜索
        .MatchByte = bByte '不区分全角和半角字符
        .Format = True
        .MatchCase = False
        .MatchWholeWord = False
        .CorrectHangulEndings = False
        .MatchSoundsLike = False
        .MatchAllWordForms = False
        With .Replacement
            .ClearFormatting
            .Text = strReplace  '替换结果
            If sRstyle <> "None" Then .Style = ActiveDocument.Styles(sRstyle)
            If sBold Then .Font.Bold = True  '加粗
        End With
        .Execute Replace:=nReplace
    End With
    ActiveDocument.Activate
End Function
Function 替换字符串(ByVal strFind$, ByVal strReplace$, _
        Optional ByVal bWild As Boolean = False, _
        Optional ByVal FindWrap% = wdFindContinue, _
        Optional ByVal bByte As Boolean = False, _
        Optional ByVal nReplace% = wdReplaceAll)
    '执行查找替换操作
    With Selection.Find
        .ClearFormatting
        .Text = strFind
        .Forward = True
        .MatchWildcards = bWild '使用通配符复选框
        .Wrap = FindWrap 'wdFindStop:停止,替换选定部分,若没选中则替换至文档末尾
        'wdFindContinue:到达文档末尾时，继续从文档开头进行搜索
        .MatchByte = bByte '不区分全角和半角字符
        .Format = True
        .MatchCase = False
        .MatchWholeWord = False
        .CorrectHangulEndings = False
        .MatchSoundsLike = False
        .MatchAllWordForms = False
        With .Replacement
            .ClearFormatting
            .Text = strReplace  '替换结果
        End With
        .Execute Replace:=nReplace
    End With
    ActiveDocument.Activate
End Function
Sub 条目加粗()
    Application.ScreenUpdating = False
    Dim i As Paragraph, mt, oRang As Range, n%, m%

    With CreateObject("vbscript.regexp")
        .Pattern = "^第[^条]+条"
        .Global = True: .IgnoreCase = False: .MultiLine = True
        For Each i In ActiveDocument.Paragraphs
            For Each mt In .Execute(i.Range.Text)
                m = mt.FirstIndex: n = mt.length
                Set oRang = ActiveDocument.Range _
                    (i.Range.Start + m, i.Range.Start + m + n)
                oRang.Bold = True
            Next
        Next
    End With

    Application.ScreenUpdating = True
End Sub
Sub 删空行()
    ' 删除空行(空格 全角空格以及tab缩进)
    On Error Resume Next
    Application.ScreenUpdating = False    '关闭屏幕更新,加快程序运行
    Dim myRange As Range, Para As Paragraph

    If Selection.Type = wdSelectionIP Then  'Selection.Start = Selection.End
        End_selection = ActiveDocument.Content.End
        Set myRange = ActiveDocument.Content '定义为主文档文字部分
    Else '有选择区
        End_selection = Selection.Range.End
        Set myRange = Selection.Range '定义为选中文字部分
    End If

    For Each Para In myRange.Paragraphs
        '查找去掉（vbTab 空格 全角空格）后，只剩下段落标记的段落
        If Len(Para.Range.Text) - CountStr(Para.Range.Text, "[\n\t 　]") = 1 Then Para.Range.Delete
    Next

    Application.ScreenUpdating = True
End Sub
Sub 删除个人信息()
    ActiveDocument.RemoveDocumentInformation (wdRDIDocumentProperties)
End Sub
Sub 转换为静态编号2()
    Selection.WholeStory
    Selection.Cut
    Selection.PasteAndFormat (wdFormatPlainText)
    Call 替换字符串(vbTab, " ")
End Sub
Sub 转换为静态编号()
    Dim myRange As Range
    If Selection.Type = wdSelectionIP Then  'Selection.Start = Selection.End
        Set myRange = ActiveDocument.Content '定义为主文档文字部分
    Else '有选择区
        Set myRange = Selection.Range '定义为选中文字部分
    End If

    myRange.ListFormat.ConvertNumbersToText
    myRange.Find.Execute FindText:="^t", ReplaceWith:=" ", Replace:=wdReplaceAll
End Sub
Sub 转换为自动编号()
    '将全文逐段设置格式为"正文GB"，并修改章节条的格式
    Application.ScreenUpdating = False
    'If ActiveDocument.Fields.Count <> 0 Then Call FieUnlink '去除域代码
    Call 公文样式
    Dim regEx As New RegExp '构建正则
    regEx.IgnoreCase = True: regEx.Global = False: regEx.MultiLine = False
    Dim idx
    For Each idx In ActiveDocument.Paragraphs '按段落循环
        If Not idx.Range.Information(wdWithInTable) Then '判断非表格内
            'idx.Range.Style = ActiveDocument.Styles("正文") '样式名称
            regEx.Pattern = "( :^[　 ]*)(第[零〇一二三四五六七八九十百\d]+条)( :[　 ]*)([^　 ][^\r]*)"
            Dim Index$, Subject$, m%, n%, oRang As Range
            If regEx.Test(idx.Range) Then
                Index = regEx.Execute(idx.Range)(0).SubMatches(0) '序号
                Subject = Replace(Replace(regEx.Execute(idx.Range)(0).SubMatches(1), "　", ""), " ", "")  '标题去掉空格
                m = regEx.Execute(idx.Range)(0).FirstIndex: n = regEx.Execute(idx.Range)(0).length
                Set oRang = ActiveDocument.Range(idx.Range.Start + m, idx.Range.Start + m + n)
                oRang.Text = Subject
                oRang.Style = ActiveDocument.Styles("条目自动") '样式名称
            End If
            Index = "": Subject = "": m = 0: n = 0: Set oRang = Nothing
        End If '判断非表格内
    Next '按段落循环
    Application.ScreenUpdating = True
End Sub
Sub 自动设置公文格式()
    '将全文逐段设置格式为"GB2312"，并修改章节条的格式
    Application.ScreenUpdating = False
    Dim t: t = Timer
    If ActiveDocument.Fields.Count <> 0 Then Call FieUnlink '去除域代码
    Dim regEx As New RegExp '构建正则
    regEx.IgnoreCase = True: regEx.Global = False: regEx.MultiLine = False
    Dim idx
    For Each idx In ActiveDocument.Paragraphs '按段落循环
        If Not idx.Range.Information(wdWithInTable) Then '判断非表格内
            idx.Range.Style = ActiveDocument.Styles("正文") '样式名称
            Dim patt, mStyle, bSp, bArticle
            patt = Array("( :^[　 ]*)(第[零〇一二三四五六七八九十百\d]+条)( :[　 ]*)([^　 ][^\r]*)", _
                "( :^[　 ]*)(第[零〇一二三四五六七八九十百\d]+章)( :[　 ]*)([^　 ][^\r]*)", _
                "( :^[　 ]*)(第[零〇一二三四五六七八九十百\d]+节)( :[　 ]*)([^　 ][^\r]*)")
            mStyle = Array("正文", "标题 1", "标题 2")
            bSp = Array(True, True, True)
            bArticle = Array(True, False, False)
            Dim i%
            For i = 0 To UBound(patt)
                regEx.Pattern = patt(i)
                Dim Index$, Subject$, m%, n%, oRang As Range
                If regEx.Test(idx.Range) Then
                    Index = regEx.Execute(idx.Range)(0).SubMatches(0) '序号
                    Subject = IIf(bSp(i), Replace(Replace(regEx.Execute(idx.Range)(0).SubMatches(1), "　", ""), " ", ""), regEx.Execute(idx.Range)(0).SubMatches(1)) '标题是否去掉空格
                    m = regEx.Execute(idx.Range)(0).FirstIndex: n = regEx.Execute(idx.Range)(0).length
                    Set oRang = ActiveDocument.Range(idx.Range.Start + m, idx.Range.Start + m + n)
                    oRang.Text = Index & "　" & Subject
                    oRang.Style = ActiveDocument.Styles(mStyle(i)) '样式名称
                    If bArticle(i) Then
                        Set oRang = ActiveDocument.Range(oRang.Start, oRang.Start + Len(Index))
                        oRang.Font.Bold = True
                    End If
                End If
                Index = "": Subject = "": m = 0: n = 0: Set oRang = Nothing
            Next i
        End If  '表格判断
    Next '按段落循环

    Call 替换字符串("条　", "条 ")
    MoveToDocStart '光标移动到文档最前端
    Selection.Style = myStyle
    Call 删除个人信息
    Application.ScreenUpdating = True
    ActiveDocument.Activate
    'MsgBox (Timer - t) * 1000
End Sub
Function CountStr(ByVal strParent As String, _
        ByVal strChild As String) As Integer
    '以正则方式，统计字符串中子字符串的数量
    Dim re As New RegExp: Dim matches As MatchCollection

    re.Pattern = strChild
    re.Global = True
    re.IgnoreCase = True
    Set matches = re.Execute(strParent)

    CountStr = matches.Count
    Set re = Nothing
End Function
Sub 千分位()
    '78085842(凯文)&1838095599(春天)@QQ群257182022（Word & VBA）
    On Error Resume Next
    Application.ScreenUpdating = False    '关闭屏幕更新,加快程序运行
    Dim Rng As Range, length%, End_selection&

    If Selection.Type = wdSelectionIP Then  'Selection.Start = Selection.End
        End_selection = ActiveDocument.Content.End
        Set Rng = ActiveDocument.Content '定义为主文档文字部分
    Else '有选择区
        End_selection = Selection.Range.End
        Set Rng = Selection.Range '定义为选中文字部分
    End If

    With Rng.Find
        .ClearFormatting
        .Text = "[.0-9]{4,}"    '查找数字
        .MatchWildcards = True

        Do While .Execute
            With .Parent
                If .Start > End_selection Then Exit Do
                If CountStr(.Text, "[\.]") > 1 Then Exit Do '数值有一个以上的小数点，则跳过
                length = Len(.Text)
                .Text = VBA.Format(VBA.Val(.Text), "Standard") '转为千分位格式
                End_selection = End_selection + Len(.Text) - length
                .Start = .End
            End With
        Loop

    End With
    '有些问题，会把年份都更改了 将修改的年份恢复（全文）
    ActiveDocument.Content.Find.Execute FindText:="(2),([0-9]{3}).00年", ReplaceWith:="\1\2年", Replace:=wdReplaceAll, MatchWildcards:=True
    Application.ScreenUpdating = True '恢复屏幕更新
End Sub
Sub 正则4千分位()
    On Error Resume Next
    ' Application.ScreenUpdating = False    '关闭屏幕更新,加快程序运行
    Dim myRange As Range, mt As Match, oRang As Range, n%, m%

    If Selection.Type = wdSelectionIP Then  'Selection.Start = Selection.End
        Set myRange = ActiveDocument.Content '定义为主文档文字部分
    Else '有选择区
        Set myRange = Selection.Range '定义为选中文字部分
    End If

    With CreateObject("vbscript.regexp")
        .Pattern = "[0-9\.]+"  '正则表达式有些问题
        .Global = True: .IgnoreCase = False: .MultiLine = True
        For Each mt In .Execute(myRange.Text)
            'MsgBox mt
            m = mt.FirstIndex: n = mt.length
            Set oRang = ActiveDocument.Range(myRange.Start + m, myRange.Start + m + n)
            oRang.Text = VBA.Format(oRang.Text, "Standard") '修改格式
        Next
    End With
End Sub
Sub Title2345Style()
    '避免激活对象！/提速成功！/完成时间=.046秒！(极速)/2018-12-31/定稿！
    Dim i As Paragraph, s$, n&
    s = "一二三四五六七八九十1234567890百零〇○"
    For Each i In ActiveDocument.Paragraphs
        With i.Range
            If Not .Information(12) Then
                n = 1
                If .Text Like "（*" Then n = 2
                Do While InStr(s, .Characters(n)) > 0
                    n = n + 1
                    If .Characters(n).Text = " " Then .Style = wdStyleHeading2: Exit Do
                    If .Characters(n).Text = "）" And Not .Text Like "（#*" Then .Style = wdStyleHeading3: Exit Do
                    If .Characters(n).Text = "．" Then .Style = wdStyleHeading4: Exit Do
                    If .Characters(n).Text = "）" And .Text Like "（#*" Then .Style = wdStyleHeading5: Exit Do
                Loop
            End If
        End With
    Next
End Sub
Sub 表格设为美观()
    '功能：光标在表格中处理当前表格；否则处理所有表格！
    Application.ScreenUpdating = False  '关闭屏幕刷新
    Application.DisplayAlerts = False  '关闭提示
    On Error Resume Next  '忽略错误
    '***************************************************************************
    Dim mytable As Table, i As Long
    If Selection.Information(wdWithInTable) = True Then i = 1
    For Each mytable In ActiveDocument.Tables
        If i = 1 Then Set mytable = Selection.Tables(1)

        'Options.DefaultHighlightColorIndex = wdNoHighlight '去除高亮

        With mytable
            '取消底色
            .Style = "表格主题"
            .Shading.ForegroundPatternColor = wdColorAutomatic
            .Shading.BackgroundPatternColor = wdColorAutomatic
            .Shading.Texture = wdTextureNone '无底纹
            .Range.HighlightColorIndex = wdNoHighlight '去除高亮



            '单元格边距
            .TopPadding = PixelsToPoints(0, True) '设置上边距为0  'CentimetersToPoints(0)
            .BottomPadding = PixelsToPoints(0, True) '设置下边距为0
            .LeftPadding = PixelsToPoints(0, True)  '设置左边距为0
            .RightPadding = PixelsToPoints(0, True) '设置右边距为0
            .Spacing = PixelsToPoints(0, True) '允许单元格间距为0
            .AllowPageBreaks = True '允许断页
            '.AllowAutoFit = True '允许自动重调尺寸

            '设置边框
            .Borders(wdBorderLeft).LineStyle = wdLineStyleNone
            .Borders(wdBorderRight).LineStyle = wdLineStyleNone
            .Borders(wdBorderTop).LineStyle = wdLineStyleThinThickMedGap
            .Borders(wdBorderTop).LineWidth = wdLineWidth225pt
            .Borders(wdBorderBottom).LineStyle = wdLineStyleThickThinMedGap
            .Borders(wdBorderBottom).LineWidth = wdLineWidth225pt

            With .Rows
                .Alignment = wdAlignRowCenter '表水平居中  wdAlignRowLeft '左对齐
                .WrapAroundText = False '取消文字环绕
                .AllowBreakAcrossPages = False '不允许行断页
                .HeadingFormat = True '设置标题行
                .HeightRule = wdRowHeightExactly '行高设为最小值   wdRowHeightAuto '行高设为自动
                .Height = CentimetersToPoints(0) '上面缩进量为0
                .LeftIndent = CentimetersToPoints(0) '左面缩进量为0
            End With

            With .Range
                With .ParagraphFormat '段落格式
                    .LeftIndent = CentimetersToPoints(0)
                    .RightIndent = CentimetersToPoints(0)
                    .SpaceBefore = 0
                    .SpaceBeforeAuto = False
                    .SpaceAfter = 0
                    .SpaceAfterAuto = False
                    .LineSpacingRule = wdLineSpaceSingle '单倍行距
                    .Alignment = wdAlignParagraphCenter '单元格水平居中
                    .WidowControl = False
                    .KeepWithNext = False
                    .KeepTogether = False
                    .PageBreakBefore = False
                    .NoLineNumber = False
                    .Hyphenation = True
                    .FirstLineIndent = CentimetersToPoints(0) '取消首行缩进
                    .OutlineLevel = wdOutlineLevelBodyText
                    .CharacterUnitLeftIndent = 0
                    .CharacterUnitRightIndent = 0
                    .CharacterUnitFirstLineIndent = 0 '取消首行缩进
                    .LineUnitBefore = 0
                    .LineUnitAfter = 0
                    .MirrorIndents = False
                    .TextboxTightWrap = wdTightNone
                    .CollapsedByDefault = False
                    .AutoAdjustRightIndent = False
                    .DisableLineHeightGrid = True
                    .FarEastLineBreakControl = True
                    .WordWrap = True
                    .HangingPunctuation = True
                    .HalfWidthPunctuationOnTopOfLine = False
                    .AddSpaceBetweenFarEastAndAlpha = True
                    .AddSpaceBetweenFarEastAndDigit = True
                    .BaseLineAlignment = wdBaselineAlignAuto
                End With
                With .Font '字体格式
                    .Name = "仿宋"
                    .Name = "仿宋"
                    .Size = 12
                    .Bold = False
                    '.DisableCharacterSpaceGrid = True
                End With

                .Cells.VerticalAlignment = wdCellAlignVerticalCenter  '单元格垂直居中

            End With

            '设置首行格式
            With .Rows.First.Range ' 操作第一行  'row(1).range
                .Font.Bold = True
                .Shading.BackgroundPatternColor = -603923969 '首行底纹填充--浅灰色
            End With

            '自动调整表格
            .Columns.PreferredWidthType = wdPreferredWidthAuto
            .AutoFitBehavior (wdAutoFitContent) '根据内容调整表格
            .AutoFitBehavior (wdAutoFitWindow) '根据窗口调整表格

        End With

        If i = 1 Then Exit For
    Next
    '***************************************************************************
    Err.Clear: On Error GoTo 0 '恢复错误捕捉
    Application.DisplayAlerts = True  '开启提示
    Application.ScreenUpdating = True   '开启屏幕刷新
End Sub
Sub 表格设为网格()
    '功能：光标在表格中处理当前表格；否则处理所有表格！
    Application.ScreenUpdating = False  '关闭屏幕刷新
    Application.DisplayAlerts = False  '关闭提示
    On Error Resume Next  '忽略错误
    '***************************************************************************
    Dim mytable As Table, i As Long
    If Selection.Information(wdWithInTable) = True Then i = 1
    For Each mytable In ActiveDocument.Tables
        If i = 1 Then Set mytable = Selection.Tables(1)

        With mytable
            '取消底色
            .Style = "网格型"
            .Shading.ForegroundPatternColor = wdColorAutomatic
            .Shading.BackgroundPatternColor = wdColorAutomatic
            .Shading.Texture = wdTextureNone '无底纹
            .Range.HighlightColorIndex = wdNoHighlight '去除高亮

            '单元格边距
            .TopPadding = PixelsToPoints(0, True) '设置上边距为0
            .BottomPadding = PixelsToPoints(0, True) '设置下边距为0
            .LeftPadding = PixelsToPoints(0, True)  '设置左边距为0
            .RightPadding = PixelsToPoints(0, True) '设置右边距为0
            .Spacing = PixelsToPoints(0, True) '允许单元格间距为0
            .AllowPageBreaks = True '允许断页
            '.AllowAutoFit = True '允许自动重调尺寸

            With .Rows
                .Alignment = wdAlignRowCenter '表水平居中
                .WrapAroundText = False '取消文字环绕
                .AllowBreakAcrossPages = False '不允许行断页
                .HeadingFormat = True '设置标题行
                .HeightRule = wdRowHeightExactly '行高设为最小值
                .Height = CentimetersToPoints(0) '上面缩进量为0
                .LeftIndent = CentimetersToPoints(0) '左面缩进量为0
            End With

            With .Range
                With .ParagraphFormat '段落格式
                    .LeftIndent = CentimetersToPoints(0)
                    .RightIndent = CentimetersToPoints(0)
                    .SpaceBefore = 0
                    .SpaceBeforeAuto = False
                    .SpaceAfter = 0
                    .SpaceAfterAuto = False
                    .LineSpacingRule = wdLineSpaceSingle
                    .Alignment = wdAlignParagraphCenter '单元格水平居中
                    .WidowControl = False
                    .KeepWithNext = False
                    .KeepTogether = False
                    .PageBreakBefore = False
                    .NoLineNumber = False
                    .Hyphenation = True
                    .FirstLineIndent = CentimetersToPoints(0) '取消首行缩进
                    .OutlineLevel = wdOutlineLevelBodyText
                    .CharacterUnitLeftIndent = 0
                    .CharacterUnitRightIndent = 0
                    .CharacterUnitFirstLineIndent = 0 '取消首行缩进
                    .LineUnitBefore = 0
                    .LineUnitAfter = 0
                    .MirrorIndents = False
                    .TextboxTightWrap = wdTightNone
                    .CollapsedByDefault = False
                    .AutoAdjustRightIndent = False
                    .DisableLineHeightGrid = True
                    .FarEastLineBreakControl = True
                    .WordWrap = True
                    .HangingPunctuation = True
                    .HalfWidthPunctuationOnTopOfLine = False
                    .AddSpaceBetweenFarEastAndAlpha = True
                    .AddSpaceBetweenFarEastAndDigit = True
                    .BaseLineAlignment = wdBaselineAlignAuto
                End With
                With .Font '字体格式
                    .Name = "仿宋"
                    .Name = "仿宋"
                    .Size = 12
                    .Bold = False
                End With

                .Cells.VerticalAlignment = wdCellAlignVerticalCenter  '单元格垂直居中

            End With

            '设置首行格式
            With .Rows.First.Range ' 指定第一行
                .Font.Bold = True
            End With

            '自动调整表格
            .Columns.PreferredWidthType = wdPreferredWidthAuto
            .AutoFitBehavior (wdAutoFitContent) '根据内容调整表格
            .AutoFitBehavior (wdAutoFitWindow) '根据窗口调整表格

        End With

        If i = 1 Then Exit For
    Next
    '***************************************************************************
    Err.Clear: On Error GoTo 0 '恢复错误捕捉
    Application.DisplayAlerts = True  '开启提示
    Application.ScreenUpdating = True   '开启屏幕刷新
End Sub
Function 调整标题样式()
    'Set myStyle = ActiveDocument.Styles.Add(Name:="标题", Type:=wdStyleTypeParagraph)
    Set myStyle = ActiveDocument.Styles("标题")
    With myStyle
        .AutomaticallyUpdate = True
        .BaseStyle = "正文"
        .NextParagraphStyle = "正文"
    End With

    With myStyle.Font
        .NameFarEast = "方正小标宋简体"
        .NameAscii = "方正小标宋简体"
        .NameOther = "宋体"
        .Name = "方正小标宋简体"
        .Size = 22
        .Bold = False
        .Italic = False
        .Underline = wdUnderlineNone
        .UnderlineColor = wdColorAutomatic
        .StrikeThrough = False
        .DoubleStrikeThrough = False
        .Outline = False
        .Emboss = False
        .Shadow = False
        .Hidden = False
        .SmallCaps = False
        .AllCaps = False
        .Color = wdColorAutomatic
        .Engrave = False
        .Superscript = False
        .Subscript = False
        .Scaling = 100
        .Kerning = 二号
        .Animation = wdAnimationNone
        .DisableCharacterSpaceGrid = False
        .EmphasisMark = wdEmphasisMarkNone
        .Ligatures = wdLigaturesNone
        .NumberSpacing = wdNumberSpacingDefault
        .NumberForm = wdNumberFormDefault
        .StylisticSet = wdStylisticSetDefault
        .ContextualAlternates = 0
    End With

    With myStyle.ParagraphFormat
        .LeftIndent = CentimetersToPoints(0)
        .RightIndent = CentimetersToPoints(0)
        .SpaceBefore = 0
        .SpaceBeforeAuto = False
        .SpaceAfter = 0
        .SpaceAfterAuto = False
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphCenter
        .WidowControl = False
        .KeepWithNext = False
        .KeepTogether = False
        .PageBreakBefore = True
        .NoLineNumber = False
        .Hyphenation = True
        .FirstLineIndent = CentimetersToPoints(0)
        .OutlineLevel = wdOutlineLevel1
        .CharacterUnitLeftIndent = 0
        .CharacterUnitRightIndent = 0
        .CharacterUnitFirstLineIndent = 0
        .LineUnitBefore = 0
        .LineUnitAfter = 0
        .MirrorIndents = False
        .TextboxTightWrap = wdTightNone
        .CollapsedByDefault = False
        .AutoAdjustRightIndent = True
        .DisableLineHeightGrid = False
        .FarEastLineBreakControl = True
        .WordWrap = True
        .HangingPunctuation = True
        .HalfWidthPunctuationOnTopOfLine = False
        .AddSpaceBetweenFarEastAndAlpha = True
        .AddSpaceBetweenFarEastAndDigit = True
        .BaseLineAlignment = wdBaselineAlignAuto
    End With

    myStyle.NoSpaceBetweenParagraphsOfSameStyle = False
    myStyle.ParagraphFormat.TabStops.ClearAll

    With myStyle.ParagraphFormat
        With .Shading
            .Texture = wdTextureNone
            .ForegroundPatternColor = wdColorAutomatic
            .BackgroundPatternColor = wdColorAutomatic
        End With
        .Borders(wdBorderLeft).LineStyle = wdLineStyleNone
        .Borders(wdBorderRight).LineStyle = wdLineStyleNone
        .Borders(wdBorderTop).LineStyle = wdLineStyleNone
        .Borders(wdBorderBottom).LineStyle = wdLineStyleNone
        With .Borders
            .DistanceFromTop = 1
            .DistanceFromLeft = 4
            .DistanceFromBottom = 1
            .DistanceFromRight = 4
            .Shadow = False
        End With
    End With

    myStyle.LanguageID = wdSimplifiedChinese
    myStyle.NoProofing = False
    myStyle.Frame.Delete

End Function
Function 调整标题1样式()
    Set myStyle = ActiveDocument.Styles("标题 1")

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
        .Italic = False
        .Underline = wdUnderlineNone
        .UnderlineColor = wdColorAutomatic
        .StrikeThrough = False
        .DoubleStrikeThrough = False
        .Outline = False
        .Emboss = False
        .Shadow = False
        .Hidden = False
        .SmallCaps = False
        .AllCaps = False
        .Color = wdColorAutomatic
        .Engrave = False
        .Superscript = False
        .Subscript = False
        .Scaling = 100
        .Kerning = 1
        .Animation = wdAnimationNone
        .DisableCharacterSpaceGrid = False
        .EmphasisMark = wdEmphasisMarkNone
        .Ligatures = wdLigaturesNone
        .NumberSpacing = wdNumberSpacingDefault
        .NumberForm = wdNumberFormDefault
        .StylisticSet = wdStylisticSetDefault
        .ContextualAlternates = 0
    End With
    With myStyle.ParagraphFormat
        .LeftIndent = CentimetersToPoints(0)
        .RightIndent = CentimetersToPoints(0)
        .SpaceBefore = 0
        .SpaceBeforeAuto = False
        .SpaceAfter = 0
        .SpaceAfterAuto = False
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphJustify
        .WidowControl = True
        .KeepWithNext = True
        .KeepTogether = True
        .PageBreakBefore = False
        .NoLineNumber = False
        .Hyphenation = True
        .FirstLineIndent = CentimetersToPoints(0.35)
        .OutlineLevel = wdOutlineLevel2
        .CharacterUnitLeftIndent = 0
        .CharacterUnitRightIndent = 0
        .CharacterUnitFirstLineIndent = 2
        .LineUnitBefore = 0
        .LineUnitAfter = 0
        .MirrorIndents = False
        .TextboxTightWrap = wdTightNone
        .CollapsedByDefault = False
        .AutoAdjustRightIndent = True
        .DisableLineHeightGrid = False
        .FarEastLineBreakControl = True
        .WordWrap = True
        .HangingPunctuation = True
        .HalfWidthPunctuationOnTopOfLine = False
        .AddSpaceBetweenFarEastAndAlpha = True
        .AddSpaceBetweenFarEastAndDigit = True
        .BaseLineAlignment = wdBaselineAlignAuto
    End With
    myStyle.NoSpaceBetweenParagraphsOfSameStyle = False
    myStyle.ParagraphFormat.TabStops.ClearAll

    With myStyle.ParagraphFormat
        With .Shading
            .Texture = wdTextureNone
            .ForegroundPatternColor = wdColorAutomatic
            .BackgroundPatternColor = wdColorAutomatic
        End With
        .Borders(wdBorderLeft).LineStyle = wdLineStyleNone
        .Borders(wdBorderRight).LineStyle = wdLineStyleNone
        .Borders(wdBorderTop).LineStyle = wdLineStyleNone
        .Borders(wdBorderBottom).LineStyle = wdLineStyleNone
        With .Borders
            .DistanceFromTop = 1
            .DistanceFromLeft = 4
            .DistanceFromBottom = 1
            .DistanceFromRight = 4
            .Shadow = False
        End With
    End With

    myStyle.LanguageID = wdSimplifiedChinese
    myStyle.NoProofing = False
    myStyle.Frame.Delete

End Function
Function 调整标题2样式()
    Set myStyle = ActiveDocument.Styles("标题 2")

    With myStyle
        .AutomaticallyUpdate = True
        .BaseStyle = "正文"
        .NextParagraphStyle = "正文"
    End With

    With myStyle.Font
        .NameFarEast = "楷体"   '"楷体_GB2312"
        .NameAscii = "楷体"
        .NameOther = "楷体"
        .Name = "楷体"
        .Size = 16
        .Bold = False
        .Italic = False
        .Underline = wdUnderlineNone
        .UnderlineColor = wdColorAutomatic
        .StrikeThrough = False
        .DoubleStrikeThrough = False
        .Outline = False
        .Emboss = False
        .Shadow = False
        .Hidden = False
        .SmallCaps = False
        .AllCaps = False
        .Color = wdColorAutomatic
        .Engrave = False
        .Superscript = False
        .Subscript = False
        .Scaling = 100
        .Kerning = 1
        .Animation = wdAnimationNone
        .DisableCharacterSpaceGrid = False
        .EmphasisMark = wdEmphasisMarkNone
        .Ligatures = wdLigaturesNone
        .NumberSpacing = wdNumberSpacingDefault
        .NumberForm = wdNumberFormDefault
        .StylisticSet = wdStylisticSetDefault
        .ContextualAlternates = 0
    End With
    With myStyle.ParagraphFormat
        .LeftIndent = CentimetersToPoints(0)
        .RightIndent = CentimetersToPoints(0)
        .SpaceBefore = 0
        .SpaceBeforeAuto = False
        .SpaceAfter = 0
        .SpaceAfterAuto = False
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphJustify
        .WidowControl = True
        .KeepWithNext = True
        .KeepTogether = True
        .PageBreakBefore = False
        .NoLineNumber = False
        .Hyphenation = True
        .FirstLineIndent = CentimetersToPoints(0.35)
        .OutlineLevel = wdOutlineLevel3
        .CharacterUnitLeftIndent = 0
        .CharacterUnitRightIndent = 0
        .CharacterUnitFirstLineIndent = 2
        .LineUnitBefore = 0
        .LineUnitAfter = 0
        .MirrorIndents = False
        .TextboxTightWrap = wdTightNone
        .CollapsedByDefault = False
        .AutoAdjustRightIndent = True
        .DisableLineHeightGrid = False
        .FarEastLineBreakControl = True
        .WordWrap = True
        .HangingPunctuation = True
        .HalfWidthPunctuationOnTopOfLine = False
        .AddSpaceBetweenFarEastAndAlpha = True
        .AddSpaceBetweenFarEastAndDigit = True
        .BaseLineAlignment = wdBaselineAlignAuto
    End With
    myStyle.NoSpaceBetweenParagraphsOfSameStyle = False
    myStyle.ParagraphFormat.TabStops.ClearAll

    With myStyle.ParagraphFormat
        With .Shading
            .Texture = wdTextureNone
            .ForegroundPatternColor = wdColorAutomatic
            .BackgroundPatternColor = wdColorAutomatic
        End With
        .Borders(wdBorderLeft).LineStyle = wdLineStyleNone
        .Borders(wdBorderRight).LineStyle = wdLineStyleNone
        .Borders(wdBorderTop).LineStyle = wdLineStyleNone
        .Borders(wdBorderBottom).LineStyle = wdLineStyleNone
        With .Borders
            .DistanceFromTop = 1
            .DistanceFromLeft = 4
            .DistanceFromBottom = 1
            .DistanceFromRight = 4
            .Shadow = False
        End With
    End With

    myStyle.LanguageID = wdSimplifiedChinese
    myStyle.NoProofing = False
    myStyle.Frame.Delete

End Function
Function 调整标题3样式()
    Set myStyle = ActiveDocument.Styles("标题 3")

    With myStyle
        .AutomaticallyUpdate = True
        .BaseStyle = "正文"
        .NextParagraphStyle = "正文"
    End With

    With myStyle.Font
        .NameFarEast = "仿宋"  '"仿宋_GB2312"
        .NameAscii = "仿宋"
        .NameOther = "仿宋"
        .Name = "仿宋"
        .Size = 16
        .Bold = False
        .Italic = False
        .Underline = wdUnderlineNone
        .UnderlineColor = wdColorAutomatic
        .StrikeThrough = False
        .DoubleStrikeThrough = False
        .Outline = False
        .Emboss = False
        .Shadow = False
        .Hidden = False
        .SmallCaps = False
        .AllCaps = False
        .Color = wdColorAutomatic
        .Engrave = False
        .Superscript = False
        .Subscript = False
        .Scaling = 100
        .Kerning = 1
        .Animation = wdAnimationNone
        .DisableCharacterSpaceGrid = False
        .EmphasisMark = wdEmphasisMarkNone
        .Ligatures = wdLigaturesNone
        .NumberSpacing = wdNumberSpacingDefault
        .NumberForm = wdNumberFormDefault
        .StylisticSet = wdStylisticSetDefault
        .ContextualAlternates = 0
    End With
    With myStyle.ParagraphFormat
        .LeftIndent = CentimetersToPoints(0)
        .RightIndent = CentimetersToPoints(0)
        .SpaceBefore = 0
        .SpaceBeforeAuto = False
        .SpaceAfter = 0
        .SpaceAfterAuto = False
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphJustify
        .WidowControl = True
        .KeepWithNext = True
        .KeepTogether = True
        .PageBreakBefore = False
        .NoLineNumber = False
        .Hyphenation = True
        .FirstLineIndent = CentimetersToPoints(0.35)
        .OutlineLevel = wdOutlineLevel4
        .CharacterUnitLeftIndent = 0
        .CharacterUnitRightIndent = 0
        .CharacterUnitFirstLineIndent = 2
        .LineUnitBefore = 0
        .LineUnitAfter = 0
        .MirrorIndents = False
        .TextboxTightWrap = wdTightNone
        .CollapsedByDefault = False
        .AutoAdjustRightIndent = True
        .DisableLineHeightGrid = False
        .FarEastLineBreakControl = True
        .WordWrap = True
        .HangingPunctuation = True
        .HalfWidthPunctuationOnTopOfLine = False
        .AddSpaceBetweenFarEastAndAlpha = True
        .AddSpaceBetweenFarEastAndDigit = True
        .BaseLineAlignment = wdBaselineAlignAuto
    End With
    myStyle.NoSpaceBetweenParagraphsOfSameStyle = False
    myStyle.ParagraphFormat.TabStops.ClearAll

    With myStyle.ParagraphFormat
        With .Shading
            .Texture = wdTextureNone
            .ForegroundPatternColor = wdColorAutomatic
            .BackgroundPatternColor = wdColorAutomatic
        End With
        .Borders(wdBorderLeft).LineStyle = wdLineStyleNone
        .Borders(wdBorderRight).LineStyle = wdLineStyleNone
        .Borders(wdBorderTop).LineStyle = wdLineStyleNone
        .Borders(wdBorderBottom).LineStyle = wdLineStyleNone
        With .Borders
            .DistanceFromTop = 1
            .DistanceFromLeft = 4
            .DistanceFromBottom = 1
            .DistanceFromRight = 4
            .Shadow = False
        End With
    End With

    myStyle.LanguageID = wdSimplifiedChinese
    myStyle.NoProofing = False
    myStyle.Frame.Delete

End Function
Function 调整标题4样式()
    Set myStyle = ActiveDocument.Styles("标题 4")

    With myStyle
        .AutomaticallyUpdate = True
        .BaseStyle = "正文"
        .NextParagraphStyle = "正文"
    End With

    With myStyle.Font
        .NameFarEast = "仿宋"  '"仿宋_GB2312"
        .NameAscii = "仿宋"
        .NameOther = "仿宋"
        .Name = "仿宋"
        .Size = 16
        .Bold = False
        .Italic = False
        .Underline = wdUnderlineNone
        .UnderlineColor = wdColorAutomatic
        .StrikeThrough = False
        .DoubleStrikeThrough = False
        .Outline = False
        .Emboss = False
        .Shadow = False
        .Hidden = False
        .SmallCaps = False
        .AllCaps = False
        .Color = wdColorAutomatic
        .Engrave = False
        .Superscript = False
        .Subscript = False
        .Scaling = 100
        .Kerning = 1
        .Animation = wdAnimationNone
        .DisableCharacterSpaceGrid = False
        .EmphasisMark = wdEmphasisMarkNone
        .Ligatures = wdLigaturesNone
        .NumberSpacing = wdNumberSpacingDefault
        .NumberForm = wdNumberFormDefault
        .StylisticSet = wdStylisticSetDefault
        .ContextualAlternates = 0
    End With
    With myStyle.ParagraphFormat
        .LeftIndent = CentimetersToPoints(0)
        .RightIndent = CentimetersToPoints(0)
        .SpaceBefore = 0
        .SpaceBeforeAuto = False
        .SpaceAfter = 0
        .SpaceAfterAuto = False
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphJustify
        .WidowControl = True
        .KeepWithNext = True
        .KeepTogether = True
        .PageBreakBefore = False
        .NoLineNumber = False
        .Hyphenation = True
        .FirstLineIndent = CentimetersToPoints(0.35)
        .OutlineLevel = wdOutlineLevel5
        .CharacterUnitLeftIndent = 0
        .CharacterUnitRightIndent = 0
        .CharacterUnitFirstLineIndent = 2
        .LineUnitBefore = 0
        .LineUnitAfter = 0
        .MirrorIndents = False
        .TextboxTightWrap = wdTightNone
        .CollapsedByDefault = False
        .AutoAdjustRightIndent = True
        .DisableLineHeightGrid = False
        .FarEastLineBreakControl = True
        .WordWrap = True
        .HangingPunctuation = True
        .HalfWidthPunctuationOnTopOfLine = False
        .AddSpaceBetweenFarEastAndAlpha = True
        .AddSpaceBetweenFarEastAndDigit = True
        .BaseLineAlignment = wdBaselineAlignAuto
    End With
    myStyle.NoSpaceBetweenParagraphsOfSameStyle = False
    myStyle.ParagraphFormat.TabStops.ClearAll

    With myStyle.ParagraphFormat
        With .Shading
            .Texture = wdTextureNone
            .ForegroundPatternColor = wdColorAutomatic
            .BackgroundPatternColor = wdColorAutomatic
        End With
        .Borders(wdBorderLeft).LineStyle = wdLineStyleNone
        .Borders(wdBorderRight).LineStyle = wdLineStyleNone
        .Borders(wdBorderTop).LineStyle = wdLineStyleNone
        .Borders(wdBorderBottom).LineStyle = wdLineStyleNone
        With .Borders
            .DistanceFromTop = 1
            .DistanceFromLeft = 4
            .DistanceFromBottom = 1
            .DistanceFromRight = 4
            .Shadow = False
        End With
    End With

    myStyle.LanguageID = wdSimplifiedChinese
    myStyle.NoProofing = False
    myStyle.Frame.Delete

End Function
Function 调整标题5样式()
    Set myStyle = ActiveDocument.Styles("标题 5")

    With myStyle
        .AutomaticallyUpdate = True
        .BaseStyle = "正文"
        .NextParagraphStyle = "正文"
    End With

    With myStyle.Font
        .NameFarEast = "仿宋"  '"仿宋_GB2312"
        .NameAscii = "仿宋"
        .NameOther = "仿宋"
        .Name = "仿宋"
        .Size = 16
        .Bold = False
        .Italic = False
        .Underline = wdUnderlineNone
        .UnderlineColor = wdColorAutomatic
        .StrikeThrough = False
        .DoubleStrikeThrough = False
        .Outline = False
        .Emboss = False
        .Shadow = False
        .Hidden = False
        .SmallCaps = False
        .AllCaps = False
        .Color = wdColorAutomatic
        .Engrave = False
        .Superscript = False
        .Subscript = False
        .Scaling = 100
        .Kerning = 1
        .Animation = wdAnimationNone
        .DisableCharacterSpaceGrid = False
        .EmphasisMark = wdEmphasisMarkNone
        .Ligatures = wdLigaturesNone
        .NumberSpacing = wdNumberSpacingDefault
        .NumberForm = wdNumberFormDefault
        .StylisticSet = wdStylisticSetDefault
        .ContextualAlternates = 0
    End With
    With myStyle.ParagraphFormat
        .LeftIndent = CentimetersToPoints(0)
        .RightIndent = CentimetersToPoints(0)
        .SpaceBefore = 0
        .SpaceBeforeAuto = False
        .SpaceAfter = 0
        .SpaceAfterAuto = False
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphJustify
        .WidowControl = True
        .KeepWithNext = True
        .KeepTogether = True
        .PageBreakBefore = False
        .NoLineNumber = False
        .Hyphenation = True
        .FirstLineIndent = CentimetersToPoints(0.35)
        .OutlineLevel = wdOutlineLevel6
        .CharacterUnitLeftIndent = 0
        .CharacterUnitRightIndent = 0
        .CharacterUnitFirstLineIndent = 2
        .LineUnitBefore = 0
        .LineUnitAfter = 0
        .MirrorIndents = False
        .TextboxTightWrap = wdTightNone
        .CollapsedByDefault = False
        .AutoAdjustRightIndent = True
        .DisableLineHeightGrid = False
        .FarEastLineBreakControl = True
        .WordWrap = True
        .HangingPunctuation = True
        .HalfWidthPunctuationOnTopOfLine = False
        .AddSpaceBetweenFarEastAndAlpha = True
        .AddSpaceBetweenFarEastAndDigit = True
        .BaseLineAlignment = wdBaselineAlignAuto
    End With
    myStyle.NoSpaceBetweenParagraphsOfSameStyle = False
    myStyle.ParagraphFormat.TabStops.ClearAll

    With myStyle.ParagraphFormat
        With .Shading
            .Texture = wdTextureNone
            .ForegroundPatternColor = wdColorAutomatic
            .BackgroundPatternColor = wdColorAutomatic
        End With
        .Borders(wdBorderLeft).LineStyle = wdLineStyleNone
        .Borders(wdBorderRight).LineStyle = wdLineStyleNone
        .Borders(wdBorderTop).LineStyle = wdLineStyleNone
        .Borders(wdBorderBottom).LineStyle = wdLineStyleNone
        With .Borders
            .DistanceFromTop = 1
            .DistanceFromLeft = 4
            .DistanceFromBottom = 1
            .DistanceFromRight = 4
            .Shadow = False
        End With
    End With

    myStyle.LanguageID = wdSimplifiedChinese
    myStyle.NoProofing = False
    myStyle.Frame.Delete

End Function
Function 调整正文样式()
    Set myStyle = ActiveDocument.Styles("正文")

    With myStyle
        .AutomaticallyUpdate = False
        .NextParagraphStyle = "正文"
    End With

    With myStyle.Font
        .NameFarEast = "仿宋"  '"仿宋_GB2312"
        .NameAscii = "仿宋"
        .NameOther = "仿宋"
        .Name = "仿宋"
        .Size = 16
        .Bold = False
        .Italic = False
        .Underline = wdUnderlineNone
        .UnderlineColor = wdColorAutomatic
        .StrikeThrough = False
        .DoubleStrikeThrough = False
        .Outline = False
        .Emboss = False
        .Shadow = False
        .Hidden = False
        .SmallCaps = False
        .AllCaps = False
        .Color = wdColorAutomatic
        .Engrave = False
        .Superscript = False
        .Subscript = False
        .Scaling = 100
        .Kerning = 1
        .Animation = wdAnimationNone
        .DisableCharacterSpaceGrid = False
        .EmphasisMark = wdEmphasisMarkNone
        .Ligatures = wdLigaturesNone
        .NumberSpacing = wdNumberSpacingDefault
        .NumberForm = wdNumberFormDefault
        .StylisticSet = wdStylisticSetDefault
        .ContextualAlternates = 0
    End With
    With myStyle.ParagraphFormat
        .LeftIndent = CentimetersToPoints(0)
        .RightIndent = CentimetersToPoints(0)
        .SpaceBefore = 0
        .SpaceBeforeAuto = False
        .SpaceAfter = 0
        .SpaceAfterAuto = False
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphJustify
        .WidowControl = False
        .KeepWithNext = False
        .KeepTogether = False
        .PageBreakBefore = False
        .NoLineNumber = False
        .Hyphenation = True
        .FirstLineIndent = CentimetersToPoints(0.35)
        .OutlineLevel = wdOutlineLevelBodyText
        .CharacterUnitLeftIndent = 0
        .CharacterUnitRightIndent = 0
        .CharacterUnitFirstLineIndent = 2
        .LineUnitBefore = 0
        .LineUnitAfter = 0
        .MirrorIndents = False
        .TextboxTightWrap = wdTightNone
        .CollapsedByDefault = False
        .AutoAdjustRightIndent = False
        .DisableLineHeightGrid = True
        .FarEastLineBreakControl = True
        .WordWrap = True
        .HangingPunctuation = True
        .HalfWidthPunctuationOnTopOfLine = False
        .AddSpaceBetweenFarEastAndAlpha = True
        .AddSpaceBetweenFarEastAndDigit = True
        .BaseLineAlignment = wdBaselineAlignAuto
    End With
    myStyle.NoSpaceBetweenParagraphsOfSameStyle = False
    myStyle.ParagraphFormat.TabStops.ClearAll

    With myStyle.ParagraphFormat
        With .Shading
            .Texture = wdTextureNone
            .ForegroundPatternColor = wdColorAutomatic
            .BackgroundPatternColor = wdColorAutomatic
        End With
        .Borders(wdBorderLeft).LineStyle = wdLineStyleNone
        .Borders(wdBorderRight).LineStyle = wdLineStyleNone
        .Borders(wdBorderTop).LineStyle = wdLineStyleNone
        .Borders(wdBorderBottom).LineStyle = wdLineStyleNone
        With .Borders
            .DistanceFromTop = 1
            .DistanceFromLeft = 4
            .DistanceFromBottom = 1
            .DistanceFromRight = 4
            .Shadow = False
        End With
    End With

    myStyle.LanguageID = wdSimplifiedChinese
    myStyle.NoProofing = False
    myStyle.Frame.Delete

End Function
Function 调整列表段落样式()
    '录制的条目自动'
    'ActiveDocument.Styles("列表段落").AutomaticallyUpdate = True
    Set myStyle = ActiveDocument.Styles("列表段落")

    With myStyle
        .AutomaticallyUpdate = True
        .BaseStyle = "正文"
        .NextParagraphStyle = "列表段落"
    End With

    With myStyle.Font
        .NameFarEast = "仿宋"  '"仿宋_GB2312"
        .NameAscii = "仿宋"
        .NameOther = "仿宋"
        .Name = "仿宋"
        .Size = 16
        .Bold = False
        .Italic = False
        .Underline = wdUnderlineNone
        .UnderlineColor = wdColorAutomatic
        .StrikeThrough = False
        .DoubleStrikeThrough = False
        .Outline = False
        .Emboss = False
        .Shadow = False
        .Hidden = False
        .SmallCaps = False
        .AllCaps = False
        .Color = wdColorAutomatic
        .Engrave = False
        .Superscript = False
        .Subscript = False
        .Scaling = 100
        .Kerning = 1
        .Animation = wdAnimationNone
        .DisableCharacterSpaceGrid = False
        .EmphasisMark = wdEmphasisMarkNone
        .Ligatures = wdLigaturesNone
        .NumberSpacing = wdNumberSpacingDefault
        .NumberForm = wdNumberFormDefault
        .StylisticSet = wdStylisticSetDefault
        .ContextualAlternates = 0
    End With
    With myStyle.ParagraphFormat
        .LeftIndent = CentimetersToPoints(0)
        .RightIndent = CentimetersToPoints(0)
        .SpaceBefore = 0
        .SpaceBeforeAuto = False
        .SpaceAfter = 0
        .SpaceAfterAuto = False
        .LineSpacingRule = wdLineSpaceExactly
        .LineSpacing = 29
        .Alignment = wdAlignParagraphJustify
        .WidowControl = False
        .KeepWithNext = False
        .KeepTogether = False
        .PageBreakBefore = False
        .NoLineNumber = False
        .Hyphenation = True
        .FirstLineIndent = CentimetersToPoints(1.13)
        .OutlineLevel = wdOutlineLevelBodyText
        .CharacterUnitLeftIndent = 0
        .CharacterUnitRightIndent = 0
        .CharacterUnitFirstLineIndent = 2
        .LineUnitBefore = 0
        .LineUnitAfter = 0
        .MirrorIndents = False
        .TextboxTightWrap = wdTightNone
        .CollapsedByDefault = False
        .AutoAdjustRightIndent = False
        .DisableLineHeightGrid = True
        .FarEastLineBreakControl = True
        .WordWrap = True
        .HangingPunctuation = True
        .HalfWidthPunctuationOnTopOfLine = False
        .AddSpaceBetweenFarEastAndAlpha = True
        .AddSpaceBetweenFarEastAndDigit = True
        .BaseLineAlignment = wdBaselineAlignAuto
    End With
    myStyle.NoSpaceBetweenParagraphsOfSameStyle = False
    myStyle.ParagraphFormat.TabStops.ClearAll

    With myStyle.ParagraphFormat
        With .Shading
            .Texture = wdTextureNone
            .ForegroundPatternColor = wdColorAutomatic
            .BackgroundPatternColor = wdColorAutomatic
        End With
        .Borders(wdBorderLeft).LineStyle = wdLineStyleNone
        .Borders(wdBorderRight).LineStyle = wdLineStyleNone
        .Borders(wdBorderTop).LineStyle = wdLineStyleNone
        .Borders(wdBorderBottom).LineStyle = wdLineStyleNone
        With .Borders
            .DistanceFromTop = 1
            .DistanceFromLeft = 4
            .DistanceFromBottom = 1
            .DistanceFromRight = 4
            .Shadow = False
        End With
    End With

    myStyle.LanguageID = wdSimplifiedChinese
    myStyle.NoProofing = False
    myStyle.Frame.Delete

End Function
Sub 公文样式()
    Call 调整标题样式
    Call 调整标题1样式
    Call 调整标题2样式
    Call 调整标题3样式
    Call 调整标题4样式
    Call 调整标题5样式
    Call 调整列表段落样式 '自动条目
    Call 调整正文样式
End Sub
