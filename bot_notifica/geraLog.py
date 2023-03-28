import logging

log_format = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
logging.basicConfig(filename='erro.log',
                    filemode='a',
                    level=logging.ERROR,
                    format=log_format)
logger = logging.getLogger('root')


def geraLog(msg):
    logger.error(msg)
