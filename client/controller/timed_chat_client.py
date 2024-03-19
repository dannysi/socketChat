import socket
import threading
import time

class TimedChatClient:
    def __init__(self, ip, port, username, message_interval):
        self.ip = ip
        self.port = port
        self.username = username
        self.message_interval = message_interval
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.ip, self.port))
            print("Connected to the server!")
            self.send_username()
            return True
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return False

    def send_username(self):
        self.client_socket.send(self.username.encode('utf-8'))

    def start_auto_messaging(self):
        while True:
            time.sleep(self.message_interval)
            self.send_message("what's up doc?")


    def send_message(self, message):
        try:
            self.client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Failed to send message: {e}")

