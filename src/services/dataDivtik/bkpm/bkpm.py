from src.library.dataDivtik import AbstractBkpm

class Bkpm(AbstractBkpm):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.start(**kwargs)
    
    def start(self, **kwargs) -> None:
        return super().start(**kwargs)