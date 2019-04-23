import tkinter.messagebox as messagebox
from tkinter import *

import db


class LoginPage:
    """登录界面"""

    def __init__(self, master):
        self.root = master
        self.root.geometry('400x200+600+400')
        self.root.title('保险计划书Alpha0.1')
        self.conn = db.MysqlHelp()
        self.手机 = StringVar()
        self.密码 = StringVar()
        self.page = Frame(self.root)
        self.creatapage()

    def creatapage(self):
        """界面布局"""
        Label(self.page).grid(row=0)
        Label(self.page, text='手机号:').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.手机).grid(row=1, column=1, stick=E)
        Label(self.page, text='密码:').grid(row=2, stick=W, pady=10)
        Entry(
            self.page, textvariable=self.密码, show='*').grid(
                row=2, stick=E, column=1)
        Button(
            self.page, text='登录', command=self.login).grid(
                row=3, stick=W, pady=10)
        Button(
            self.page, text='注册账号', command=self.register).grid(
                row=3, stick=E, column=1)
        self.page.pack()

    def login(self):
        """登录功能"""
        query = "select 手机, 密码,登陆次数 from users where 手机='%s'" % self.手机.get()
        c = self.conn.getall(query)  # 返回一个迭代器
        if len(c) == 0:
            messagebox.showerror('登录失败', '手机号不存在')
        else:
            us, pw, lerror = c[0]
            if int(lerror) >= 3:
                messagebox.showwarning('登录失败', '手机号已被锁定')
            elif us == self.手机.get() and pw == self.密码.get():
                #self.conn.close()
                messagebox.showinfo('登录成功', '欢迎：%s' % us)
            else:
                messagebox.showwarning('登录失败', '密码错误')

    def register(self):
        """注册功能跳转"""
        self.conn.close()
        self.page.destroy()
        RegisterPage(self.root)


class RegisterPage:
    """注册界面"""

    def __init__(self, master=None):
        self.root = master
        self.root.title('账号注册')
        self.root.geometry('400x250')
        self.conn = db.MysqlHelp()
        self.手机 = StringVar()
        self.密码0 = StringVar()  # 第一次输入密码
        self.密码1 = StringVar()  # 第二次输入密码
        self.email = StringVar()
        self.page = Frame(self.root)
        self.createpage()

    def createpage(self):
        """界面布局"""
        Label(self.page).grid(row=0)
        Label(self.page, text="手机:").grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.手机).grid(row=1, column=1, stick=E)
        Label(self.page, text="密码:").grid(row=2, stick=W, pady=10)
        Entry(
            self.page, textvariable=self.密码0, show='*').grid(
                row=2, column=1, stick=E)
        Label(self.page, text="再次输入:").grid(row=3, stick=W, pady=10)
        Entry(
            self.page, textvariable=self.密码1, show='*').grid(
                row=3, column=1, stick=E)
        Button(
            self.page, text="返回", command=self.repage).grid(
                row=5, stick=W, pady=10)
        Button(
            self.page, text="注册", command=self.register).grid(
                row=5, column=1, stick=E)
        self.page.pack()

    def repage(self):
        """返回登录界面"""
        self.page.destroy()
        self.conn.close()
        LoginPage(self.root)

    def register(self):
        """注册"""
        if self.密码0.get() != self.密码1.get():
            messagebox.showwarning('错误', '密码核对错误')
        elif len(self.手机.get()) == 0 or len(self.密码0.get()) == 0:
            messagebox.showerror("错误", "不能为空")
        else:
            str1 = "insert into users(手机, 密码) values('{}','{}','{}')".format(
                self.手机.get(), self.密码0.get())
            rel = self.conn.workon(str1)
            if rel:
                messagebox.showinfo("成功", "注册成功，按确定返回登录界面")
                self.page.destroy()
                LoginPage(self.root)
            else:
                messagebox.showerror("注册失败", e)


def L():
    root = Tk()
    LoginPage(root)
    root.mainloop()


if __name__ == '__main__':
    L()
