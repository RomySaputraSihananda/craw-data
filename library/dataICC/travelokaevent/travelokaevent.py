import re
import os
import asyncio

from aiohttp import ClientSession
from requests import Response, Session
from json import loads, dumps
from dotenv import load_dotenv
from time import time
from concurrent.futures import ThreadPoolExecutor

from helpers import Iostream, Datetime, ConnectionS3, Decorator

load_dotenv()

class BaseTravelokaEvent:
    def __init__(self, **kwargs) -> None:
        self.__s3: bool = kwargs.get('s3')
        self.__clean: bool = kwargs.get('clean')
        self.__requests: Session = Session()
        self.__requests.headers.update({
            'user-agent': 'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
            'cookie': os.getenv('COOKIE_TRAVELOKA'),
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'origin': 'https://www.traveloka.com',
            'x-domain': 'experience',
            'x-route-prefix': 'en-id'
        })
    
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

    async def __get_detail_experience(self, experience: dict) -> None:
        experience_id: str = experience["experienceId"]

        link: str = f'https://www.traveloka.com/en-id/activities/indonesia/product/{experience_id}'

        async with ClientSession() as session:
            async with session.get(link) as response:
                response_text: str = await response.text()
                event_detail: dict = loads(re.findall(r'<script id="__NEXT_DATA__" type="application/json" nonce="[^"]*" crossorigin="anonymous">(.*?)</script>', response_text)[0])['props']['pageProps']["productDetailData"]

                link: str = f'https://www.traveloka.com/en-id/activities/indonesia/product/{event_detail["experienceSearchInfo"]["labelEN"]}-{experience_id}'
                link_split: list = link.split('/')

                tickets: list = self.__get_tickets(experience_id)
                (ticket_price_details, ticket_available) = self.__get_ticket_avaliable_dates(experience_id)
                user_reviews: dict = self.__get_user_reviews(experience_id)

                province: str = event_detail["experienceSearchInfo"]["subLabel"].split(',')[1].replace('Province', '').strip(' ')

                headers: dict = {
                    "link": link,
                    "domain": link_split[2],
                    "tag": link_split[2:],
                    "crawling_time": Datetime.now(),
                    "crawling_time_epoch": int(time()),
                    'event_detail': event_detail | experience,
                    'detail_tickets': [ticket | ticket_price_details[i] for i, ticket in enumerate(tickets)],
                    'ticket_available': ticket_available,
                    'user_reviews': user_reviews,
                    "path_data_raw": f'S3://ai-pipeline-statistics/data/data_raw/traveloka/event/{province}/{link_split[-1]}.json',
                    "path_data_clean": f'S3://ai-pipeline-statistics/data/data_raw/traveloka/event/{province}/{link_split[-1]}.json',
                }

                paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [headers["path_data_raw"]]] 
                
                if(self.__clean):
                    paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [headers["path_data_raw"], headers["path_data_clean"]]] 
                
                with ThreadPoolExecutor() as executor:
                    headers: dict = Iostream.dict_to_deep(headers)
                    try:
                        if(self.__s3):
                            executor.map(lambda path: ConnectionS3.upload(headers, path), paths)
                        else:
                            executor.map(lambda path: Iostream.write_json(headers, path), paths)
                    except Exception as e:
                        raise e

                return Iostream.dict_to_deep(headers)

    async def __get_experience_by_location(self, location_id: str) -> None:
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

        await asyncio.gather(*(self.__get_detail_experience(experience) for experience in experiences))

    @Decorator.counter_time
    def start(self) -> None:
        asyncio.run(self.__get_experience_by_location('100003'))

if(__name__ == '__main__'):
    baseTravelokaEvent: BaseTravelokaEvent = BaseTravelokaEvent()

    baseTravelokaEvent.start()
