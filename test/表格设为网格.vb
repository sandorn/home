'
' @Description  : 头部注释
' @Develop      : VSCode
' @Author       : sandorn sandorn@live.cn
' @Date         : 2025-02-12 18:11:53
' @LastEditTime : 2025-05-16 09:54:23
' @FilePath     : /CODE/test/表格设为网格.vb
' @Github       : https://github.com/sandorn/home
'
Sub 表格设为网格()
    ' ==================== 初始化设置 ====================
    ' 关闭屏幕刷新和提示（提升执行速度）
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    On Error Resume Next ' 错误处理
    
    ' ==================== 判断操作范围 ====================
    Dim isSingleTable As Boolean
    isSingleTable = Selection.Information(wdWithInTable) ' 检查是否选中单个表格
    
    ' ==================== 遍历处理所有表格 ====================
    Dim mytable As Table
    For Each mytable In ActiveDocument.Tables
        ' 若选中单个表格，则仅处理当前选中表格
        If isSingleTable Then Set mytable = Selection.Tables(1)

        With mytable
            ' ========== 表格基础设置 ==========
            ' -- 自动调整与尺寸控制 --
            .AutoFitBehavior wdAutoFitContent ' 根据内容自动调整
            .AutoFitBehavior wdAutoFitWindow ' 根据窗口自动调整
            ' 注：此处实际未锁定尺寸，后续操作可能被覆盖
            '禁用表格自动根据内容调整列宽的功能
            .AllowAutoFit = False
            .Rows.Alignment = wdAlignRowCenter ' 设置表格水平居中
            '禁用文字环绕表格的功能，
            .Rows.WrapAroundText = False

            ' -- 清除样式干扰 --
            '.Range.ClearFormatting              ' 清除表格格式
            .Style = "Normal" ' 应用无格式样式
            .Range.Style = "正文" ' 重置文本样式
            .Shading.Texture = wdTextureNone ' 清除底纹纹理
            .Range.HighlightColorIndex = wdNoHighlight ' 清除高亮
            .Shading.BackgroundPatternColor = RGB(255, 255, 255) ' 设置白色背景色
            .Shading.BackgroundPatternColor = wdColorAutomatic ' 恢复自动背景色

            ' ========== 单元格格式设置 ==========
            .Range.Cells.VerticalAlignment = wdAlignVerticalCenter ' 文本垂直居中
            .Range.ParagraphFormat.Alignment = wdAlignParagraphCenter ' 文本水平居中
            ' 禁用文字环绕

            Dim cell As cell
            For Each cell In .Range.Cells
                With cell.Range
                    ' === 删除所有空格（包括普通空格和不间断空格） ===
                    .Text = Replace(.Text, " ", "") ' 删除普通空格
                    .Text = Replace(.Text, Chr(160), "") ' 删除不间断空格（ASCII 160））
                    .Text = Replace(.Text, ChrW(&HA0), "") ' 删除不间断空格）
                    ' === 删除段落标记（^p） ===
                    '.Text = Replace(.Text, vbCr, "") ' 删除回车符（段落标记）
                    ' === 清除首尾空格（保险操作） ===
                    .Text = Trim(.Text)
                End With

                ' -- 段落格式：水平居中与缩进清除 --
                With cell.Range.ParagraphFormat
                    '.Alignment = wdAlignParagraphCenter   ' 文本水平居中
                    .LeftIndent = 0 ' 清除左缩进
                    .RightIndent = 0 ' 清除右缩进
                    .FirstLineIndent = 0 ' 清除首行缩进
                    .CharacterUnitFirstLineIndent = 0 ' 清除缩进
                    .SpaceBefore = 0 ' 段前间距清零
                    .SpaceAfter = 0 ' 段后间距清零
                    .LineSpacingRule = wdLineSpaceExactly ' 固定值行距
                    .LineSpacing = 14 '设置表格内段落的行距为固定值14磅
                End With

                ' 方法2：遍历每个段落双重保险
                For Each para In cell.Range.Paragraphs
                    With para.Format
                        .LeftIndent = 0 ' 清除左缩进
                        .RightIndent = 0 ' 清除右缩进
                        .FirstLineIndent = 0 ' 清除首行缩进
                        .CharacterUnitFirstLineIndent = 0 ' 清除缩进
                        .SpaceBefore = 0 ' 段前间距清零
                        .SpaceAfter = 0 ' 段后间距清零
                        .LineSpacingRule = wdLineSpaceExactly ' 固定值行距
                        .LineSpacing = 14 '设置表格内段落的行距为固定值14磅
                    End With
                Next para
            Next cell
            
            ' ========== 行高与边距设置 ==========
            ' -- 行高设置--
            With .Rows
                .HeightRule = wdRowHeightAtLeast ' 行高最小值规则
                .Height = MillimetersToPoints(7) ' 7毫米
                .AllowBreakAcrossPages = True ' 允许跨页断行
                '.WrapAroundText = False                   ' 禁用文字环绕
                .LeftIndent = 0 ' 行左缩进清零
            End With

            ' -- 单元格边距 --
            .LeftPadding = MillimetersToPoints(2) ' 左内边距2毫米
            .RightPadding = MillimetersToPoints(2) ' 右内边距2毫米
            .TopPadding = 0 ' 上内边距0毫米
            .BottomPadding = 0 ' 下内边距0毫米
            
            ' ========== 字体与边框设置 ==========
            With .Range.Font
                .Name = "宋体" ' 字体
                .Size = 12 ' 字号
                .Bold = False ' 非加粗
                .Color = wdColorBlack ' 黑色文字
            End With

            With .Borders
                .InsideLineStyle = wdLineStyleSingle ' 内部边框单线
                .InsideLineWidth = wdLineWidth025pt ' 内部线宽0.25磅
                .OutsideLineStyle = wdLineStyleSingle ' 外部边框单线
                .OutsideLineWidth = wdLineWidth025pt ' 外部线宽0.25磅
            End With
            
            ' ========== 首行特殊处理 ==========
            With .Rows.First
                .Height = MillimetersToPoints(8) ' 行高8毫米
                .Alignment = wdAlignParagraphCenter ' 文本水平居中
                .HeadingFormat = True ' 启用标题行格式
                .Range.Font.Bold = True ' 加粗文本
                ' 设置首行底纹颜色
                Dim cellinFirstRow As cell
                For Each cellinFirstRow In .Cells
                    cellinFirstRow.Shading.BackgroundPatternColor = RGB(215, 215, 215) ' 浅灰色
                Next cellinFirstRow
            End With
        End With ' 结束当前表格设置
        If isSingleTable Then Exit For
    Next mytable ' 处理下一个表格
    
    ' ==================== 恢复默认设置 ====================
    Err.Clear
    On Error GoTo 0
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    MsgBox "表格格式化完成！", vbInformation
End Sub