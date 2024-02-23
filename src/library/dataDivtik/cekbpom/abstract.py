from abc import ABC, abstractmethod

class AbstractCekbpom(ABC):
    @abstractmethod
    def get_detail_by_product_id(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def get_detail_by_page(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def get_all_detail(self, *args, **kwargs) -> None:
        ...
