

import requests

cookies = {
    'tvs': 's5Qv47D8QkkiydM8qMRuQY/4fHPRwx6xoGkxyQ700LiYh1IGQ26ryeB1/V8cObU+Fmt8SCkKT622Wh0AjIykncuRJpHA77mZyGaRPc3+qYhK/oQecEiH5VNEfWWfQAzO4y48dGJ+jWrz8NecdTP28AqZdDbhZ5qgJiLpXnkIzUtjb4/KXolNS/ONsN022tVH7AiLrLnUNQ==~djAy',
    'tv-repeat-visit': 'true',
    'tv_user': '{"authorizationLevel":100,"id":null}',
    'tvl': 'ISIQqKDDyRR/9wYEdzLV549QDqEqJoKv/Fw9p0ihZY3d1ZJOLxaF+x5+kednXC+Ag7y+bGZSFsQzkm9GkNS7W3q3zTudmmpbrSevzoGlyKmIE+JVndJx6WXffH+r7d/korNhvsDltT5rJ1irjwIS3qXQGQAuC9nbF+VJd4awH7l62/JFdxVXugUlzQ1toKItC4bBGV+5Kpvvidb06RGV6VhwVb/13OqeY0TnOp4aJt2JT4QktIV9bJyptl5cvPtKcjaXoEMQb/w=~djAy',
    'experienceVisit': '{"visitId":"36ab0302-1b91-4168-bb95-188fc42aeca6","eventSeq":40,"eventKey":"36ab0302-1b91-4168-bb95-188fc42aeca6.40"}',
    'experienceFunnelAndUTM': '{}',
    '_dd_s': 'rum=0&expire=1708498775807&logs=1&id=08ff88b4-edcb-41e7-8195-031b80de138d&created=1708497398381',
    'countryCode': 'ID',
    'g_state': '{"i_p":1708504608648,"i_l":1}',
    'aws-waf-token': '0151a78a-6e91-49d6-9b26-44cb2537c7f4:GgoAiUQt9x9KAAAA:2cqD7UTaofkJCiucnDATjYkXKj8S7fV0A5r6Ywmp7foNkfnafvsSbmvQsJkM7iiMmZUdZV0uuQ6O95UbwWQpGFcLVk1H+mrrR8PNj15FCoM7C2efuKToUGoSlxTBYal4tpr4P/qda+BZo/nBZbHF4KuxAwwA/zWwC9vzG7j/lA3833wlz2Ahx56C2ID5ZvCE6ZxX6UYXmlWlmd2v6Kr+ezQrapjlgw==',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/118.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.traveloka.com/id-id/activities/search?st=GEO&eid=103130&theme=EVENT',
    'x-domain': 'experience',
    'content-type': 'application/json',
    'x-route-prefix': 'id-id',
    'Origin': 'https://www.traveloka.com',
    'DNT': '1',
    'Alt-Used': 'www.traveloka.com',
    'Connection': 'keep-alive',
    # 'Cookie': 'tvs=s5Qv47D8QkkiydM8qMRuQY/4fHPRwx6xoGkxyQ700LiYh1IGQ26ryeB1/V8cObU+Fmt8SCkKT622Wh0AjIykncuRJpHA77mZyGaRPc3+qYhK/oQecEiH5VNEfWWfQAzO4y48dGJ+jWrz8NecdTP28AqZdDbhZ5qgJiLpXnkIzUtjb4/KXolNS/ONsN022tVH7AiLrLnUNQ==~djAy; tv-repeat-visit=true; tv_user={"authorizationLevel":100,"id":null}; tvl=ISIQqKDDyRR/9wYEdzLV549QDqEqJoKv/Fw9p0ihZY3d1ZJOLxaF+x5+kednXC+Ag7y+bGZSFsQzkm9GkNS7W3q3zTudmmpbrSevzoGlyKmIE+JVndJx6WXffH+r7d/korNhvsDltT5rJ1irjwIS3qXQGQAuC9nbF+VJd4awH7l62/JFdxVXugUlzQ1toKItC4bBGV+5Kpvvidb06RGV6VhwVb/13OqeY0TnOp4aJt2JT4QktIV9bJyptl5cvPtKcjaXoEMQb/w=~djAy; experienceVisit={"visitId":"36ab0302-1b91-4168-bb95-188fc42aeca6","eventSeq":40,"eventKey":"36ab0302-1b91-4168-bb95-188fc42aeca6.40"}; experienceFunnelAndUTM={}; _dd_s=rum=0&expire=1708498775807&logs=1&id=08ff88b4-edcb-41e7-8195-031b80de138d&created=1708497398381; countryCode=ID; g_state={"i_p":1708504608648,"i_l":1}; aws-waf-token=0151a78a-6e91-49d6-9b26-44cb2537c7f4:GgoAiUQt9x9KAAAA:2cqD7UTaofkJCiucnDATjYkXKj8S7fV0A5r6Ywmp7foNkfnafvsSbmvQsJkM7iiMmZUdZV0uuQ6O95UbwWQpGFcLVk1H+mrrR8PNj15FCoM7C2efuKToUGoSlxTBYal4tpr4P/qda+BZo/nBZbHF4KuxAwwA/zWwC9vzG7j/lA3833wlz2Ahx56C2ID5ZvCE6ZxX6UYXmlWlmd2v6Kr+ezQrapjlgw==',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

json_data = ''

response = requests.post(
    'https://www.traveloka.com/api/v2/experience/softRecommendation',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

print(response.json())

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"fields":[],"data":{"caller":"SEARCH_RESULT","currency":"IDR","sortType":"MOST_POPULAR","filters":{"typeFilterList":["EVENT"],"priceFilter":{"minPrice":null,"maxPrice":null},"instantVoucherOnly":false,"subTypeFilter":[],"durationFilter":[],"geoIdsFilter":[],"availabilityFilter":[],"featureFilter":[],"promoFilterList":[]},"basicSearchSpec":{"searchType":"GEO","entityId":"103130"},"rowsToReturn":12,"skip":180,"recommendationType":null,"trackingProperties":{"visitId":"36ab0302-1b91-4168-bb95-188fc42aeca6","eventSeq":40,"eventKey":"36ab0302-1b91-4168-bb95-188fc42aeca6.40"}},"clientInterface":"desktop"}'
#response = requests.post(
#    'https://www.traveloka.com/api/v2/experience/softRecommendation',
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)

