import socket
import threading
from concurrent.futures import ThreadPoolExecutor

PORT = 9090
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "disconnect"
DEFAULT_RESPONSE = "hello from server"
THREAD_POOL_NO = 20

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(ADDR)


def send_mess(conn, msg):
    message = msg.encode(FORMAT)
    conn.send(message)


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
        send_mess(conn, DEFAULT_RESPONSE)
    conn.close()


def start():
    serverSocket.listen()
    print(f"[Server {SERVER} is listening]")
    executor = ThreadPoolExecutor(max_workers=THREAD_POOL_NO)
    while True:
        conn, addr = serverSocket.accept()
        # print(f"connected to {addr}")
        # thread = threading.Thread(target=handle_conn, args=(conn, addr))
        # thread.start()
        thread = executor.submit(handle_conn, (conn, addr))
        executor.map(handle_conn, range(30))
        # print(f"[current connections: {threading.active_count() -1 }]")


print("[--- server is starting ---]")
start()
