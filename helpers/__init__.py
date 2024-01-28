from .iostream import Iostream
from .datetime import Datetime
from config.logging import logging 

from time import perf_counter
from functools import wraps

def counter_time(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start: float = perf_counter()
        logging.info('start crawling')
        func(self, *args, **kwargs)
        logging.info(f'task completed in {perf_counter() - start} seconds')
    
    return wrapper