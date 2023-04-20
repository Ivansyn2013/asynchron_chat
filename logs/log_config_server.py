import logging
import logging.handlers


server_format_log = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

file_path = './server.log'

server_handler_log = logging.StreamHandler()
server_handler_log.setFormatter(server_format_log)
server_handler_log.setLevel(logging.DEBUG)

server_file_handler = logging.handlers.TimedRotatingFileHandler(file_path,
                                                                encoding='utf-8',
                                                                interval=1,
                                                                when='D')
server_file_handler.setFormatter(server_format_log)

server_loger = logging.getLogger('server_loger')
server_loger.setLevel(logging.DEBUG)
server_loger.addHandler(server_file_handler)
server_loger.addHandler(server_handler_log)

if __name__ == '__main__':
    server_loger.critical('Ошибка')
    server_loger.info('INFO')
    server_loger.debug('debug')
    server_loger.error('error')
    server_loger.warning('warning1')