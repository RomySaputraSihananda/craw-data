import asyncio

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

    async def _get_all(self):
        self.__requests: ClientSession = ClientSession()
        for media_type in ("games", "apps"):
            async with self.__requests.get('https://microsoft-store.azurewebsites.net/api/Reco/GetCollectionFiltersList', 
                                           params={
                                               'mediaType': media_type
                                           }) as response:
                print(await response.json())
        
        await self.__requests.close()


    async def _start(self):
        self.__requests: ClientSession = ClientSession()
        print("hello")

        await self.__requests.close()


if(__name__ == '__main__'):
    microsoftStore: BaseMicrosoftStore = BaseMicrosoftStore()
    asyncio.run(microsoftStore._get_all())