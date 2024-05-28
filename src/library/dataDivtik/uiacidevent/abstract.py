from abc import ABC, abstractmethod
from typing import Any, Coroutine

from .uiacidevent import BaseUiacidEvent

class AbstractUiacidEvent(BaseUiacidEvent, ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    async def get_event_by_date(self, year: int, month: int) -> Coroutine[Any, Any, dict]:
        return await super()._get_event_by_date(year, month)