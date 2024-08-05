import asyncio
import requests

from requests import Session, Response
from aiohttp import ClientSession
from json import dumps, loads
from concurrent.futures import ThreadPoolExecutor
from time import sleep, time
from greenstalk import Client

from .paramsBuilder import ParamsBuilder
from .provinceEnum import ProvinceEnum
from src.helpers import ConnectionKafka, Iostream, ConnectionS3, Datetime

class BaseAgoda:
    def __init__(self, **kwargs) -> None:
        self.__s3: bool = kwargs.get('s3')
        self.__kafka: bool = kwargs.get('kafka')
        self.__clean: bool = kwargs.get('clean')
        self.__timeout: int= kwargs.get('timeout')
        self.__headers: dict = {
            'accept': '*/*',
            'accept-language': 'id-ID,id;q=0.9,id;q=0.8',
            'ag-debug-override-origin': 'ID',
            'ag-language-locale': 'id-id',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        self.__proxy: dict = {
            'http':  'socks5://192.168.29.154:9050',
            'https': 'socks5://192.168.29.154:9050'
        }

        self.__beanstalk_use: Client = Client(('192.168.150.21', 11300), use='dev-target-hotel-agoda')
        self.__beanstalk_watch: Client = Client(('192.168.150.21', 11300), watch='dev-target-hotel-agoda')

        self.__requests: Session = Session()
        self.__requests.headers.update(self.__headers)
        
        if(kwargs.get('proxy')):
            self.__requests.proxies.update(self.__proxy)

        if(self.__kafka): 
            self.__bootstrap: str = kwargs.get('bootstrap')
            self.__connectionKafka: ConnectionKafka = ConnectionKafka(kwargs.get('topic'), kwargs.get('bootstrap'))
        
    def __process_property(self, property: dict, province_name: str):
        property_detail: dict = self.__get_property_detail(property_id := property['propertyId'])
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
        all_reviews: list = []
        while True:
            for _ in range(5):
                reviews: list = self.__get_reviews(property['propertyId'], i, 50)
                if(reviews): break

            if(not reviews): break

            all_reviews.extend(reviews)

            i += 1

        log['total_data'] += len(all_reviews)
        Iostream.update_log(log, name=__name__, title=property_name)
            
        self.__process_data(property | property_detail, all_reviews, province_name, log)

        log['status'] = 'Done'
        log['total_success'] += len(all_reviews)

        Iostream.update_log(log, name=__name__, title=property_name)


    def __process_data(self, property_detail: dict, reviews: dict, province_name: str, log: dict):
        try:
            link: str = f"https://www.agoda.com{property_detail['content']['informationSummary']['propertyLinks']['propertyPage']}"
            link_split: list = link.split('/')

            data: dict = {
                "link": link,
                "domain": link_split[2],
                "tag": [*link_split[2:], province_name.title()],
                "crawling_time": Datetime.now(),
                "crawling_time_epoch": int(time()),
                'property_detail': property_detail,
                'rooms': self.__get_secondary_data(property_detail["propertyId"]),
                'reviews': reviews,
                "path_data_raw": f'S3://ai-pipeline-statistics/data/data_raw/agoda/{province_name.title()}/json/{link_split[3]}.json',
                "path_data_clean": f'S3://ai-pipeline-statistics/data/data_clean/agoda/{province_name.title()}/json/{link_split[3]}.json',
            }

            paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"]]] 

            if(self.__clean):
                paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"], data["path_data_clean"]]] 
            
            del data['path_data_raw']
            del data['path_data_clean']
            
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
                    
            Iostream.info_log(log, {link_split[3]}, 'success', name=__name__)
                
            Iostream.update_log(log, name=__name__, title=property_detail['content']['informationSummary']['localeName'])
        except Exception as e:
            print(e)

    def __get_all_provinces(self) -> list:
        return self.__requests.get('https://www.agoda.com/api/cronos/geo/AllStates', 
                                    params={
                                        'objectId': 192
                                    }).json()

    def __get_secondary_data(self, property_id: str) -> tuple:
        response: Response = self.__requests.get('https://www.agoda.com/api/cronos/property/BelowFoldParams/GetSecondaryData',
            params=ParamsBuilder.secondaryDataParams(property_id)
        ).json()

        return {
            'soldOutRooms': response["soldOutRooms"] if "soldOutRooms" in response else [], 
            'readyRooms': response["roomGridData"]["masterRooms"]
        }
    
    def __get_property_detail(self, property_id: int) -> dict:
        response: Response = self.__requests.post('https://www.agoda.com/graphql/property', 
                                    json=ParamsBuilder.detailParams(property_id),
                                   )                        
                

        return response.json()['data']['propertyDetailsSearch']['propertyDetails'][0]

    def __get_reviews(self, property_id: int, page: int, size: int) -> list: 
        return self.__requests.post('https://www.agoda.com/api/cronos/property/review/ReviewComments',                       
                                    json=ParamsBuilder.reviewParams(property_id, page, size),
                                    ).json()['comments']
    
    def __get_object_id_by_keyword(self, keyword: str) -> int: 
        response: Response = self.__requests.get('https://www.agoda.com/api/cronos/search/GetUnifiedSuggestResult/3/26/26/0/id-id/',                      
                                                params={
                                                    'searchText': keyword,
                                                    'origin': 'ID'
                                                })
        return response.json()['ViewModelList'][0]['ObjectId']

    def __get_properties_by_city_id(self, city_id: int, page: int, size: int, token: str = '') -> tuple:
        print(page)
        response = None
        try:
            response: Response = self.__requests.post('https://www.agoda.com/graphql/search', 
                                            headers=self.__headers,
                                                json=ParamsBuilder.cityParams(city_id, page, size, token))

            result: dict = response.json()['data']['citySearch']

            return (result['properties'], result['searchEnrichment']['pageToken'])
        except:
            print('retry', response)
            return self.__get_properties_by_city_id(city_id, page, size, token)
        

    def _get_detail_by_province(self, province_enum: ProvinceEnum) -> list:
        response: Response = self.__requests.get('https://www.agoda.com/api/cronos/geo/NeighborHoods',
                                                params={
                                                    'pageTypeId': 8,
                                                    'objectId': province_enum.value
                                                })
        
        for city in response.json():
            print(city)
            (properties, token, page) = (None, '', 1) 
            # while(True):
            for _ in range(5):
                (properties, token) = self.__get_properties_by_city_id(city['hotelId'], page, 5)

                if(properties): break

            if(not len(properties)): break


            for property in properties:
                # self.__process_property(property, province_enum) 
                self.__beanstalk_use.put(dumps({'property': property, 'province_name': province_enum.name})) 

            page += 1
    
    def _watch_beanstalk(self):
        while(job := self.__beanstalk_watch.reserve(timeout=self.__timeout)):
            def process():
                data: dict = loads(job.body)
                self.__process_property(data['property'], data['province_name'])
                self.__beanstalk_watch.delete(job)
                
            try:
                process()
            except:
                print('error')
                self.__beanstalk_watch.delete(job)
                sleep(10)

    def _get_all_detail(self) -> None:
        for province in ProvinceEnum:
            asyncio.run(self._get_detail_by_province(province))
    
    def test(self) -> None:
        with open('src/library/dataICC/agoda/test.json', 'r') as file:
            from json import loads
            data = loads(file.read())
        
        asyncio.run(self.__process_property(data, ProvinceEnum.JAWA_TIMUR))

if(__name__ == "__main__"):
    BaseAgoda(
        # **{
        #     'topic': 'test', 
        #     'bootstrap': 'localhost:9092',
        #     'kafka': True
        # }
    )._get_all_detail()

# 'test', 'localhost:9092'
# Hotel Tugu Malang
# The Shalimar Boutique Hotel
# grand mercure malang