import click

from src.library.dataICC import AbstractAgoda, ProvinceEnum
from src.helpers import Decorator, logging

class Agoda(AbstractAgoda):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        method: str = str(kwargs.get('method'))

        match(method):
            case 'by_province':
                if(not kwargs.get('province')): raise click.BadParameter("--province is required for :method 'by_province'")

                province: str = kwargs.get('province').replace('_', ' ').replace(' ', '_').upper()
                if(province not in ProvinceEnum.__members__): raise click.BadParameter("province not found !!")

                self.get_detail_by_province(province=ProvinceEnum[province])
            case 'all_detail':
                start: str = kwargs.get('start').replace('_', ' ').replace(' ', '_').upper() if kwargs.get('start') else None
                # if(start not in ProvinceEnum.__members__ and start): raise click.BadParameter("start location not found !!")
        
                self.get_all_detail()
            case 'watch_beanstalk':
                self.watch_beanstalk()
            case _:
                logging.error('Wait.............')
    
    @Decorator.counter_time
    def get_detail_by_province(self, *args, **kwargs) -> None:
        return super().get_detail_by_province(*args, **kwargs)
    
    @Decorator.counter_time
    def get_all_detail(self, *args, **kwargs) -> None:
        return super().get_all_detail(*args, **kwargs)
    
    @Decorator.counter_time
    def watch_beanstalk(self):
        return super()._watch_beanstalk()