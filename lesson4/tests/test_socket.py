from lesson3.client import *
from lesson3.server import *
import json
import unittest


class TestSocket:
    def __init__(self, test_message):
        self.test_message = test_message
        self.encode_message = None
        self.received_message = None

    def send(self, message):
        json_test_mess = json.dumps(self.test_message)
        self.encode_message = json_test_mess.encode(AppConfig.APP_ENCODING)
        self.received_message = message

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_message)
        return json_test_message.encode(AppConfig.APP_ENCODING)


class TestConnection(unittest.TestCase):
    test_mess = AppConfig.APP_JIM_DICT
    test_mess['action'] = 'presence'
    test_mess['time'] = time.time()
    test_mess['user'] = 'Guest'

    test_mess_200 = {'responce': 200}
    test_mess_400 = {'responce': 400, 'error': 'Bad request'}

    def test_send_message(self):
        test_socket = TestSocket(self.test_mess)
        send_message(test_socket, self.test_mess)
        self.assertEqual(test_socket.encode_message, test_socket.received_message)
        with self.assertRaises(Exception):
            send_message(test_socket, test_socket)

    def test_get_message(self):
        test_socket_ok = TestSocket(self.test_mess_200)
        test_socket_err = TestSocket(self.test_mess_400)
        self.assertEqual(get_message(test_socket_ok), self.test_mess_200)
        self.assertEqual(get_message(test_socket_err), self.test_mess_400)

if __name__ == '__main__':
    unittest.main()