from __future__ import annotations

import ttkbootstrap as ttk

window = ttk.Window(themename='minty')
entry = ttk.Entry(window)
btn = ttk.Button(window, text='提交', command=lambda: print(entry.get()))
# 创建输入框
entry = ttk.Entry(window)
entry.pack(pady=10)
btn.pack(pady=10)
# 创建自定义样式
style = ttk.Style()
style.configure('Custom.TButton', font=('Helvetica', 12, 'bold'), foreground='blue')

# 使用自定义样式的按钮
button = ttk.Button(window, text='Styled Button', style='Custom.TButton')
button.pack(pady=10)


# 创建一个函数来更改主题
def change_theme():
    window.set = 'darkly'


# 添加一个按钮来切换主题
button = ttk.Button(window, text='Change Theme', command=change_theme)
button.pack(pady=20)
window.mainloop()
