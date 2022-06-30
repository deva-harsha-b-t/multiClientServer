import socket
import threading
import select
# from concurrent.futures import ThreadPoolExecutor

PORT = 9090
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "disconnect"
DEFAULT_RESPONSE = "hello from server"
THREAD_POOL_NO = 20
connections = []
addrs = []

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(ADDR)


def send_mess(conn, msg):
    message = msg.encode(FORMAT)
    conn.send(message)


def handel_connectins():
    while True:
        if len(connections) > 0:
            readables, writeables, errors = select.select(
                connections, connections, connections, 1.0)

            for conn_r in readables:
                mess_ = conn_r.recv(HEADER).decode(FORMAT)
                for conn_s in writeables:
                    conn_s.send(mess_.encode(FORMAT))
                print(mess_)

            # for conn_e in errors:
            #     print(f'error: {conn_e}')


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
    con_thread = threading.Thread(target=handel_connectins, args=())
    con_thread.start()
    # executor = ThreadPoolExecutor(max_workers=THREAD_POOL_NO)
    while True:
        conn, addr = serverSocket.accept()
        connections.append(conn)
        addrs.append(addr)

        # print(f"connected to {addr}")
        # thread = threading.Thread(target=handle_conn, args=(conn, addr))
        # thread.start()
        # thread = executor.submit(handle_conn, (conn, addr))
        # executor.map(handle_conn, range(30))
        # print(f"[current connections: {threading.active_count() -1 }]")


print("[--- server is starting ---]")
start()
