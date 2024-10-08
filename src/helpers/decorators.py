import os

from time import perf_counter
from functools import wraps
from typing import Callable, Any, final
from json import loads, dumps

from src.config import logging
from click import style

@final
class Decorator:
    @staticmethod
    def counter_time(func: Callable[..., None]) -> Callable[..., None]:
        @wraps(func)
        def wrapper(self, *args: Any, **kwargs: Any) -> None:
            start: float = perf_counter()
            logging.info('start crawling')
            result: Any = func(self, *args, **kwargs)
            
            logging.info(f'task completed in {perf_counter() - start} seconds')
            return result
        
        return wrapper
    
    @staticmethod
    def logging_path(name: str = style('CRAWLING', fg='bright_green')) -> Callable[..., None]:
        def decorator(func: Callable[..., None]) -> Callable[..., None]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs) -> None:
                try:
                    path = args[1]
                except:
                    path = args[0]
                logging.info(f'[ {name} ] :: {path}')
                
                return func(*args, **kwargs)
            return wrapper
        
        return decorator if isinstance(name, str) else decorator(name)
    
    @staticmethod
    def check_path(func: Callable[..., None]) -> Callable[..., None]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> None:
            directory: str = os.path.dirname(path if (path := args[1]).find(payload := 'S3://ai-pipeline-statistics/') < 0 else path.replace(payload, ''))
            print(directory)
            if not os.path.isdir(directory) and bool(directory):
                os.makedirs(directory)
            
            return func(*args, **kwargs)
        
        return wrapper