import click
import asyncio

from typing import final
from helpers import logging

from helpers.decorators import Decorator 
from library.dataReview import BaseTaptap, AbstractTaptap

class Taptap(BaseTaptap, AbstractTaptap):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    @Decorator.counter_time
    def get_all_platform(self, **kwargs) -> None:
        return asyncio.run(super()._get_all_platform())
    
    @Decorator.counter_time
    def get_by_platform(self, **kwargs) -> None:
        return asyncio.run(super()._get_by_platform(kwargs.get('platform')))
    
    @Decorator.counter_time
    def get_by_app_id(self, **kwargs) -> None:
        return asyncio.run(super()._get_by_app_id(kwargs.get('app_id')))