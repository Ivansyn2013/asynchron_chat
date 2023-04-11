from socket import *
import time
from config import AppConfig
from colorama import Fore

def server_start():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', AppConfig.APP_PORT))
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