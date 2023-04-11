from socket import *
from config import AppConfig
def client_connect():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((AppConfig.APP_ADR, AppConfig.APP_PORT))
    package = client_socket.recv(AppConfig.APP_MAX_MESS_SIZE)
    client_socket.close()
    print("Server message\n")
    print(package.decode(AppConfig.APP_ENCODING))

if __name__ == "__main__":
    client_connect()