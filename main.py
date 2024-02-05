import click

from typing import final

from services.lemon8 import Lemon8 
from services.quora import Quora 

@final
class Main:
    @click.group()
    def main(**kwargs) -> None:
        """ Main Engine """
        ...

    @staticmethod
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_user_id', 'by_username', 'by_url', 'by_post_id']))
    @click.option('--user_id', default=None, help='User ID')
    @click.option('--post_id', default=None, help='Post ID')
    @click.option('--username', default=None, help='Username')
    @click.option('--url', default=None, help='Url')
    @click.option('--s3', default=False, help='Send to S3 ?')
    @click.option('--clean', default=False, help='Send to clean path')
    def lemon8(**kwargs):
        """ Lemon8 Engine """
        return Lemon8(**kwargs)

    @staticmethod
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_question_str']))
    @click.option('--s3', default=False, help='Send to S3 ?')
    @click.option('--clean', default=False, help='Send to clean path')
    @click.option('--question', default=None, help='Question')
    def quora(**kwargs):
        """ Quora Engine """
        return Quora(**kwargs)

if(__name__ == "__main__"):
    Main.main()
