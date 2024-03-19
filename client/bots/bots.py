import time
from abc import ABC, abstractmethod

class Bot(ABC):
    @abstractmethod
    def get_message(self):
        """
        Generate or retrieve a message to be sent.

        Returns:
            str: The message to be sent.
        """
        pass

    @abstractmethod
    def should_send_message(self):
        """
        Determine whether a message should be sent at this time.

        Returns:
            bool: True if a message should be sent, False otherwise.
        """
        pass

class TimedBot(Bot):
    def __init__(self, seconds_to_respond):
        self.seconds_to_respond = seconds_to_respond * 1000
        self.last_message = time.time()

    def get_message(self):
        # Example implementation
        self.last_message = time.time()
        return "This is a timed message."

    def should_send_message(self):
        return time.time() - self.last_message >= self.seconds_to_respond

