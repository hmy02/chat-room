"""
# Author   : Huang Mingyi
# coding=utf-8
# @version : 1.0
# @Time    : 2022/5/31 21:00
# @File    : chat_Server.py
# @Software: PyCharm
# @describe: 服务端
"""


import socket
from threading import Thread
import math
import chat_mysql


online_connection = list()

connection_user = dict()
join_user = ""
flag = 0
chat_user = ""

# 发送带长度的字符串的函数
def send_string_with_length(_conn, content):
    _conn.sendall(bytes(content, encoding='utf-8').__len__().to_bytes(4, byteorder='big'))
    _conn.sendall(bytes(content, encoding='utf-8'))

# 发送在线用户数的函数
def send_number(_conn, number):
    _conn.sendall(int(number).to_bytes(4, byteorder='big'))

# 获取变长字符串的函数
def recv_all_string(connection):
    length = int.from_bytes(connection.recv(4), byteorder='big')
    b_size = 3 * 1024
    times = math.ceil(length / b_size)
    content = ''
    for i in range(times):
        if i == times - 1:
            seg_b = connection.recv(length % b_size)
        else:
            seg_b = connection.recv(b_size)
        content += str(seg_b, encoding='utf-8')
    return content

# 检查用户名密码是否正确函数
def check_user(user_name, password):
    return chat_mysql.LogInformation.login_check(user_name, password)

# 添加用户函数
def add_user(user_name, password):
    if chat_mysql.LogInformation.select_user_name(user_name) == "1":
        return "0"
    elif chat_mysql.LogInformation.create_new_user(user_name, password) == "0":
        return "1"
    else:
        return "2"

# 处理刷新列表的请求函数
def handle_online_list():
    for con in online_connection:
        send_string_with_length(con, "#!onlinelist#!")
        send_number(con, online_connection.__len__())
        for c in online_connection:
            send_string_with_length(con, connection_user[c])
    return True

# 处理登录请求函数
def handle_login(connection, address):
    global join_user
    global flag
    user_name = recv_all_string(connection)
    password = recv_all_string(connection)
    check_result = check_user(user_name, password)
    if check_result:
        connection.sendall(bytes("1", "utf-8"))
        connection_user[connection] = user_name
        join_user = user_name
        flag = 1
        online_connection.append(connection)
        handle_online_list()
        handle_message(connection, address)
    else:
        connection.sendall(bytes("0", "utf-8"))
    return True

# 处理注册请求函数
def handle_register(connection, address):
    user_name = recv_all_string(connection)
    password = recv_all_string(connection)
    connection.sendall(bytes(add_user(user_name, password), "utf-8"))
    return True

# 处理消息发送请求函数
def handle_message(connection, address):
    global flag
    global chat_user
    if flag == 1:
        for c in online_connection:
            send_string_with_length(c, "#!message#!")
            send_string_with_length(c, "group_chat")
            send_string_with_length(c, connection_user[connection])
            content = '* 系统提示: ' + connection_user[connection] + ' 加入聊天室'
            send_string_with_length(c, content)
    else:
        chat_user = recv_all_string(connection)
        content = recv_all_string(connection)
        if content == "exit":
            for c in online_connection:
                send_string_with_length(c, "#!message#!")
                send_string_with_length(c, "group_chat")
                send_string_with_length(c, connection_user[connection])
                send_string_with_length(c, '* 系统提示: ' + connection_user[connection] + ' 已离开群聊')
        else:
             if chat_user == "【群聊】":
                for c in online_connection:
                    send_string_with_length(c, "#!message#!")
                    send_string_with_length(c, "group_chat")
                    send_string_with_length(c, connection_user[connection])
                    send_string_with_length(c, content)
             else:
                 for c in online_connection:
                     if connection_user[c] == chat_user:
                         send_string_with_length(c, "#!message#!")
                         send_string_with_length(c, "private_chat")
                         send_string_with_length(c, connection_user[connection])
                         send_string_with_length(c, content)
                         send_string_with_length(connection, "#!message#!")
                         send_string_with_length(connection, "private_chat")
                         send_string_with_length(connection, connection_user[connection])
                         send_string_with_length(connection, content)
    flag = 0
    return True

# 处理请求线程的执行函数
def handle(connection, address):
    try:
        while True:
            request_type = str(connection.recv(1024).decode())
            no_go = True
            if request_type == "1":
                print("开始处理登录请求")
                # 调用函数处理请求
                no_go = handle_login(connection, address)
            elif request_type == "2":
                print("开始处理注册请求")
                no_go = handle_register(connection, address)
            elif request_type == "3":
                print("开始处理发送消息请求")
                no_go = handle_message(connection, address)
            elif request_type == "4":
                print("开始处理刷新列表请求")
                no_go = handle_online_list()
            if not no_go:
                break
    except Exception as e:
        print(str(address) + " 连接异常，准备断开: " + str(e))
    finally:
        try:
            connection.close()
            online_connection.remove(connection)
            connection.pop(connection)
        except:
            print(str(address) + "连接关闭异常")

# 入口
if __name__ == "__main__":
    try:
        server = socket.socket()
        server.bind(('127.0.0.1', 7777))
        # 最大挂起数
        server.listen(10)
        print("服务器启动成功，开始监听...")
        while True:
            connection, address = server.accept()
            Thread(target=handle, args=(connection, address)).start()
    except Exception as e:
        print("服务器出错: " + str(e))
