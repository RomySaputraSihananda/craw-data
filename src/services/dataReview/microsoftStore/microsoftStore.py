import asyncio

from click import BadParameter
from typing import final

from src.library.dataReview import BaseMicrosoftStore, AbstractMicrosoftStore
from src.helpers import Decorator, logging

@final
class MicrosoftStore(BaseMicrosoftStore, AbstractMicrosoftStore):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        method: str = kwargs.get('method')

        match(method):
            case 'by_product_id':
                if(not kwargs.get('product_id')): raise BadParameter("--product_id is required for :method 'by_product_id'")
                self.get_by_product_id(**kwargs)
            case 'by_media_type':
                if(not kwargs.get('media_type')): raise BadParameter("--media_type is required for method 'by_media_type'")
                self.get_by_media_type(**kwargs)
            case 'all_media':
                self.get_all_media()
            case _:
                logging.error('Wait.............')
    
    @Decorator.counter_time
    def get_by_product_id(self, **kwargs) -> None:
        return asyncio.run(super()._get_by_product_id(kwargs.get('product_id')))
    
    @Decorator.counter_time
    def get_by_media_type(self, **kwargs) -> None:
        return asyncio.run(super()._get_by_media_type(kwargs.get('media_type')))

    @Decorator.counter_time
    def get_all_media(self) -> None:
        return asyncio.run(super()._get_all_media())
    
if(__name__ == '__main__'):
    MicrosoftStore(**{
        'method': 'by_product_id',
        'product_id': '9NBLGGGZM6WM'
    })