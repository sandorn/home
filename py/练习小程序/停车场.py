import tkinter
from tkinter import messagebox

# 设置窗口居中


def window_info():
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - 200
    y = (hs / 2) - 200
    print("%d,%d" % (ws, hs))
    return x, y


# 设置登陆窗口属性
window = tkinter.Tk()
window.title('欢迎使用停车场收费系统')
a, b = window_info()
window.geometry("450x300+%d+%d" % (a, b))

# 登陆界面的信息
tkinter.Label(window, text="停车场收费系统", font=("宋体", 32)).place(x=80, y=50)
tkinter.Label(window, text="账号：").place(x=120, y=150)
tkinter.Label(window, text="密码：").place(x=120, y=190)
# 显示输入框
var_usr_name = tkinter.StringVar()
# 显示默认账号
var_usr_name.set('1400370101')
entry_usr_name = tkinter.Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=190, y=150)
var_usr_pwd = tkinter.StringVar()
# 设置输入密码后显示*号
entry_usr_pwd = tkinter.Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=190, y=190)


# 登陆函数
def usr_login():
    # 获取输入的账号密码
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    # 获取存储的账户信息，此处使用的是数据库，调用数据库查询函数，也可以使用其他方式，如文件等
    dicts = SQL.load('login')
    print(dicts)
    bool = False
    for row in dicts:
        print(row.get("name"))
    if usr_name == row["name"]:
        bool = True
        pwd = row["password"]
        print(row)
    if bool:
        if usr_pwd == pwd:
            tkinter.messagebox.showinfo(
                title='Welcome', message='How are you?' + usr_name)
            mainwindow()
        else:
            tkinter.messagebox.showerror(message='对不起，输入错误，请重试！')
    else:
        is_sign_up = tkinter.messagebox.askyesno('Welcome', '您还没有注册，是否现在注册呢？')
    if is_sign_up:
        usr_sign_up()


# 注册账号
def usr_sign_up():
    def sign_to_Pyhon():
        np = new_pwd.get()

    npc = new_pwd_confirm.get()
    nn = new_name.get()

    dicts = SQL.load('login')
    print(dicts)
    bool = False
    for row in dicts:
        if nn == row["name"]:
            bool = True
        print(row)
    if np != npc:
        tkinter.messagebox.showerror('对不起', '两次密码输入不一致！')
    elif bool:
        tkinter.messagebox.showerror(('对不起', '此账号已经存在!'))
    else:
        try:
            SQL.insert_login(str(nn), str(np))
            tkinter.messagebox.showinfo('Welcome', '您已经注册成功！')
        except BaseException:
            tkinter.messagebox.showerror(('注册失败!'))
            window_sign_up.destroy()

    # 创建top窗口作为注册窗口
    window_sign_up = tkinter.Toplevel(window)
    window_sign_up.geometry('350x200')
    window_sign_up.title('注册')

    new_name = tkinter.StringVar()
    new_name.set('1400370115')
    tkinter.Label(window_sign_up, text='账号:').place(x=80, y=10)
    entry_new_name = tkinter.Entry(window_sign_up, textvariable=new_name)
    entry_new_name.place(x=150, y=10)

    new_pwd = tkinter.StringVar()
    tkinter.Label(window_sign_up, text='密码:').place(x=80, y=50)
    entry_usr_pwd = tkinter.Entry(
        window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=150, y=50)

    new_pwd_confirm = tkinter.StringVar()
    tkinter.Label(window_sign_up, text='再次输入:').place(x=80, y=90)
    entry_usr_pwd_again = tkinter.Entry(
        window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_again.place(x=150, y=90)

    btn_again_sign_up = tkinter.Button(
        window_sign_up, text='注册', command=sign_to_Pyhon)
    btn_again_sign_up.place(x=160, y=130)


# 登陆和注册按钮
btn_login = tkinter.Button(window, text="登陆", command=usr_login)
btn_login.place(x=170, y=230)
btn_sign_up = tkinter.Button(window, text="注册", command=usr_sign_up)
btn_sign_up.place(x=270, y=230)

window.mainloop()
