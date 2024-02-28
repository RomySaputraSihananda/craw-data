from click import Context

from abc import ABC, abstractmethod
from typing import Any

class BaseGroupClick(ABC):
    @staticmethod
    def merge(ctx: Context, **kwargs) -> dict:
        return {**ctx.obj, **kwargs}
    
    @abstractmethod
    def main(*args, **kwargs) -> Any:
        ...