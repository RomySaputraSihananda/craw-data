from src.library.dataDivtik import AbstractBnn

class Bnn(AbstractBnn):
    def __init__(self) -> None:
        super().__init__()
        self.start()
    
    def start(self, *args, **kwargs) -> None:
        return super().start(*args, **kwargs)