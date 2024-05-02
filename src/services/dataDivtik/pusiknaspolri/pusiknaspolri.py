from src.helpers import logging, Decorator 
from src.library.dataDivtik import AbstractPusiknasPolri

class PusiknasPolri(AbstractPusiknasPolri):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
        match(kwargs.get('method')):
            case 'yesterday':
                print(self.get_yesterday())
            case 'by_date':
                self.get_by_date(kwargs.get('date'))
            case _ :
                logging.error('Wait.............')
    
    @Decorator.counter_time
    def get_by_date(self, date: str) -> None:
        return super().get_by_date(date)
    
    @Decorator.counter_time
    def get_by_range(self, **kwargs) -> None:
        return super().get_by_range(**kwargs)
    
    @Decorator.counter_time
    def get_yesterday(self) -> None:
        return super().get_yesterday()