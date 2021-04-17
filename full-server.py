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
            conn, addr = self.s.accept()

            username = conn.recv(1024).decode()

            print('New connection. Username: ' + str(username))
            self.broadcast('New user joined the room. Username: ' + username)

            self.username_lookup[conn] = username

            self.clients.append(conn)

            threading.Thread(target=self.handle_client, args=(conn, addr,)).start()

    def send_msg(self, conn, msg):
        try:
            conn.send(msg.encode())
        except:
            print('failed to send msg to: ' + conn)

    def broadcast(self, msg):
        for connection in self.clients:
            self.send_msg(connection, msg)

    def handle_client(self, conn, addr):
        username = self.username_lookup[conn]
        while True:
            try:
                msg = conn.recv(1024)
            except:
                conn.shutdown(socket.SHUT_RDWR)
                self.clients.remove(conn)

                print(f'{username} left the room.')
                self.broadcast(f'{username} has left the room.')
                break

            if msg.decode() != '':
                print(f'New message from {username}: {str(msg.decode())}')
                for connection in self.clients:
                    if connection != conn:
                        self.send_msg(connection, f'{username}: {msg.decode()}')


server = Server()