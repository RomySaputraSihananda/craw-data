from abc import ABC, abstractmethod

class AbstractGlassdoor(ABC):
    @abstractmethod
    def get_detail_by_employer_id(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def get_detail_by_page(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def get_all_detail(self, *args, **kwargs) -> None:
        ...
