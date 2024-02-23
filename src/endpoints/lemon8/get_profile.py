import requests
import urllib3

urllib3.disable_warnings()

userId: str = '7138599741986915329'

response = requests.get(
    'https://api22-normal-useast1a.lemon8-app.com/api/550/user/profile/homepage',
    params={
        'user_id': userId,
        'aid': '2657',
    },
    headers={
        'User-Agent': 'com.bd.nproject/55014 (Linux; U; Android 9; en_US; unknown; Build/PI;tt-ok/3.12.13.1)',
    },
    verify=False
)

print(response.json())