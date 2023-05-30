# decorators.py

import logging

def log_decorator(func):
    """
    Decorator function used to log the output of a function.
    """
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        logger.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        ch.setFormatter(formatter)

        logger.handlers = []  # remove existing handlers

        logger.addHandler(ch)

        result = func(*args, **kwargs)
        logger.info(f"Result: {result}")
        return result

    return wrapper
