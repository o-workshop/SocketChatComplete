import socket
import threading


class Client:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 1234
        self.username = ''
        self.create_connection()

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.s.connect((self.host, self.port))
        except:
            print("Couldn't connect to server")

        self.username = input('Enter username: ')
        self.s.send(self.username.encode())

        message_handler = threading.Thread(target=self.handle_messages, args=())
        message_handler.start()

        input_handler = threading.Thread(target=self.input_handler, args=())
        input_handler.start()

    def handle_messages(self):
        while 1:
            print(self.s.recv(1204).decode())

    def input_handler(self):
        while 1:
            msg = input(f'>')
            if str(msg) == "QUIT":
                self.s.close()
                exit(0)
            self.s.send(f'{self.username} > {msg}'.encode())


client = Client()