<!--
 * @==============================================================
 * @Descripttion : None
 * @Develop      : VSCode
 * @Author       : Even.Sand
 * @Contact      : sandorn@163.com
 * @Date         : 2020-05-18 17:41:21
 * @LastEditTime : 2020-05-20 20:13:24
 * @Github       : https://github.com/sandorn/home
 * @License      : (C)Copyright 2009-2020, NewSea
 * #==============================================================
-->


### QT StyleSheet templates ###
Themes available:
1. [Ubuntu](https://github.com/GTRONICK/QSS/blob/master/Ubuntu.qss)

![Ubuntu theme screenshot](https://sites.google.com/site/gtronick/QSS-Ubuntu.png)

2. [ElegantDark](https://github.com/GTRONICK/QSS/blob/master/ElegantDark.qss)

![ElegantDark theme screenshot](https://sites.google.com/site/gtronick/QSS-ElegantDark.png)

3. [MaterialDark](https://github.com/GTRONICK/QSS/blob/master/MaterialDark.qss)

![MaterialDark theme screenshot](https://sites.google.com/site/gtronick/QSS-MaterialDark.png)

4. [ConsoleStyle](https://github.com/GTRONICK/QSS/blob/master/ConsoleStyle.qss)

![ConsoleStyle theme screenshot](https://sites.google.com/site/gtronick/QSS-ConsoleStyle.png)

5. [AMOLED](https://github.com/GTRONICK/QSS/blob/master/AMOLED.qss)

![AMOLED theme screenshot](https://sites.google.com/site/gtronick/QSS-Amoled.png)

6. [Aqua](https://github.com/GTRONICK/QSS/blob/master/Aqua.qss)

![Aqua theme screenshot](https://sites.google.com/site/gtronick/QSS-Aqua.png)

## The ManjaroMix Theme!: Includes a radial gradient for Checkboxes, and minimalist arrows for scrollbars. ##
7. [ManjaroMix](https://github.com/GTRONICK/QSS/blob/master/ManjaroMix.qss)

![ManjaroMix theme screenshot](https://5c57bd3a-a-62cb3a1a-s-sites.googlegroups.com/site/gtronick/QSS-ManajaroMix.PNG)

Stay tunned!, this files are being updated frequently.

*Consider donating :)* **PayPal Account:** gtronick@gmail.com



Pyqt5 ——setStyleSheet用法_c/c++_bluewhu的博客-CSDN博客
https://blog.csdn.net/bluewhu/article/details/102527958

jhonconal/QUI-Creator: QUI Creator，一个QSS皮肤文件生成器，适用于所有Qt版本
https://github.com/jhonconal/QUI-Creator

CSS参考手册_web前端开发参考手册系列
https://css.doyoe.com/

所有控件
QPushButton: 所有按钮控件
QPushButton[name='mybtn'] :属性选择器
.QPushButton 类选择器

declaration部份是一系列的（属性：值）对，使用分号（;）将各个不同的属性值对分离，使用大括号（{}）将所有declaration包括在同时。

1， 平常选择器（selector）
Qt扶持所有的CSS2定义的选择器，其祥细内容可以在w3c的网站上查找http://www.w3.org/TR/CSS2/selector.html， 中间对照常用的selector类别有：
1.1 通用类型选择器：*
会对所有控件有结果。
1.2 类别选择器：QPushButton
匹配所有QPushButton的实例和其子类的实例。
1.3 属性选择器：QPushButton[flat=”false”]
匹配所有QPushButton属性flat为false的实例，属性分为两种，静态的和动态的，静态属性可以通过Q_PROPERTY() 来指定，动态属性可以使用setProperty来指定，如：

QLineEdit *nameEdit = new QLineEdit(this);
nameEdit->setProperty("mandatoryField", true);
如果在设置了qss后Qt属性变动了，必要重新设置qss来使其见效，可以使用先unset再set qss。

1.4 类选择器：.QPushButton
所有QPushButton的实例，但不包括其子类，这相当于：

*[class~="QPushButton"]
~=的含义是测验一个QStringList类别的属性是否包罗给定的QString。
1.5 ID抉择器：QPushButton#okButton
对应Qt里面的object name设置，使用这条CSS之前要先设置对应控件的object name为okButton，如：

Ok->setObjectName(tr(“okButton”));
1.6 后代选择器：QDialog QPushButton
对于所有为QDialog后代（包括儿子，与儿子的儿子的递归）为QPushButton的实例
1.7 子选择器：QDialog > QPushButton
对于所有的QDialog直接子类QPushButton的实例，不包罗儿子的儿子的递归。

伪类选择器
1、:checked: 按钮控件被选中
2、:unchecked:按钮控件未被选中
3、:indeterminate:对于checkBox或者redioButton部分选中(三态的时候)
4、:hover:控件被鼠标放上去
5、:pressed:控件被按下
6、:focus:控件获取焦点
7、:disabled:控件禁用
8、:enabled:控件有效的时候
9、:on:控件属于on状态
10、:off: 控件处于off状态
11、关于伪类取反的操作:!checked
12、伪类连接使用:hover:checked表示鼠标在上面且被选中

#QProgressBar{border:1px solid grey;border-radius: 5px;text-align: center;font:bold 8pt 微软雅黑;}
#QProgressBar::chunk{background-color: #CD96CD;width: 10px;margin: 0.5px;}# 斑马线,色条


子部件	描述
::down-arrow	combo box或spin box的下拉箭头
::down-button	spin box的向下按钮
::drop-down	combo box的下拉箭头
::indicator	checkbox、radio button或可选择group box的指示器
::item	menu、menu bar或status bar的子项目
::menu-indicator	push button的菜单指示器
::title	group box的标题
::up-arrow	spin box的向上箭头
::up-button	spin box的向上按钮
通过指定subcontrol-position和subcontrol-origin属性，子部件可以被放置在部件箱体内的任何位置。并且，子部件的位置 还可以使用相对或绝对的方式进一步的调整。具体选择何种调整方式取决于子部件具有固定的大小，还是会随着父部件而变化。
