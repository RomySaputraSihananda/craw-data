import click
import asyncio

from typing import final

from helpers import logging
from helpers.decorators import Decorator 
from library.dataDivtik import AbstractCekbpom, BaseCekbpom

@final
class Cekbpom(BaseCekbpom, AbstractCekbpom):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
        method: str = str(kwargs.get('method'))

        match(method):
            case 'by_product_id':
                if(not kwargs.get('product_id')): raise click.BadParameter("--product_id is required for :method 'by_product_id'")
                self.get_detail_by_product_id(**kwargs)
            case 'by_page':
                if(not kwargs.get('page')): raise click.BadParameter("--page is required for :method 'by_page'")
                self.get_detail_by_page(**kwargs)
            case 'all_detail':
                self.get_all_detail(**kwargs)
            case _:
                logging.error('Wait.............')

    def get_detail_by_product_id(self, **kwargs) -> None:
        return asyncio.run(super()._get_detail_by_product_id(kwargs.get('product_id')))

    def get_detail_by_page(self, **kwargs) -> None:
        return asyncio.run(super()._get_product_by_page(int(kwargs.get('page'))))

    def get_all_detail(self, **kwargs) -> None:
        return super()._get_all()