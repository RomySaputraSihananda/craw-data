from greenstalk import Client

class BeanStalk:
    def __init__(
        self: 'BeanStalk',
        host: str,
        port: int,
        tube: str
    ) -> None:
        self._beanstalk_watch: Client = Client(
            (host, port),
            watch=tube
        )
        self._beanstalk_use: Client = Client(
            (host, port),
            use=tube
        )
    @property
    def watch(
        self: 'BeanStalk'
    ) -> Client:
        return self._beanstalk_watch

    @property
    def use(
        self: 'BeanStalk'
    ) -> Client:
        return self._beanstalk_use