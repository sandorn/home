'
' @==============================================================
' @Descripttion : None
' @Develop      : VSCode
' @Author       : Even.Sand
' @Contact      : sandorn@163.com
' @Date         : 2020-05-01 14:53:26
' @LastEditTime : 2020-05-01 14:53:27
' @Github       : https://github.com/sandorn/home
' @License      : (C)Copyright 2009-2020, NewSea
' #==============================================================
'



Sub WebCrawlerDangD()
    Dim objDOM As Object
    Dim objDOMLI As Object
    Dim strURL As String
    Dim strText As String
    Dim strKey As String
    Dim strMsg As String
    Dim strMsgYesOrNo As String
    Dim strDOMLiHtml As String
    Dim objShape As Shape
    Dim objShapePic As Variant
    Dim intPN As Integer
    Dim intLiLength As Integer
    Dim lngaResult As Long
    Dim i As Long
    Dim k As Long
    Dim RNG_HEIGHT As Integer
    Dim PIC_HEIGHT As Integer
    Dim RNG_WIDTH As Integer
    Set objDOM = CreateObject("htmlfile")
    strKey = [a2].Value
    '查询关键字
    If Len(strKey) = 0 Then MsgBox "未在a2单元格输入查询关键字。": Exit Sub
    '如果查询关键字为空，则退出程序
    ReDim aResult(1 To 7, 1 To 1)
    '放置查询结果的数组
    For intPN = 1 To 100
    '当当网最高支持100页的结果
        strURL = "http://search.dangdang.com/?key=" & strKey & "&category_path=01.00.00.00.00.00#J_tab&act=input&page_index=" & intPN
        With CreateObject("msxml2.xmlhttp")
            .Open "GET", strURL, False
            .send
            strText = .responseText
        End With
        '发送请求数据，获得responsetext
        If InStr(strText, "没有找到") Then Exit For
        '判断该页是否有查询结果，存在关键字“没有找到”说明没有查询结果。
        objDOM.body.innerHTML = strText
        Set objDOMLI = objDOM.getElementById("search_nature_rg").getElementsByTagName("li")
        'LI标签的元素集合
        intLiLength = objDOMLI.Length
        'LI标签的数量
        lngaResult = lngaResult + intLiLength
        ReDim Preserve aResult(1 To 7, 1 To lngaResult)
        '动态调整结果数组大小
        For i = 0 To intLiLength - 1
            k = k + 1
            aResult(1, k) = k '序号
            strDOMLiHtml = objDOMLI(i).innerHTML & "now_price>search_pre_price>search_discount>&nbsp;("
            aResult(4, k) = Val(Mid(Split(strDOMLiHtml, "now_price>")(1), 2))
            '现价
            aResult(5, k) = Val(Mid(Split(strDOMLiHtml, "search_pre_price>")(1), 2))
            '定价
            If aResult(5, k) = 0 Then aResult(5, k) = aResult(4, k)
            '定价为空则等于现价
            aResult(6, k) = Val(Split(strDOMLiHtml, "search_discount>&nbsp;(")(1))
            '折扣
            If aResult(6, k) = 0 Then aResult(6, k) = ""
            '折扣为空则没有折扣
            With objDOMLI(i).getElementsByTagName("A")(0)
                aResult(3, k) = .Title '书名
                aResult(7, k) = .href '商品链接
            End With
            With objDOMLI(i).getElementsByTagName("IMG")(0)
                aResult(2, k) = .src
                '封面链接
                If Left(aResult(2, k), 4) <> "http" Then aResult(2, k) = .getAttribute("data-original")
                '如果.src属性不是封面链接，则读data-original属性
            End With
        Next
    Next
    If k = 0 Then MsgBox "未找到符合条件的查询结果。": Exit Sub
    ActiveSheet.UsedRange.Offset(3).ClearContents
    '删除表格内容
    Application.ScreenUpdating = False
    For Each objShape In ActiveSheet.Shapes
        If objShape.Type = msoLinkedPicture Then objShape.Delete
    Next
    '删除表格内带链接的图片
    If k > 200 Then
        strMsg = "一共有" & k & "张图片需要导入Excel工作表，耗时过长，不建议导入！"
    Else
        strMsg = "一共有" & k & "张图片需要导入Excel工作表。"
    End If
    '根据查询条目数量建议是否导入图片
    strMsgYesOrNo = MsgBox("请选择是否需要导入图书图片！" & vbCrLf & strMsg, vbYesNo)
    If strMsgYesOrNo = vbYes Then
        PIC_HEIGHT = 100 '图片高度
        RNG_HEIGHT = 110 '单元格高度
        RNG_WIDTH = 16 '单元格宽度
        [b:b].ColumnWidth = RNG_WIDTH
        [a5].Resize(k, 1).EntireRow.RowHeight = RNG_HEIGHT
        For i = 1 To k
            Set objShapePic = ActiveSheet.Pictures.Insert(aResult(2, i))
            '插入图片,并设置图片在单元格居中显示
            With Cells(i + 4, 2)
                objShapePic.Height = PIC_HEIGHT
                objShapePic.Top = (RNG_HEIGHT - PIC_HEIGHT) / 2 + .Top
                objShapePic.Left = (.Width - objShapePic.Width) / 2 + .Left
            End With
            aResult(2, i) = ""
            '删除数组内封面链接
        Next
    End If
    [a4:g4] = Array("序号", "封面", "书名", "现价", "定价", "折扣", "链接")
    [a5].Resize(k, UBound(aResult)).Value = Application.Transpose(aResult)
    Application.ScreenUpdating = True
    Set objDOM = Nothing
End Sub
