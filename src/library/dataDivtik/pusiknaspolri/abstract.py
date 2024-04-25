from abc import ABC, abstractmethod
from .pusiknaspolri import BasePusiknasPolri

class AbstractPusiknasPolri(BasePusiknasPolri, ABC):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    @abstractmethod
    def get_by_date(self, date: str) -> None:
        return super()._get_by_date(date)
    
    @abstractmethod
    def get_by_range(self, **kwargs) -> None:
        return super()._get_by_range(**kwargs)
    
    @abstractmethod
    def get_yesterday(self) -> None:
        return super()._get_yesterday()