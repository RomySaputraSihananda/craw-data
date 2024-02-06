import click
import asyncio

from typing import final

from helpers import logging
from helpers.decorators import Decorator 
from library.glassdoor import AbstractGlassdoor, BaseGlassDoor

@final
class Glassdoor(BaseGlassDoor, AbstractGlassdoor):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        method: str = str(kwargs.get('method'))

        match(method):
            case 'by_employer_id':
                if(not kwargs.get('employer_id')): raise click.BadParameter("--employer_id is required for :method 'by_employer_id'")
                self.get_detail_by_employer_id(**kwargs)
            case 'by_page':
                if(not kwargs.get('page')): raise click.BadParameter("--page is required for :method 'by_page'")
                self.get_detail_by_page(**kwargs)
            case 'all_detail':
                self.get_all_detail(**kwargs)
            case _:
                logging.error('Wait.............')
    
    @Decorator.counter_time
    def get_detail_by_employer_id(self, **kwargs) -> None:
        return asyncio.run(super()._get_detail_by_employer_id(int(kwargs.get('employer_id'))))

    @Decorator.counter_time
    def get_detail_by_page(self, **kwargs) -> None:
        return asyncio.run(super()._get_detail_by_page(int(kwargs.get('page'))))
    
    @Decorator.counter_time
    def get_all_detail(self, **kwargs) -> None:
        return asyncio.run(super()._get_all_detail())

if(__name__ == '__main__'):
    Glassdoor(**{
        'employer_id': '1050335',
        'method': 'by_employer_id'
    })