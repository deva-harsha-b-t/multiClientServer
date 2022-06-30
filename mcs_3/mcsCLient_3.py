import socket
import threading

PORT = 9090
SERVER = "192.168.56.1"
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "disconnect"
ADDR = (SERVER, PORT)

print("[--- client strted ---]")


def receive_message():
    while True:
        message = clientSocket.recv(HEADER).decode(FORMAT)
        print(message)


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(ADDR)
recv_thread = threading.Thread(target=receive_message, args=())


def send_mess(msg):
    message = msg.encode(FORMAT)
    clientSocket.send(message)

    # print(clientSocket.recv(HEADER).decode(FORMAT))


recv_thread.start()
mssg = input("")
while mssg != DISCONNECT_MESSAGE:
    send_mess(mssg)
    mssg = input("")
# start()
