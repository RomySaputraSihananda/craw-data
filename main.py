from click import command, option

class Main:
    def __init__(self, **kwargs) -> None:
        print(kwargs)

@command()
@option('--count', default=1, help='number of greetings')
@option('--count2', default=1, help='number of greetings')
def main(**kwargs) -> None:
    Main(**kwargs)


if(__name__ == "__main__"):
    main()