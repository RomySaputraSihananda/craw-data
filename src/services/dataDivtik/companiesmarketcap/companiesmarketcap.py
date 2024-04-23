from typing import final

from src.helpers import logging, Decorator 
from src.library.dataDivtik import AbstractCompaniesMarketCap

@final
class CompaniesMarketCap(AbstractCompaniesMarketCap):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.start()

    @Decorator.counter_time
    def start(self, *args, **kwargs) -> None:
        return super().start(*args, **kwargs)

if(__name__ == '__main__'):
    CompaniesMarketCap().start()