class AppConfig():
    APP_PORT = 7777
    APP_ADR = "127.0.0.1"
    APP_ENCODING = "utf-8"
    APP_CLIENTS_NUMBER = 5
    APP_MAX_MESS_SIZE = 1024
    APP_WELCOME_MESS = "Привет! Вы удачно подключились к приложению"
    APP_AUTH_USERS = ["Guest", ]
    APP_JIM_DICT = {"action": "",
                    "time": "",
                    "user": "",
                    "sender": "",
                    "destination": "",
                    "account_name": "",
                    "response": "",
                    "body": "",
                    "error": "",
                    }
