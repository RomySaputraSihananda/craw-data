import click
import asyncio

from src.library.dataICC import AbstractTravelokaEvent, BaseTravelokaEvent, GeoEnum
from src.helpers import Decorator, logging

class TravelokaEvent(BaseTravelokaEvent, AbstractTravelokaEvent):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
        method: str = str(kwargs.get('method'))

        match(method):
            case 'by_location':
                if(not kwargs.get('location')): raise click.BadParameter("--location is required for :method 'by_location'")

                location: str = kwargs.get('location').replace('_', ' ').replace(' ', '_').upper()
                if(location not in GeoEnum.__members__): raise click.BadParameter("location not found !!")

                self.get_experience_by_location(location=location)
            case 'all_location':
                start: str = kwargs.get('start').replace('_', ' ').replace(' ', '_').upper()
                if(start not in GeoEnum.__members__): raise click.BadParameter("start location not found !!")
        
                self.get_experience_all_location(start=start)
            case _:
                logging.error('Wait.............')

    @Decorator.counter_time
    def get_experience_by_location(self, **kwargs) -> None:
        return asyncio.run(super()._get_experience_by_location(GeoEnum[kwargs.get('location')]))
    
    @Decorator.counter_time
    def get_experience_all_location(self, **kwargs) -> None:
        return super()._get_experience_all_location(GeoEnum[kwargs.get('start')])

if(__name__ == '__main__'):
    TravelokaEvent(**{
        'method': 'by_location',
        'location': 'jawa_timur'
    })