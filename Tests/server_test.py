import unittest
from Server import VNCServer, MyThread
from unittest.mock import MagicMock, patch
class TestServerMethods(unittest.TestCase):
    def testMyThreadInit(self):
        thread_test = MyThread('127.0.0.1', 4444)
        self.assertEqual(thread_test.port, 4444)
        self.assertEqual(thread_test.ip, '127.0.0.1')
        thread_test.quit()

    def test_init(self):
        self.thread = MyThread('127.0.0.1', 1234)
        self.assertEqual(self.thread.ip, '127.0.0.1')
        self.assertEqual(self.thread.port, 1234)
        self.assertIsNotNone(self.thread.server)
        self.thread.quit()


    @patch('socket.socket')
    def test_run(self, mock_socket):
        self.thread = MyThread('127.0.0.1', 1234)
        mock_socket.return_value.accept.return_value = (MagicMock(), MagicMock())
        self.thread.run()
        self.thread.quit()
        # Add assertions for the expected behavior of the run method

    @patch('socket.socket')
    def test_send_json(self, mock_socket):
        mock_socket.return_value.send.return_value = None
        self.thread.active_socket = MagicMock()
        self.thread.send_json('test_data')
        self.thread.quit()
        # Add assertions for the expected behavior of the send_json method

    @patch('socket.socket')
    def test_receive_json(self, mock_socket):
        mock_socket.return_value.recv.return_value = b"{'key': 'value'}"
        self.thread.active_socket = MagicMock()
        result = self.thread.receive_json()
        self.assertEqual(result, {'key': 'value'})
        self.thread.quit()
        # Add assertions for the expected behavior of the receive_json method

if __name__ == '__main__':
    unittest.main()