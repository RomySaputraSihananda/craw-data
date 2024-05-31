import requests
import asyncio


from requests import Response
from json import loads, dumps
from datetime import datetime
from aiohttp import ClientSession
from time import time
from calendar import month_name

from src.helpers import Parser, Iostream, Datetime, ConnectionS3

class BaseUiacidEvent:
    def __init__(self, **kwargs) -> None:
        self.__write: bool = kwargs.get('write') 
        self.__token: dict = self.get_token()
    
    @staticmethod
    def get_token() -> dict:
        response: Response = requests.get('https://www.ui.ac.id/events/month')
        
        return loads(Parser(response.text).select_one('script[data-js="tribe-events-view-nonce-data"]').string)

    async def __get_detail_event(self, url: str) -> dict:
        async with ClientSession() as session:
            async with session.get(url) as response:
                return {
                    data.pop('type'): data
                    for data in loads(Parser(await response.text()).select_one('script[type="application/ld+json"]').string.replace('@', ''))['graph']
                }

    async def _get_event_by_date(self, year: int, month: int) -> list:
        response: Response = requests.post('https://www.ui.ac.id/wp-json/tribe/views/v2/html', 
                                            data={
                                                'view_data[tribe-bar-date]': datetime(year, month, 1).strftime('%Y-%m'),
                                                'url': '',
                                                'prev_url': '',
                                                'should_manage_url': 'true',
                                                **self.__token
                                            })
        try:
            events: list = await asyncio.gather(*(self.__get_detail_event(data['url']) for data in loads(Parser(response.text).select_one('script[type="application/ld+json"]').string.replace('@', ''))))
        except:
            return []
        
        if(self.__write):
            for event in events:
                data: dict = {
                    "link": (link := (Event := event["Event"])['url']),
                    "domain": (link_split := link.split('/')[:-1])[2],
                    "tag": link_split[2:],
                    "crawling_time": Datetime.now(),
                    "crawling_time_epoch": int(time()),
                    **event,
                    "path_data_raw": f'S3://ai-pipeline-raw-data/data/data_descriptive/ui.ac.id/data_event/{year}/{month_name[month].lower()}/json/{Event["name"].lower().replace(" ", "_")}.json',
                }

                # Iostream.write_json(data, data['path_data_raw'].replace('S3://ai-pipeline-raw-data/', ''), indent=4)
                ConnectionS3.upload(data, data['path_data_raw'].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')

        return events
    
    async def _get_event_by_year(self, year: int) -> iter:
        for month in range(1, 12 + 1):
            await self._get_event_by_date(year, month)


if(__name__ == '__main__'): 
    uiacidEvent: BaseUiacidEvent = BaseUiacidEvent(write=True)
    for year in range(2020, 2024 + 1):
        asyncio.run(uiacidEvent._get_event_by_year(year))

