import socket
import threading
import sys

class Client:
    def __init__(self):
        self.host = '165.22.177.88'
        self.port = 1234
        self.username = ''
        self.create_connection()

    def create_connection(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.connect((self.host, self.port))

        except:
            print("Couldn't connect to server")

        self.username = input('Enter username: ')
        self.socket.send(self.username.encode())

        message_handler = threading.Thread(target=self.handle_messages, args=())
        message_handler.start()

        input_handler = threading.Thread(target=self.input_handler, args=())
        input_handler.start()

    def handle_messages(self):
        while True:
            print(self.socket.recv(1204).decode())

    def input_handler(self):
        while True:
            msg = input('>')
            if str(msg) == "QUIT":
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
                sys.exit()
            self.socket.send(str(msg).encode())


client = Client()