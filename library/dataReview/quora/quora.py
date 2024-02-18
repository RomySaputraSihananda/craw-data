import re
import requests
import os
import asyncio

from requests import Response
from aiohttp import ClientSession
from json import loads
from dotenv import load_dotenv
from typing import final
from concurrent.futures import ThreadPoolExecutor

from helpers import Datetime, Iostream, Datetime, ConnectionS3, Cryptography
from time import time

from helpers import logging

load_dotenv()

class BaseQuora:
    def __init__(self, **kwargs) -> None:
        self.__s3: bool = kwargs.get('s3')
        self.__clean: bool = kwargs.get('clean')
        self.__request: ClientSession = None

    @final
    @staticmethod
    def get_detail_question(question_str: str) -> dict: 
        link: str = f'https://id.quora.com/{question_str}'
        response: Response = requests.get(link)

        if(response.status_code != 200): raise Exception(f'error with code {response}')

        response_text: str = response.text

        all_detail: dict = loads(re.findall(r'.push\((.*?)\);window', response_text)[-1].replace('\\"', '"').replace('\\\\"', '\\"').strip('"'))
        question_detail: dict = loads(re.findall(r'<script type="application/ld\+json">(.*?)</script>', response_text, re.DOTALL)[0])["mainEntity"] 
        question_id: str = re.findall(r'\\"qid\\":(\d+),', response_text)[0]
            
        if 'acceptedAnswer' in question_detail: del question_detail['acceptedAnswer'] 
        if 'suggestedAnswer' in question_detail: del question_detail['suggestedAnswer']
       
        all_detail: dict = {
            'link': link,
            'list_detail': all_detail['data']['question']['pagedListDataConnection']['edges'],
            'question_detail': question_detail,
            'question_id': Cryptography.encode_base64(f'Question@10:{question_id}'),
            'question_str': question_str,
            'answers_n_relevant_answer': [],
            'total_data': all_detail['data']['question']['pagedListDataConnection']['edges'][1]['node']['question']['mixRankedAnswersCount']
        }

        for data in all_detail['list_detail']:
            type: str = data['node']['__typename']
            if type == 'QuestionAnswerHeaderItem': all_detail['question_headers'] = data['node']
            elif type == 'QuestionAnswerItem2' or type  == 'QuestionRelevantAnswerItem2': all_detail['answers_n_relevant_answer'].append(data['node'])

        return all_detail
    
    @final
    @staticmethod
    def get_next_answer(cursor: int, question_id: str) -> list:
        next_answers: list = []
        while(True):
            response: Response = requests.post('https://id.quora.com/graphql/gql_para_POST',
                                                params = {
                                                    'q': 'QuestionPagedListPaginationQuery',
                                                },
                                                json={
                                                    'queryName': 'QuestionPagedListPaginationQuery',
                                                    'variables': {
                                                        'count': 10,
                                                        'cursor': str(cursor),
                                                        'forceScoreVersion': None,
                                                        'initial_count': 2,
                                                        'topAid': None,
                                                        'id': question_id,
                                                    },
                                                    'extensions': {
                                                        'hash': 'ef8f92455df92a263fadc048a763c911b36df11e0bbe0360cbb0d245af3943b1',
                                                    },
                                                },
                                                headers = {
                                                    'cookie': os.getenv('QUORA_COOKIE'),
                                                    'quora-formkey': os.getenv('QUORA_FORMKEY'),
                                                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                                                })
            data: list = [loads(data) for i, data in enumerate(response.text.split('\n')) if ((i + 1) % 3 == 0)]


            cursor: str = data[-1]['data']['pageInfo']['endCursor']
            has_next_page: bool = data[-1]['data']['pageInfo']['hasNextPage']

            data: list = [
                *[answer['node'] for answer in data[0]['data']['node']['answers']['edges']],
                *[answer['data']['node'] for answer in data[1:-2]]
            ] 


            next_answers.extend(data)
            if(not has_next_page): break

        return next_answers
    
    @final
    async def __all_comments_list_query(self, answer_id: str, after: int) -> dict:
        async with self.__request.post('https://id.quora.com/graphql/gql_para_POST',            
                                                params={
                                                    'q': 'AllCommentsListQuery',
                                                },
                                                json={
                                                    'queryName': 'AllCommentsListQuery',
                                                    'variables': {
                                                        'id': answer_id,
                                                        'after': after,
                                                        'first': 10,
                                                    },
                                                    'extensions': {
                                                        'hash': '4225f312dd020c9a77077c5e224e8cf6d3b9bc60033099c979e8ea5dfda8bd05',
                                                    },
                                                }) as response:

            response_json: dict = await response.json()
            data: dict = response_json['data']['node']['allCommentsConnection']

            return {
                'has_next_page': data['pageInfo']['hasNextPage'],
                'reply': [node['node'] for node in data['edges']]
            }
    @final
    async def __commentable_comment_area_loader_inner_query(self, answer_id: str) -> None:
        async with self.__request.post('https://id.quora.com/graphql/gql_para_POST',            
                                                params={
                                                    'q': 'CommentableCommentAreaLoaderInnerQuery',
                                                },
                                                json={
                                                    'queryName': 'CommentableCommentAreaLoaderInnerQuery',
                                                    'variables': {
                                                        'id': answer_id,
                                                        'first': 10,
                                                    },
                                                    'extensions': {
                                                        'hash': '7049e6ccf2e18aa1683cf340f4ab83a167ffe783381fdc89195a88646d2bba57',
                                                    },
                                                }) as response:

            response_json: dict = await response.json()
            data: dict = response_json['data']['node']['allCommentsConnection']

            return {
                'has_next_page': data['pageInfo']['hasNextPage'],
                'reply': [node['node'] for node in data['edges']]
            }
    
    @final
    async def __get_replies(self, answer_id: str) -> dict:
        first_response: dict = await self.__commentable_comment_area_loader_inner_query(answer_id)
        replies: list = first_response['reply']
        after: int = 9

        if(not first_response['has_next_page']): return replies

        while(True):
            response: dict = await self.__all_comments_list_query(answer_id, after)
            replies.extend(response['reply'])

            if(not response['has_next_page']): break        
            after += 10

        return replies
    
    @final
    async def __process_data(self, all_detail: dict, answer: dict, headers: dict, log: dict) -> None: 
        try:
            answer_id = re.findall(r'answer:(\d+)', Cryptography.decode_base64(answer['id']))[0]
            answer_id_encrypt = Cryptography.encode_base64(f'Answer@10:{answer_id}')
            total_reply: int = answer['answer']['numDisplayComments']
            
            type: str = 'answers' if answer['__typename'] == 'QuestionAnswerItem2' else 'relevan_answers'

            data: dict = {
                **headers,
                'answer_detail': answer,
                "path_data_raw": f'S3://ai-pipeline-statistics/data/data_raw/data_review/quora/{all_detail["question_str"]}/json/{type}/{answer_id}.json',
                "path_data_clean": f'S3://ai-pipeline-statistics/data/data_clean/data_review/quora/{all_detail["question_str"]}/json/{type}/{answer_id}.json',
            }

            paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"]]] 
            
            if self.__clean:
                paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"], data["path_data_clean"]]] 

            if(not total_reply): 
                with ThreadPoolExecutor() as executor:
                        data: dict = Iostream.dict_to_deep(data)
                        try:
                            if(self.__s3):
                                executor.map(lambda path: ConnectionS3.upload(data, path), paths)
                            else:
                                executor.map(lambda path: Iostream.write_json(data, path), paths)
                        except Exception as e:
                            raise e
                Iostream.info_log(log, answer_id, 'success', name=__name__)
                    
                log['total_success'] += 1
                Iostream.update_log(log, name=__name__)
                return 
            
            data['answer_detail']['replies'] = await self.__get_replies(answer_id_encrypt)

            with ThreadPoolExecutor() as executor:
                        data: dict = Iostream.dict_to_deep(data)
                        try:
                            if(self.__s3):
                                executor.map(lambda path: ConnectionS3.upload(data, path), paths)
                            else:
                                executor.map(lambda path: Iostream.write_json(data, path), paths)
                        except Exception as e:
                            raise e

            Iostream.info_log(log, answer_id, 'success', name=__name__)
                    
            log['total_success'] += 1
            Iostream.update_log(log, name=__name__)
        except Exception as e:
            Iostream.info_log(log, answer_id, 'failed', error=e, name=__name__)

            log['total_failed'] += 1
            Iostream.update_log(log, name=__name__)
            
        
        log['status'] = 'Done'
        Iostream.update_log(log, name=__name__)
        


    @final
    async def __get_detail_answers(self, question_str: str) -> None:
        self.__request: ClientSession = ClientSession(headers={
            'cookie': os.getenv('QUORA_COOKIE'),
            'quora-formkey': os.getenv('QUORA_FORMKEY'),
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        })

        try:
            all_detail = self.get_detail_question(question_str)
        except Exception as e:
            await self.__request.close()
            return logging.error(e)

        cursor: int = len(all_detail['answers_n_relevant_answer'])
        link_split: list = all_detail['link'].split('/')

        headers: dict = {
            "link": all_detail['link'],
            "domain": link_split[2],
            "tag": link_split[2:],
            "crawling_time": Datetime.now(),
            "crawling_time_epoch": int(time()),
            'question_detail': {
                **all_detail['question_headers'], 
                **all_detail['question_detail']
            },
            "path_data_raw": f'S3://ai-pipeline-statistics/data/data_raw/data_review/quora/{all_detail["question_str"]}/json/detail.json',
            "path_data_clean": f'S3://ai-pipeline-statistics/data/data_clean/data_review/quora/{all_detail["question_str"]}/json/detail.json',
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
            "sub_source_name": question_str,
            "id_sub_source": all_detail['question_id'],
            "total_data": all_detail['total_data'],
            "total_success": 0,
            "total_failed": 0,
            "status": "Process",
            "assign": "romy",
        }
        Iostream.write_log(log, name=__name__)

        if(not cursor == all_detail['total_data']):
            next_answers: list = self.get_next_answer(cursor, all_detail['question_id'])
            all_detail['answers_n_relevant_answer'].extend(next_answers)
        
        await asyncio.gather(*([self.__process_data(all_detail, i, headers, log) for i in all_detail['answers_n_relevant_answer']]))
        
        await self.__request.close()

    @final
    def _get_answers_by_question_str(self, question_str: str) -> None:
        return asyncio.run(self.__get_detail_answers(question_str))

# testing
if(__name__ == '__main__'):
    BaseQuora()._get_answers_by_question_str('Bagaimana-pengalamanmu-menggunakan-jasa-ekspedisi-sicepat')
    # BaseQuora()._get_answers_by_question_str('Bagaimana-kesanmu-terhadap-PT-Pos-Indonesia')
