import asyncio

from typing import final

from helpers.decorators import Decorator
from library.lemon8 import BaseLemon8

@final
class Lemon8(BaseLemon8):
    @Decorator.counter_time
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        method: str = kwargs.get('method')

        match(method):
            case 'by_user_id':
                self.get_comments_by_user_id(**kwargs)

    def get_comments_by_user_id(self, **kwargs):
        asyncio.run(self.by_user_id(kwargs.get('user_id')))
    
    # def get_comments_by_user_id(self, user_id: str):
    #     asyncio.run(self.by_user_id(user_id))
    

if(__name__ == '__main__'):
    Lemon8(user_id='7138599741986915329', method='by_user_id')