import logging
import time
import requests
from functools import wraps
from requests import exceptions as requests_exceptions
from requests import Response

# This wrapper was created to handle requests exceptions that may occur in the functions
# that are decorated with it. It logs the exception and returns None instead of
# raising the exception, allowing the program to continue running without crashing.

def exception_handler_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except requests_exceptions.RequestException as e:
            logging.error(f"Exception occurred in {func.__name__}: {e}", exc_info=True)
            return None
    return wrapper


