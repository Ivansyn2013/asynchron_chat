from socket import *
import time
from lesson3.config import AppConfig
import sys
import json
import logging
import logs.client_log_config

log = logging.getLogger('client_logger')
def get_message(client):
    '''get message from client in serrialize it
    :return responce'''
    package = client.recv(AppConfig.APP_MAX_MESS_SIZE)
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
    log.debug('Отправка сообщения серверу')
    json_message = json.dumps(message)
    package = json_message.encode(AppConfig.APP_ENCODING)
    work_socket.send(package)
def client_active(user_name='Guest'):
    '''send online message to server '''

    log.debug('Создание сообщения серверу')
    responce = AppConfig.APP_JIM_DICT
    responce['action'] = 'presence'
    responce['time'] = time.time()
    responce['user'] = user_name
    return responce

def valid_server_message(message):
    '''check message on conformity'''
    if 'responce' in message:
        if message['responce'] == 200:
            log.info('Ответ сервера - ОК')
            return '200: ok'
        log.info('Отказ сервера')
        return f'400 : {message["error"]}'
    raise ValueError

def client_connect():
    '''connet to server'''

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

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((IP, PORT))
    message = client_active()
    send_message(client_socket, message)
    try:
        responce = get_message(client_socket)
        log.info(f'Ответ сервера: {responce}')
    except (ValueError, json.JSONDecodeError):
        log.error('Ошибка отправки сообщения')

if __name__ == "__main__":
    client_connect()