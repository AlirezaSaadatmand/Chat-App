import socket
import threading


PORT = 7070

FORMAT = "utf_8"

HEADER = 64

SERVER = socket.gethostbyname(socket.gethostname())

clients = {}

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

server.bind((SERVER , PORT))

def handle_client(connection , address):
    print(f"NEW CONNECTION {address}")
    clients[connection] = ""
    
    while True:
        masg = connection.recv(HEADER).decode(FORMAT)
        if masg:
            masg = int(masg)
            masg = connection.recv(masg).decode(FORMAT)
            if masg == "<DISCONNECT>":
                break
            if clients[connection] == "":
                clients[connection] = masg
                continue
            for client in clients.keys():
                if client != connection:
                    client.send(f"{clients[connection]} {masg}".encode(FORMAT))
                    
    clients.pop(connection)
    for client in clients.keys():
        client.send(f"{clients[connection]} <DISCONNECTED>".encode(FORMAT))
    print(f"Active clients : {len(clients.keys())}")
    connection.close()

        

def start():
    print("[SERVER IS RUNNING] server is starting... ")
    server.listen()
    while True:   
        conection , address = server.accept()
        thread = threading.Thread(target=handle_client , args=(conection , address))
        thread.start()
        print(f"ACTiVE CONNECTIONS =====> {threading.active_count() - 1} \n")

start()

