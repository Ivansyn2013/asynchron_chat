import logging
import logs.client_log_config
import logs.server_log_config
from datetime import datetime

from functools import wraps
class Logs():
    def __init__(self):
        if self.__module__ == 'server.py':
            self.logger = logging.getLogger('server')
        else:
            self.logger = logging.getLogger('client')
    def __call__(self, func):
        @wraps()
        def wrapper(*args,**kwargs):
            result = func(*args, **kwargs)
            log_message = f'{datetime} Функция {func.__name__} Вызвана из ' \
                          f'функции {func.__module__}'
            self.logger.debug(log_message)
            return result
        return wrapper


