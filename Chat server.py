import socket
import threading
import time

start_time = time.time()

PORT = 7070

FORMAT = "utf_8"

HEADER = 64

SERVER = socket.gethostbyname(socket.gethostname())

clients = {}

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

server.bind((SERVER , PORT))

def send_memebers():
    while True:
        if len(clients.keys()) != ['']:

            time.sleep(1)
            s = "<MEMBERS> "
            for client in clients.keys(): 
                s += clients[client] + " "
            s = s[:-1]
            for client in clients.keys():
                if clients[client] != "":
                    client.send(s.encode(FORMAT))
    

def handle_client(connection , address):
    print(f"NEW CONNECTION {address}")
    clients[connection] = ""
    
    while True:

        masg = connection.recv(HEADER).decode(FORMAT)
        if masg:
            masg = int(masg)
            masg = connection.recv(masg).decode(FORMAT)
            if masg == "<DISCONNECT>":
                for client in clients.keys():
                    if client != connection:
                        client.send(f"<DISCONNECT> {clients[connection]}".encode(FORMAT))
                clients.pop(connection)
                print(f"Active clients : {len(clients.keys())}")
                break
            if clients[connection] == "" and masg.split(" ")[0] == "<CONNECTED>":
                clients[connection] = masg.split(" ")[1]
                continue
            for client in clients.keys():
                if client != connection:
                    client.send(f"<MESSAGE> {clients[connection]} {masg}".encode(FORMAT))

    connection.close()

        

def start():
    thread2 = threading.Thread(target=send_memebers)
    thread2.start()
    print("[SERVER IS RUNNING] server is starting... ")
    server.listen()
    while True:   
        conection , address = server.accept()
        thread = threading.Thread(target=handle_client , args=(conection , address))
        thread.start()
        print(f"ACTiVE CONNECTIONS =====> {len(clients.keys())+1} \n")

start()

