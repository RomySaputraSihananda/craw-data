import requests
import asyncio

from json import loads, dumps
from datetime import datetime
from aiohttp import ClientSession
from time import time
from calendar import month_name

from src.helpers import Parser, Iostream, Datetime

class BaseUiacidEvent:
    def __init__(self, **kwargs) -> None:
        self.__write: bool = kwargs.get('write') 

    async def __get_detail_event(self, url: str) -> dict:
        async with ClientSession() as session:
            async with session.get(url) as response:
                return {
                    data.pop('type'): data
                    for data in loads(Parser(await response.text()).select_one('script[type="application/ld+json"]').string.replace('@', ''))['graph']
                }

    async def _get_event_by_date(self, year: int, month: int) -> dict:
        response = requests.post('https://www.ui.ac.id/wp-json/tribe/views/v2/html', 
                                data={
                                    'view_data[tribe-bar-date]': datetime(year, month, 1).strftime('%Y-%m'),
                                    'url': '',
                                    'prev_url': '',
                                    'should_manage_url': 'true',
                                    '_tec_view_rest_nonce_primary': '513300b6f6',
                                    '_tec_view_rest_nonce_secondary': '',
                                })
        events: list = await asyncio.gather(*(self.__get_detail_event(data['url']) for data in loads(Parser(response.text).select_one('script[type="application/ld+json"]').string.replace('@', ''))))
        
        if(self.__write):
            for event in events:
                data: dict = {
                    "link": (link := 'https://emis.kemenag.go.id/pontren/statistik/pontren'),
                    "domain": (link_split := link.split('/'))[2],
                    "tag": link_split[2:],
                    "crawling_time": Datetime.now(),
                    "crawling_time_epoch": int(time()),
                    **event,
                    "path_data_raw": f'S3://ai-pipeline-raw-data/data/data_descriptive/ui.ac.id/data_event/{year}/{month_name[month].lower()}/json/{event["Event"]["name"].lower().replace(" ", "_")}.json',
                }
                Iostream.write_json(data, data['path_data_raw'].replace('S3://ai-pipeline-raw-data/', ''), indent=4)

        return events


if(__name__ == '__main__'): asyncio.run(BaseUiacidEvent(write=True)._get_event(2024, 5))

