# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-02-22 12:06:59
LastEditTime : 2023-02-22 12:07:09
FilePath     : /CODE/py学习/UI学习/pywebview测试.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import webview

chinese = {
    'global.quitConfirmation': u'确定关闭?',
}

HTML = '''
    <!DOCTYPE html>
    <html>
    <head lang="en">
    <meta charset="UTF-8">
    </head>
    <body>
    <input id="select_dir_id" disabled="disabled" style="width: 400px" placeholder="显示选择的目录">
    <button onClick="selectDir()">测试选择目录</button><br/>
    <input id="select_file_id" disabled="disabled" style="width: 400px" placeholder="显示选择的文件(*.bmp;*.jpg;*.gif;*.png)">
    <button onClick="selectFile()">测试选择文件</button><br/>
    <input id="input1_id" placeholder="参数1">
    <input id="input2_id" placeholder="参数2">
    <input id="input3_id" placeholder="参数3">
    <button onClick="testArgcs()">测试传入多参数，模拟耗时请求</button><br/>
    <div id="response-container"></div>
    <script>
        window.addEventListener('pywebviewready', function() {
            console.log('pywebview is ready');
        })

        function selectDir() {
            pywebview.api.select_dir().then((response)=>{
                //alert(response);
                document.getElementById('select_dir_id').value = response;
            })
        }

        function selectFile() {
            pywebview.api.select_file().then((response)=>{
                //alert(response);
                document.getElementById('select_file_id').value = response;
            })
        }
        function testArgcs() {
            var arg1 = document.getElementById('input1_id').value;
            var arg2 = document.getElementById('input2_id').value;
            var arg3 = document.getElementById('input3_id').value;
            pywebview.api.test_argcs(arg1, arg2, arg3).then((response)=>{
                //alert(response);
            })
        }
    </script>
    </body>
    </html>
    '''


class Api:

    def select_dir(self):  # 选择目录
        result = window.create_file_dialog(webview.FOLDER_DIALOG)
        print(result)
        return result[0] if result else ''

    def select_file(self):  # 选择文件
        file_types = ('Image Files (*.bmp;*.jpg;*.gif;*.png)', 'All files (*.*)')
        result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types)
        print(result)
        return result[0] if result else ''

    def test_argcs(self, arg1, arg2, arg3):  # 测试传入多参数，模拟耗时请求
        print(arg1, arg2, arg3)
        import time
        time.sleep(0.3)

        return '返回结果：{0},{1},{2}'.format(arg1, arg2, arg3)

    def check_login(self, user, pwd):  # 用户登录接口
        print(user, pwd)
        if user != 'test' or pwd != 'test':
            return {'code': '4103', 'msg': '用户名或密码错误'}
        import time
        time.sleep(1)

        groups = {"首页": [], "业务菜单": ["3D模型", "画图展示", "业务3"], "系统设置": ["用户管理", "系统日志"]}
        roles = {"首页": ["读"], "3D模型": ["读", "写"], "业务2": ["读", "写"], "业务3": ["读", "写"], "用户管理": ["读", "写"], "系统日志": ["读", "写"]}

        return {'code': '0', 'data': {'groups': groups, 'roles': roles}, 'msg': 'ok'}

    def addItem(self, title):
        print(f'Added item {title}')

    def removeItem(self, item):
        print(f'Removed item {item}')

    def editItem(self, item):
        print(f'Edited item {item}')

    def toggleItem(self, item):
        print(f'Toggled item {item}')

    def toggleFullscreen(self):
        webview.windows[0].toggle_fullscreen()

    def load_page(self):
        file_url = 'file:///C:/Users/admin/workplace/github/pywebview/examples/todos/assets/hello.html'
        webview.windows[0].load_url(file_url)


def aa():
    api = Api()
    # js_api 获得 api 实例
    webview.create_window('Todos magnificos', 'assets/index.html', js_api=api, min_size=(600, 450))
    webview.start(debug=True)


def main():

    win = webview.create_window(
        title='百度一下,全是广告',
        url='http://www.baidu.com',
        width=1280,
        height=840,
        # resizable=True,  # 固定窗口大小
        text_select=False,  # 禁止选择文字内容
        confirm_close=True,  # 关闭时提示
        # html=None,
        # js_api=None,
        # x=None,
        # y=None,
        # fullscreen=False, # 以全屏模式启动
        # min_size=(200, 100),
        # hidden=False,
        # frameless=False,
        # easy_drag=True,
        # minimized=False,
        # on_top=False,
        # background_color='#FFFFFF',
        # transparent=False,
        # zoomable=False,
        # draggable=False,
        # vibrancy=False,
        # localization=None,
        # server=http.BottleServer,
        # server_args={},
    )

    api = Api()
    window = webview.create_window(
        title='pywebview+vue实现系统登录',
        url='static',
        width=900,
        height=620,
        resizable=True,  # 固定窗口大小
        text_select=False,  # 禁止选择文字内容
        confirm_close=True,  # 关闭时提示
        js_api=api,  # api中定义供html调用的函数
        min_size=(900, 620)  # 设置窗口最小尺寸
    )

    # 添加监听窗口事件
    # window.closed += on_closed
    # window.closing += on_closing
    # window.shown += on_shown
    # window.loaded += on_loaded

    # 启动窗口
    webview.start(localization=chinese, http_server=True)


def main2():

    from threading import Thread

    api = Api()

    def create_new_window():
        child_window = webview.create_window('#2', js_api=api, width=800, height=400)
        child_window.load_html('<h1>Child Window</h1>')

    # t = Thread(target=create_new_window)
    # t.start()
    # Master window
    Master_window = webview.create_window('#1', js_api=api, html=HTML, width=800, height=600)
    webview.start(localization=chinese)


def main3():

    # Create a gui window
    window = webview.create_window('My App', 'https://my-app.com/index.html')

    def my_function(window):
        ...
        # Do some processing here

    # Register the above function to be called when the window is closed
    # window.launch()
    # window.bind('close', my_function)

    # Run the window
    webview.start()


if __name__ == '__main__':
    ...
    main2()
