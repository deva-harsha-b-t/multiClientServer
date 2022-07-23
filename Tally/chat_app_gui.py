import threading
import tkinter
from tkinter import simpledialog
import tkinter.scrolledtext
from connection_handler import Connection

HOST = "127.0.1.1"
PORT = 9095

class ChatApp:
    def __init__(self):
        self.conn = Connection(HOST, PORT)
        self.conn.connect_to_server()
        msg = tkinter.Tk()
        msg.withdraw()
        self.name = simpledialog.askstring(
            "Name", "Enter your name", parent=msg)
        self.gui_done = False
        self.conn.running = True

        gui_thread = threading.Thread(target=self.gui_)
        recv_thread = threading.Thread(target=self.read_)
        down_thread = threading.Thread(target=self.ping_)
        gui_thread.start()
        recv_thread.start()
        down_thread.start()


    def gui_(self):
        self.window = tkinter.Tk(className=self.name)
        self.window.configure(bg="black")

        self.chat_label = tkinter.Label(
            self.window,bg="black", text="Chat:", fg="white")
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
            self.window, text="send", command=self.write_)
        self.send_btn.config(font=("Arial", 12))
        self.send_btn.pack(padx=20, pady=5)

        self.notify = tkinter.Label(
            self.window, text="message sent", bg="black", fg="green")
        self.notify.config(font=("Arial", 12))

        self.gui_done = True
        self.window.protocol("WM_DELETE_WINDOW", self.stop_)
        self.window.mainloop()


    def write_(self):
        message = f"{self.name}: {self.msg_input.get('1.0', 'end')}"
        try:
            self.conn.sendMessage(message)
        except BrokenPipeError:
            print("----- server is down -----")
            self.server_down_cnt = self.server_down_cnt - 1
            if self.server_down_cnt <= 0:
                self.server_down_close()
                self.window.destroy()        
        self.msg_input.delete('1.0', 'end')


    def read_(self):
        while self.conn.running:
            try:
                res_type = ""
                mess_ = self.conn.recvFun()

                for line in mess_.split('\r\n'):
                    if(line.split(': ')[0] == 'Res-Type'):
                        res_type = line.split(': ')[1]

                if(res_type == 'ack'):
                    self.notify.place(relx=1.0, rely=0.0, anchor = 'ne')
                    self.notify.after(2000, lambda: self.notify.place_forget())

                elif self.gui_done and res_type=='msg':
                    message = mess_.split("\r\n\r\n")[1]
                    self.text_area.config(state="normal")
                    self.text_area.insert("end", message)
                    self.text_area.yview("end")
                    self.text_area.config(state="disabled")

            except ConnectionAbortedError:
                break
            except Exception as e:
                print(e)
                self.conn.closeConn()
                exit(0)


    def stop_(self):
        self.conn.running = False
        self.window.destroy()
        self.conn.closeConn()


    def ping_(self):
        while True:
            self.conn.ping_()
            if self.conn.server_status == "down": 
                self.window.destroy()


gui = ChatApp()