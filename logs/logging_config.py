import logging
import os
from logging.handlers import RotatingFileHandler

def configure_logging():
    """
    Configura o logging para a aplicação.
    """
    log_directory = 'logs/app/app_logger'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    logger = logging.getLogger('app/app_logger')
    logger.setLevel(logging.DEBUG)

    # Configuração do log para arquivo
    handler = RotatingFileHandler(os.path.join(log_directory, 'app.log'), maxBytes=10000, backupCount=3)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # Configuração do log para o console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger

# Inicialize o logger
logger = configure_logging()
