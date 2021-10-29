import socket
import threading

from server_offline import ServerSocket


class Client:
    def __init__(self, app):
        self.app = app
        self.type = 'receiver'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 声明socket类型，同时生成链接对象
        self.host = socket.gethostbyname(socket.gethostname())
        self.pingTimes = 0
        self.isPing = True
        self.pingInterval = 60
        self.timer = threading.Timer(self.pingInterval, self.send_ping)

    def start(self):
        threading.Thread(target=self.run).start()

    def run(self):
        while True:
            try:
                self.client.connect(('zhude.guet.ltd', 12345))
                print("服务器已连接")
                self.send(self.type)
                break
            except ConnectionRefusedError:
                print("连接到远程服务器出错，尝试局域网……")
                try:
                    self.client.connect((self.host, 12345))
                    print("局域网已连接")
                except TimeoutError:
                    print("局域网内未运行服务端，正在作为服务端启动……")
                    self.start_server()
                    print("本机服务端启动")
                    continue
        try:
            while True:
                if self.app.win.type == 'receiver':
                    # print('等待接收...')
                    data = self.readline()
                    self.app.win.received.emit(data)
                    # print('接收:', data)
        finally:
            self.client.close()

    def readline(self, size: int = 32 * 1024):
        buf = b''
        while len(buf) < size:
            recv = self.client.recv(1)  # 接收一个信息，并指定接收的大小最大为1字节
            if len(recv) == 0:
                raise Exception("unexpected end of stream")
            buf += recv
            if buf[-1] == 10:
                break
        buf = buf[:-1]
        return buf.decode('utf8')

    def send(self, data):
        if type(data) == str:
            data = (data + '\n').encode('utf8')
        self.client.send(data)

    def start_server(self):
        server = ServerSocket(self.host, 12345)
        server.start()

    def send_ping(self):
        if self.isPing:
            print('ping')
            self.send('ping')
            self.timer = threading.Timer(self.pingInterval, self.send_ping)
            self.timer.start()

    def stop_ping(self):
        self.isPing = False

