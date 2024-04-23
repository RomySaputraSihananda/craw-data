from abc import ABC, abstractmethod

from .bkpm import BaseBkpm

class AbstractBkpm(BaseBkpm, ABC):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    

    @abstractmethod
    def start(self, **kwargs) -> None:
        return super()._start(**kwargs)
