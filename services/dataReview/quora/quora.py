import click

from typing import final
from helpers import logging

from helpers.decorators import Decorator 
from library.dataReview import BaseQuora, AbstractQuora

@final
class Quora(BaseQuora, AbstractQuora):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        method: str = kwargs.get('method')

        match(method):
            case 'by_question_str':
                if(not kwargs.get('question')): raise click.BadParameter("--question is required for method 'by_question_str'")
                self.get_answers_by_question_str(**kwargs)
            case _:
                logging.error('Wait.............')
    
    @Decorator.counter_time
    def get_answers_by_question_str(self, **kwargs) -> None:
        return super()._get_answers_by_question_str(kwargs.get('question'))

if(__name__ == '__main__'):
    Quora(**{
        'question': 'Bagaimana-kesanmu-terhadap-PT-Pos-Indonesia', 
        'method': 'by_question_str'
    })