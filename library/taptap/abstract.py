from abc import ABC, abstractmethod

class AbstractTaptap(ABC):
    @abstractmethod
    def get_all_platform(self, *args, **kwargs) -> None:
        ...
    
    @abstractmethod
    def get_by_platform(self, *args, **kwargs) -> None:
        ...
    
    @abstractmethod
    def get_by_app_id(self, *args, **kwargs) -> None:
        ...