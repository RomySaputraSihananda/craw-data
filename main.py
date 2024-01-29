from click import command, option, argument

from services.lemon8 import Lemon8

from typing import final

@final
class Main:
    @staticmethod
    @command()
    @argument('engine', default='lemon8')
    @argument('method', default='by_user_id')
    @option('--user_id', default='7138599741986915329', help='user_id')
    @option('--username', default='jktfoodsquad', help='user_id')
    @option('--s3', default=False, help='send s3 ?')
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