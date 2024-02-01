import requests
import urllib3

urllib3.disable_warnings()

user_id: str = '7138599741986915329'
media_id: str = '7147953600210240002'
comment_id: str = '7148272678682493698'

response = requests.get(
    'https://api22-normal-useast1a.lemon8-app.com/api/550/comment_v2/detail',
    params={   
    'group_id': media_id, 
    'item_id': media_id, 
    'media_id': user_id, 
    'comment_id': comment_id, 
    'count': '6', 
},
    headers={    
        'User-Agent': 'com.bd.nproject/55014 (Linux; U; Android 9; en_US; unknown; Build/PI;tt-ok/3.12.13.1)',
    },
)
from json import dumps

with open('test.json', 'w') as file:
    file.write(dumps(response.json()['data'], indent=4, ensure_ascii=False))


