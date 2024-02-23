

import requests

cookies = {
    'tv-repeat-visit': 'true',
    'countryCode': 'ID',
    '_gid': 'GA1.2.1069121496.1708414933',
    'tv_user': '{"authorizationLevel":100,"id":null}',
    '_gcl_au': '1.1.629115660.1708414968',
    '_fbp': 'fb.1.1708414968526.1062905284',
    'experienceFunnelAndUTM': '%7B%7D',
    'g_state': '{"i_p":1708422546305,"i_l":1}',
    'experienceFunnelAndUTM': '{}',
    'aws-waf-token': 'f92567c3-693e-4c03-b57a-46c34c49a0a4:GgoAoAQ/Mz8BAAAA:CURVUN+5jrCs7rVp2zO5JkLnDBdp8qrR0zIzzisaitUwgUogbr/KRTSMm72CPm0U3tcB7+IwYJsP3RIh+Fsb3St8Iqi9MV4gTj3o7ScoMzw7DvQw3QrUGYnldEqrDaU5n02Ju3g8ZtSk6lGblwTWDsn2mi8WAhRGUoAdR7ox6ZuJj+KS2X+iJA2o9SrRWOJzNb4=',
    'tvl': 'u9BgUfT0xOToHTgk5CBqavCxCqY3eFFyu/XwiQuekTRUVK/oWamJHKluXALJsphln84aJ83uvdF4lNW+927Yk11POq7YhmCQbwDyF/iRzGaXQvjzL6W5owIg8fbEn97r4JAuXPUyKv9WBLFmHVoBSoBQvY3bYm/yVyOJ0iJLz2IgztiAJIeT+3+IStOP71+je6eewncS99YeH7mTQGt+zSg52Juv+dHVcEO0a5Otwe96TtHgWSvyLdUf2u3T4vO5OJZNe9+JN1s=~djAy',
    'tvs': 'diYHHqSspBx3zXsjSSuo37xjapJKapkiTf5QO4uuoJC4XnHgsSH0V9DIO11jrOuqnqgr+/xJcU3m9BMg8H+mV2RB7fKyvbAIeqbNcPTwROj2pbutrnhXG1W03T7iqZ0yel4jbs/BF+7Cai2rSredA1/fiwZO9Fu0ng4ncHS/cOJJKD25uup9aSzPgHD4Low8yCI1PNobmLRpqw46GOBYNaLpEhcy7VzdA740LKo4l1qzFJcEOAf44uAexLaIZAz9bKhMj7vum4M454ndOQlg/1+V4xt56gRPu7k=~djAy',
    'experienceVisit': '%7B%22visitId%22%3A%22de071076-867f-4894-8f39-801993f4c4a8%22%2C%22eventSeq%22%3A8%2C%22eventKey%22%3A%22de071076-867f-4894-8f39-801993f4c4a8.8%22%7D',
    'experienceVisit': '{"visitId":"de071076-867f-4894-8f39-801993f4c4a8","eventSeq":9,"eventKey":"de071076-867f-4894-8f39-801993f4c4a8.9"}',
    'amp_f4354c': 'EcGHr05_dObwDwHLbw1utw...1hn2r9bp7.1hn2s0je8.0.9.9',
    '_ga': 'GA1.2.107669995.1708414933',
    '_gat_UA-29776811-12': '1',
    'cto_bundle': 'pKipP19LN2pGTVZ1MUtKb1A0UFJlb3pkZU9ERWtydXJwVnhON256MlJJTG9XZ0JaNXNIeUp1dFJpdnAxUG5XMWRpTTBodncxUW9vZGlVU2V2OHJZaUtubTElMkJBbThjY2hqNnVkRjlycnE0MElHYmRlWDBKQ3ZrSG9DMldNTjExSHAzJTJCTG53aFN0SXlXeXBmVHV3eEhRRjVFcU1LT2xtdTVPS3JyNCUyRjclMkJqWE51cUhCbyUzRA',
    '_ga_RSRSMMBH0X': 'GS1.1.1708418425.2.1.1708419732.50.0.0',
    'amp_1a5adb': 'LWaYs6iQPl61IkBZ9O8W3l...1hn2r9bp1.1hn2s0l3i.1r.9.24',
    '_dd_s': 'rum=0&expire=1708420629841&logs=1&id=fafec850-5b9e-477e-b6d9-a10ee7f7eb99&created=1708414931453',
}

headers = {
    'authority': 'www.traveloka.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'content-type': 'application/json',
    # 'cookie': 'tv-repeat-visit=true; countryCode=ID; _gid=GA1.2.1069121496.1708414933; tv_user={"authorizationLevel":100,"id":null}; _gcl_au=1.1.629115660.1708414968; _fbp=fb.1.1708414968526.1062905284; experienceFunnelAndUTM=%7B%7D; g_state={"i_p":1708422546305,"i_l":1}; experienceFunnelAndUTM={}; aws-waf-token=f92567c3-693e-4c03-b57a-46c34c49a0a4:GgoAoAQ/Mz8BAAAA:CURVUN+5jrCs7rVp2zO5JkLnDBdp8qrR0zIzzisaitUwgUogbr/KRTSMm72CPm0U3tcB7+IwYJsP3RIh+Fsb3St8Iqi9MV4gTj3o7ScoMzw7DvQw3QrUGYnldEqrDaU5n02Ju3g8ZtSk6lGblwTWDsn2mi8WAhRGUoAdR7ox6ZuJj+KS2X+iJA2o9SrRWOJzNb4=; tvl=u9BgUfT0xOToHTgk5CBqavCxCqY3eFFyu/XwiQuekTRUVK/oWamJHKluXALJsphln84aJ83uvdF4lNW+927Yk11POq7YhmCQbwDyF/iRzGaXQvjzL6W5owIg8fbEn97r4JAuXPUyKv9WBLFmHVoBSoBQvY3bYm/yVyOJ0iJLz2IgztiAJIeT+3+IStOP71+je6eewncS99YeH7mTQGt+zSg52Juv+dHVcEO0a5Otwe96TtHgWSvyLdUf2u3T4vO5OJZNe9+JN1s=~djAy; tvs=diYHHqSspBx3zXsjSSuo37xjapJKapkiTf5QO4uuoJC4XnHgsSH0V9DIO11jrOuqnqgr+/xJcU3m9BMg8H+mV2RB7fKyvbAIeqbNcPTwROj2pbutrnhXG1W03T7iqZ0yel4jbs/BF+7Cai2rSredA1/fiwZO9Fu0ng4ncHS/cOJJKD25uup9aSzPgHD4Low8yCI1PNobmLRpqw46GOBYNaLpEhcy7VzdA740LKo4l1qzFJcEOAf44uAexLaIZAz9bKhMj7vum4M454ndOQlg/1+V4xt56gRPu7k=~djAy; experienceVisit=%7B%22visitId%22%3A%22de071076-867f-4894-8f39-801993f4c4a8%22%2C%22eventSeq%22%3A8%2C%22eventKey%22%3A%22de071076-867f-4894-8f39-801993f4c4a8.8%22%7D; experienceVisit={"visitId":"de071076-867f-4894-8f39-801993f4c4a8","eventSeq":9,"eventKey":"de071076-867f-4894-8f39-801993f4c4a8.9"}; amp_f4354c=EcGHr05_dObwDwHLbw1utw...1hn2r9bp7.1hn2s0je8.0.9.9; _ga=GA1.2.107669995.1708414933; _gat_UA-29776811-12=1; cto_bundle=pKipP19LN2pGTVZ1MUtKb1A0UFJlb3pkZU9ERWtydXJwVnhON256MlJJTG9XZ0JaNXNIeUp1dFJpdnAxUG5XMWRpTTBodncxUW9vZGlVU2V2OHJZaUtubTElMkJBbThjY2hqNnVkRjlycnE0MElHYmRlWDBKQ3ZrSG9DMldNTjExSHAzJTJCTG53aFN0SXlXeXBmVHV3eEhRRjVFcU1LT2xtdTVPS3JyNCUyRjclMkJqWE51cUhCbyUzRA; _ga_RSRSMMBH0X=GS1.1.1708418425.2.1.1708419732.50.0.0; amp_1a5adb=LWaYs6iQPl61IkBZ9O8W3l...1hn2r9bp1.1hn2s0l3i.1r.9.24; _dd_s=rum=0&expire=1708420629841&logs=1&id=fafec850-5b9e-477e-b6d9-a10ee7f7eb99&created=1708414931453',
    'origin': 'https://www.traveloka.com',
    'referer': 'https://www.traveloka.com/en-id/activities/indonesia/product/holeoexperience-4244872323737',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-domain': 'experience',
    'x-route-prefix': 'en-id',
}

json_data = {
    'fields': [],
    'data': {
        'experienceId': '4244872323737',
        'currency': 'IDR'
    },
    'clientInterface': 'desktop',
}

response = requests.post(
    'https://www.traveloka.com/api/v2/experience/ticketAvailableDates',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

print(response.json()['data']['ticketAvailableDateGroups'])

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"fields":[],"data":{"experienceId":"4244872323737","currency":"IDR","trackingProperties":{"visitId":"de071076-867f-4894-8f39-801993f4c4a8","eventSeq":9,"eventKey":"de071076-867f-4894-8f39-801993f4c4a8.9"}},"clientInterface":"desktop"}'
#response = requests.post(
#    'https://www.traveloka.com/api/v2/experience/ticketAvailableDates',
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)

