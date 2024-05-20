from abc import ABC, abstractmethod

from.jiexpocomevent import BaseJiexpocomEvent

class AbstractJiexpocomEvent(BaseJiexpocomEvent, ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    async def get_event_by_date(self, month, year):
        return await super()._get_event_by_date(month, year)