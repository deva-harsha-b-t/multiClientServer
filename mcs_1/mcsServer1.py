import socket
import threading

PORT = 9090
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "disconnect"
DEFAULT_RESPONSE = "hello from server"

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(ADDR)


def send_mess(conn, msg):
    message = msg.encode(FORMAT)
    try:
        conn.send(message)
        return 0
    except BrokenPipeError:
        return -1


def handle_conn(conn, addr):
    print(f"[connection : {addr} connected]")

    connected = True
    while connected:
        mess_ = conn.recv(HEADER).decode(FORMAT)
        if mess_:
            if mess_ == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {mess_}")
        # mssg = input("Enter message: ")
        if send_mess(conn, DEFAULT_RESPONSE) == -1:
            print(f"client {addr} disconnected")
            break
    conn.close()


def start():
    serverSocket.listen()
    print(f"[Server {SERVER} is listening]")
    while True:
        conn, addr = serverSocket.accept()
        thread = threading.Thread(target=handle_conn, args=(conn, addr))
        thread.start()
        print(f"[current connections: {threading.active_count() -1 }]")


print("[--- server is starting ---]")
start()
