import socket
import threading


class Server:
    def __init__(self):
        self.username_lookup = {}
        self.clients = []
        self.host = '127.0.0.1'
        self.port = 1234
        self.start_server()

    def start_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.s.bind((self.host, self.port))
        self.s.listen(100)

        print(f'Running on host {self.host}')
        print(f'Running on port: {self.port}')

        while True:
            c, addr = self.s.accept()

            username = c.recv(1024).decode()

            print('New connection. Username: ' + str(username))
            self.broadcast('New user joined the room. Username: ' + username)

            self.username_lookup[c] = username

            self.clients.append(c)

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, msg):
        for connection in self.clients:
            try:
                connection.send(msg.encode())
            except:
                print('failed to send msg to: ' + connection)

    def handle_client(self, c, addr):
        while True:
            try:
                msg = c.recv(1024)
            except:
                c.shutdown(socket.SHUT_RDWR)
                self.clients.remove(c)

                print(str(self.username_lookup[c]) + ' left the room.')
                self.broadcast(str(self.username_lookup[c]) + ' has left the room.')

                break

            if msg.decode() != '':
                print('New message: ' + str(msg.decode()))
                for connection in self.clients:
                    if connection != c:
                        connection.send(msg)


server = Server()