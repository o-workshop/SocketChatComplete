import socket
import threading


class Client:
    def __init__(self):
        self.host = '165.22.177.88'
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
            try:
                print(self.s.recv(1204).decode())
            except:
                print("failed to receive")

    def input_handler(self):
        while 1:
            msg = input('>')
            if str(msg) == "QUIT":
                self.s.shutdown()
                self.s.close()
                exit(0)
            self.s.send(str(msg).encode())


client = Client()