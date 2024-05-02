import asyncio

from abc import ABC, abstractmethod
from .agoda import BaseAgoda

class AbstractAgoda(ABC, BaseAgoda):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @abstractmethod
    def get_detail_by_province(self, *args, **kwargs) ->  None:
        return self._get_detail_by_province(*args, kwargs.get('province'))

    @abstractmethod
    def get_all_detail(self, *args, **kwargs) -> None: 
        return self._get_all_detail(*args, **kwargs )
    
    @abstractmethod
    def watch_beanstalk(self):
        return super()._watch_beanstalk()

if(__name__ == "__main__"):
    BaseAgoda()._get_all_detail()