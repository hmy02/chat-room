"""
# Author   : Guo JianZhou, Wu Linlin
# coding=utf-8
# @version : 1.0
# @Time    : 2022/5/30 20:00
# @File    : chat_main_panel.py
# @Software: PyCharm
# @describe: 聊天界面
"""


from tkinter import *
import tkinter.font as tf
import time

# 主界面类
class MainPanel:
    # 构造方法，参数为按钮事件处理函数，从客户端main传进来，可以实现按钮回调
    def __init__(self, user_name, send_message, refurbish_user, private_talk, close_main_window):
        self.user_name = user_name
        self.send_message = send_message
        self.refurbish_user = refurbish_user
        self.private_talk = private_talk
        self.close_main_window = close_main_window


    def show_main_panel(self):
        global main_frame


        # 创建主窗口
        main_frame = Tk()
        self.main_frame = main_frame
        self.main_frame.title("python聊天室")
        self.main_frame.configure(background="white")
        # 设置关闭主窗口的回调函数
        self.main_frame.protocol("WM_DELETE_WINDOW", self.close_main_window)
        width = 1300
        height = 700
        screen_width = self.main_frame.winfo_screenwidth()
        screen_height = self.main_frame.winfo_screenheight()
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height - 1.2 * height) / 2)
        self.main_frame.geometry(gm_str)
        self.main_frame.resizable(width=False, height=False)



        # 设置文本标签和位置
        self.label1 = Label(self.main_frame, text="    在线用户         python聊天室欢迎您：" + self.user_name + "   "
                                                                                                      "              "
                                                                                                      "      " +
                                                  "                           ", font=("黑体", 20), bg="white", fg="black")
        self.label1.grid(row=0, column=0, ipady=0, padx=0, columnspan=3, sticky=E+W)

        # 在线用户列表框
        friend_list_var = StringVar()
        # 设置列表框及位置
        self.friend_list = Listbox(self.main_frame, selectmode=NO, listvariable=friend_list_var,
                                   bg="gainsboro", fg="black", font=("宋体", 14),
                                   highlightcolor="gainsboro", selectbackground="gray")
        self.friend_list.grid(row=1, column=0, rowspan=3, sticky=N + S, padx=0, pady=(0, 0))
        self.friend_list.bind('<ButtonRelease-1>', self.private_talk)  # 绑定列表框点击事件

        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(1, weight=1)
        # 滚动条
        sc_bar = Scrollbar(self.main_frame)
        sc_bar.grid(row=1, column=0, sticky=N + S + E, rowspan=3, pady=(0, 3))

        # 列表框和滚动条的绑定
        sc_bar['command'] = self.friend_list.yview
        self.friend_list['yscrollcommand'] = sc_bar.set


        msg_sc_bar = Scrollbar(self.main_frame)
        msg_sc_bar.grid(row=1, column=1, sticky=E + N + S, padx=(0, 1), pady=1)

        # 显示消息的文本框
        self.message_text = Text(self.main_frame, bg="white", height=1,
                            highlightcolor="white", highlightthickness=1)
        self.message_text.config(state=DISABLED)
        self.message_text.grid(row=1, column=1, sticky=W + E + N + S, padx=(0, 15), pady=(0, 27))


        # 绑定消息框和消息框滚动条
        msg_sc_bar["command"] = self.message_text.yview
        self.message_text["yscrollcommand"] = msg_sc_bar.set

        # 设置发送消息框滚动条
        send_sc_bar = Scrollbar(self.main_frame)
        send_sc_bar.grid(row=2, column=1, sticky=E + N + S, padx=(0, 1), pady=1)

        # 发送消息框
        self.send_text = Text(self.main_frame, bg="white", height=11, highlightcolor="white",
                         highlightbackground="#444444", highlightthickness=0)
        self.send_text.see(END)
        self.send_text.grid(row=2, column=1, sticky=W + E + N + S, padx=(0, 15), pady=0)

        # 绑定发送消息框和发送消息框滚动条
        send_sc_bar["command"] = self.send_text.yview
        self.send_text["yscrollcommand"] = send_sc_bar.set


        # 设置发送消息按钮及位置，事件处理函数为send_message
        button1 = Button(self.main_frame, command=lambda: self.send_message(self), text="发送", bg="gainsboro",
                         fg="limegreen", width=13, height=2, font=('黑体', 12),)
        button1.place(x=650, y=640)

        # 设置关闭窗口按钮及位置，事件处理函数为close_main_window
        button2 = Button(self.main_frame, text="关闭", bg="white", fg="black", width=13, height=2,
                              font=('黑体', 12), command=self.close_main_window)
        button2.place(x=530, y=640)


        # 设置聊天记录按钮及位置，事件处理为create_window实例方法
        botton4 = Button(self.main_frame, command=self.create_window, text="聊天记录", relief=FLAT, bd=0)
        botton4.place(x=250, y=525)

        # 设置刷新用户列表按钮及位置，事件处理为refurbish_user函数
        botton5 = Button(self.main_frame, command=self.refurbish_user, text="刷新在线用户", bg="white", fg="black",
                         width=13, height=2, font=('黑体', 12),)
        botton5.place(x=40, y=650)


    # 调用定时器函数，执行循环mainloop显示界面实例方法
    def load(self):
        self.main_frame.mainloop()

    # 聊天记录按钮处理事件实例方法
    def create_window(self):
        top1 = Toplevel()  # 创建子窗口
        top1.configure(background="#FFFAFA")
        screen_width = top1.winfo_screenwidth()
        screen_height = top1.winfo_screenheight()
        width = 600
        height = 650
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height - 1.2 * height) / 2)
        top1.geometry(gm_str)
        top1.title("聊天记录")
        top1.resizable(width=False, height=False)

        # 设置文本标签
        title_lable = Label(top1, text="聊天记录", font=('粗斜体', 20, 'bold italic'),
                            fg="limegreen", bg="gainsboro")
        # 设置文本在窗口的位置
        title_lable.pack(ipady=10, fill=X)

        # 设置文本框，用户存放聊天记录信息
        self.chatting_records = Text(top1, bg="white", height=50, highlightcolor="white", highlightthickness=1)
        self.chatting_records.pack(ipady=10, fill=X)
        self.chatting_records.config(state=DISABLED)

        # 设置清除聊天记录按钮及位置，事件处理函数为clear_chatting_records实例方法
        botton = Button(top1,  text="清空聊天记录", command=self.clear_chatting_records, bg="white",
                        fg="black", width=12, height=2, font=('黑体', 11))
        botton.place(x=490, y=600)

        # 调用实例方法显示聊天记录
        self.show_chatting_records()

    # 显示聊天记录的实例方法
    def show_chatting_records(self):
        # 设置文本框可编辑
        self.chatting_records.config(state=NORMAL)
        f = open("chatting_records/" + self.user_name + ".txt", 'r')
        while True:
            content = f.readline()
            ft = tf.Font(family='微软雅黑', size=13)
            self.chatting_records.tag_config("tag_9", foreground="black", font=ft)
            if content != "":
                self.chatting_records.insert(END, content, 'tag_9')
            else:
                self.chatting_records.config(state=DISABLED)  # 设置文本不可编辑
                return

    # 清除聊天记录按钮处理实例方法
    def clear_chatting_records(self):
        # 设置文本框可编辑
        self.chatting_records.config(state=NORMAL)
        self.chatting_records.delete('1.0', END)
        a = open("chatting_records/" + self.user_name + ".txt",
                 'w')
        a.write("")
        a.close()
        self.chatting_records.config(state=DISABLED)  # 设置文本不可编辑

    # 保存聊天记录实例方法
    def sava_chatting_records(self, content):
        a = open("chatting_records/" + self.user_name + ".txt", 'a')
        a.write(content)
        a.close()


    # 刷新在线列表实例方法
    def refresh_friends(self, online_number, names):
        self.friend_list.delete(0, END)
        for name in names:
            self.friend_list.insert(0, name)
        self.friend_list.insert(0, "【群聊】")
        self.friend_list.itemconfig(0, fg="black")
        self.friend_list.insert(0, '在线用户数: ' + str(online_number))
        self.friend_list.itemconfig(0, fg="black")

    # 在界面显示消息的实例方法
    # 接受到消息，在文本框中显示，自己的消息用绿色，别人的消息用灰色
    def show_send_message(self, user_name, content, chat_flag):
        self.message_text.config(state=NORMAL)   # 设置消息框可编辑
        title = user_name + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
        if content == '* 系统提示: ' + user_name + ' 加入聊天室':
            ft = tf.Font(family='微软雅黑', size=13)
            self.message_text.tag_config("tag_1", foreground="red", font=ft)
            self.message_text.insert(END, content + "\n", 'tag_1')
            self.message_text.config(state=DISABLED)
        elif content == '* 系统提示: ' + user_name + ' 已离开群聊':
            ft = tf.Font(family='微软雅黑', size=13)
            self.message_text.tag_config("tag_2", foreground="red", font=ft)
            self.message_text.insert(END, content + "\n", 'tag_2')
            self.message_text.config(state=DISABLED)
        elif user_name == self.user_name:
            if chat_flag == "group_chat":  # 如果标记是群聊标记，则自己的消息用绿
                ft = tf.Font(family='微软雅黑', size=13)
                self.message_text.tag_config("tag_4", foreground="green", font=ft)
                self.message_text.insert(END, title, 'tag_4')
                self.sava_chatting_records(title)   # 调用实例方法保存聊天记录
            elif chat_flag == "private_chat":  # 如果是标记是私聊，则消息用浅绿
                ft = tf.Font(family='微软雅黑', size=13)
                self.message_text.tag_config("tag_5", foreground="lime", font=ft)
                self.message_text.insert(END, title, 'tag_5')
                self.sava_chatting_records(title)
        else:  #  如果发送消息的用户不是自己
            if chat_flag == "group_chat":  # 如果标记是群聊，则消息用灰
                ft = tf.Font(family='微软雅黑', size=13)
                self.message_text.tag_config("tag_6", foreground="dimgray", font=ft)
                self.message_text.insert(END, title, 'tag_6')
                self.sava_chatting_records(title)
            elif chat_flag == "private_chat":  # 标记是私聊，则消息用浅灰
                ft = tf.Font(family='微软雅黑', size=13)
                self.message_text.tag_config("tag_7", foreground="darkgray", font=ft)
                self.message_text.insert(END, title, 'tag_7')
                self.sava_chatting_records(title)
        if content != '* 系统提示: ' + user_name + ' 加入聊天室' and content != '* 系统提示: ' + user_name + ' 已离开群聊':
            time.sleep(0.5)
            ft = tf.Font(family='微软雅黑', size=15)
            self.message_text.tag_config("tag_8", foreground="black", font=ft)
            self.message_text.insert(END, content, 'tag_8')
            self.message_text.config(state=DISABLED)
            self.message_text.see(END)
            self.sava_chatting_records(content)
            self.sava_chatting_records("------------------------------------------------------------------------------\n")

    # 群聊私聊改变标签的实例方法
    def change_title(self, title):
        self.label1['text'] = title

    # 清空发送消息输入框的实例方法
    def clear_send_text(self):
        self.send_text.delete('0.0', END)

    # 获取消息输入框内容的实例方法
    def get_send_text(self):
        return self.send_text.get('0.0', END)
