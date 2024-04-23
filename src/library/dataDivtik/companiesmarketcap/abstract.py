from abc import ABC, abstractmethod

from .companiesmarketcap import BaseCompaniesMarketCap

class AbstractCompaniesMarketCap(BaseCompaniesMarketCap, ABC):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    @abstractmethod
    def start(self, *args, **kwargs) -> None:
        return super()._start(*args, **kwargs)


if(__name__ == '__main__'):
    AbstractCompaniesMarketCap().start()