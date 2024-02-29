import click
import asyncio

from typing import Coroutine, Any

from src.library.dataTeritorial import BaseWikipedia
from src.helpers import Decorator, logging

class Wikipedia(BaseWikipedia):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        method: str = str(kwargs.get('method'))

        match(method):
            case 'by_location':
                ...
            case 'all_location':
                self.get_all_location(**kwargs)
            case _:
                logging.error('Wait.............')

    @Decorator.counter_time
    def get_all_location(self, **kwargs) -> Coroutine[Any, Any, None]:
        return asyncio.run(super()._get_all_location())
    
if(__name__ == '__main__'):
    Wikipedia(**{
        'method': 'all_location',
        's3': True
    })