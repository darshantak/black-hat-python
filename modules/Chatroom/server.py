import socket , threading 
CLIENTS = {}
ADDRESS = {}
HOST = "127.0.0.1"
PORT = "6969"
BUFFSIZE = 4096
ADDR = (HOST,PORT) 

SERVER = socket(socket.AF_INET,socket.SOCK_STREAM)
SERVER.bind(ADDR)


def accept_incoming_connections():
    while True:
        client, client_addr = SERVER.accept()
        print("%s is connected now", client)
        client.send(bytes("You are now connected to the server","utf-8"))
        client.send(("You are now connected to the server").encode("utf8"))
        ADDRESS[client] = client_addr
        threading.Thread(target=handle_clients,args=(client,)).start()
        
def handle_clients(client):
    name = client.recv(BUFFSIZE).decode("utf8")
    client.send(("*****Hey there ! If you want to get out of here type \"quit\" to exit*****").encode('utf8'))
    broadcast_msg = ("User has joined").encode('utf8')
    broadcaster(broadcast_msg)
    CLIENTS[client] = name
    while True:
        msg = client.recv(BUFFSIZE)
        if msg != ("quit").encode('utf8'):
            broadcaster(msg)
        else:
            pass
def broadcaster():
    pass

if __name__ == "__main__":
    pass
    

