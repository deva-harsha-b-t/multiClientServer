import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = "127.0.1.1"
PORT = 9090
FORMAT = "utf-8"


class Client:
    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()
        # msg.geometry("800x600")
        self.name = simpledialog.askstring(
            "Name", "Enter your name", parent=msg)
        self.gui_done = False
        self.running = True

        gui_therad = threading.Thread(target=self.gui_)
        recv_therad = threading.Thread(target=self.recv_)
        gui_therad.start()
        recv_therad.start()

    def gui_(self):
        self.window = tkinter.Tk(className=self.name)
        self.window.configure(bg="black")

        self.chat_label = tkinter.Label(
            self.window, text="Chat:", bg="black", fg="white")
        self.chat_label.config(font=("Arial", 12, "bold"))
        self.chat_label.pack(padx=5, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(
            self.window, bg="#2a282b", fg="white", font=("Arial", 12, "bold"))
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.msg_label = tkinter.Label(
            self.window, text="message:", bg="black", fg="white")
        self.msg_label.config(font=("Arial", 12, "bold"))
        self.msg_label.pack(padx=20, pady=5)

        self.msg_input = tkinter.Text(
            self.window, height=2, bg="#2a282b", fg="white",insertbackground='white',
             font=("Arial", 12, "bold"))
        self.msg_input.pack(padx=20, pady=5)

        self.send_btn = tkinter.Button(
            self.window, text="send", command=self.write)
        self.send_btn.config(font=("Arial", 12))
        self.send_btn.pack(padx=20, pady=5)

        self.gui_done = True
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        self.window.mainloop()

    def write(self):
        message = f"{self.name}: {self.msg_input.get('1.0', 'end')}"
        self.sock.send(message.encode(FORMAT))
        self.msg_input.delete('1.0', 'end')

    def recv_(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode(FORMAT)
                if message == "Name":
                    self.sock.send(self.name.encode(FORMAT))
                    if self.gui_done:
                        self.text_area.config(state="normal")
                        self.text_area.insert("end", "connected to the server")
                        self.text_area.yview("end")
                        self.text_area.config(state="disabled")
                else:
                    if self.gui_done:
                        self.text_area.config(state="normal")
                        self.text_area.insert("end", message)
                        self.text_area.yview("end")
                        self.text_area.config(state="disabled")

            except ConnectionAbortedError:
                break
            except:
                print("error")
                self.sock.close()
                exit(0)
                break

    def stop(self):
        # self.sock.send(f"{self.name} disconnected".encode(FORMAT))
        self.running = False
        self.window.destroy()
        self.sock.close()
        exit(0)


client = Client(HOST, PORT)
