import socket
import sys
import time

from utils import Utilities

FORMAT = "utf-8"
PING_CODE = "pingCheck"
utils = Utilities()

class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        self.sock.connect((self.host, self.port))
        self.running = False
        self.server_status = "up"
        self.server_down_cnt = 1

    def listen_to_clients(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen()

    def accept_connection(self):
        return self.sock.accept()

    def server_down_close(self):
        print("--- closing client ---\n3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        self.running = False
        sys.exit()

    def sendMessage(self, msg):
        self.sock.send(utils.post_req("msg", msg).encode())

    def recvFun(self):
        return self.sock.recv(1024).decode(FORMAT)

    def ping_(self):
        try:
            self.sock.send(PING_CODE.encode(FORMAT))
            time.sleep(5)
        except Exception as e:
            self.server_status = "down"
            self.server_down_close()

    def closeConn(self):
        self.sock.close()

    