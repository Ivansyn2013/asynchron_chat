import logging
import logs.client_log_config
import logs.server_log_config
from datetime import datetime
import  inspect

from functools import wraps
class Logs:
    def __init__(self):
        if self.__module__ == 'server.py':
            self.logger = logging.getLogger('server_logger')
        else:
            self.logger = logging.getLogger('client_logger')
        self.logger.setLevel(logging.DEBUG)
    def __call__(self, func):

        def wrapper(*args,**kwargs):
            result = func(*args, **kwargs)
            log_message = f'{datetime.now()} Функция {func.__name__} Вызвана из ' \
                          f'функции {inspect.stack()[1][3]}'
            self.logger.debug(log_message)

            return result
        return wrapper


