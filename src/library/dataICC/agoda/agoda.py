import asyncio

from requests import Session, Response
from aiohttp import ClientSession
from .paramsBuilder import ParamsBuilder
from .provinceEnum import ProvinceEnum
from json import dumps
from concurrent.futures import ThreadPoolExecutor

from time import time
from src.helpers import ConnectionKafka, Iostream, ConnectionS3, Datetime

class BaseAgoda:
    def __init__(self, **kwargs) -> None:
        self.__s3: bool = kwargs.get('s3')
        self.__kafka: bool = kwargs.get('kafka')
        self.__clean: bool = kwargs.get('clean')
        self.__headers: dict = {
            'accept': '*/*',
            'accept-language': 'id-ID,id;q=0.9,id;q=0.8',
            'ag-debug-override-origin': 'ID',
            'ag-language-locale': 'id-id',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        self.__proxy: dict = {
            'http':  'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }

        self.__requests: Session = Session()
        self.__requests.headers.update(self.__headers)
        self.__requests.proxies.update(self.__proxy)

        if(self.__kafka): 
            self.__bootstrap: str = kwargs.get('bootstrap')
            self.__connectionKafka: ConnectionKafka = ConnectionKafka(kwargs.get('topic'), kwargs.get('bootstrap'))
        
    async def __process_property(self, property: dict, province_enum: ProvinceEnum):
        property_detail: dict = await self.__get_property_detail(property_id := property['propertyId'])
        property_name: str = property['content']['informationSummary']['localeName']

        i: int = 1
        log: dict = {
            "Crawlling_time": Datetime.now(),
            "id_project": None,
            "project": "Data Intelligence",
            "sub_project": "data ICC",
            "source_name": 'agoda',
            "sub_source_name": property_name,
            "id_sub_source": property_id,
            "total_data": 0,
            "total_success": 0,
            "total_failed": 0,
            "status": "Process",
            "assign": "romy",
        }

        Iostream.write_log(log, indent=2, name=__name__)
        while True:
            for _ in range(5):
                reviews = self.__get_reviews(property['propertyId'], i, 5)

                if(reviews): break

            if(not reviews): break

            log['total_data'] += len(reviews)
            Iostream.update_log(log, name=__name__, title=property_name)
            
            for review in reviews:
                self.__process_data(property | property_detail, review, province_enum, log)
                
                # break

            i += 1

            # break

        log['status'] = 'Done'
        Iostream.update_log(log, name=__name__, title=property_name)


    def __process_data(self, property_detail: dict, review: dict, province_enum: ProvinceEnum, log: dict):
        try:
            link: str = f"https://www.agoda.com{property_detail['content']['informationSummary']['propertyLinks']['propertyPage']}"
            link_split: list = link.split('/')
            review_id: str = review["hotelReviewId"]

            data: dict = {
                "link": link,
                "domain": link_split[2],
                "tag": [*link_split[2:], province_enum.name.title()],
                "crawling_time": Datetime.now(),
                "crawling_time_epoch": int(time()),
                'property_detail': property_detail,
                'review_detail': review,
                "path_data_raw": f'S3://ai-pipeline-statistics/data/data_raw/agoda/{province_enum.name.title()}/{link_split[3]}/json/{review_id}.json',
                "path_data_clean": f'S3://ai-pipeline-statistics/data/data_clean/agoda/{province_enum.name.title()}/{link_split[3]}/json/{review_id}.json',
            }


            paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"]]] 

            if(self.__clean):
                paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"], data["path_data_clean"]]] 

            data: dict = Iostream.dict_to_deep(data)
            
            if(self.__kafka):
                self.__connectionKafka.send(data, name=self.__bootstrap)
            else:
                with ThreadPoolExecutor() as executor:
                    try:
                        if(self.__s3):
                            executor.map(lambda path: ConnectionS3.upload(data, path), paths)
                        else:
                            executor.map(lambda path: Iostream.write_json(data, path, indent=2), paths)
                    except Exception as e:
                        raise e
                    
            Iostream.info_log(log, review_id, 'success', name=__name__)
                
            log['total_success'] += 1
            Iostream.update_log(log, name=__name__, title=property_detail['content']['informationSummary']['localeName'])
        except Exception as e:
            print(e)

    def __get_all_provinces(self) -> list:
        return self.__requests.get('https://www.agoda.com/api/cronos/geo/AllStates', 
                                    params={
                                        'objectId': 192
                                    }).json()

    
    async def __get_property_detail(self, property_id: int) -> dict:
        async with ClientSession() as session:
            async with session.post('https://www.agoda.com/graphql/property', 
                                   headers=self.__requests.headers,
                                   json=ParamsBuilder.detailParams(property_id),
                                   ) as response:
                
                response_json: dict = await response.json()
                self.__requests.headers.update(response.headers)

                return response_json['data']['propertyDetailsSearch']['propertyDetails'][0]

    def __get_reviews(self, property_id: int, page: int, size: int) -> dict: 
        return self.__requests.post('https://www.agoda.com/api/cronos/property/review/ReviewComments',                       
                                    json=ParamsBuilder.reviewParams(property_id, page, size)
                                    ).json()['comments']
    
    def __get_object_id_by_keyword(self, keyword: str) -> int: 
        response: Response = self.__requests.get('https://www.agoda.com/api/cronos/search/GetUnifiedSuggestResult/3/26/26/0/id-id/',                      
                                                params={
                                                    'searchText': keyword,
                                                    'origin': 'ID'
                                                })
        return response.json()['ViewModelList'][0]['ObjectId']

    def __get_properties_by_city_id(self, city_id: int, page: int, size: int, token: str = '') -> tuple:
        response: Response = self.__requests.post('https://www.agoda.com/graphql/search', 
                                                  json=ParamsBuilder.cityParams(city_id, page, size, token))

        result: dict = response.json()['data']['citySearch']

        return (result['properties'], result['searchEnrichment']['pageToken'])
        

    async def _get_detail_by_province_id(self, province_enum: ProvinceEnum) -> list:
        response: Response = self.__requests.get('https://www.agoda.com/api/cronos/geo/NeighborHoods',
                                                params={
                                                    'pageTypeId': 8,
                                                    'objectId': province_enum.value
                                                })
        
        for city in response.json():
            (properties, token, page) = (None, '', 1) 
            while(True):
                for _ in range(5):
                    (properties, token) = self.__get_properties_by_city_id(city['hotelId'], page, 3, token)
                    if(properties): break

                if(not properties): break

                await asyncio.gather(*(self.__process_property(property, province_enum) for property in properties))

                page += 1
                # break
            # break
    
    def _get_all(self) -> None:
        asyncio.run(self._get_detail_by_province_id(ProvinceEnum.JAWA_TIMUR))
        # for province in ProvinceEnum:
        #     self._get_detail_by_province_id(province)

if(__name__ == "__main__"):
    BaseAgoda(
        # **{
        #     'topic': 'test', 
        #     'bootstrap': 'localhost:9092',
        #     'kafka': True
        # }
    )._get_all()

# 'test', 'localhost:9092'