from click import command, option, argument

class Main:
    @staticmethod
    @command()
    @argument('method', default='get_by_user_id', help='method want use')
    @option('--user_id', default=1, help='user_id')
    def main(**kwargs) -> None:
        pass

if(__name__ == "__main__"):
    Main.main()