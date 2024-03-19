import unittest
from unittest.mock import patch
from chat_client import ChatClient

class TestChatClient(unittest.TestCase):
    @patch('socket.socket')
    def test_connect_success(self, mock_socket):
        mock_socket_instance = mock_socket.return_value
        mock_socket_instance.connect.return_value = None

        client = ChatClient('127.0.0.1', 65432, 'testuser')
        result = client.connect()
        self.assertTrue(result)
        mock_socket_instance.connect.assert_called_with(('127.0.0.1', 65432))

    @patch('socket.socket')
    def test_connect_failure(self, mock_socket):
        mock_socket_instance = mock_socket.return_value
        mock_socket_instance.connect.side_effect = Exception('Connection error')

        client = ChatClient('127.0.0.1', 65432, 'testuser')
        result = client.connect()
        self.assertFalse(result)

    @patch('socket.socket')
    def test_send_message(self, mock_socket):
        mock_socket_instance = mock_socket.return_value
        client = ChatClient('127.0.0.1', 65432, 'testuser')
        client.connect()
        client.send_message('Hello, world!')
        mock_socket_instance.send.assert_called_with(b'Hello, world!')


if __name__ == '__main__':
    unittest.main()