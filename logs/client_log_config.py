import logging
import logging.handlers

client_log_format = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

file_path = '../logs/client.log'

client_log_handler = logging.StreamHandler()
client_log_file_handler = logging.FileHandler(file_path,
                                              encoding='utf-8',
                                              )
client_log_handler.setLevel(logging.DEBUG)
client_log_file_handler.setLevel(logging.DEBUG)

client_log_file_handler.setFormatter(client_log_format)
client_log_handler.setFormatter(client_log_format)

client_logger = logging.getLogger('client_logger')
client_logger.addHandler(client_log_handler)
client_logger.addHandler(client_log_file_handler)
client_logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    client_logger.debug('debug')
    client_logger.error('error')
    client_logger.info('info')
    client_logger.critical('critical')
    client_logger.warning('warning')
