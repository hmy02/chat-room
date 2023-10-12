"""
# Author   : Huang Mingyi
# coding=utf-8
# @version : 1.0
# @Time    : 2022/5/31 21:00
# @File    : chat_client.py
# @Software: PyCharm
# @describe: 客户端
"""


import math
import socket

class ChatSocket:
    # 构造方法
    def __init__(self):
        print("初始化tcp客户端")
        self.client_socket = socket.socket()
        self.client_socket.connect(('127.0.0.1', 7777))

    # 请求登录类型
    def login_type(self, user_name, password):
        self.client_socket.sendall(bytes("1", "utf-8"))
        self.send_string_with_length(user_name)
        self.send_string_with_length(password)
        check_result = self.recv_string_by_length(1)
        return check_result

    # 请求注册类型
    def register_user(self, user_name, password):
        self.client_socket.sendall(bytes("2", "utf-8"))
        self.send_string_with_length(user_name)
        self.send_string_with_length(password)

        return self.recv_string_by_length(1)

    # 发送消息类型
    def send_message(self, message, chat_user):
        self.client_socket.sendall(bytes("3", "utf-8"))
        self.send_string_with_length(chat_user)
        self.send_string_with_length(message)

    # 发送刷新用户列表类型
    def send_refurbish_mark(self):
        self.client_socket.sendall(bytes("4", "utf-8"))

    # =============== 封装一些发送接受数据的方法 =================
    # 发送带长度的字符串
    def send_string_with_length(self, content):
        self.client_socket.sendall(bytes(content, encoding='utf-8').__len__().to_bytes(4, byteorder='big'))
        self.client_socket.sendall(bytes(content, encoding='utf-8'))

    # 获取服务器传来的定长字符串
    def recv_string_by_length(self, len):
        return str(self.client_socket.recv(len), "utf-8")

    # 获取服务端传来的变长字符串，这种情况下服务器会先传一个长度值
    def recv_all_string(self):
        length = int.from_bytes(self.client_socket.recv(4), byteorder='big')
        b_size = 3 * 1024
        times = math.ceil(length / b_size)
        content = ''
        for i in range(times):
            if i == times - 1:
                seg_b = self.client_socket.recv(length % b_size)
            else:
                seg_b = self.client_socket.recv(b_size)
            content += str(seg_b, encoding='utf-8')
        return content

    # 获取服务器发的在线用户人数
    def recv_number(self):
        return int.from_bytes(self.client_socket.recv(4), byteorder='big')
