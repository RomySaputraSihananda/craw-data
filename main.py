import click 

from typing import final

from services.lemon8 import Lemon8

@final
class Main:
    @staticmethod
    @click.command()
    @click.argument('engine', metavar='ENGINE', type=click.Choice(['lemon8']))
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_user_id', 'by_username']))
    @click.option('--user_id', default=None, help='User ID')
    @click.option('--username', default=None, help='Username')
    @click.option('--s3', default=False, is_flag=True, help='Send to S3 ?')
    def main(**kwargs) -> None:
        match(kwargs.get('engine')):
            case 'lemon8':
                Main.lemon8(**kwargs)
            case 'kafka':
                print(1)
    
    @staticmethod
    def lemon8(**kwargs):
        return Lemon8(**kwargs)

if(__name__ == "__main__"):
    Main.main()
