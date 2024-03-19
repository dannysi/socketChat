import socket
import select

from server.database.clients_db import ClientsDB


class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = self.create_server_socket()
        self.sockets_list = [self.server_socket]
        self.client_db = ClientsDB()

    def create_server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        server_socket.setblocking(False)
        return server_socket


    def receive_message(self, client_socket):
        try:
            message = client_socket.recv(1024)
            if not len(message):
                return False
            return message
        except:
            return False

    def run(self):
        print(f"Listening for connections on {self.host}:{self.port}...")
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list, 0.5)

            for notified_socket in read_sockets:
                if notified_socket == self.server_socket:
                    client_socket, client_address = self.server_socket.accept()
                    user = self.receive_message(client_socket)
                    if user is False:
                        continue
                    self.sockets_list.append(client_socket)
                    self.client_db.add(client_socket, user)
                    print('Accepted new connection from {}:{}, username: {}'.format(*client_address,
                                                                                    user.decode('utf-8')))
                else:
                    # Handle messages from clients
                    message = self.receive_message(notified_socket)
                    if message is False:
                        print('Closed connection from: {}'.format(self.client_db.get(notified_socket).decode('utf-8')))
                        self.sockets_list.remove(notified_socket)
                        self.client_db.remove(notified_socket)
                        continue
                    user = self.client_db.get(notified_socket)
                    print(f"Received message from {user.decode('utf-8')}: {message.decode('utf-8')}")
                    print(f"clients size = {len(self.client_db)}")
                    for client_socket in self.client_db.get_all_clients():
                        if client_socket != notified_socket:
                            client_socket.send(user + b': ' + message)
            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                self.client_db.remove(notified_socket)

