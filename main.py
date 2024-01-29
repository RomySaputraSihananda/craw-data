import click 

from typing import final

from services.lemon8 import Lemon8

@final
class Main:
    @click.group()
    def main(**kwargs) -> None:
        pass

    @staticmethod
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_user_id', 'by_username', 'by_url', 'by_keyword']))
    @click.option('--user_id', default=None, help='User ID')
    @click.option('--username', default=None, help='Username')
    @click.option('--url', default=None, help='Url')
    @click.option('--s3', default=False, help='Send to S3 ?')
    def lemon8(**kwargs):
        return Lemon8(**kwargs)

if(__name__ == "__main__"):
    Main.main()
