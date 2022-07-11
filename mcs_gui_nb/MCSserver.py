import socket
import threading
import select

HOST = "127.0.1.1"
FORMAT = "utf-8"
PORT = 9090
clients = []
names = []
connections = []
DISCONNECT_MESSAGE = "disconnect"
HEADER = 1024


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()


# boradcast
# def broadcast_messages(message):
#     for client in clients:
#         client.send(message)


# handle connections
# def handle_connection_b(client):
#     while True:
#         try:
#             message = client.recv(HEADER)
#             print(f"{names[clients.index(client)]}")
#             broadcast_messages(message)

#         except:
#             print("----------------error---------------")
#             index = clients.index(client)
#             clients.remove(client)
#             names.remove(names[index])
#             client.close()
#             break
#             # pass

def handel_connectins():
    while True:
        if len(connections) > 0:
            try:
                readables, writeables, errors = select.select(
                    connections, connections, connections, 1.0)

                for conn_r in readables:
                    mess_ = conn_r.recv(HEADER).decode(FORMAT)
                    if mess_ == DISCONNECT_MESSAGE:
                        connections.remove(conn_r)
                        pass
                    else:
                        for conn_s in writeables:
                            conn_s.send(mess_.encode(FORMAT))
                    print(mess_)
            except :
                print("--- error ---")
# recv


def receive():
    con_thread = threading.Thread(target=handel_connectins, args=())
    con_thread.start()
    while True:
        client, addr = server.accept()
        print(f"connectd {str(addr)}")

        # client.send("Name".encode(FORMAT))
        # name = client.recv(1024).decode(FORMAT)
        # # name = name.decode("utf-8")
        #  names.append(name)
        clients.append(client)
        connections.append(client)
        # print(f"name of the client is {name}")
        # print(f"current client count: {len(clients)}")
        # broadcast_messages(f"{name} joined the chat\n".encode(FORMAT))
        # client.send("connectd to the server".encode(FORMAT))

        # thread = threading.Thread(target=handle_connection_b, args=(client,))
        # thread.start()


print("--- server running ---")
print(f"{HOST} is listening")
receive()
