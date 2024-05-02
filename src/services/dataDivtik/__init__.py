import click

from click import Context
from typing import Any

from .cekbpom import Cekbpom
from .companiesmarketcap import CompaniesMarketCap
from .bkpm import Bkpm
from .bnn import Bnn
from .pusiknaspolri import PusiknasPolri

from src.interfaces import BaseGroupClick
from src.library.dataDivtik.pusiknaspolri.pusiknaspolri import ok

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
    
    @main.command()
    @click.pass_context
    def companiesmarketcap(ctx: Context, **kwargs):
        """ Companies Market Cap Engine"""
        return CompaniesMarketCap(**DataDivtik.merge(ctx, **kwargs))
    
    @main.command()
    @click.pass_context
    @click.argument('type', metavar='TYPE', type=click.Choice(['PMDN', 'PMA']))
    @click.option('--headless', is_flag=True, help='headless browser')
    def bkpm(ctx: Context, **kwargs):
        """ Bkpm Engine"""
        return Bkpm(**DataDivtik.merge(ctx, **kwargs))
    
    @main.command()
    @click.pass_context
    def bnn(ctx: Context, **kwargs):
        """ Bnn Engine"""
        return Bnn(**DataDivtik.merge(ctx, **kwargs))
    
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['yesterday', 'by_range', 'by_date']))
    @click.option('--date', help='headless browser')
    @click.pass_context
    def pusiknaspolri(ctx: Context, **kwargs):
        """ Pusiknas Polri Engine """
        return PusiknasPolri(**DataDivtik.merge(ctx, **kwargs))
