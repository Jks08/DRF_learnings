import logging 
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def logger_config():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # File handler for logging SQL queries and other events

    file_handler = logging.FileHandler(os.path.join(LOG_DIR, 'project.log'))
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def my_function():
    logger = logger_config()
    # logger.debug('This is a debug message')
    # logger.info('This is an info message')
    # logger.warning('This is a warning message')
    # logger.error('This is an error message')
    # logger.critical('This is a critical message')