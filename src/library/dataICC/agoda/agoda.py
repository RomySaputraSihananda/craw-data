import asyncio

from requests import Session, Response
from aiohttp import ClientSession
from .paramsBuilder import ParamsBuilder
from .provinceEnum import ProvinceEnum
from json import dumps
from concurrent.futures import ThreadPoolExecutor

from time import sleep, time
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
            'cookie': 'agoda.version.03=CookieId=8e0681f8-949d-4173-8683-3327beded15b&TItems=2$-1$04-01-2024 12:23$05-01-2024 12:23$&DLang=en-us&CurLabel=IDR;FPLC=tk9k9hu%2B9v6FVPsczPhOcedl%2BIkTnA2IjrRy2MYzYOryjEyR4k4D%2FWJhCta1QxC9XopdCZ%2FZ6xP6Mk9vL9r%2BF0ms%2BR7senNhZEJPw%2FZTEag7w1ohqBOoLl8vX2yPKQ%3D%3D;agoda.l2=eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyMGI3M2ZkNS02NmE4LTRjYTctOGUzMy05NGU3MzM1MzRmMTIiLCJtaWQiOjQyODAwNzU0OCwibmJmIjoxNzExMDk2NTEyLCJleHAiOjE3MTEwOTgzMTIsImlhdCI6MTcxMTA5NjUxMn0.rcYJmIG2fnD81lREo7k1VxS3FBB0vfZGu_8evAIBxuzMacPM3SDnyuHVvbZPpF-s;agoda.user.03=UserId=20b73fd5-66a8-4ca7-8e33-94e733534f12;agoda.search.01=SHist=&H=8491|10$71934|9$71934$45582394|8$45582394|0$45582394$44506763;xsrf_token=CfDJ8Dkuqwv-0VhLoFfD8dw7lYzmefb0uoa3OGn2iFWiL0HkMBSYgiMAkeYKF-8x0WRqUbHpoVkTXIRZur6TO0uVUSr-3la8A4d0W25DYQxFSVLEGfp4Kc36nNwQmX-4pqtbUFRH9kcd1FiuqS2EyyZNsF4;agoda.landings=-1|||40bepcthftzsx34k0qt2wbid|2024-04-01T12:23:04|False|19-----1|||40bepcthftzsx34k0qt2wbid|2024-04-01T12:23:04|False|20-----1|||40bepcthftzsx34k0qt2wbid|2024-04-01T12:23:04|False|99;agoda.lastclicks=-1||||2024-04-01T12:23:04||40bepcthftzsx34k0qt2wbid||{"IsPaid":false,"gclid":"","Type":""};_amb=7BB744795D86D6FBE7E1351E214591F4CD00D76C4BFBEF989CC6419B5C47E804059DB94D2C27222A4FDCC7F86C9C861A;agoda.analytics=Id=-338220279402192710&Signature=4836133818910981660&Expiry=1711954448787;agoda.attr.03=ATItems=-1$04-01-2024 12:23$;agoda.consent=ID||2024-04-01 05:54:09Z;agoda.familyMode=Mode=0;agoda.firstclicks=-1||||2024-04-01T12:23:04||40bepcthftzsx34k0qt2wbid||{"IsPaid":false,"gclid":"","Type":""};agoda.price.01=PriceView=1&ApplyGC=1&DefaultApplyGC=1;ASP.NET_SessionId=40bepcthftzsx34k0qt2wbid;FPID=FPID2.2.omnqUA3A6%2BSBVaBbEpOrr9%2B8tETaxysQQM9V9kykrRo%3D.1711087147;token=eyJhbGciOiJFUzI1NiJ9.eyJtIjo0MjgwMDc1NDgsInIiOltdLCJlIjoiSUJDOFU0WEBTVG1aSDg4VW1lZ2VJKilcXDdIWExuZWtmJWFLTjpAWTFVJD5ZbyhKVVBQRXMmOiVfUilkPyVKYDwxUS9dUDZEcXQ6a0Nubzk_Iiwic3JjIjoic3JjIiwic3ViIjoiM1ltWm94ZjFUZlNvQ2cwMFFONlI2dyIsImp0aSI6Il8yVVhacjhUUU1HZ1djd0liZDZlLXciLCJpYXQiOjE3MTEwODg2MTEsImV4cCI6MTcxODg2NDYxMSwid2x0IjoiZjFhNTkwNWYtOTYyMC00NWU1LTlkOTEtZDI1MWMwN2UwYjQyIiwicyI6Nn0.eBR_hHW1SmKoVqP3Kr0khCUkJsQgNi8Y4utsWNnuspIP-cSQBH-ZhJlR-0qTVmErbGv5JtHYSxCnwA9b7fD_sA',
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
        all_reviews: list = []
        while True:
            for _ in range(5):
                reviews: list = self.__get_reviews(property['propertyId'], i, 50)
                if(reviews): break

                sleep(2)
                

            if(not reviews): break

            all_reviews.extend(reviews)

            i += 1

        log['total_data'] += len(all_reviews)
        Iostream.update_log(log, name=__name__, title=property_name)
            
        self.__process_data(property | property_detail, all_reviews, province_enum, log)

        log['status'] = 'Done'
        log['total_success'] += len(all_reviews)

        Iostream.update_log(log, name=__name__, title=property_name)


    def __process_data(self, property_detail: dict, reviews: dict, province_enum: ProvinceEnum, log: dict):
        try:
            link: str = f"https://www.agoda.com{property_detail['content']['informationSummary']['propertyLinks']['propertyPage']}"
            link_split: list = link.split('/')

            data: dict = {
                "link": link,
                "domain": link_split[2],
                "tag": [*link_split[2:], province_enum.name.title()],
                "crawling_time": Datetime.now(),
                "crawling_time_epoch": int(time()),
                'property_detail': property_detail,
                'reviews': reviews,
                "path_data_raw": f'S3://ai-pipeline-statistics/data/data_raw/agoda/{province_enum.name.title()}/json/{link_split[3]}.json',
                "path_data_clean": f'S3://ai-pipeline-statistics/data/data_clean/agoda/{province_enum.name.title()}/json/{link_split[3]}.json',
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

    
    async def __get_property_detail(self, property_id: int) -> dict:
        async with ClientSession() as session:
            async with session.post('https://www.agoda.com/graphql/property', 
                                   headers=self.__requests.headers,
                                   json=ParamsBuilder.detailParams(property_id),
                                   ) as response:
                
                response_json: dict = await response.json()
                self.__requests.headers.update(response.headers)

                return response_json['data']['propertyDetailsSearch']['propertyDetails'][0]

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
        response: Response = self.__requests.post('https://www.agoda.com/graphql/search', 
                                                  json=ParamsBuilder.cityParams(city_id, page, size, token))

        result: dict = response.json()['data']['citySearch']

        return (result['properties'], result['searchEnrichment']['pageToken'])
        

    async def _get_detail_by_province(self, province_enum: ProvinceEnum) -> list:
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
    
    def _get_all_detail(self) -> None:
        for province in ProvinceEnum:
            asyncio.run(self._get_detail_by_province(province))

if(__name__ == "__main__"):
    BaseAgoda(
        # **{
        #     'topic': 'test', 
        #     'bootstrap': 'localhost:9092',
        #     'kafka': True
        # }
    )._get_all()

# 'test', 'localhost:9092'