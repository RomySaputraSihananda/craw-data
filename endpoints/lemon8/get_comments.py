import requests
import urllib3

urllib3.disable_warnings()


userId: str = '7279186948648158214'
mediaId: str = '7279238426292945413'
response = requests.get(
    'https://api22-normal-useast1a.lemon8-app.com/api/550/comment_v2/comments',
    params={
        'group_id': mediaId, 
        'item_id': mediaId, 
        'media_id': userId, 
        'count': '99999999', 
        'aid': '2657', 
    },
    headers={
        'User-Agent': 'com.bd.nproject/55014 (Linux; U; Android 9; en_US; unknown; Build/PI;tt-ok/3.12.13.1)'
    },
)

for i in response.json()['data']['data']:
    print(f'[{i["id"]} :: {i["user_name"]} :: {i["reply_count"]}] :: {i["text"]}')