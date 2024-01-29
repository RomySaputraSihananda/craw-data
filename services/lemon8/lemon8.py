import asyncio
import click

from typing import final

from helpers.decorators import Decorator
from library.lemon8 import BaseLemon8

@final
class Lemon8(BaseLemon8):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        method: str = kwargs.get('method')

        match(method):
            case 'by_user_id':
                if(not kwargs.get('user_id')): raise click.BadParameter("--user_id is required for method 'by_user_id'")
                self.get_comments_by_user_id(**kwargs)
            case 'by_username':
                if(not kwargs.get('username')): raise click.BadParameter("--username is required for method 'by_username'")
                self.get_comments_by_username(**kwargs)

    @Decorator.counter_time
    def get_comments_by_user_id(self, **kwargs):
        asyncio.run(self.by_user_id(kwargs.get('user_id')))
    
    @Decorator.counter_time
    def get_comments_by_username(self, **kwargs):
        self.by_username(kwargs.get('username'))

if(__name__ == '__main__'):
    Lemon8(user_id='7138599741986915329', method='by_user_id')