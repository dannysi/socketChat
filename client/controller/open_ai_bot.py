import socket
import openai


class OpenAIChatBot:
    def __init__(self, ip, port, username, number_of_messages_to_respond):
        self.ip = ip
        self.port = port
        self.username = username
        self.client_socket = None
        self.last_messages = []
        self.number_of_messages_to_respond = number_of_messages_to_respond

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
        print(self.client_socket.send(self.username.encode('utf-8')))

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    print("\r" + message + "\n> ", end="")
                    self.last_messages.append(message)
                    # Keep only the last 5 messages
                    self.last_messages = self.last_messages[-5:]
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

    def generate_response(self):
        prompt = "\n".join(self.last_messages) + "\nAI:"
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chat user."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def start_responding(self):
        while True:
            if len(self.last_messages) >= self.number_of_messages_to_respond:
                response = self.generate_response()
                print(f"Bot> {response}")
                self.send_message(response)
                # Reset last_messages
                self.last_messages = []
