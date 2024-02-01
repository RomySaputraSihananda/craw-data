import requests

from os import getenv
from dotenv import load_dotenv

load_dotenv()

class BaseQuora:
    def __init__(self, cursor) -> None:
        headers = {
            'cookie': getenv('QUORA_COOKIE'),
            'quora-formkey': getenv('QUORA_FORMKEY'),
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        json_data = {
            'queryName': 'QuestionPagedListPaginationQuery',
            'variables': {
                'count': 10,
                'cursor': cursor,
                'forceScoreVersion': None,
                'initial_count': 0, 
                'topAid': None,
                'id': 'UXVlc3Rpb25AMTA6NTg2MTE4NTI=',
            },
            'extensions': {
                'hash': getenv('QUORA_HASH'),
            },
        }

        response = requests.post('https://id.quora.com/graphql/gql_para_POST', 
                                params={
                                    'q': 'QuestionPagedListPaginationQuery',
                                },
                                headers=headers,
                                json=json_data,
                            )
        print(response.text)

if(__name__ == '__main__'):
    for i in range(5):
        BaseQuora(i * 10)

