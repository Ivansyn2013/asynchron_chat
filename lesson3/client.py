from socket import *
import time
from config import AppConfig
import sys
import json
import logging
import logs.client_log_config
from lesson6_dec.wrapper import Logs
import threading
from colorama import Fore

log = logging.getLogger('client_logger')


def message_from_server(client_socket, username):
    while True:
        try:
            message = get_message(client_socket)
            if 'ACTION' in message and message["DESTINATION"] == username.upper():
                print(f'\nПолучено сообщение от пользователя {message["SENDER"]}:'
                      f'\n{message["BODY"]}')
                log.info(f'Получено сообщение от пользователя {message["SENDER"]}:'
                         f'\n{message["BODY"]}')
            else:
                log.error(f'Получено некорректное сообщение с сервера: {message}')

        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            log.critical(f'Потеряно соединение с сервером.')
            break


@Logs()
def user_interface(client_socket, username):
    while True:
        message = input(Fore.RESET + '\nВведите сообщение или exit для выхода:\n ')
        if message == 'exit':
            log.info('Завершение работы по команде пользователя.')
            time.sleep(0.5)
            print('Завершение соединения.')
            break
        destination = input('\n Введите получателя:\n')
        send_message(client_socket, message, username=username, destination=destination)


def slots_fun():
    pass


def get_message(client, username='Guest'):
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


@Logs()
def send_message(work_socket, message, username='Guest', destination='server'):
    '''encoding and sending messages
    :return'''
    log.debug('Отправка сообщения серверу')

    responce = AppConfig.APP_JIM_DICT
    responce['action'] = 'message'
    responce['time'] = time.time()
    responce['user'] = username
    responce['body'] = message
    responce['sender'] = username
    responce['destination'] = destination

    json_message = json.dumps(responce)
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


@Logs()
def valid_server_message(message):
    '''check message on conformity'''
    if 'responce' in message:
        if message['responce'] == 200:
            log.info('Ответ сервера - ОК')
            return '200: ok'
        log.info('Отказ сервера')
        return f'400 : {message["error"]}'
    raise ValueError


@Logs()
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

    print(Fore.GREEN + f'Запущен клиент IP {IP} PORT {PORT}' + Fore.RESET)
    with socket(AF_INET, SOCK_STREAM) as client_socket:

        client_socket.connect((IP, PORT))
        # message = client_active()
        # send_message(client_socket, message)
        user_name = input("Введите имя пользователя:")
        try:
            receiver = threading.Thread(target=message_from_server, args=(client_socket, user_name))
            receiver.daemon = True
            receiver.start()
            log.debug(f'Запущен поток "клиент на связи"')

            user_interface_thread = threading.Thread(target=user_interface, args=(client_socket, user_name))
            user_interface_thread.daemon = True
            user_interface_thread.start()
            log.debug('Запущен поток отправки сообщений')

            while True:
                time.sleep(1)
                if user_interface_thread.is_alive():
                    continue
                else:
                    break


        except OSError as error:
            log.error('Ошибка отправки сообщения', f'{error}')


if __name__ == "__main__":
    client_connect()
