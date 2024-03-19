import os

from server.controller.chat_server import ChatServer
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST') or '127.0.0.1'
PORT = int(os.getenv('PORT') or 65432)

if __name__ == '__main__':
    server = ChatServer(HOST, PORT)
    server.run()
