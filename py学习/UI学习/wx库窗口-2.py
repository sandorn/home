# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Software:   VSCode
@File    :   wx库窗口-2.py
@Time    :   2019/04/30 10:22:43
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
'''

import wx


class win(wx.Frame):

    def __init__(self, parent=None):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="本文查看编辑器",
            pos=wx.DefaultPosition,
            size=wx.Size(800, 600),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        '''框架的形状和尺寸标记
wx.FRAME_NO_TASKBAR：一个完全标准的框架，除了一件事：在Windows系统和别的支持这个特性的系统下，它不显示在任务栏中。当最小化时，该框架图标化到桌面而非任务栏。
wx.FRAME_SHAPED：非矩形的框架。框架的确切形状使用SetShape()方法来设置。窗口的形状将在本章后面部分讨论。
wx.FRAME_TOOL_WINDOW：该框架的标题栏比标准的小些，通常用于包含多种工具按钮的辅助框架。在Windows操作系统下，工具窗口将不显示在任务栏中。
wx.ICONIZE：窗口初始时将被最小化显示。这个样式仅在Windows系统中起作用。
wx.MAXIMIZE：窗口初始时将被最大化显示（全屏）。这个样式仅在Windows系统中起作用。
wx.MINIMIZE：同wx.ICONIZE。

窗口漂浮行为的样式
wx.FRAME_FLOAT_ON_PARENT：框架将漂浮在其父窗口（仅其父窗口）的上面。（很明显，要使用这个样式，框架需要有一个父窗口）。其它的框架可以遮盖这个框架。
wx.STAY_ON_TOP：该框架将始终在系统中其它框架的上面。（如果你有多个框架使用了这个样式，那么它们将相互重叠，但对于系统中其它的框架，它们仍在上面。）

装饰窗口的样式
wx.CAPTION：给窗口一个标题栏。如果你要放置最大化框、最小化框、系统菜单和上下文帮助，那么你必须包括该样式。
wx.FRAME_EX_CONTEXTHELP：这是用于Windows操作系统的，它在标题栏的右角放置问号帮助图标。这个样式是与wx.MAXIMIZE_BOX和WX.MINIMIZE_BOX样式互斥的。它是一个扩展的样式，并且必须使用两步来创建，稍后说明。
wx.FRAME_EX_METAL：在Mac OS X上，使用这个样式的框架有一个金属质感的外观。这是一个附加样式，必须使用SetExtraStyle方法来设置。
wx.MAXIMIZE_BOX：在标题栏的标准位置放置一个最大化框。
wx.MINIMIZE_BOX：在标题栏的标准位置放置一个最小化框。
wx.CLOSE_BOX：在标题栏的标准位置放置一个关闭框。
wx.RESIZE_BORDER：给框架一个标准的可以手动调整尺寸的边框。
wx.SIMPLE_BORDER：给框架一个最简单的边框，不能调整尺寸，没有其它装饰。该样式与所有其它装饰样式是互斥的。
wx.SYSTEM_MENU：在标题栏上放置一个系统菜单。这个系统菜单的内容与你所使用的装饰样式有关。例如，如果你使用wx.MINIMIZE_BOX，那么系统菜单项就有“最小化”选项。

wx.Frame的公共属性
SetBackgroundColor(wx.Color)：背景色是框架中没有被其子窗口部件覆盖住的那些部分的颜色。你可以传递一个wx.Color或颜色名给设置方法。任何传递给需要颜色的wxPython方法的字符串，都被解释为对函数wx.NamedColour()的调用。
SetId(int)：返回或设置窗口部件的标识符。
SetMenuBar(wx.MenuBar)：得到或设置框架当前使用的的菜单栏对象，如果没有菜单栏，则返回None。
GetPositionTuple()
SetPosition(wx.Point)：以一个wx.Point或Python元组的形式返回窗口左上角的x,y的位置。对于顶级窗口，该位置是相对于显示区域的坐标，对于子窗口，该位置是相对于父窗口的坐标。
GetSizeTuple()
SetSize(wx.Size)：C++版的get*或set*方法被覆盖。默认的get*或set*使用一个wx.Size对象。GetSizeTuple()方法以一个Python元组的形式返回尺寸。也可以参看访问该信息的另外的方法SetDimensions()。
SetTitle(String)：得到或设置框架标题栏的字符串。

wx.Frame的方法
Center(direction=wx.BOTH)：框架居中（注意，非美语的拼写Centre，也被定义了的）。参数的默认值是wx.BoTH，在此情况下，框是在两个方向都居中的。参数的值若是wx.HORIZONTAL或wx.VERTICAL，表示在水平或垂直方向居中。
Enable(enable=true)：如果参数为true，则框架能够接受用户的输入。如果参数为False，则用户不能在框架中输入。相对应的方法是Disable()。
GetBestSize()：对于wx.Frame，它返回框架能容纳所有子窗口的最小尺寸。
Iconize(iconize)：如果参数为true，最小化该框架为一个图标（当然，具体的行为与系统有关）。如果参数为False，图标化的框架恢复到正常状态。
IsEnabled()：如果框架当前有效，则返回True。
IsFullScreen()：如果框架是以全屏模式显示的，则返回True，否则False。细节参看ShowFullScreen。
IsIconized()：如果框架当前最小化为图标了，则返回True，否则False。
IsMaximized()：如果框架当前是最大化状态，则返回True，否则False。
IsShown()：如果框架当前可见，则返回True。
IsTopLevel()：对于顶级窗口部件如框架或对话框，总是返回True，对于其它类型的窗口部件返回False。
Maximize(maximize)：如果参数为True，最大化框架以填充屏幕（具体的行为与系统有关）。这与敲击框架的最大化按钮所做的相同，这通常放大框架以填充桌面，但是任务栏和其它系统组件仍然可见。
Refresh(eraseBackground=True,rect=None)：触发该框架的重绘事件。如果rect是none，那么整个框架被重画。
如果指定了一个矩形区域，那么仅那个矩形区域被重画。如果eraseBackground为True，那么这个窗口的北影也将被重画，如果为False，那么背景将不被重画。

Show(show=True)：如果参数值为True，导致框架被显示。如果参数值为False，导致框架被隐藏。Show(False)等同于Hide()。
ShowFullScreen(show,style=wx.FULLSCREEN_ALL)
如果布尔参数是True，那么框架以全屏的模式被显示——意味着框架被放大到填充整个显示区域，包括桌面上的任务栏和其它系统组件。如果参数是False，那么框架恢复到正常尺寸。
style参数是一个位掩码。默认值wx.FULLSCREEN_ALL指示wxPython当全屏模式时隐藏所有窗口的所有样式元素。
后面的这些值可以通过使用按位运算符来组合，以取消全屏模式框架的部分装饰：
wx.FULLSCREEN_NOBORDER, wx.FULLSCREEN_NOCAPTION,wx.FULLSCREEN_NOMENUBAR,wx.FULLSCREEN_NOSTATUSBAR,wx.FULLSCREEN_NOTOOLBAR。

SetDimensions(x, y, width, height,sizeFlags=wx.SIZE_AUTO)：
使你能够在一个方法调用中设置窗口的尺寸和位置。位置由参数x和y决定，尺寸由参数width和height决定。前四个参数中，如果有的为-1，那么这个-1将根据参数sizeFlags的值作相应的解释。表8.6包含了参数sizeFlags的可能取值。
SetDimensions方法的尺寸标记
wx.ALLOW_MINUS_ONE：一个有效的位置或尺寸。
wx.SIZE_AUTO：转换为一个wxPython默认值。
wx.SIZE_AUTO_HEIGHT：一个有效的高度，或一个wxPython默认高度。
wx.SIZE_AUTO_WIDTH：一个有效的宽度，或一个wxPython默认宽度。
wx.SIZE_USE_EXISTING：使用现有的尺寸。
'''
        '''初始化控件'''
        self.panel = wx.Panel(self)  # 设置画布
        self.panel.SetBackgroundColour('white')
        self.path_text = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        self.open_button = wx.Button(self.panel, label="打开")
        self.save_button = wx.Button(self.panel, label="保存")
        self.saveas_button = wx.Button(self.panel, label="另存")
        self.content_text = wx.TextCtrl(
            self.panel, style=wx.TE_MULTILINE)  #  wx.TE_MULTILINE实现滚动多行
        self.状态栏 = self.CreateStatusBar()  # 状态栏
        toolBar = self.CreateToolBar()  # 创建工具栏
        #self.ToolBar = toolBar
        toolBar.AddSimpleTool(wx.NewId(), wx.Bitmap('D:/CODE/py/toolbar.bmp'),
                              "New", "long help for 'New'")
        #toolBar.AddTool(101, wx.Bitmap("new.png"))
        #toolBar.AddTool(102, wx.Bitmap("save.png"))
        toolBar.Realize()
        '''菜单'''
        menuBar = wx.MenuBar()  # 菜单栏对象
        fileMenu = wx.Menu()  # 菜单对象
        fileMenu.Append(wx.ID_NEW, "&New")
        fileMenu.Append(wx.ID_OPEN, '&Open')
        fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()  # 插入分割线
        fileMenu.Append(wx.ID_ANY, 'Import bookmarks...')
        fileMenu.Append(wx.ID_ANY, 'Import mail...')
        fileMenu.AppendSeparator()  # 插入分割线
        fileMenu.Append(wx.ID_ABOUT, "About", "How are you")
        fitem = fileMenu.Append(wx.ID_EXIT, "EXIT", "EXIT Applications1111111")

        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)  # 设置菜单栏对象到frame
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)  # 绑定菜单执行的函数
        '''绑定打开文件事件到open_button按钮上'''
        self.open_button.Bind(wx.EVT_BUTTON, self.openfile)
        self.save_button.Bind(wx.EVT_BUTTON, self.__SaveFile)
        self.saveas_button.Bind(wx.EVT_BUTTON, self.saveas)
        '''设置水平布局'''
        self.box = wx.BoxSizer()  # 不带参数表示默认实例化一个水平尺寸器
        self.box.Add(
            self.path_text, proportion=5, flag=wx.EXPAND | wx.ALL, border=3)
        '''添加组件|proportion：相对比例;flag：填充的样式和方向,wx.EXPAND为完整填充，wx.ALL为填充的方向;border：边框'''
        self.box.Add(
            self.open_button, proportion=1, flag=wx.EXPAND | wx.ALL,
            border=3)  # 添加组件
        self.box.Add(
            self.save_button, proportion=1, flag=wx.EXPAND | wx.ALL,
            border=3)  # 添加组件
        self.box.Add(
            self.saveas_button, proportion=1, flag=wx.EXPAND | wx.ALL,
            border=3)  # 添加组件
        '''垂直布局'''
        self.v_box = wx.BoxSizer(wx.VERTICAL)  # wx.VERTICAL参数表示实例化一个垂直尺寸器
        self.v_box.Add(
            self.box, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件
        self.v_box.Add(
            self.content_text, proportion=9, flag=wx.EXPAND | wx.ALL,
            border=3)  # 添加组件
        self.panel.SetSizer(self.v_box)  # 设置主尺寸器
        '''布局完毕'''
        self.Center()
        self.Show()

    def OnQuit(self, e):
        self.Close()

    #定义事件函数,放在类里面必须传入self
    def openfile(self, event):
        filesFilter = "txt(*.txt)|*.txt|" "All files (*.*)|*.*"
        fileDialog = wx.FileDialog(
            self, message="选择单个文件", wildcard=filesFilter, style=wx.FD_OPEN)
        dialogResult = fileDialog.ShowModal()
        if dialogResult != wx.ID_OK:
            return
        path = fileDialog.GetPath()
        self.path_text.SetValue(path)
        with open(path, "r", encoding="utf-8") as f:
            '''encoding参数将编码转为utf8'''
            self.content_text.SetValue(f.read())
        self.view_button = wx.Button(self.panel, label="查看")
        self.box.Add(
            self.view_button, proportion=1, flag=wx.EXPAND | wx.ALL,
            border=3)  # 添加组件
        #self.Refresh(eraseBackground=True, rect=None)
        #self.Show(show=False)
        self.ShowFullScreen(True)
        self.ShowFullScreen(False)
        #self.Show(show=True)

    def __SaveFile(self, event):
        path = self.path_text.GetValue()
        with open(path, "w", encoding="utf-8") as f:
            '''encoding参数将编码转为utf8'''
            f.write(self.content_text.GetValue())
            f.close()

    def saveas(self, event):
        fileDialog = wx.FileDialog(
            self, message="保存文件", wildcard=filesFilter, style=wx.FD_SAVE)
        dialogResult = fileDialog.ShowModal()
        if dialogResult != wx.ID_OK:
            return
        path = fileDialog.GetPath()
        with open(path, "w", encoding="utf-8") as f:
            '''encoding参数将编码转为utf8'''
            f.write(self.content_text.GetValue())
            f.close()


def main():
    app = wx.App()
    frame = win()
    app.MainLoop()




if __name__ == '__main__':
    main()
