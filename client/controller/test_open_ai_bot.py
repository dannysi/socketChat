import unittest
from unittest.mock import patch, MagicMock

from client.controller.open_ai_bot import OpenAIChatBot


class TestOpenAIChatBot(unittest.TestCase):
    @patch('socket.socket')
    def test_connect_success(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        bot = OpenAIChatBot('127.0.0.1', 65432, 'testuser',1)
        self.assertTrue(bot.connect())
        mock_socket_instance.connect.assert_called_with(('127.0.0.1', 65432))

    @patch('socket.socket')
    def test_connect_failure(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket_instance.connect.side_effect = Exception("Connection failed")
        mock_socket.return_value = mock_socket_instance
        bot = OpenAIChatBot('127.0.0.1', 65432, 'testuser',1)
        self.assertFalse(bot.connect())

    @patch('socket.socket')
    def test_send_message(self, mock_socket):
        message = "Hello, world!"
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        bot = OpenAIChatBot('127.0.0.1', 65432, 'testuser',1)
        bot.connect()  # Assuming connect is successful
        bot.send_message(message)
        mock_socket_instance.send.assert_called_with(message.encode('utf-8'))


if __name__ == '__main__':
    unittest.main()