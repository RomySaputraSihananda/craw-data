import os

from time import perf_counter
from functools import wraps
from typing import Callable, Any, final

from config.logging import logging

@final
class Decorator:
    @staticmethod
    def counter_time(func: Callable[..., None]) -> Callable[..., None]:
        @wraps(func)
        def wrapper(self, *args: any, **kwargs: Any) -> None:
            start: float = perf_counter()
            logging.info('start crawling')
            func(self, *args, **kwargs)
            logging.info(f'task completed in {perf_counter() - start} seconds')
        
        return wrapper
    
    @staticmethod
    def logging_path(name: str = 'CRAWLING') -> Callable[..., None]:
        def decorator(func: Callable[..., None]) -> Callable[..., None]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs) -> None:
                func(*args, **kwargs)
                logging.info(f'[ {name} ] :: {args[1]}')
            return wrapper
        
        return decorator if isinstance(name, str) else decorator(name)
    
    @staticmethod
    def check_path(func: Callable[..., None]) -> Callable[..., None]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> None:
            directory: str = os.path.dirname(args[1])

            if not os.path.isdir(directory) and bool(directory):
                os.makedirs(directory)
            
            return func(*args, **kwargs)
        
        return wrapper