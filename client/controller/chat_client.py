import socket
import threading


class ChatClient:
    def __init__(self, ip, port, username):
        self.ip = ip
        self.port = port
        self.username = username
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.ip, self.port))
            print("Connected to the server!")
            return True
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return False

    def send_username(self):
        self.client_socket.send(self.username.encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.handle_message(message)
                else:
                    print("\nConnection closed by the server")
                    break
            except Exception as e:
                print("\nError receiving message: ", str(e))
                break

    def send_message(self, message):
        try:
            self.client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Failed to send message: {e}")

    def handle_message(self, message):
        print("\r" + message + "\n> ", end="")


def start_client(ip, port):
    username = input("Enter your username: ")
    chat_client = ChatClient(ip, port, username)

    if chat_client.connect():
        chat_client.send_username()
        thread = threading.Thread(target=chat_client.receive_messages)
        thread.daemon = True
        thread.start()

        while True:
            message = input("> ")
            if message.lower() == 'quit':
                break
            chat_client.send_message(message)

        chat_client.client_socket.close()