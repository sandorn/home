# -*- coding: utf-8 -*-
# -*- coding: cp936 -*-

import getpass
import tkinter as tk
import time
import datetime
from tkinter import messagebox

"""
1.输入用户名密码
2.认证成功后显示欢迎信息
3.输错三次后锁定
"""

count = 0


def tick():
	global time1
	# 从运行程序的计算机上面获取当前的系统时间
	time2 = time.strftime('%Y-%m-%d %H:%M:%S')
	# 如果时间发生变化，代码自动更新显示的系统时间
	if time2 != time1:
		time1 = time2
		clock.config(text=time2)
	# calls itself every 200 milliseconds
	# to update the time display as needed
	# could use >200 ms, but display gets jerky
	clock.after(200, tick)


def handler():
	'''事件处理函数'''
	global count
	global t1, t2
	username = entry.get()
	password = entry2.get()

	if count > 3:
		t2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		t2 = datetime.datetime.strptime(t2, '%Y-%m-%d %H:%M:%S')
		dateline = datetime.timedelta(seconds=12, minutes=0, hours=0)
		if (dateline - (t2 - t1)).days == 0:
			print(u'密码输入错误超过3次，该账号已被锁定，请'),
			print
			dateline - (t2 - t1),
			print(u'小时之后再试')
			var = '密码输入错误超过3次，该账号已被锁定，请' + str(dateline - (t2 - t1)) + '小时之后再试'
			tk.messagebox.showwarning('警告', var)
		if (dateline - (t2 - t1)).days < 0:
			count = 0
			print(u'账号锁定已解除，请输入正确的账号密码！')
			tk.messagebox.showwarning('警告', '账号锁定已解除，请输入正确的账号密码！')

	else:
		if username == '' and password == '':
			tk.messagebox.showinfo('警告', '账号和密码不能为空')
		elif username == '' and password != '':
			tk.messagebox.showinfo('警告', '账号不能为空')
		elif username != '' and password == '':
			tk.messagebox.showinfo('警告', '密码不能为空')
		else:
			if username == 'Navy' and password == '9527':
				print(u'欢迎 Navy')
				window.destroy()
				tk.messagebox.showinfo('主页面', '欢迎 Navy')

			else:

				count += 1

				if count == 1:
					print(u'密码输入错误，请重新输入！')
					print('再输错%d次该账号将被锁定' % (3 - count))
					tk.messagebox.showwarning('警告', '密码输入错误，请重新输入！再输错2次该账号将被锁定！')

				if count == 2:
					print(u'密码输入错误，请重新输入！')
					print('再输错%d次该账号将被锁定' % (3 - count))
					tk.messagebox.showwarning('警告', '密码输入错误，请重新输入！再输错1次该账号将被锁定！')

				if count == 3:
					t1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
					t1 = datetime.datetime.strptime(t1, '%Y-%m-%d %H:%M:%S')
					print(u'密码输入错误超过3次，该账号已被锁定，请24小时之后再试')
					tk.messagebox.showwarning('警告', '密码输入错误超过3次，该账号已被锁定，请24小时之后再试')
					count = count + 1


if __name__ == '__main__':
	window = tk.Tk()
	window.title('个人网上银行登录')  # 标题
	window.geometry('320x200')  # 窗体大小
	window.resizable(False, False)  # 固定窗体

	frame1 = tk.Frame(window)
	frame2 = tk.Frame(window)
	frame3 = tk.Frame(window)

	userNameLabel = tk.Label(frame1, text="账号：", fg='green')
	userNameLabel.pack(side=tk.LEFT)

	passWordLabel = tk.Label(frame2, text="密码：", fg='green')
	passWordLabel.pack(side=tk.LEFT)

	entry = tk.Entry(frame1)
	entry.pack(side=tk.RIGHT)

	entry2 = tk.Entry(frame2, show='*')
	entry2.pack(side=tk.RIGHT)

	# 通过中介函数handlerAdapotor进行command设置
	btn = tk.Button(frame3, text=u'安全登录', command=handler, fg='blue')
	btn.pack(side=tk.BOTTOM)

	time1 = ''
	clock = tk.Label(window, font=('times', 10, 'bold'), fg='blue')
	clock.pack(side=tk.BOTTOM)
	tick()

	frame1.pack(fill=tk.Y, expand=tk.YES)
	frame2.pack(fill=tk.Y, expand=tk.NO)
	frame3.pack(fill=tk.NONE, expand=tk.YES)
	window.mainloop()