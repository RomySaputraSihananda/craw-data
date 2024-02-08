import asyncio
import requests
import re

from aiohttp import ClientSession
from requests import Response

class BaseMicrosoftStore:
    def __init__(self) -> None:
        self.__requests: ClientSession = None 
    
    async def __get_detail(self, product_id: int) -> dict:
        async with self.__requests.get('https://microsoft-store.azurewebsites.net/api/pages/pdp', 
                                        params={
                                            'productId': product_id
                                        }) as response:

            return await response.json()
        
    async def __get_rating(self, product_id: int) -> dict: 
        async with self.__requests.get(f'https://microsoft-store.azurewebsites.net/api/Products/GetReviewsSummary/{product_id}') as response:
            return await response.json()
        
    async def __get_reviews(self, product_id: int) -> list: 
        reviews: list = []
        i: int = 1

        while(True):
            async with self.__requests.get(f'https://microsoft-store.azurewebsites.net/api/products/getReviews/{product_id}',
                                            params={
                                                'pgNo': i,
                                                'noItems': 25,
                                            }) as response:
                response_json: dict = await response.json()

                items: list = response_json['items']
                has_more_pages: bool = response_json['hasMorePages']

                reviews.extend(items)

            if (not has_more_pages): break
            i += 1

        return reviews
    
    async def __process(self, product_id: str) -> None:
        app: dict = await self.__get_detail(product_id)
        rating: dict = await self.__get_rating(product_id)
        reviews: list = await self.__get_reviews(product_id)

        link: str = f'https://microsoft-store.azurewebsites.net/detail/${app["productId"]}'
        link_split: list = link.split("/")

        # title: str = app['title']

        print(link_split[2])

    async def _get_by_media_type(self, media_type: str):
        self.__requests: ClientSession = ClientSession()
        async with self.__requests.get('https://microsoft-store.azurewebsites.net/api/Reco/GetCollectionFiltersList', 
                                        params={
                                            'mediaType': media_type
                                        }) as response:
            response_json = await response.json()
            for choice in response_json[0]['choices']:
                choice_id: str = re.sub(r'^.', choice['choiceId'][0].upper(), choice['choiceId'])

                page: int = 1
                while(True):
                    response: Response = requests.get('https://microsoft-store.azurewebsites.net/api/Reco/GetComputedProductsList',
                        params={
                            'listName': choice_id,
                            'pgNo': page,
                            'noItems': 5,
                            'filteredCategories': "AllProducts",
                            'mediaType': media_type,
                        }
                    )
                    
                    response_json: dict = response.json()
                    
                    products_list: list = response_json['productsList']
                    if (response_json['nextPageNumber'] < 0): break

                    await asyncio.gather(*(self.__process(product['productId']) for product in products_list))
                    break

                    page += 1
                
                break

        await self.__requests.close()

    async def _get_all(self):
        for media_type in ("games", "apps"):
            await self._get_by_media_type(media_type)
        
    async def _start(self):
        self.__requests: ClientSession = ClientSession()
        print("hello")

        await self.__requests.close()


if(__name__ == '__main__'):
    microsoftStore: BaseMicrosoftStore = BaseMicrosoftStore()
    asyncio.run(microsoftStore._get_by_media_type('games'))