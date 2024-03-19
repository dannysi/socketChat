import os
from client.controller.chat_client import start_client
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST') or '127.0.0.1'
PORT = int(os.getenv('PORT') or 65432)

if __name__ == "__main__":
    start_client(HOST, PORT)
