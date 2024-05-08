import tkinter as tk
from sys import exit
import socket
import threading

active_users = []

PORT = 7070
FORMAT = "utf_8"
HEADER = 64
SERVER = "192.168.14.151"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat GUI")
        self.root.geometry("500x500")
        
        self.name_lb = tk.Label(root, text="Enter your name:")
        self.name_lb.pack(pady=15)
        self.name_entry = tk.Entry(root)
        self.name_entry.pack(pady=15)
        self.btn1 = tk.Button(root, text="Submit", command=self.set_name)
        self.btn1.pack()
        
        self.name = ""
        self.made = False
        
        self.done = True


    def set_name(self):
        name = self.name_entry.get()
        if name:
            self.name += name
            
            self.create_gui()
            
            self.thread2 = threading.Thread(target=self.receive_messages)
            self.thread2.start()    
            
            self.name_lb.destroy()
            self.name_entry.destroy()
            self.btn1.destroy()

    def create_gui(self):
        if not self.made:
            self.frame = tk.Frame(self.root)
            self.frame.pack(pady=10)
            
            self.name_list = tk.Listbox(self.frame, width=15, height=18)
            self.name_list.pack(side=tk.RIGHT)
            self.scrollbar2 = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.name_list.yview)
            self.scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
            self.name_list.config(yscrollcommand=self.scrollbar2.set)
            
            self.chat_list = tk.Listbox(self.frame, width=50, height=18)
            self.chat_list.pack(side=tk.LEFT)
            self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.chat_list.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.chat_list.config(yscrollcommand=self.scrollbar.set)
            
            self.entry = tk.Entry(self.root, width=40)
            self.entry.pack(pady=10)
            self.send_button = tk.Button(self.root, text="Send", command=self.send)
            self.send_button.pack()
            self.made = True


    def receive_messages(self):
        self.send_message(f"<CONNECTED> {self.name}")

        while True:
            msg = client.recv(2048).decode(FORMAT)
            if msg.split(" ")[0] == "<MESSAGE>":
                self.root.after(0, self.update_chat, msg.split(" ")[1], " ".join(msg.split(" ")[2:]))
                
            elif msg.split(" ")[0] == "<MEMBERS>":
                if msg[10:] != "":
                    
                    lst = msg[10:].split(" ")
                    self.root.after(0 , self.update_names , lst)
                    
                    for x in msg[10:].split(" "):
                        if x not in active_users:
                            active_users.append(x)

    def send(self):
        message = self.entry.get()
        if message and self.name:
            self.chat_list.insert(tk.END, "You: " + message)
            self.send_message(message)
            self.entry.delete(0, tk.END)

    def send_message(self, message):
        message = message.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        client.send((send_length))
        client.send(message)

    def update_chat(self, name, message):
        if name == self.name:
            self.chat_list.insert(tk.END, "You: " + message)
        else:
            self.chat_list.insert(tk.END, f"{name}: " + message)
            
    def update_names(self , names):
        self.name_list.delete(0 , tk.END)
        # if message == "<DISCONNECTED>":
        #     print("hello")
        #     idx = active_users.index(name)
        #     self.name_list.delete(idx)
        for name in names:
            if name != "" or name != " ":
                self.name_list.insert(tk.END , f"{name}")

def main():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
    app.send_message("<DISCONNECT>")
    exit()

if __name__ == "__main__":
    main()