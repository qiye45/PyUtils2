import logging

logging.basicConfig(format='[%(asctime)s %(filename)s line:%(lineno)d] %(levelname)s: %(message)s',
                    level=logging.DEBUG, filename="log.txt", filemode="w", encoding='utf-8')

logging.debug('This message should appear on the console')
logging.info('So should this')
logging.warning('And this, too')
