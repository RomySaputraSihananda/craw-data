import asyncio
from aiohttp import ClientSession

class Requests:
    def __init__(self) -> None:
        self.__user_id: str = '7138599741986915329'
        self.__media_id: str = '7147953600210240002'
        self.__request: ClientSession = None
        
    async def fetch_data(self, comment_id):
        async with self.__request.get('https://api22-normal-useast1a.lemon8-app.com/api/550/comment_v2/detail',
                                params={
                                    'group_id': self.__media_id, 
                                    'item_id': self.__media_id, 
                                    'media_id': self.__user_id, 
                                    'comment_id': comment_id, 
                                    'count': '6', 
                                    'dpi': '420', 
                                    'language': 'en', 
                                },
                                ) as response:
            data = await response.json()
            print(data)

    async def get(self):
        self.__request: ClientSession = ClientSession(headers={
            'User-Agent': 'com.bd.nproject/55014 (Linux; U; Android 9; en_US; unknown; Build/PI;tt-ok/3.12.13.1)',
        })

        async with self.__request.get('https://api22-normal-useast1a.lemon8-app.com/api/550/comment_v2/comments',                             
                                    params={
                                        'group_id': self.__media_id, 
                                        'item_id': self.__media_id, 
                                        'media_id': self.__user_id, 
                                        'count': '1000', 
                                        'aid': '2657', 
                                    }) as response:
            data = await response.json()

        await asyncio.gather(*(self.fetch_data(i["id"]) for i in data['data']['data']))
        await self.__request.close()

    def main(self):
        asyncio.run(self.get())

if __name__ == "__main__":
    req = Requests()
    req.main()