from lesson3.client import *
from lesson3.server import *
import json
import unittest


class TestServer(unittest.TestCase):
    def test_no_action(self):
        self.assertEqual(valid_message({'user': 'user', 'time': time.time(), }),
                         {'response': 400, "error": 'Bad request'})

    def test_not_authorized(self):
        self.assertEqual(valid_message({'user': 'user', 'time': time.time(), 'action': 'presence'}),
                         {'response': 403, "error": 'Not authorized'})

    def test_wrong_action(self):
        self.assertEqual(valid_message({'user': 'user', 'time': time.time(), 'action': ''}),
                         {'response': 400, "error": 'Bad request'})

    def test_no_time(self):
        self.assertEqual(valid_message({'user': 'user', 'time': '', 'action': 'presence'}),
                         {'response': 400, "error": 'Bad request'})

    def test_no_user(self):
        self.assertEqual(valid_message({'user': '', 'time': time.time(), 'action': 'presence'}),
                         {'response': 400, "error": 'Bad request'})

    def test_ok_request(self):
        self.assertEqual(valid_message({'user': 'Guest', 'time': time.time(), 'action': 'presence'}),
                         {'response': 200})

if __name__ == '__main__':
    unittest.main()
