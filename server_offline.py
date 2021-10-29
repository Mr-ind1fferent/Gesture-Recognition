import socket
from threading import *
from typing import List


class ServerSocket(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.HOST = host
        self.PORT = port
        self.clients: List[ClientServer] = []
        self.controller_stack = []

    def run(self):
        ss = socket.socket()  # 创建 socket 对象
        ss.bind((self.HOST, self.PORT))  # 绑定端口
        ss.listen(10)  # 等待客户端连接，最大等待数量10
        print("服务端已启动")

        while True:
            (socket_to_client, addr) = ss.accept()  # 建立客户端连接
            cs = ClientServer(socket_to_client, addr, self)
            cs.start()

    def push(self, name: str):
        if name in [c.name for c in self.clients]:
            if (not self.controller_stack) or self.controller_stack[-1] != name:  # 如果栈为空或栈顶不是自己
                self.controller_stack.append(name)
        # top()

    def pop(self):
        if len(self.controller_stack) > 1:
            self.controller_stack.pop()
            if self.controller_stack[-1] not in [c.name for c in self.clients]:  # 检查出栈后栈顶人是否还在线
                self.pop()  # 不在线则递归出栈
        else:
            self.controller_stack.clear()  # 最后一个控制者退出，清空栈
        # top()

    def top(self):
        for c in self.clients:
            c.try_send('change_controller ' + (self.controller_stack[-1] if self.controller_stack else ' '))


class ClientServer(Thread):
    def __init__(self, ss, addr, server):
        Thread.__init__(self)
        self.server = server
        self.socket = ss
        self.addr = addr
        self.type = 'unknown'
        self.name = ''
        self.controlling = False
        self.clients = self.server.clients
        self.controller_stack = self.server.controller_stack

    def read(self, size: int):
        buf = b''
        while len(buf) < size:
            buf += self.socket.recv(size - len(buf))
        return buf

    def readline(self, size: int = 32 * 1024):
        buf = b''
        while len(buf) < size:
            buf += self.socket.recv(1)  # 接收一个信息，并指定接收的大小最大为1字节
            if buf[-1] == 10:
                break
        buf = buf[:-1]
        return buf.decode('utf8')

    def run(self):
        try:
            self.handle()
        finally:
            if self.controlling:
                self.server.pop()
            if self in self.clients:
                self.clients.remove(self)
            self.get_list()
            self.socket.close()  # 关闭这个链接
            print("已关闭链接：" + self.name)

    def handle(self):
        print('client connected', self.addr)

        firstLine = self.readline()
        if firstLine == "receiver":
            self.type = 'receiver'
            print("接收者接入")
        elif firstLine == "controller":
            self.type = 'controller'
            self.controlling = True
            print("控制者接入")
        else:
            self.socket.send(b'Who are you?')
            return

        self.name = self.readline()
        if not self.is_name_useable(self.name):
            self.try_send("duplicate_name")
            print("拒绝重名用户加入：", self.name)
            return
        print(self.name, "已加入会议")
        self.clients.append(self)
        self.get_list()

        while True:
            # 接收
            line: str = self.readline()
            print(self.addr, line)
            splits = line.split(' ')
            if splits[0] == 'command':
                if self.type == 'receiver' or not self.controlling:  # 如果自己是接收者则不发送
                    continue
                # 发送给每个接收者
                self.send_to_receiver(line)
            elif splits[0] == 'exchange_control':
                self.exchange_control()
            elif splits[0] == 'switch_control':
                self.switch_control()
            else:
                print('Unknown message:', line)

    def get_list(self):
        member_list = 'member_list ' + ' '.join([c.name for c in self.clients])
        for c in self.clients:
            c.try_send(member_list)

    def is_name_useable(self, name):
        for c in self.clients:
            if c.name == name:
                return False
        return True

    def exchange_control(self):
        if self.type == 'receiver':
            print("接收者入栈")
            self.server.push(self.name)
            for c in self.clients:
                if c.type == 'controller':
                    c.type = 'receiver'
            self.type = 'controller'
            self.controlling = True
        elif self.type == 'controller':
            print("控制者出栈")
            self.server.pop()
            self.type = 'receiver'
            self.controlling = False
            if self.controller_stack:
                for c in self.clients:
                    if c.name == self.controller_stack[-1]:
                        c.type = 'controller'
                        c.controlling = True

        self.server.top()
        # for c in self.clients:
        #     if c.type == 'receiver':
        #         c.controlling = False

        print(self.controller_stack)

    def switch_control(self):
        if self.type == 'controller':
            for c in self.clients:
                c.try_send(('control_switched ' + self.name))

    def send_to_receiver(self, msg: str):
        print("搜索并发送给接收者...")
        for c in self.clients:
            if c.type == 'receiver':
                c.try_send(msg)

    def send(self, data):
        if type(data) == str:
            data = (data + '\n').encode('utf8')
        self.socket.send(data)

    def try_send(self, data):
        try:
            self.send(data)
        except Exception as e:
            print("尝试发送时发生错误", e)
