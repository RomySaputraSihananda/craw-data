from abc import ABC, abstractmethod

from .bdsp import BaseBdsp

class AbstrackBdsp(BaseBdsp, ABC):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    # @abstractmethod
    # def 