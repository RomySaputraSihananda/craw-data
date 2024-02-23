import click
import asyncio

from typing import final
from src.config import logging

from src.helpers.decorators import Decorator 
from src.library.dataReview import BaseTaptap, AbstractTaptap

class Taptap(BaseTaptap, AbstractTaptap):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        method: str = kwargs.get('method')

        match(method):
            case 'by_app_id':
                if(not kwargs.get('app_id')): raise click.BadParameter("--app_id is required for method 'by_app_id'")
                self.get_answers_by_app_id(**kwargs)
            case 'by_platform':
                if(not kwargs.get('platform')): raise click.BadParameter("--platform is required for method 'by_platform'")
                self.get_answers_by_platform(**kwargs)
            case 'all_platform':
                self.get_all_platform(**kwargs)
    
    @Decorator.counter_time
    def get_all_platform(self, **kwargs) -> None:
        return asyncio.run(super()._get_all_platform())
    
    @Decorator.counter_time
    def get_by_platform(self, **kwargs) -> None:
        return asyncio.run(super()._get_by_platform(kwargs.get('platform')))
    
    @Decorator.counter_time
    def get_by_app_id(self, **kwargs) -> None:
        return asyncio.run(super()._get_by_app_id(kwargs.get('app_id')))