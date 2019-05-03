# ！/usr/bin/env python
# -*-coding:utf-8-*-
'''
@Software:   VSCode
@File    :   sct.py
@Time    :   2019/04/24 10:51:26
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
'''

import sciter
import time
import threading
import ctypes

ctypes.windll.user32.SetProcessDPIAware(2)
'''def run(self):
    while 1:
        time.sleep(2)
        # 调用html中方法
        self.eval_script('hello("42");')'''


class Frame(sciter.Window):

    def __init__(self):
        super().__init__(ismain=True, uni_theme=True)
        pass

    @sciter.script
    def PythonCall(self, arg):
        print("参数：", str(arg))
        return "通信成功了，返回值：" + str(arg) + ' -_-'

    @sciter.script
    def inti(self):
        # 启动独立的线程
        t = threading.Thread(target=run, args=(self,))
        t.start()


if __name__ == '__main__':
    import os
    htm = os.path.join(os.path.dirname(__file__), 'sct.html')
    #phtml文件编码格式必须 Unix(LF) UTF-8-BOM 以防止中文乱码
    frame = Frame()
    frame.load_file(htm)
    frame.run_app()
    frame.PythonCall("参数")
    array = (1, 2, 3, 4, 5, 6, 7, 9)
    for index in enumerate(array):
        frame.eval_script('hello(' + index + ');')
