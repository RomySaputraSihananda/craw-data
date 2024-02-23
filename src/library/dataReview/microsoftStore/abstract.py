from abc import ABC, abstractmethod

class AbstractMicrosoftStore(ABC):
    @abstractmethod
    def get_by_product_id(self, *args, **kwargs) -> None:
        ...
    @abstractmethod
    def get_by_media_type(self, *args, **kwargs) -> None:
        ...
    @abstractmethod
    def get_all_media(self, *args, **kwargs) -> None:
        ...
        