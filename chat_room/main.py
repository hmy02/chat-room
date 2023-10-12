"""
# Author   : Huang Mingyi
# coding=utf-8
# @version : 1.0
# @Time    : 2022/5/31 21:00
# @File    : main.py
# @Software: PyCharm
# @describe: 主函数
"""


from tkinter import messagebox
import threading
import time

import chat_register_panel
import chat_main_panel
import chat_login_panel
import chat_client

chat_user = "【群聊】"


# 关闭socket函数
def close_socket():
    print("尝试断开socket连接")
    client.client_socket.close()


# 关闭登陆界面函数
def close_login_window():
    close_socket()
    login_frame.login_frame.destroy()


# 关闭聊天界面函数
def close_main_window():
    client.send_message("exit", chat_user)
    close_socket()
    main_frame.main_frame.destroy()


# 处理私聊功能函数
def private_talk(self):
    global chat_user
    indexs = main_frame.friend_list.curselection()
    index = indexs[0]
    if index > 0:
        chat_user = main_frame.friend_list.get(index)
        if chat_user == '【群聊】':
            title = "    在线用户         python聊天室欢迎您：" + main_frame.user_name + "                       " + \
            "                           "
            main_frame.change_title(title)
        elif chat_user == main_frame.user_name:
            messagebox.showwarning(title="提示", message="自己不能和自己进行对话!")
            chat_user = '【群聊】'
        else:
            title = "                                " + main_frame.user_name + "  私聊 -> " + chat_user + \
                    "                                                    "
            main_frame.change_title(title)

# 登录按钮处理事件函数
def handding_login(self):
    user_name, password = login_frame.get_input()
    if user_name == "":
        messagebox.showwarning(title="提示", message="用户名不能为空")
        return
    if password == "":
        messagebox.showwarning(title="提示", message="密码不能为空")
        return
    if client.login_type(user_name, password) == "1":
        go_to_main_panel(user_name)
    else:
        messagebox.showwarning(title="提示", message="用户名或密码错误！")

# 登陆界面注册按钮处理事件函数
def handding_register():
    login_frame.close_login_panel()
    global register_frame
    register_frame = chat_register_panel.RegisterPanel(close_register_window, register_submit)
    register_frame.show_register_panel()
    register_frame.load()

# 关闭注册界面函数
def close_register_window():
    register_frame.close_register_panel()
    global login_frame
    login_frame = chat_login_panel.LoginPanel(handding_login, handding_register, close_login_window)
    login_frame.show_login_panel()
    login_frame.load()

# 注册界面注册按钮处理事件函数
def register_submit(self):
    user_name, password, confirm_password = register_frame.get_input()
    if user_name == "" or password == "" or confirm_password == "":
        messagebox.showwarning("不能为空", "请完成注册表单")
        return
    if not password == confirm_password:
        messagebox.showwarning("错误", "两次密码输入不一致")
        return

    result = client.register_user(user_name, password)
    if result == "1":
        messagebox.showinfo("成功", "注册成功")
        close_register_window()
    elif result == "0":
        messagebox.showerror("错误", "该用户名已被注册")
    else:
        messagebox.showerror("错误", "发生未知错误")

# 发送消息按钮处理事件函数
def send_message(self):
    global chat_user
    print("send message:")
    content = main_frame.get_send_text()
    if content == "" or content == "\n":
        messagebox.showwarning(title="提示", message="空消息，拒绝发送")
        return
    print(content)
    main_frame.clear_send_text()
    client.send_message(content, chat_user)


# 刷新用户列表按钮处理事件函数
def refurbish_user():
    client.send_refurbish_mark()

# 关闭登陆界面前往主界面
def go_to_main_panel(user_name):
    login_frame.close_login_panel()
    global main_frame
    main_frame = chat_main_panel.MainPanel(user_name, send_message, refurbish_user, private_talk, close_main_window)
    threading.Thread(target=recv_data).start()
    main_frame.show_main_panel()
    main_frame.load()

# 处理消息接收的线程方法
def recv_data():
    time.sleep(1)
    while True:
        try:
            data_type = client.recv_all_string()
            print("recv type: " + data_type)
            # 获取当前在线用户列表
            if data_type == "#!onlinelist#!":
                print("获取在线列表数据")
                online_list = list()
                online_number = client.recv_number()
                for n in range(online_number):
                    online_list.append(client.recv_all_string())
                main_frame.refresh_friends(online_number, online_list)
                print(online_list)
            elif data_type == "#!message#!":
                print("获取新消息")
                chat_flag = client.recv_all_string()
                user = client.recv_all_string()
                print("user: " + user)
                content = client.recv_all_string()
                print("message: " + content)
                main_frame.show_send_message(user, content, chat_flag)
        except Exception as e:
            print("接受服务器消息出错，消息接受子线程结束。" + str(e))
            break

#  前往登录界面，同时开启客户端口连接连接服务器的函数
def go_to_login_panel():
    global client
    client = chat_client.ChatSocket()
    global login_frame
    login_frame = chat_login_panel.LoginPanel(handding_login, handding_register, close_login_window)
    login_frame.show_login_panel()
    login_frame.load()

# 入口
if __name__ == "__main__":
    go_to_login_panel()   # 调用此类的前往登录界面函数