import argparse
import os
import threading

import openai

from controller.open_ai_bot import OpenAIChatBot
from controller.timed_chat_client import TimedChatClient
from controller.chat_client import start_client
from dotenv import load_dotenv

load_dotenv()
parser = argparse.ArgumentParser(description='Chat Client')

HOST = os.getenv('HOST') or '127.0.0.1'
PORT = int(os.getenv('PORT') or 65432)

parser.add_argument('--timed_bot', type=int, help='Bot responds every X seconds')
parser.add_argument('--message_bot', type=int, help='Bot responds every X messages')


if __name__ == "__main__":
    args = parser.parse_args()
    bot = None
    if args.timed_bot:
        chat_client = TimedChatClient(HOST, PORT,"BotClient", message_interval=args.timed_bot)
        chat_client.connect()
        chat_client.start_auto_messaging()
    elif args.message_bot:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        bot = OpenAIChatBot(HOST, PORT, "OpenAIChatBot", args.message_bot)
        if bot.connect():
            threading.Thread(target=bot.receive_messages, daemon=True).start()
            bot.start_responding()
    else:
        start_client(HOST, PORT)
