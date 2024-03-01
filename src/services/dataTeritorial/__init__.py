import click

from click import Context

from src.interfaces import BaseGroupClick
from .wikipedia import  Wikipedia

class DataTeritorial(BaseGroupClick):
    @click.group()
    @click.pass_context
    def main(ctx: Context):
            """ Data Teritorial """
    
    @staticmethod
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_location', 'all_location']))
    @click.option('--user_id', default=None, help='User ID')
    @click.option('--post_id', default=None, help='Post ID')
    @click.option('--username', default=None, help='Username')
    @click.option('--url', default=None, help='Url')
    @click.pass_context
    def wikipedia(ctx: Context, **kwargs):
        """ Wikipedia Engine """
        return Wikipedia(**DataTeritorial.merge(ctx, **kwargs))