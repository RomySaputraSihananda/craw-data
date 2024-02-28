import click

from click import Context
from typing import Any

from .lemon8 import Lemon8
from .quora import Quora
from .glassdoor import Glassdoor
from .microsoftStore import MicrosoftStore
from .taptap import Taptap
from src.interfaces import BaseGroupClick


class DataReview(BaseGroupClick):
    @click.group()
    @click.pass_context
    def main(ctx: Context):
            """ Data Review """
    
    @staticmethod
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_user_id', 'by_username', 'by_url', 'by_post_id']))
    @click.option('--user_id', default=None, help='User ID')
    @click.option('--post_id', default=None, help='Post ID')
    @click.option('--username', default=None, help='Username')
    @click.option('--url', default=None, help='Url')
    @click.pass_context
    def lemon8(ctx: Context, **kwargs):
        """ Lemon8 Engine """
        return Lemon8(**DataReview.merge(ctx, **kwargs))

    @staticmethod
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_question_str']))
    @click.option('--question', default=None, help='Question')
    @click.pass_context
    def quora(ctx: Context, **kwargs):
        """ Quora Engine """
        return Quora(**DataReview.merge(ctx, **kwargs))


    @staticmethod
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_employer_id', 'by_page', 'all_detail']))
    @click.option('--employer_id', default=None, help='Employer id')
    @click.option('--page', default=None, help='Number page')
    @click.pass_context
    def glassdoor(ctx: Context, **kwargs):
        """ Glassdoor Engine """
        return Glassdoor(**DataReview.merge(ctx, **kwargs))
    
    @staticmethod
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_product_id', 'by_media_type', 'all_media']))
    @click.option('--product_id', default=None, help='Product id')
    @click.option('--media', default=None, help='Media type')
    @click.pass_context
    def microsoftStore(ctx: Context, **kwargs):
        """ MicrosoftStore Engine """
        return MicrosoftStore(**DataReview.merge(ctx, **kwargs))
    
    @staticmethod
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_app_id', 'by_platform', 'all_platform']))
    @click.option('--app_id', default=None, help='App id')
    @click.option('--platform', default=None, help='platform type')
    @click.pass_context
    def taptap(ctx: Context, **kwargs):
        """ TapTap Engine """
        return Taptap(**DataReview.merge(ctx, **kwargs))