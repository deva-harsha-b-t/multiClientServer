from distutils.log import error
from logging import exception
import socket
import threading
import select
import sys

from connection_handler import Connection
from utils import Utilities

HOST = "127.0.1.1"
FORMAT = "utf-8"
PORT = 9095
clients = []
names = []
connections = []
DISCONNECT_MESSAGE = "disconnect"
HEADER = 1024
PING_CODE = "pingCheck"


serverConn = Connection(HOST, PORT)
utils = Utilities()
serverConn.listen_to_clients()

def handle_connections():
    while True:
        if len(connections) > 0:
                readables, writeables, errors = select.select(
                    connections, connections, connections, 1.0)

                for conn_r in readables:
                    try:
                        mess_ = conn_r.recv(HEADER).decode(FORMAT)
                        req_type = ''
                        for line in mess_.split('\r\n'):
                            if(line.split(': ')[0] == 'Req-Type'):
                                req_type = line.split(': ')[1]

                        if req_type == 'msg':
                            message = mess_.split("\r\n\r\n")[1]
                            utils.send_ack(conn_r)

                            for conn_s in writeables:
                                try:
                                    print(message)
                                    conn_s.send(utils.post_res('msg', message).encode())
                                except BrokenPipeError:
                                    pass
                            
                        

                    except Exception as error:
                        print(error)
                        print("--- error ---")
                for err in errors:
                    try:
                        print(f"error in connection {err}")
                        connections.remove(err)
                        err.close()
                    except:
                        pass

def receive():
    con_thread = threading.Thread(target=handle_connections, args=())
    con_thread.start()
    while True:
        client, addr = serverConn.accept_connection()
        print(f"connected {str(addr)}")
        clients.append(client)
        client.setblocking(0)
        connections.append(client)


print("--- server running ---")
print(f"{HOST} is listening")
receive()