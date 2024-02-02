import asyncio
import click

from typing import final
from helpers import logging

from helpers.decorators import Decorator 
from library.lemon8 import BaseLemon8, AbstractLemon8

@final
class Lemon8(BaseLemon8, AbstractLemon8):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        method: str = str(kwargs.get('method'))

        match(method):
            case 'by_user_id':
                if(not kwargs.get('user_id')): raise click.BadParameter("--user_id is required for :method 'by_user_id'")
                self.get_comments_by_user_id(**kwargs)
            case 'by_username':
                if(not kwargs.get('username')): raise click.BadParameter("--username is required for method 'by_username'")
                self.get_comments_by_username(**kwargs)
            case 'by_url':
                if(not kwargs.get('url')): raise click.BadParameter("--url is required for method 'by_url'")
                self.get_comments_by_url(**kwargs)
            case 'by_post_id':
                if(not kwargs.get('post_id')): raise click.BadParameter("--post_id is required for method 'by_post_id'")
                self.get_comments_by_post_id(**kwargs)
            case _:
                logging.error('Wait.............')
    
    @Decorator.counter_time
    def get_comments_by_user_id(self, **kwargs) -> None:
        return asyncio.run(super()._get_comments_by_user_id(str(kwargs.get('user_id'))))
    
    @Decorator.counter_time
    def get_comments_by_username(self, **kwargs) -> None:
        return super()._get_comments_by_username(str(kwargs.get('username')))

    @Decorator.counter_time
    def get_comments_by_url(self, **kwargs) -> None:
        return super()._get_comments_by_url(str(kwargs.get('url')))
    
    @Decorator.counter_time
    def get_comments_by_post_id(self, **kwargs) -> None:
            return super()._get_comments_by_post_id(str(kwargs.get('post_id')))

if(__name__ == '__main__'):
    Lemon8(**{
        'user_id': '7138599741986915329', 
        'method': 'by_user_id'
    })
