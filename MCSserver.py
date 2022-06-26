import socket
import threading

HOST = "127.0.0.1"
FORMAT = "utf-8"
PORT = 9090
clients = []
names = []


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()


# boradcast
def broadcast_messages(message):
    for client in clients:
        client.send(message)


# handle connections
def handle_connection(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{names[clients.index(client)]}")
            broadcast_messages(message)

        except:
            print("----------------error---------------")
            index = clients.index(client)
            clients.remove(client)
            names.remove(names[index])
            client.close()
            break
            # pass

# recv


def receive():
    while True:
        client, addr = server.accept()
        print(f"connectd {str(addr)}")

        client.send("Name".encode(FORMAT))
        name = client.recv(1024).decode(FORMAT)
        # name = name.decode("utf-8")
        names.append(name)
        clients.append(client)
        print(f"name of the client is {name}")
        print(f"current client count: {len(clients)}")
        broadcast_messages(f"{name} joined the chat\n".encode(FORMAT))
        client.send("connectd to the server".encode(FORMAT))

        thread = threading.Thread(target=handle_connection, args=(client,))
        thread.start()


print("--- server running ---")
receive()
