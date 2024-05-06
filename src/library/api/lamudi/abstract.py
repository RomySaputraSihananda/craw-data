from abc import ABC, abstractmethod
from typing import Any, Coroutine

from .lamudi import BaseLamudi

class AbstractLamudi(BaseLamudi, ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def get_location(self, keyword: str, **kwargs) -> Coroutine[Any, Any, list]:
        return super()._get_location(keyword, **kwargs)
    
    @abstractmethod
    def get_property(self, **kwargs) -> Coroutine[Any, Any, list]:
        return super()._get_property(**kwargs)