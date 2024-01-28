import requests
import urllib3

urllib3.disable_warnings()


userId: str = '7138599741986915329'
response = requests.get(
    'https://api22-normal-useast1a.lemon8-app.com/api/550/stream',
    params={
        'category': '486', 
        'count': '1000', 
        'category_parameter': userId, 
        'session_cnt': '1', 
        'aid': '2657', 
        'device_platform': 'android', 
},
    headers={
        'User-Agent': 'com.bd.nproject/55014 (Linux; U; Android 9; en_US; unknown; Build/PI;tt-ok/3.12.13.1)',
    },
    verify=False
)



# from json import dumps

items: list = response.json()['data']['items']
print({
    'len': len(items),
})

# with open('test.json', 'w') as file:
#     file.write(dumps({
#         'len': len(items),
#         'items': [item['title'] for item in items]
#     }, indent=4, ensure_ascii=False))
