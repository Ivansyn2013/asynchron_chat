import sys
from socket import *
import time
from lesson3.config import AppConfig
from colorama import Fore
import json
import logging
import logs.server_log_config

log = logging.getLogger('server_logger')
def valid_message(message):
    '''check message on conformity
    :param get message from client
    :retun dict'''

    log.debug('Проверка сообщения пользователя')
    if 'action' in message and message['action'] == 'presence' and 'time' in \
            message and 'user' in message:
        if message['user'] not in AppConfig.APP_AUTH_USERS:
            return {'response': 403,
                    'error': 'Not authorized'}
        return {'response':200}
    return {'response': 400,
            'error': 'Bad request'}
def get_message(client):
    '''get message from client in serrialize it
    :return responce'''

    package = client.recv(AppConfig.APP_MAX_MESS_SIZE)
    log.debug('Обработка сообщения пользователя')
    if isinstance(package, bytes):
        json_responce = package.decode(AppConfig.APP_ENCODING)
        responce = json.loads(json_responce)
        if isinstance(responce, dict):
            return responce
        raise ValueError
    raise ValueError


def send_message(work_socket, message):
    '''encoding and sending messages
    :return'''
    log.debug('Отправка сообщения пользователю')
    json_message = json.dumps(message)
    package = json_message.encode(AppConfig.APP_ENCODING)
    work_socket.send(package)



def server_start():
    '''Start servet app'''

    try:
        if '-a' in sys.argv:
            IP = str(sys.argv[sys.argv.index('-a') + 1])
        else:
            IP = AppConfig.APP_ADR
    except (IndexError, ValueError) as error:
        log.error(f'Ошибка в указанных аргументиах {error}')

    try:
        if '-p' in sys.argv:
            PORT = int(sys.argv[sys.argv.index('-p') + 1])
            if not 1024 < PORT < 65535:
                raise ValueError
        else:
            PORT = AppConfig.APP_PORT

    except (IndexError, ValueError) as error:
        log.error(f'Ошибка в указанных аргументах {error}')

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(AppConfig.APP_CLIENTS_NUMBER)

    log.info(f'Сервер запущен адрес {IP} порт {PORT}')

    while True:
        print(Fore.GREEN + 'App is started' + Fore.RESET)
        client, client_ip = server_socket.accept()
        time_str = time.ctime(time.time()) + "\n"
        log.debug(f'Соединение с клиентом {client_ip}')

        try:
            message = get_message(client)
            log.info(f'Сообщение пользователя: {message}')
            responce = valid_message(message)
            send_message(client, responce)
            client.close()
        except (ValueError, json.JSONDecodeError):
            log.warning('Получено некорректное сообщение')
            client.close()

if __name__ == "__main__":
    server_start()
