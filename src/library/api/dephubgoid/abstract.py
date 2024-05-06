from abc import ABC, abstractmethod
from typing import Any, Coroutine

from .dephubgoid import BaseDephubgoid

class AbstractDephubgoid(BaseDephubgoid, ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def search(self, **kwargs) -> Coroutine[Any, Any, Coroutine]:
        return super()._search(**kwargs)