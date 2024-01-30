import click 

from typing import final

from services.lemon8 import Lemon8

@final
class Main:
    @click.group()
    @click.option('--s3', default=False, help='Send to S3 ?')
    def main(**kwargs) -> None:
        """ Main Engine """
        pass

    @staticmethod
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_user_id', 'by_username', 'by_url', 'by_post_id']))
    @click.option('--user_id', default=None, help='User ID')
    @click.option('--post_id', default=None, help='Post ID')
    @click.option('--username', default=None, help='Username')
    @click.option('--url', default=None, help='Url')
    def lemon8(**kwargs):
        """ Lemon8 Engine """
        return Lemon8(**kwargs)

if(__name__ == "__main__"):
    Main.main()
