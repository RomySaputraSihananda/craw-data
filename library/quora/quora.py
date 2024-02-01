import re
import requests
import os

from requests import Response, Session
from json import loads, dumps
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

from helpers import Datetime, Iostream, Datetime, ConnectionS3, Cryptography
from time import time

load_dotenv()

# {
#     'AllCommentsListQuery': '4225f312dd020c9a77077c5e224e8cf6d3b9bc60033099c979e8ea5dfda8bd05',
#     'CommentableCommentAreaLoaderInnerQuery': '7049e6ccf2e18aa1683cf340f4ab83a167ffe783381fdc89195a88646d2bba57'
# }

class BaseQuora:
    def __init__(self, **kwargs) -> None:
        self.__s3: bool = kwargs.get('s3')
        
        self.__request: Session = Session()
        self.__request.headers.update({
            'cookie': os.getenv('QUORA_COOKIE'),
            'quora-formkey': os.getenv('QUORA_FORMKEY'),
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        })
        
    @staticmethod
    def get_detail_question(question_str: str) -> dict:
        link: str = f'https://id.quora.com/{question_str}'
        response: Response = requests.get(link)
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
        } 

        for data in all_detail['list_detail']:
            type: str = data['node']['__typename']
            if type == 'QuestionAnswerHeaderItem': all_detail['question_headers'] = data['node']
            elif type == 'QuestionAnswerItem2' or type  == 'QuestionRelevantAnswerItem2': all_detail['answers_n_relevant_answer'].append(data['node'])

        return all_detail
    
    def __all_comments_list_query(self, answer_id: str, after: int) -> dict:
        response: Response = self.__request.post('https://id.quora.com/graphql/gql_para_POST',            
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
                                                })

        data: dict = response.json()['data']['node']['allCommentsConnection']

        return {
            'has_next_page': data['pageInfo']['hasNextPage'],
            'reply': [node['node'] for node in data['edges']]
        }
    
    def __commentable_comment_area_loader_inner_query(self, answer_id: str) -> None:
        response: Response = self.__request.post('https://id.quora.com/graphql/gql_para_POST',            
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
                                                })

        data: dict = response.json()['data']['node']['allCommentsConnection']

        return {
            'has_next_page': data['pageInfo']['hasNextPage'],
            'reply': [node['node'] for node in data['edges']]
        }
    
    def __get_replies(self, answer_id: str) -> dict:
        first_response: dict = self.__commentable_comment_area_loader_inner_query(answer_id)
        replies: list = first_response['reply']
        after: int = 9

        if(not first_response['has_next_page']): return replies

        while(True):
            response: dict = self.__all_comments_list_query(answer_id, after)
            replies.extend(response['reply'])

            if(response['has_next_page']): break        
            after += 10

        return replies

    
    def __get_reply(self, answer: str) -> None: 
        answer_id = re.findall(r'answer:(\d+)', Cryptography.decode_base64(answer['id']))[0]
        answer_id_encrypt = Cryptography.encode_base64(f'Answer@10:{answer_id}')
        total_reply: int = answer['answer']['numDisplayComments']
        

        if(not total_reply): return
        
        replies: list = self.__get_replies(answer_id_encrypt)

        # if answer['__typename'] == 'QuestionAnswerItem2': return self.__process_answer(answer, replies)

        # return self.__process_relevant_answer(answer, replies)

    def __process_answer(self, answer, replies) -> None:
        # print(len(replies))
        ...

    def __process_relevant_answer(self, answer, replies) -> None:
        # print(len(replies))
        ...

    def __get_detail_answers(self, all_detail: dict) -> None:
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

        # print(dumps(all_detail['answers_n_relevant_answer']))
        for i in all_detail['answers_n_relevant_answer']:
            self.__get_reply(i)

        # paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [headers["path_data_raw"], headers["path_data_clean"]]] 

        # with ThreadPoolExecutor() as executor:
        #         headers: dict = Iostream.dict_to_deep(headers)
        #         try:
        #             if(self.__s3):
        #                 executor.map(lambda path: ConnectionS3.upload(headers, path), paths)
        #             else:
        #                 executor.map(lambda path: Iostream.write_json(headers, path), paths)
        #         except Exception as e:
        #             raise e

    
    def _get_answers_by_question_str(self, question_str: str) -> None:
        return self.__get_detail_answers(self.get_detail_question(question_str))

# testing
if(__name__ == '__main__'):
    BaseQuora()._get_answers_by_question_str('Bagaimana-kesanmu-terhadap-PT-Pos-Indonesia')
    # BaseQuora().get_answers_by_quetion('Bagaimana-pengalamanmu-menggunakan-jasa-ekspedisi-sicepat')