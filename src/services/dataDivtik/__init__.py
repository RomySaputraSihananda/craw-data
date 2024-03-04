import click

from click import Context
from typing import Any

from src.interfaces import BaseGroupClick
from .cekbpom import Cekbpom

class DataDivtik(BaseGroupClick):
    @click.group()
    @click.pass_context
    def main(ctx: Context) -> Any:
        """ Data Divtik """
    
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_product_id', 'by_page', 'all_detail', 'retry_error']))
    @click.option('--product_id', default=None, help='Product id')
    @click.option('--page', default=None, help='Number page')
    @click.option('--start', default=1, help='start page')
    @click.pass_context
    def cekbpom(ctx: Context, **kwargs):
        """ Cek BPOM Product Engine"""
        return Cekbpom(**DataDivtik.merge(ctx, **kwargs))
