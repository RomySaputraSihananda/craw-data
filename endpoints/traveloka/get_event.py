

import requests

cookies = {
    'tv-repeat-visit': 'true',
    'countryCode': 'ID',
    '_gid': 'GA1.2.1069121496.1708414933',
    'tv_user': '{"authorizationLevel":100,"id":null}',
    '_gcl_au': '1.1.629115660.1708414968',
    '_fbp': 'fb.1.1708414968526.1062905284',
    'experienceFunnelAndUTM': '{}',
    'g_state': '{"i_p":1708513235472,"i_l":2}',
    '_gat_UA-29776811-12': '1',
    'aws-waf-token': 'f92567c3-693e-4c03-b57a-46c34c49a0a4:GgoAmphNeqIKAAAA:0Rjznhiql6qlwJ0o09yXDRu4nHE+4Qneew71uy3omkYC2yMBu7/BfN/hH5/aUqhr827oKNyrWJ/VjMwE62KieovIhDZ2S5eaN3FbMpupcqRyPtX3iS4+7IhcZen+UkfU4QfIoqdocLlLU7ftGbfGHascQyPPUmmVpsl4rXtDN5OJc5LOcTn6EPvAzCcIdvSDpAk=',
    'amp_f4354c': 'EcGHr05_dObwDwHLbw1utw...1hn32ou9d.1hn33absm.0.b.b',
    '_ga': 'GA1.2.107669995.1708414933',
    'cto_bundle': 'Fo7uE19LN2pGTVZ1MUtKb1A0UFJlb3pkZU9CJTJGYUElMkIyU2NvNVdLc1VDRCUyQnlPMnVXS1ZwcmNtTkpncE1FWGYxUG9xVW9oaFM1MUptR1dmMjRwU0dTWlNxVHp4NCUyRkp0bEQwUU9EdVRrY3N2JTJCbnMyVTJoNVZvc3FvZGY1UGFUUDlIRnMxNSUyQnpiUUlvJTJCZkRWbHZrUU02bEpLS0RlNlpHTXMxUnZVaFRzZVJZWno1d0wyYyUzRA',
    'amp_1a5adb': 'LWaYs6iQPl61IkBZ9O8W3l...1hn32ou95.1hn33ad9u.2q.b.35',
    '_dd_s': 'rum=0&expire=1708428298762&logs=1&id=2ca2259d-b468-417b-ae30-9c446fd3129b&created=1708426771113',
    'tvl': 'CdexWwVPWTZE1oIZPmskZdx1ruDsnLKlphVFR1VnPAuS4EoMyKIEip265u3QHmBT9bNSDTRdOdeu9aB89D3/EWr/bMfvRvtUf5Y658qahI4AonToY9ldqnetsAoKSzoOU4u5XAdV980oQTtpWiUz5JnOl4Hr/TrBR9nBOgBKfHi5f3VKtSQOEpV9UGoMvZdtnvYMcVP7Qz1GSfsAgXF3pV80rJE5G1dQ8j3fRvbsdgbVViOy7AoLwvZtBPtJ4wPTMk8PTCqaD1c=~djAy',
    'tvs': 'xcYBEIz5cJfb+jVua5m2kbUa8gwskH34MCi8h8glPINLb5DUmAn/N+NGc8UBVc01iaTIBMENWQuhtTvSbYYTSGgm7YGot5q4Uuo1sJDsPC8n8k5QZbDPLMWC/Hz4TXgD2sItcWwZMojGdxw1xp/hqnVn2Mb68VnEpaTwCTRYfexfjbPV2jrI50TB/s0oRwBUn7EgVfNQdItikVRFAV5hzJmxEYJtkLYgC2OcZDNNKK+FNcw4PrIkDebUXwPpC416F5eLzMGhXnH1YKwj41YLmy2lbqruCr9Ojv0=~djAy',
    '_ga_RSRSMMBH0X': 'GS1.1.1708426795.3.1.1708427398.38.0.0',
    'experienceVisit': '{"visitId":"9ebcc05f-4e9f-414a-b26a-35d1be576947","eventSeq":166,"eventKey":"9ebcc05f-4e9f-414a-b26a-35d1be576947.166"}',
}

headers = {
    'authority': 'www.traveloka.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'content-type': 'application/json',
    # 'cookie': 'tv-repeat-visit=true; countryCode=ID; _gid=GA1.2.1069121496.1708414933; tv_user={"authorizationLevel":100,"id":null}; _gcl_au=1.1.629115660.1708414968; _fbp=fb.1.1708414968526.1062905284; experienceFunnelAndUTM={}; g_state={"i_p":1708513235472,"i_l":2}; _gat_UA-29776811-12=1; aws-waf-token=f92567c3-693e-4c03-b57a-46c34c49a0a4:GgoAmphNeqIKAAAA:0Rjznhiql6qlwJ0o09yXDRu4nHE+4Qneew71uy3omkYC2yMBu7/BfN/hH5/aUqhr827oKNyrWJ/VjMwE62KieovIhDZ2S5eaN3FbMpupcqRyPtX3iS4+7IhcZen+UkfU4QfIoqdocLlLU7ftGbfGHascQyPPUmmVpsl4rXtDN5OJc5LOcTn6EPvAzCcIdvSDpAk=; amp_f4354c=EcGHr05_dObwDwHLbw1utw...1hn32ou9d.1hn33absm.0.b.b; _ga=GA1.2.107669995.1708414933; cto_bundle=Fo7uE19LN2pGTVZ1MUtKb1A0UFJlb3pkZU9CJTJGYUElMkIyU2NvNVdLc1VDRCUyQnlPMnVXS1ZwcmNtTkpncE1FWGYxUG9xVW9oaFM1MUptR1dmMjRwU0dTWlNxVHp4NCUyRkp0bEQwUU9EdVRrY3N2JTJCbnMyVTJoNVZvc3FvZGY1UGFUUDlIRnMxNSUyQnpiUUlvJTJCZkRWbHZrUU02bEpLS0RlNlpHTXMxUnZVaFRzZVJZWno1d0wyYyUzRA; amp_1a5adb=LWaYs6iQPl61IkBZ9O8W3l...1hn32ou95.1hn33ad9u.2q.b.35; _dd_s=rum=0&expire=1708428298762&logs=1&id=2ca2259d-b468-417b-ae30-9c446fd3129b&created=1708426771113; tvl=CdexWwVPWTZE1oIZPmskZdx1ruDsnLKlphVFR1VnPAuS4EoMyKIEip265u3QHmBT9bNSDTRdOdeu9aB89D3/EWr/bMfvRvtUf5Y658qahI4AonToY9ldqnetsAoKSzoOU4u5XAdV980oQTtpWiUz5JnOl4Hr/TrBR9nBOgBKfHi5f3VKtSQOEpV9UGoMvZdtnvYMcVP7Qz1GSfsAgXF3pV80rJE5G1dQ8j3fRvbsdgbVViOy7AoLwvZtBPtJ4wPTMk8PTCqaD1c=~djAy; tvs=xcYBEIz5cJfb+jVua5m2kbUa8gwskH34MCi8h8glPINLb5DUmAn/N+NGc8UBVc01iaTIBMENWQuhtTvSbYYTSGgm7YGot5q4Uuo1sJDsPC8n8k5QZbDPLMWC/Hz4TXgD2sItcWwZMojGdxw1xp/hqnVn2Mb68VnEpaTwCTRYfexfjbPV2jrI50TB/s0oRwBUn7EgVfNQdItikVRFAV5hzJmxEYJtkLYgC2OcZDNNKK+FNcw4PrIkDebUXwPpC416F5eLzMGhXnH1YKwj41YLmy2lbqruCr9Ojv0=~djAy; _ga_RSRSMMBH0X=GS1.1.1708426795.3.1.1708427398.38.0.0; experienceVisit={"visitId":"9ebcc05f-4e9f-414a-b26a-35d1be576947","eventSeq":166,"eventKey":"9ebcc05f-4e9f-414a-b26a-35d1be576947.166"}',
    'origin': 'https://www.traveloka.com',
    'referer': 'https://www.traveloka.com/id-id/activities/search?st=GEO&eid=100003&theme=EVENT',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-domain': 'experience',
    'x-route-prefix': 'id-id',
}

json_data = {
    'fields': [],
    'data': {
        'currency': 'IDR',
        'caller': 'SEARCH_RESULT',
        'basicSearchSpec': {
            'searchType': 'GEO',
            'entityId': '100003',
        },
        'filters': {
            'availabilityFilter': [],
            'durationFilter': [],
            'featureFilter': [],
            'geoIdsFilter': [],
            'instantVoucherOnly': False,
            'priceFilter': {
                'minPrice': None,
                'maxPrice': None,
            },
            'promoFilterList': [],
            'subTypeFilter': [],
            'typeFilterList': [
                'EVENT',
            ],
        },
        'sortType': 'MOST_POPULAR',
        'rowsToReturn': 50,
        'skip': 0,
        'trackingProperties': {
            'visitId': '9ebcc05f-4e9f-414a-b26a-35d1be576947',
            'eventSeq': 164,
            'eventKey': '9ebcc05f-4e9f-414a-b26a-35d1be576947.164',
        },
    },
    'clientInterface': 'desktop',
}

response = requests.post('https://www.traveloka.com/api/v2/experience/searchV2', cookies=cookies, headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"fields":[],"data":{"currency":"IDR","caller":"SEARCH_RESULT","basicSearchSpec":{"searchType":"GEO","entityId":"100003"},"filters":{"availabilityFilter":[],"durationFilter":[],"featureFilter":[],"geoIdsFilter":[],"instantVoucherOnly":false,"priceFilter":{"minPrice":null,"maxPrice":null},"promoFilterList":[],"subTypeFilter":[],"typeFilterList":["EVENT"]},"sortType":"MOST_POPULAR","rowsToReturn":50,"skip":0,"trackingProperties":{"visitId":"9ebcc05f-4e9f-414a-b26a-35d1be576947","eventSeq":164,"eventKey":"9ebcc05f-4e9f-414a-b26a-35d1be576947.164"}},"clientInterface":"desktop"}'
#response = requests.post('https://www.traveloka.com/api/v2/experience/searchV2', cookies=cookies, headers=headers, data=data)

