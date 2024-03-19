import unittest
import socket
from unittest.mock import MagicMock, patch
from chat_server import ChatServer

class TestChatServer(unittest.TestCase):
    @patch('chat_server.socket.socket')
    def test_create_server_socket(self, mock_socket):
        server = ChatServer('127.0.0.1', 65432)
        mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
        self.assertTrue(mock_socket().setsockopt.called)
        self.assertTrue(mock_socket().bind.called)
        self.assertTrue(mock_socket().listen.called)

    @patch('chat_server.ClientsDB')
    @patch('chat_server.socket.socket')
    def test_receive_message(self, mock_socket, mock_db):
        mock_client_socket = MagicMock()
        mock_client_socket.recv.return_value = b'Test message'
        server = ChatServer('127.0.0.1', 65432)

        message = server.receive_message(mock_client_socket)
        self.assertEqual(message, b'Test message')



if __name__ == '__main__':
    unittest.main()