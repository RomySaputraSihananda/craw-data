from abc import ABC, abstractmethod

class AbstractLemon8(ABC):
    @abstractmethod
    def get_comments_by_user_id(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def get_comments_by_username(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def get_comments_by_url(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def get_comments_by_post_id(self, *args, **kwargs) -> None:
        ...