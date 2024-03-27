import os
import re
import asyncio

from dotenv import load_dotenv
from json import dumps, loads
from requests import Response, Session
from aiohttp import ClientSession

from .categoryEnum import PenawaranEnum

load_dotenv()

class BaseLamudi:
    def __init__(self) -> None: 
        self.__requests: Session = Session()
        self.__requests.headers.update({
            'Authorization': os.getenv('AUTH_LAMUDI'),
            'Content-Type': 'application/x-ndjson',
            'User-Agent': 'okhttp/4.10.0'
        }) 
    
    @staticmethod
    def query_builder(index: str, query: dict, **kwargs) -> str:
        data: list = [
            {"index": index}, 
            {
                "from": (kwargs.get('page', 1) - 1) * kwargs.get('size', 10),
                "query": query,
                "size": kwargs.get('size', 10),
                "track_total_hits": 1000000
            }
        ]
        return f"""
{dumps(data[0])}
{dumps(data[1])}
"""

    async def __proccess_property(self, property: dict) -> dict:
        async with ClientSession() as session:
            async with session.get(url := f'https://www.lamudi.co.id/{property["slug"]}.html', headers=self.__requests.headers) as response: 
                if not (match := re.search(r'dataLayer\s*=\s*\[(.*?)\];', await response.text(), re.DOTALL)): return {}
                
                cleaned_json_string = re.sub(r'"device_agent":.*?,\n', '', match.group(1))
                cleaned_json_string = re.sub(r'JSON\.parse\("(.*?)"\)', r'\1', cleaned_json_string)
                cleaned_json_string = re.sub(r',\s*}', '}', cleaned_json_string)

                property['photoIDs'] = [f'https://lamudi-id-production.s3.amazonaws.com/thumbnails/{photo_id}-800x600.webp' for photo_id in property['photoIDs']]

                return {'url': url} | loads(cleaned_json_string) | property
                

    async def _get_property(self, **kwargs) -> list:
        query: dict = {
            "bool": {
                "must": [
                    {
                        "term": {
                            "purpose": kwargs.get('penawaran').value
                        }
                    },
                ]
            }
        } 

        add_query: function = lambda data: query['bool']['must'].append(data)

        if(location_keyword := kwargs.get('location_keyword')):
            location_slugs: list = [location['slug'] for location in await self._get_location(location_keyword, size=5)]
            
            if(location_slug := kwargs.get('location_slug')): location_slugs.append(location_slug)
            print(location_slugs)

            add_query(
                {
                    "terms": {
                        "location.slug": location_slugs
                    }
                }
            )
            
        if(frekuensi := kwargs.get('frekuensi')): 
            add_query(
                {
                    "term": {
                        "rentFrequency": frekuensi.value
                    }
                }
            )

        if(property := kwargs.get('property')): 
            add_query(
                {
                    "term": {
                        "category.slug": property.value
                    }
                }
            )

        if(rentang_harga := kwargs.get('rentang_harga')):
            [gte, lte] = rentang_harga.split('-') 
            add_query(
                {
                    "range": {
                        "price": {
                            "gte": gte,
                            "lte": lte
                        }
                    }
                }
            )

        if(rentang_area := kwargs.get('rentang_area')): 
            [gte, lte] = rentang_area.split('-') 
            add_query(
                {
                    "range": {
                        "area": {
                            "gte": gte,
                            "lte": lte
                        }
                    }
                }
            )

        if(kamar_mandi := kwargs.get('kamar_mandi')): 
            add_query(
                {
                    "bool": {
                        "should": [
                            {
                                "term": {
                                    "baths": kamar_mandi
                                }
                            }
                        ]
                    }
                }
            )

        if(kamar_tidur := kwargs.get('kamar_tidur')): 
            add_query(
                {
                    "bool": {
                        "should": [
                            {
                                "term": {
                                    "rooms": kamar_tidur
                                }
                            }
                        ]
                    }
                }
            )

        if(extra_keyword := kwargs.get('extra_keyword')): 
            add_query(
                {
                    "multi_match":{
                        "fields":"*",
                        "fuzziness":"AUTO",
                        "query":extra_keyword,
                        "type":"most_fields"
                    }
                }
            )

        response: Response = self.__requests.post('https://search.asia.lamudi.sector.run/_msearch/',
                                                    self.query_builder('lamudi-id-production-ads-id', query, **kwargs)
                                                )
        properties: list = [property['_source'] for property in response.json()['responses'][0]['hits']['hits']]
        return await asyncio.gather(*(self.__proccess_property(property) for property in properties))

        
    async def _get_location(self, keyword: str, **kwargs) -> list: 
        async with ClientSession() as session:
            async with session.post('https://search.asia.lamudi.sector.run/_msearch/',
                                    headers=self.__requests.headers,
                                    data=self.query_builder('lamudi-id-production-locations-id',
                                                        {
                                                            "bool": {
                                                                "minimum_should_match": 1,
                                                                "must": [
                                                                    {
                                                                        "match": {
                                                                            "level": kwargs.get('level', 2)
                                                                        }
                                                                    }
                                                                ],
                                                                "should": [
                                                                    {
                                                                        "multi_match": {
                                                                            "fields": "*",
                                                                            "query": keyword,
                                                                            "type": "phrase_prefix"
                                                                        }
                                                                    },
                                                                    {
                                                                        "multi_match": {
                                                                            "fields": "*",
                                                                            "query": keyword,
                                                                            "type": "most_fields"
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        },
                                        **kwargs)
                                    ) as response:
                
                response_json: dict = await response.json()
                return [location['_source'] for location in response_json['responses'][0]['hits']['hits']]

    def start(self):
        self.__get_location('jakarta selatan', page=2)

if(__name__ == '__main__'):
    BaseLamudi().start()
