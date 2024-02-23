from abc import ABC, abstractmethod

class AbstractTravelokaEvent(ABC):
    @abstractmethod
    def get_experience_by_location(self, *args, **kwargs) -> None:
        ...
    
    @abstractmethod
    def get_experience_all_location(self, *args, **kwargs) -> None:
        ...