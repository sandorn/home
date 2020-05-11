'
' @==============================================================
' @Descripttion : None
' @Develop      : VSCode
' @Author       : Even.Sand
' @Contact      : sandorn@163.com
' @Date         : 2020-05-07 16:26:41
' @LastEditTime : 2020-05-07 20:01:25
' @Github       : https://github.com/sandorn/home
' @License      : (C)Copyright 2009-2020, NewSea
' #==============================================================
'


Function setStyles(styles_name)
    Set myStyle = ActiveDocument.Styles(styles_name)

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
        .TabStops.ClearAll
        .SpaceBefore = 0
        .SpaceBeforeAuto = False
        .SpaceAfter = 0
        .SpaceAfterAuto = False
        .LeftIndent = CentimetersToPoints(0)
        .RightIndent = CentimetersToPoints(0)
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

    myStyle.NoSpaceBetweenParagraphsOfSameStyle = False

    myStyle.LanguageID = wdSimplifiedChinese
    myStyle.NoProofing = False
    myStyle.Frame.Delete

End Function

Function 调整标题样式()
    'Set myStyle = ActiveDocument.Styles.Add(Name:="标题 1", Type:=wdStyleTypeParagraph)
    call setStyles("标题")
    Set myStyle = ActiveDocument.Styles("标题")

    With myStyle
        .BaseStyle = "正文"
        With .Font
            .NameFarEast = "方正小标宋简体"
            .NameAscii = "方正小标宋简体"
            .NameOther = "宋体"
            .Name = "方正小标宋简体"
            .Size = 22
            .Kerning = 二号
        End With

        With .ParagraphFormat
            .LeftIndent = CentimetersToPoints(0)
            .RightIndent = CentimetersToPoints(0)
            .PageBreakBefore = True
            .FirstLineIndent = CentimetersToPoints(0)
            .CharacterUnitFirstLineIndent = 0
            .Alignment = wdAlignParagraphCenter
            .OutlineLevel = wdOutlineLevel1
        End With
    End With
End Function

Function 调整标题1样式()
    call setStyles("标题 1")
    Set myStyle = ActiveDocument.Styles("标题 1")

    With myStyle
        .BaseStyle = "正文"
        With .Font
            .NameFarEast = "黑体"
            .NameAscii = "黑体"
            .NameOther = "黑体"
            .Name = "黑体"
        End With

        With .ParagraphFormat
            .OutlineLevel = wdOutlineLevel2
        End With
    End With
End Function

Function 调整标题2样式()
    call setStyles("标题 2")
    Set myStyle = ActiveDocument.Styles("标题 2")

    With myStyle
        .BaseStyle = "正文"
        With .Font
            .NameFarEast = "楷体"   '"楷体_GB2312"
            .NameAscii = "楷体"
            .NameOther = "楷体"
            .Name = "楷体"
        End With

        With .ParagraphFormat
            .OutlineLevel = wdOutlineLevel3
        End With
    End With
End Function

Function 调整标题3样式()
    call setStyles("标题 3")
    Set myStyle = ActiveDocument.Styles("标题 3")

    With myStyle
        .BaseStyle = "正文"
        With .ParagraphFormat
            .OutlineLevel = wdOutlineLevel4
        End With
    End With
End Function
Function 调整标题4样式()
    call setStyles("标题 4")
    Set myStyle = ActiveDocument.Styles("标题 4")

    With myStyle
        .BaseStyle = "正文"
        With .ParagraphFormat
            .OutlineLevel = wdOutlineLevel5
        End With
    End With
End Function
Function 调整标题5样式()
    call setStyles("标题 5")
    Set myStyle = ActiveDocument.Styles("标题 5")

    With myStyle
        .BaseStyle = "正文"
        With .ParagraphFormat
            .OutlineLevel = wdOutlineLevel6
        End With
    End With
End Function
Function 调整正文样式()
    call setStyles("正文")
End Function
Function 调整自动条目样式()
    call setStyles("列表段落")
    Set myStyle = ActiveDocument.Styles("列表段落")

    With myStyle
        .BaseStyle = "正文"
        .NextParagraphStyle = "列表段落"
        With .ParagraphFormat
            .FirstLineIndent = CentimetersToPoints(1.13)
            .CharacterUnitFirstLineIndent = 2
        End With
    End With
End Function
Sub 更新公文样式()
    Call 调整标题样式
    Call 调整标题1样式
    Call 调整标题2样式
    Call 调整标题3样式
    Call 调整标题4样式
    Call 调整标题5样式
    Call 调整自动条目样式
    Call 调整正文样式
End Sub
