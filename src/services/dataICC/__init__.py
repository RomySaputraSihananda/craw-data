import click

from click import Context
from typing import Any

from .travelokaevent import TravelokaEvent
from .agoda import Agoda

from src.interfaces import BaseGroupClick

class DataICC(BaseGroupClick):
        @click.group()
        @click.pass_context
        def main(ctx: Context):
                """ Data ICC """
                ... 

        @main.command()
        @click.argument('method', metavar='METHOD', type=click.Choice(['by_location', 'all_location']))
        @click.option('--location', default=None, help='Location name')
        @click.option('--start', default=None, help='strtstart location')
        @click.pass_context
        def travelokaEvent(ctx: Context, **kwargs: Any):
                """ Traveloka Event Engine """
                return TravelokaEvent(**DataICC.merge(ctx, **kwargs))
        
        @main.command()
        @click.argument('method', metavar='METHOD', type=click.Choice(['by_province', 'all_detail']))
        @click.option('--province', default=None, help='Province name')
        @click.pass_context
        def agoda(ctx: Context, **kwargs: Any):
                """ Agoda Engine """
                return Agoda(**DataICC.merge(ctx, **kwargs))