import socket
import sys
import time

FORMAT = "utf-8"
PING_CODE = "pingCheck"

class Connection:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.running = False
        self.server_status = "up"
        self.server_down_cnt = 1

    def server_down_close(self):
        print("--- closing client ---\n3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        self.running = False
        sys.exit()

    def sendFun(self, data):
        self.sock.send(data.encode(FORMAT))

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

    