import asyncio
import requests
import re
import asyncio

from aiohttp import ClientSession
from requests import Response
from json import dumps, loads

class Lemon8:
    def __init__(self) -> None:
        self.__request: ClientSession = None
    
    @staticmethod
    def get_user_profile(user_id) -> dict:
        response: Response = requests.get(
            'https://api22-normal-useast1a.lemon8-app.com/api/550/user/profile/homepage',
            params={
                'user_id': user_id,
                'aid': '2657',
            },
            headers={
                'User-Agent': 'com.bd.nproject/55014 (Linux; U; Android 9; en_US; unknown; Build/PI;tt-ok/3.12.13.1)',
            },
        )

        return response.json()['data']
    
    @staticmethod
    def get_user_posts(user_id) -> dict:
        response: Response = requests.get(
            'https://api22-normal-useast1a.lemon8-app.com/api/550/stream',
            params={
                'category': '486', 
                'count': '1000', 
                'category_parameter': user_id, 
                'session_cnt': '1', 
                'aid': '2657', 
                'device_platform': 'android', 
            },
            headers={
                'User-Agent': 'com.bd.nproject/55014 (Linux; U; Android 9; en_US; unknown; Build/PI;tt-ok/3.12.13.1)',
            },
        )

        return loads(re.sub(r'<[^>]*>', '', dumps(response.json(), ensure_ascii=False)))['data']['items']

    async def __get_comments(self, post) -> None:
        async with self.__request.get('https://api22-normal-useast1a.lemon8-app.com/api/550/comment_v2/comments',                             
                                    params={
                                        'group_id': post['group_id'], 
                                        'item_id': post['item_id'], 
                                        'media_id': post['media_id'], 
                                        'count': '1000', 
                                        'aid': '2657', 
                                    }) as response:
            comments = await response.json()

        return await asyncio.gather(*(self.__get_detail_comment(comment["id"], post) for comment in comments['data']['data']))        

    async def __get_detail_comment(self, comment_id, post):
        async with self.__request.get('https://api22-normal-useast1a.lemon8-app.com/api/550/comment_v2/detail',
                                params={
                                    'group_id': post['group_id'], 
                                    'item_id': post['item_id'], 
                                    'media_id': post['media_id'], 
                                    'comment_id': comment_id, 
                                    'count': '1000', 
                                    'aid': '2657', 
                                    'language': 'en', 
                                },
                                ) as response:
            data = await response.json()
        
        return data

    async def get_comments_by__user_id(self, user_id) -> None:
        self.__request: ClientSession = ClientSession(headers={
            'User-Agent': 'com.bd.nproject/55014 (Linux; U; Android 9; en_US; unknown; Build/PI;tt-ok/3.12.13.1)',
        })

        posts: dict = self.get_user_posts(user_id)
        data = await asyncio.gather(*(self.__get_comments(post) for post in posts))


        print(dumps(data, indent=4, ensure_ascii=False))

        await self.__request.close()


if(__name__ == '__main__'):
    lemon8: Lemon8 = Lemon8()

    asyncio.run(lemon8.get_comments_by__user_id('7138599741986915329'))