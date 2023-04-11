import sys
from socket import *
import time
from config import AppConfig
from colorama import Fore


def get_message(client):
    pass
def send_message(client):
    pass


def server_start():

    try:
        if '-a' in sys.argv:
            IP = int(sys.argv[sys.argv.index('-a') + 1 ])
        else:
            IP = AppConfig.APP_ADR
    except (IndexError, ValueError) as error:
        print(f'Ошибка в указанных аргументиах {error}')

    try:
        if '-p' in sys.argv:
            PORT = int(sys.argv[sys.argv.index('-p') + 1 ])
            if not 1024 < PORT < 65535:
                raise ValueError
        else:
            PORT = AppConfig.APP_PORT

    except (IndexError, ValueError) as error:
        print(f'Ошибка в указанных аргументах {error}')

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(AppConfig.APP_CLIENTS_NUMBER)

    while True:
        print(Fore.GREEN + 'App is started' + Fore.RESET)
        client, client_ip = server_socket.accept()
        time_str = time.ctime(time.time()) + "\n"
        print(Fore.YELLOW + f'Connection from {client_ip} is accepted' + Fore.RESET)
        client.send(AppConfig.APP_WELCOME_MESS.encode(AppConfig.APP_ENCODING))
        client.send(time_str.encode('ascii'))
        client.close()


if __name__ == "__main__":
    server_start()