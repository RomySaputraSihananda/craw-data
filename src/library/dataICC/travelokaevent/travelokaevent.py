import re
import os
import asyncio

from aiohttp import ClientSession
from requests import Response, Session
from json import loads, dumps
from dotenv import load_dotenv
from time import time
from concurrent.futures import ThreadPoolExecutor

from src.helpers import Iostream, Datetime, ConnectionS3, ConnectionKafka
from .geoenum import GeoEnum

load_dotenv()

class BaseTravelokaEvent:
    def __init__(self, **kwargs) -> None:
        self.__s3: bool = kwargs.get('s3')
        self.__kafka: bool = kwargs.get('kafka')
        self.__clean: bool = kwargs.get('clean')
        
        if(self.__kafka): 
            self.__bootstrap: str = kwargs.get('bootstrap')
            self.__topik: str = kwargs.get('topic')
            self.__connectionKafka: ConnectionKafka = ConnectionKafka(kwargs.get('bootstrap'))

        self.__headers: dict = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
            'cookie': os.getenv('COOKIE_TRAVELOKA'),
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'origin': 'https://www.traveloka.com',
            'x-domain': 'experience',
            'x-route-prefix': 'id-id'
        }
        
        self.__requests: Session = Session()
        self.__requests.headers.update(self.__headers)
    
    async def __get_recomendation_by_loation(self, geo: GeoEnum, log: dict) -> None:
        start: int = 0
        while(True):
            experiences: list = self.__get_recomendation_by_loation_page(geo, start)
            
            if(not experiences): break

            log['total_data'] += len(experiences)
            Iostream.update_log(log, name=__name__, title=geo.name)

            await asyncio.gather(*(self.__get_detail_experience(experience, log, geo) for experience in experiences))

            start += 12

        log['status'] = 'Done'
        Iostream.update_log(log, name=__name__, title=geo.name)

    def __get_recomendation_by_loation_page(self, geo: GeoEnum, start: int) -> list:
        response: Response = self.__requests.post('https://www.traveloka.com/api/v2/experience/softRecommendation',
                                                    json={
                                                        'fields': [],
                                                        'data': {
                                                            'caller': 'SEARCH_RESULT',
                                                            'currency': 'IDR',
                                                            'sortType': 'MOST_POPULAR',
                                                            'filters': {
                                                                'typeFilterList': [
                                                                    'EVENT',
                                                                ],
                                                                'priceFilter': {
                                                                    'minPrice': None,
                                                                    'maxPrice': None,
                                                                },
                                                                'instantVoucherOnly': False,
                                                                'subTypeFilter': [],
                                                                'durationFilter': [],
                                                                'geoIdsFilter': [],
                                                                'availabilityFilter': [],
                                                                'featureFilter': [],
                                                                'promoFilterList': [],
                                                            },
                                                            'basicSearchSpec': {
                                                                'searchType': 'GEO',
                                                                'entityId': geo.value,
                                                            },
                                                            'rowsToReturn': 12,
                                                            'skip': start,
                                                            'recommendationType': None,
                                                        },
                                                        'clientInterface': 'desktop',
                                                    })
        
        return response.json()['data']['results']

    def __get_user_reviews(self, experience_id: str) -> dict:
        response: Response = self.__requests.post('https://www.traveloka.com/api/v2/experience/reviews',         
                                                    json={
                                                        'fields': [],
                                                        'data': {
                                                            'experienceId': experience_id,
                                                            'skip': 0,
                                                            'rowsToReturn': 20,
                                                        },
                                                        'clientInterface': 'desktop',
                                                    })
        
        return response.json()['data']['userReviews']

    def __get_tickets(self, experience_id: str) -> list:
        response: Response = self.__requests.post('https://www.traveloka.com/api/v2/experience/ticketListV2',       
                                                json={
                                                    'fields': [],
                                                    'data': {
                                                        'experienceId': experience_id,
                                                        'sortBy': 'LOWEST_PRICE',
                                                        'currency': 'IDR',
                                                    },
                                                    'clientInterface': 'desktop',
                                                })
        
        return response.json()['data']['ticketTypeDisplays']
    
    def __get_ticket_avaliable_dates(self, experience_id: str) -> tuple:
        response: Response = self.__requests.post('https://www.traveloka.com/api/v2/experience/ticketAvailableDates',       
                                                json={
                                                    'fields': [],
                                                    'data': {
                                                        'experienceId': experience_id,
                                                        'currency': 'IDR'
                                                    },
                                                    'clientInterface': 'desktop',
                                                })
        data: dict = response.json()['data']

        return (data['defaultExperienceTicketIdWithPriceDetails'], data['ticketAvailableDateGroups'])

    async def __get_detail_experience(self, experience: dict, log: dict, geo: GeoEnum) -> None:
        try:
            experience_id: str = experience["experienceId"]

            link: str = f'https://www.traveloka.com/id-id/activities/indonesia/product/{experience_id}'

            async with ClientSession() as session:
                async with session.get(link, headers=self.__headers) as response:
                    response_text: str = await response.text()
                    event_detail: dict = loads(re.findall(r'<script id="__NEXT_DATA__" type="application/json" nonce="[^"]*" crossorigin="anonymous">(.*?)</script>', response_text)[0])['props']['pageProps']["productDetailData"]

                    link: str = f'https://www.traveloka.com/id-id/activities/indonesia/product/{event_detail["experienceSearchInfo"]["labelEN"]}-{experience_id}'
                    link_split: list = link.split('/')

                    tickets: list = self.__get_tickets(experience_id)
                    (ticket_price_details, ticket_available) = self.__get_ticket_avaliable_dates(experience_id)
                    user_reviews: dict = self.__get_user_reviews(experience_id)

                    address: list = [label.replace('Province', '').strip(' ') for label in event_detail["experienceSearchInfo"]["subLabel"].split(',')]

                    data: dict = {
                        "link": link,
                        "domain": link_split[2],
                        "tag": [*link_split[2:], *address],
                        "crawling_time": Datetime.now(),
                        "crawling_time_epoch": int(time()),
                        'event_detail': event_detail | experience,
                        'detail_tickets': [ticket | ticket_price_details[i] for i, ticket in enumerate(tickets)],
                        'ticket_available': ticket_available,
                        'user_reviews': user_reviews,
                        "path_data_raw": f'S3://ai-pipeline-statistics/data/data_raw/traveloka/event/{address[1]}/{link_split[-1]}.json',
                        "path_data_clean": f'S3://ai-pipeline-statistics/data/data_raw/traveloka/event/{address[1]}/{link_split[-1]}.json',
                    }

                    paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"]]] 
                    
                    if(self.__clean):
                        paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"], data["path_data_clean"]]] 
                    

                    data: dict = Iostream.dict_to_deep(data)
                    
                    if(self.__kafka):
                        self.__connectionKafka.send(self.__topik, data, name=self.__bootstrap)
                    else:
                        with ThreadPoolExecutor() as executor:
                            try:
                                if(self.__s3):
                                    executor.map(lambda path: ConnectionS3.upload(data, path), paths)
                                else:
                                    executor.map(lambda path: Iostream.write_json(data, path), paths)
                            except Exception as e:
                                raise e
                    
                    
                    log['total_success'] += 1
                    Iostream.update_log(log, name=__name__, title=geo.name)
        
        except Exception as e:
            self.__get_detail_experience(experience, log, geo)

    async def _get_experience_by_location(self, geo: GeoEnum) -> None:
        location_id: str = geo.value
        response: Response = self.__requests.post('https://www.traveloka.com/api/v2/experience/searchV2',
                                                  json={
                                                    'fields': [],
                                                    'data': {
                                                        'currency': 'IDR',
                                                        'caller': 'SEARCH_RESULT',
                                                        'basicSearchSpec': {
                                                            'searchType': 'GEO',
                                                            'entityId': location_id,
                                                        },
                                                        'filters': {
                                                            'availabilityFilter': [],
                                                            'durationFilter': [],
                                                            'featureFilter': [],
                                                            'geoIdsFilter': [],
                                                            'instantVoucherOnly': False,
                                                            'priceFilter': {
                                                                'minPrice': None,
                                                                'maxPrice': None,
                                                            },
                                                            'promoFilterList': [],
                                                            'subTypeFilter': [],
                                                            'typeFilterList': [
                                                                'EVENT',
                                                            ],
                                                        },
                                                        'sortType': 'MOST_POPULAR',
                                                        'rowsToReturn': 50,
                                                        'skip': 0
                                                    },
                                                    'clientInterface': 'desktop',
                                                })
        experiences: list = response.json()['data']['results']
        

        log: dict = {
            "Crawlling_time": Datetime.now(),
            "id_project": None,
            "project": "Data Intelligence",
            "sub_project": "data ICC",
            "source_name": 'traveloka',
            "sub_source_name": geo.name,
            "id_sub_source": location_id,
            "total_data": len(experiences),
            "total_success": 0,
            "total_failed": 0,
            "status": "Process",
            "assign": "romy",
        }
        Iostream.write_log(log, indent=2, name=__name__)

        if(not experiences): return await self.__get_recomendation_by_loation(geo, log)
        

        await asyncio.gather(*(self.__get_detail_experience(experience, log, geo) for experience in experiences))

        log['status'] = 'Done'
        Iostream.update_log(log, name=__name__, title=geo.name)

    def _get_experience_all_location(self, start: GeoEnum) -> None:
        for i in GeoEnum if not start else list(GeoEnum)[list(GeoEnum).index(start):]:
            asyncio.run(self._get_experience_by_location(i))

if(__name__ == '__main__'):
    baseTravelokaEvent: BaseTravelokaEvent = BaseTravelokaEvent()

