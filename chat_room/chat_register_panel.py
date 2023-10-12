"""
# Author   : Guo JianZhou
# coding=utf-8
# @version : 1.0
# @Time    : 2022/5/30 20:00
# @File    : chat_register_panel.py
# @Software: PyCharm
# @describe: 注册界面
"""


from tkinter import *

# 注册界面类
class RegisterPanel(object):
    # 构造方法，参数为按钮事件处理函数，从客户端main传进来，可以实现按钮回调
    def __init__(self, close_register_window, register_submit):
        self.close_register_window = close_register_window
        self.register_submit = register_submit

    # 显示注册界面的实例方法
    def show_register_panel(self):
        global register_frame


        # 创建主窗口
        self.register_frame = Tk()
        register_frame = self.register_frame
        self.register_frame.configure(background="white")
        screen_width = self.register_frame.winfo_screenwidth()
        screen_height = self.register_frame.winfo_screenheight()
        width = 503
        height = 400
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height - 1.2 * height) / 2)
        self.register_frame.geometry(gm_str)
        self.register_frame.title("注册")
        self.register_frame.resizable(width=False, height=False)





        # 设置文本标签及位置
        Label(self.register_frame, text="用户名：", font=("宋体", 12), bg="white", fg="black") \
            .place(x=60, y=230)
        Label(self.register_frame, text="密  码：", font=("宋体", 12), bg="white", fg="black") \
            .place(x=60, y=260)
        Label(self.register_frame, text="确认密码：", font=("宋体", 12), bg="white", fg="black") \
            .place(x=60, y=290)

        # 声明用户名，密码，确认密码变量
        self.user_name = StringVar()
        self.password = StringVar()
        self.confirm_password = StringVar()

        # 设置输入文本框和位置，用于获取用户的输入
        Entry(self.register_frame, textvariable=self.user_name, fg="black", width=30) \
            .place(x=140, y=230)
        Entry(self.register_frame, textvariable=self.password, show="*", fg="black", width=30) \
            .place(x=140, y=260)
        Entry(self.register_frame, textvariable=self.confirm_password, show="*", fg="black", width=30) \
            .place(x=140, y=290)

        # 设置退出注册页面按钮及位置，按钮事件为close_register_window函数
        self.botton_quit = Button(self.register_frame, text="返回",  relief=FLAT, bg='white', fg="grey",
                               font=('黑体', 15), command=self.close_register_window).place(x=0, y=370)

        self.register_frame.bind('<Return>', self.register_submit)  # 绑定注册按钮回车事件
        # 设置注册按钮及位置，按钮事件为register.submit函数
        self.botton_register = Button(self.register_frame, text="立即注册", bg="gainsboro", fg="limegreen", width=27, height=2,
                              font=('黑体', 15), command=lambda: self.register_submit(self)).place(x=120, y=330)

    # 调用定时器函数，执行循环mainloop显示界面实例方法
    def load(self):
        self.register_frame.mainloop()

    # 关闭注册界面实例方法
    def close_register_panel(self):
        if self.register_frame == None:
            print("未显示界面")
        else:
            self.register_frame.destroy()

    # 获取输入的用户名、密码、确认密码实例方法
    def get_input(self):
        return self.user_name.get(), self.password.get(), self.confirm_password.get()
