from lesson3.client import *

import unittest


class TestClient(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_client_active(self):
        test = AppConfig.APP_JIM_DICT
        test['action'] = 'presence'
        test['time'] = time.time()
        test['user'] = 'Guest'
        self.assertEqual(client_active(), test)

    def test_valid_server_message_200(self):
        test = {'responce': 200}
        self.assertEqual(valid_server_message(test), '200: ok')

    def test_valid_server_message_400(self):
        test = AppConfig.APP_JIM_DICT
        test['responce'] = 400
        self.assertEqual(valid_server_message(test), f"{test['responce']} : {test['error']}", 'Test not passed')

    def test_valid_server_message_no_responce(self):
        self.assertRaises(ValueError, valid_server_message, {'': ''})


if __name__ == '__main__':
    unittest.main()
