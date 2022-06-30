import socket

PORT = 9090
SERVER = "192.168.56.1"
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "disconnect"
ADDR = (SERVER, PORT)

print("[--- client strted ---]")

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(ADDR)


def send_mess(msg):
    message = msg.encode(FORMAT)
    clientSocket.send(message)
    print(clientSocket.recv(HEADER).decode(FORMAT))


mssg = input("Enter message: ")
while mssg != DISCONNECT_MESSAGE:
    send_mess(mssg)
    mssg = input("Enter message: ")
# start()
