from abc import ABC, abstractmethod

class AbstractQuora(ABC):
    @abstractmethod
    def get_answers_by_question_str(self, *args, **kwargs) -> None:
        ...