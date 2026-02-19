import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(log_file='trading_bot.log'):
    """
    Sets up logging configuration.
    Logs to both console and a file.
    """
    # Use data directory if available
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    if os.path.exists(data_dir):
        log_file = os.path.join(data_dir, log_file)

    # Create a custom logger
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)

    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
