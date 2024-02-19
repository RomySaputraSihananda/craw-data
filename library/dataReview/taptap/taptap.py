import asyncio
import requests
import re

from aiohttp import ClientSession
from requests import Response
from json import dumps
from typing import final
from time import time
from concurrent.futures import ThreadPoolExecutor

from helpers import Datetime, Iostream, ConnectionS3

class BaseTaptap:
    def __init__(self, **kwargs) -> None:
        self.__s3: bool = kwargs.get('s3')
        self.__clean: bool = kwargs.get('clean')
        self.__platforms: tuple = ("android", "ios", "pc")
        self.__requests: ClientSession = None 
        self.__xua: str = "V=1&PN=WebAppIntl2&LANG=en_US&VN_CODE=114&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=4df88e5d-b4f4-4173-8985-a83672c5d35a&CURR=ID&DT=PC&OS=Linux&OSV=x86_64"

    async def __get_detail_game(self, game_id: str) -> dict:
        async with self.__requests.get('https://www.taptap.io/webapiv2/i/app/v5/detail', 
                                       params={
                                        'id': game_id,
                                        "X-UA": self.__xua,
                                      }) as response:

          response_json: dict = await response.json()
          
          return response_json['data']['app']
    
    async def __get_reviews(self, app_id: str, start: int) -> list | None:
        async with self.__requests.get('https://www.taptap.io/webapiv2/feeds/v1/app-ratings',
                                       params={
                                            'app_id': app_id,
                                            'from': start,
                                            'limit': 50,
                                            "X-UA": self.__xua,
                                       }) as response:
            response_json: dict = await response.json()

            if('list' not in response_json['data']): return None
            
            reviews: list = [review['post'] for review in response_json['data']['list']]
            detail_reviews: list = await asyncio.gather(*(self.__get_detail_review(review['id_str']) for review in reviews))

            return [{**review, **detail_reviews[i]} for i, review in enumerate(reviews)]
    
    async def __get_detail_review(self, id_str: str) -> dict:
        async with self.__requests.get('https://www.taptap.io/webapiv2/creation/post/v1/detail',
                                        params={
                                            'id_str': id_str,
                                            "X-UA": self.__xua,
                                        }) as response:
            response_json: dict = await response.json()

            return response_json['data']['post']
    
    async def __get_replies(self, post_id_str: str) -> list:
        result_replies: list = []
        start: int = 0
        while(True):
            async with self.__requests.get('https://www.taptap.io/webapiv2/creation/comment/v1/by-post',
                                           params={
                                               'post_id_str': post_id_str,
                                               'from': start,
                                               'limit': 10,
                                                "X-UA": self.__xua,
                                           }) as response:
                response_json = await response.json()

                if('list' not in response_json['data']): break 

                replies: list = response_json['data']['list']

                result_replies.extend(replies)
                start += 10
            
        return await asyncio.gather(*(self.__parser_reply(reply) for reply in result_replies))
    
    async def __parser_reply(self, reply: dict) -> dict:
        return {
            'username_reply_reviews': reply['user']['name'],
            'content_reply_reviews': reply['contents']['raw_text'] if 'raw_text' in reply['contents'] else "",
            'image_reply_reviews': reply['images'] if 'images' in reply else None,
            'avatar_reply_reviews': reply['user']['avatar'],
            'gender_reviews': reply['user']['gender'] if reply['user']['gender'] else None,
            'total_likes_reviews': reply['stat']['ups'],
            'total_reply_reviews': reply['stat']['comments'],
            'created_time': Datetime.execute(reply['created_time']),
            'created_time_epoch': reply['created_time'],
            'edited_time': Datetime.execute(reply['edited_time']),
            'edited_time_epoch': reply['edited_time'],
            'child_comments': await self.__get_child_reply(reply['id_str'], reply['stat']['comments']) if 'child_comments' in reply else []
        }
    
    async def __get_child_reply(self, reply_id_str: str, limit: int) -> list | None:
        async with self.__requests.get('https://www.taptap.io/webapiv2/creation/comment/v1/by-comment',
                                       params={
                                            'id_str': reply_id_str,
                                            'from': 0,
                                            'limit': limit,
                                            "X-UA": self.__xua,
                                       }) as response:
            response_json: dict = await response.json()
            
            if 'list' not in response_json['data']: 
                return []
            
            return await asyncio.gather(*(self.__parser_reply(reply) for reply in response_json['data']['list']))
    
    async def __process_review(self, review: dict, headers: dict, app: dict, log: dict) -> list:
        user: dict= review['user']

        username: dict = user['name'].replace("/", "").replace("\n", "")
        stat: dict = review['stat'] if review['stat'] else {} 
        rating: dict = review['list_fields']['app_ratings'][str(app['id'])]['score'] if 'app_ratings' in review['list_fields'] else None

        data: dict = {
            **headers,
            'path_data_raw': f'S3://ai-pipeline-statistics/data/data_raw/data_review/taptap_io/{app["title"]}/json/data_review/{review["id"]}.json',
            'path_data_clean': f'S3://ai-pipeline-statistics/data/data_clean/data_review/taptap_io/{app["title"]}/json/data_review/{review["id"]}.json',
            'detail_reviews': {
                'username_reviews': username,
                'gender_reviews': user['gender'] if user['gender'] else None,
                'avatar_reviews': user['avatar'],
                'media_reviews': review['files'],
                'created_time': Datetime.execute(review['published_time']),
                'created_time_epoch': review['published_time'],
                'edited_time': Datetime.execute(review['edited_time']),
                'edited_time_epoch': review['edited_time'],
                'email_reviews': None,
                'company_name': None,
                'location_reviews': None,
                'title_detail_reviews': review['title'],
                'reviews_rating': rating,
                'detail_reviews_rating': None,
                'total_likes_reviews': stat['ups'] if 'ups' in stat else 0,
                'total_dislikes_reviews': None,
                'total_reply_reviews': stat['comments'] if 'comments' in stat else 0,
                'total_favorites_reviews': stat['favorites'] if 'favorites' in stat else 0,
                'content_reviews': " ".join([
                    "".join([e["text"] for e in content["children"]])
                    for content in review['contents']['json']
                    if content["type"] == "paragraph" and any(content["children"])
                ]),
                'reply_content_reviews': await self.__get_replies(review['id_str']) if stat and 'comments' in stat else [],
                'date_of_experience': None,
                'date_of_experience_epoch': None,
            },
        }

        paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"]]] 
        
        if(self.__clean):
            paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"], data["path_data_clean"]]] 
        
        with ThreadPoolExecutor() as executor:
                data: dict = Iostream.dict_to_deep(data)
                try:
                    if(self.__s3):
                        executor.map(lambda path: ConnectionS3.upload(data, path), paths)
                    else:
                        executor.map(lambda path: Iostream.write_json(data, path), paths)
                except Exception as e:
                    raise e
                
        Iostream.info_log(log, review["id_str"], 'success', name=__name__)
                
        log['total_success'] += 1
        Iostream.update_log(log, name=__name__, title=app['title'])

    async def _get_by_app_id(self, game_id: str) -> None:
        if(not self.__requests): self.__requests: ClientSession = ClientSession()

        app: dict = await self.__get_detail_game(game_id)
        link: str = f'https://www.taptap.io/app/{app["id"]}'
        link_split: list = link.split("/")

        headers: dict = {
            'link': link,
            'domain': link_split[2],
            'tag': link_split[2:],
            'crawling_time': Datetime.now(),
            'crawling_time_epoch': int(time()),
            'reviews_name': app['title'],
            'description_reviews': app['description'],
            'developers_reviews': [developer['name'] for developer in app['developers']],
            'tags_reviews': [tag['value'] for tag in app['tags']] if 'tags' in app else None,
            'location_reviews': None,
            'category_reviews': "application",
            'total_reviews': app['stat']['review_count'],
            'total_fans': app['stat']['fans_count'],
            'total_user_want': app['stat']['user_want_count'],
            'total_user_played': app['stat']['user_played_count'],
            'total_user_playing': app['stat']['user_playing_count'],
            'reviews_rating': {
                'total_rating': float(app['stat']['rating']['score']),
                'detail_total_rating': None,
            },
            'review_info': app['stat']['vote_info'],
            'path_data_raw': f'S3://ai-pipeline-statistics/data/data_raw/data_review/taptap_io/{app["title"]}/json/detail.json',
            'path_data_clean': f'S3://ai-pipeline-statistics/data/data_clean/data_review/taptap_io/{app["title"]}/json/detail.json',
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
        
        log: dict = {
            "Crawlling_time": Datetime.now(),
            "id_project": None,
            "project": "Data Intelligence",
            "sub_project": "data review",
            "source_name": headers['domain'],
            "sub_source_name": app['title'],
            "id_sub_source": str(app['id']),
            "total_data": 0,
            "total_success": 0,
            "total_failed": 0,
            "status": "Process",
            "assign": "romy",
        }
        Iostream.write_log(log, name=__name__)

        start: int = 0
        while(True):
            reviews: list | None = await self.__get_reviews(app['id'], start)
            if(not reviews): break

            log['total_data'] += len(reviews)
            Iostream.update_log(log, name=__name__, title=app['title'])

            await asyncio.gather(*(self.__process_review(review, headers, app, log) for review in reviews))
            
            start += 50

        if(self.__requests): await self.__requests.close()

    async def _get_by_platform(self, platform: str) -> None:
        self.__requests: ClientSession = ClientSession()

        if platform not in self.__platforms: return

        start: int = 0
        while(True):
            response: Response = requests.get('https://www.taptap.io/webapiv2/i/app-top/v2/hits',
                                                params={
                                                    'from': start,
                                                    'limit': 2,
                                                    'platform': platform,
                                                    'type_name': "hot",
                                                    "X-UA": self.__xua,
                                                }) 
            
            response_json: dict = response.json()

            apps: list = [app['app'] for app in response_json['data']['list']] 

            # await asyncio.gather(*(self._get_by_app_id(app['id']) for app in apps))
            for app in apps:
                await self._get_by_app_id(app['id'])
        
            if(not response_json['next_page']): break

            start += 2
        
        await self.__requests.close()

    
    def _get_all_platform(self) -> None:
        for platform in self.__platforms:
            asyncio.run(self._get_by_platform(platform))
            

if(__name__ == '__main__'):
    baseTaptap: BaseTaptap = BaseTaptap()
    asyncio.run(baseTaptap._get_all_platform())
    # asyncio.run(baseTaptap._get_by_platform("android"))
    # asyncio.run(baseTaptap._get_by_app_id("232311"))
