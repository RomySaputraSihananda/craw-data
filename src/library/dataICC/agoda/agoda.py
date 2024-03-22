from requests import Session, Response
from aiohttp import ClientSession
from .paramsBuilder import ParamsBuilder
from json import dumps
class Agoda:
    def __init__(self) -> None:
        self.__headers: dict = {
            'accept': '*/*',
            'accept-language': 'id-ID,id;q=0.9,id;q=0.8',
            'ag-debug-override-origin': 'ID',
            'ag-language-locale': 'id-id',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        self.__requests: Session = Session()
        self.__requests.headers.update(self.__headers)

    def __get_all_provinces(self) -> list:
        return self.__requests.get('https://www.agoda.com/api/cronos/geo/AllStates', 
                                    params={
                                        'objectId': 192
                                    }).json()

    
    def __get_detail_property(self, property_id: int) -> dict:
        return self.__requests.post('https://www.agoda.com/graphql/property',
                                    json=ParamsBuilder.detailParams(property_id)
                                    ).json()

    def __get_reviews(self, property_id: int, page: int, size: int) -> dict: 
        return self.__requests.post('https://www.agoda.com/api/cronos/property/review/ReviewComments',                       
                                    json=ParamsBuilder.reviewParams(property_id, page, size)
                                    ).json()
    
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

    def _get_detail_by_province_id(self, province_id: int) -> list:
        response: Response = self.__requests.get('https://www.agoda.com/api/cronos/geo/NeighborHoods',
                                                params={
                                                    'pageTypeId': 8,
                                                    'objectId': province_id
                                                })
        
        for city in response.json():
            (properties, token, page) = (None, '', 1) 
            while(True):
                for _ in range(5):
                    (properties, token) = self.__get_properties_by_city_id(city['hotelId'], page, 10, token)
                    if(properties): break

                if(not properties): break

                for property in properties:
                    print(city['name'], property['content']['informationSummary']['localeName'])

                page += 1
                break

if(__name__ == "__main__"):
    Agoda()._get_detail_by_province_id(3169)

