import sys
from socket import *
import time
from lesson3.config import AppConfig
from colorama import Fore
import json
import logging
from lesson6_dec.wrapper import Logs
import select
import logs.server_log_config

log = logging.getLogger('server_logger')


def write_client_query(requests, clients_write, all_clients):
    for sock in clients_write:
        if sock in requests:
            try:
                resp = requests[sock].upper()
                sock.send(resp.encode('utf-8'))
            except Exception:
                log.info(f'ip client {sock.getpeername()}')
                print(f"Клиент {sock.fileno()} {sock.getpeername()} отключился")
                sock.close()
                all_clients.remove(sock)


def client_query(read_clients, all_clients):
    '''
    Find clients who write something in all clients
    :param read_clients:
    :param all_clients:
    :return:
    '''
    responce = {}

    for sock in read_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responce[sock] = data
        except Exception:
            log.warning(f"Клиент {sock.fileno()} {sock.getpeername()} отключился")
            all_clients.remove(sock)
    return responce


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
        return {'response': 200}
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


@Logs()
def send_message(work_socket, message):
    '''encoding and sending messages
    :return'''
    log.debug('Отправка сообщения пользователю')
    json_message = json.dumps(message)
    package = json_message.encode(AppConfig.APP_ENCODING)
    work_socket.send(package)


@Logs()
def server_start(mode='default'):
    '''Start servet app'''

    all_clients = []
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

    with socket(AF_INET, SOCK_STREAM) as server_socket:
        server_socket.bind((IP, PORT))
        server_socket.listen(AppConfig.APP_CLIENTS_NUMBER)
        server_socket.settimeout(0.2)
    ####
        log.info(f'Сервер запущен адрес {IP} порт {PORT}')
        print(Fore.GREEN + 'App is started' + Fore.RESET)

        while True:

            try:
                client, client_ip = server_socket.accept()
            except OSError as error:
                pass
            else:
                log.info(f'Получен запрос на соединение {client_ip}')
                all_clients.append(client)
            finally:
                time_str = time.ctime(time.time()) + "\n"
                #            log.debug(f'Соединение с клиентом {client_ip}')
                wait = 1
                clients_read = []
                clients_write = []
                try:
                    clients_read, clients_write, errors = select.select(all_clients, all_clients, [], wait)

                    ###

                    requests = client_query(clients_read, all_clients)
                    print(requests)
                    if requests:
                        # print(requests)
                        write_client_query(requests, clients_write, all_clients)
                except (ValueError, json.JSONDecodeError):
                    log.warning('Получено некорректное сообщение')
                    client.close()


if __name__ == "__main__":
    server_start()
