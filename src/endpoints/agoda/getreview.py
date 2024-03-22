

import requests

cookies = {
    'agoda.landings': '1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7||hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|19----1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7|EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE|hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|20----1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7|EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE|hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|99',
    'agoda.analytics': 'Id=1759663807146755370&Signature=3768117790359846960&Expiry=1711104411594',
    'ASP.NET_SessionId': 'hwz4ybyt0vqbbcb3morfkfek',
    'agoda.version.03': 'CookieId=7628156b-a104-42e8-8c31-1877034bbb88&TItems=2$1891460$03-22-2024 15:46$04-21-2024 15:46$f71b0106-fb42-0cf2-b13e-84355fbe83c7&DLang=en-us&CurLabel=IDR',
    'agoda.firstclicks': '1891460||f71b0106-fb42-0cf2-b13e-84355fbe83c7||2024-03-22T15:46:47||hwz4ybyt0vqbbcb3morfkfek||{"IsPaid":true,"gclid":"","Type":""}',
    'agoda.user.03': 'UserId=d2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0',
    'agoda.lastclicks': '1891460||f71b0106-fb42-0cf2-b13e-84355fbe83c7||2024-03-22T15:46:47||hwz4ybyt0vqbbcb3morfkfek||{"IsPaid":true,"gclid":"EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE","Type":""}',
    'agoda.prius': 'PriusID=0&PointsMaxTraffic=Agoda',
    'agoda.attr.03': 'ATItems=1891460$03-22-2024 15:46$f71b0106-fb42-0cf2-b13e-84355fbe83c7',
    'agoda.price.01': 'PriceView=1',
    'xsrf_token': 'CfDJ8Dkuqwv-0VhLoFfD8dw7lYyW3DV2i_AgBuSaJO-ms2PzSot77dQp1a8XJA7LtTpj_G6i_PdMHhPB2zYNikT3BVfLJ6MraBpPHEE6jzIc_ThUJ58yUqHk9vlW420jboLdiXVmiKAgnE_tV_L5BRGvuuY',
    'tealiumEnable': 'true',
    'deviceId': '03a52854-f95d-479d-bf1d-73552986527e',
    'agoda.consent': 'ID||2024-03-22 09:27:06Z',
    '_gcl_aw': 'GCL.1711100363.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE',
    '_gcl_au': '1.1.913130779.1711097211',
    '_ga_T408Z268D2': 'GS1.1.1711097210.1.1.1711100813.0.0.1525321318',
    '_ga': 'GA1.2.1816605990.1711097211',
    'FPID': 'FPID2.2.dl5Al7XRNkZWXCxvNet1hQLPWYuBLUT4WYjODVwcrj0%3D.1711097211',
    'FPLC': 'AzMc0Z83T9eFMBgX39%2BZYEXz4xJkVgRWLDnrAogM41szJZ6EGfpsx55LcLfGWyPIFurYFfyD9UfSTHEEr6at%2BkBrD94nef9Q7AjB%2Fqn7dTtseIrIKn9tKARPslsxdw%3D%3D',
    'ab.storage.userId.d999de98-30bc-4346-8124-a15900a101ae': '%7B%22g%22%3A%22d2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0%22%2C%22c%22%3A1711097213422%2C%22l%22%3A1711097213422%7D',
    'ab.storage.sessionId.d999de98-30bc-4346-8124-a15900a101ae': '%7B%22g%22%3A%22f0599a65-5088-82b3-9089-e1d5286ee5ad%22%2C%22e%22%3A1711102163773%2C%22c%22%3A1711099654839%2C%22l%22%3A1711100363773%7D',
    'ab.storage.deviceId.d999de98-30bc-4346-8124-a15900a101ae': '%7B%22g%22%3A%22762e89e3-75cf-4bed-ec2d-c7dc7fced657%22%2C%22c%22%3A1711097213423%2C%22l%22%3A1711097213423%7D',
    'agoda.familyMode': 'Mode=0',
    'agoda.search.01': 'SHist=1$10779$8490$1$1$1$0$0$1711099648$|1$5414$8490$1$1$2$0$0$1711100356$|4$532093$8490$1$1$2$0$0$$|4$71870$8490$1$1$2$0$0$$&H=8481|0$532093$71870',
    '_ab50group': 'GroupA',
    '_40-40-20Split': 'Group40A',
    'utag_main': 'v_id:018e65578f6e000d5d8ba448bb8a0504604bb00900bd0$_sn:1$_se:29$_ss:0$_st:1711102276708$ses_id:1711097220975%3Bexp-session$_pn:15%3Bexp-session',
    'lastRskxRun': '1711097227929',
    'rskxRunCookie': '0',
    'rCookie': 'qpu7p60xr4s53aj4bo4zajlu2f3udy',
    '_ha_aw': 'GCL.1711100363.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE',
    '_hab_aw': 'GCL.1711100363.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE',
    '_gid': 'GA1.2.28862958.1711097226',
    '_gac_UA-6446424-30': '1.1711100364.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE',
    '_fbp': 'fb.1.1711097225963.1923692797',
    '_ga_C07L4VP9DZ': 'GS1.2.1711099631.2.1.1711100482.48.0.0',
    '__gads': 'ID=67b7a66e41f1db10:T=1711097225:RT=1711100364:S=ALNI_MaQ4CFngpLi-6-0aTnwyXM9UclBgg',
    '__gpi': 'UID=00000d52b95a2a0f:T=1711097225:RT=1711100364:S=ALNI_MbzzWyJU7zEyLRiAabcoTgGx63pig',
    'cto_bundle': 'ATzKM19Ud2FNM1dwWSUyQkh2eGdOemUlMkZScFNOQlNXRCUyQlBrWGswQVc2TlVWJTJGUjJZbnBVZnpOY2xmbkVuY2ZTMkgwNWw3OSUyQkpMcGJpJTJGbVBvSjlRbmtYZXBQVkg1ck8lMkZ4UEQ2Z1Bnd0F3WlhhOHVxMEJxQkl6b3lGeklBaHJmZ0I5eUdycm9ESWFrejY5dDlUdlVYRHdsSlA2TWNXQSUzRCUzRA',
    '_uetsid': 'c2a40160e82811eeae954114e4cfa07e',
    '_uetvid': 'c2a41f20e82811eeba84755b2afc03f2',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.agoda.com/hotel-santika-premiere-malang/hotel/malang-id.html?finalPriceView=1&isShowMobileAppPrice=false&cid=1891460&numberOfBedrooms=&familyMode=false&adults=2&children=0&rooms=1&maxRooms=0&checkIn=2024-03-31&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=1&showReviewSubmissionEntry=false&currencyCode=IDR&isFreeOccSearch=false&tag=f71b0106-fb42-0cf2-b13e-84355fbe83c7&isCityHaveAsq=false&los=1&searchrequestid=fe94e148-c808-423d-949f-35ba5ec53590&ds=en8tWMNuMxqNWXE8',
    'AG-REQUEST-ATTEMPT': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-type': 'application/json; charset=utf-8',
    'AG-Language-Locale': 'en-us',
    'AG-Language-Id': '1',
    'CR-Currency-Id': '25',
    'CR-Currency-Code': 'IDR',
    'AG-Correlation-Id': 'c3ce60af-faa4-4405-a3ae-80fc7a77c2a0',
    'AG-Analytics-Session-Id': '1759663807146755370',
    'Origin': 'https://www.agoda.com',
    'Connection': 'keep-alive',
    # 'Cookie': 'agoda.landings=1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7||hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|19----1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7|EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE|hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|20----1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7|EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE|hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|99; agoda.analytics=Id=1759663807146755370&Signature=3768117790359846960&Expiry=1711104411594; ASP.NET_SessionId=hwz4ybyt0vqbbcb3morfkfek; agoda.version.03=CookieId=7628156b-a104-42e8-8c31-1877034bbb88&TItems=2$1891460$03-22-2024 15:46$04-21-2024 15:46$f71b0106-fb42-0cf2-b13e-84355fbe83c7&DLang=en-us&CurLabel=IDR; agoda.firstclicks=1891460||f71b0106-fb42-0cf2-b13e-84355fbe83c7||2024-03-22T15:46:47||hwz4ybyt0vqbbcb3morfkfek||{"IsPaid":true,"gclid":"","Type":""}; agoda.user.03=UserId=d2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0; agoda.lastclicks=1891460||f71b0106-fb42-0cf2-b13e-84355fbe83c7||2024-03-22T15:46:47||hwz4ybyt0vqbbcb3morfkfek||{"IsPaid":true,"gclid":"EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE","Type":""}; agoda.prius=PriusID=0&PointsMaxTraffic=Agoda; agoda.attr.03=ATItems=1891460$03-22-2024 15:46$f71b0106-fb42-0cf2-b13e-84355fbe83c7; agoda.price.01=PriceView=1; xsrf_token=CfDJ8Dkuqwv-0VhLoFfD8dw7lYyW3DV2i_AgBuSaJO-ms2PzSot77dQp1a8XJA7LtTpj_G6i_PdMHhPB2zYNikT3BVfLJ6MraBpPHEE6jzIc_ThUJ58yUqHk9vlW420jboLdiXVmiKAgnE_tV_L5BRGvuuY; tealiumEnable=true; deviceId=03a52854-f95d-479d-bf1d-73552986527e; agoda.consent=ID||2024-03-22 09:27:06Z; _gcl_aw=GCL.1711100363.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE; _gcl_au=1.1.913130779.1711097211; _ga_T408Z268D2=GS1.1.1711097210.1.1.1711100813.0.0.1525321318; _ga=GA1.2.1816605990.1711097211; FPID=FPID2.2.dl5Al7XRNkZWXCxvNet1hQLPWYuBLUT4WYjODVwcrj0%3D.1711097211; FPLC=AzMc0Z83T9eFMBgX39%2BZYEXz4xJkVgRWLDnrAogM41szJZ6EGfpsx55LcLfGWyPIFurYFfyD9UfSTHEEr6at%2BkBrD94nef9Q7AjB%2Fqn7dTtseIrIKn9tKARPslsxdw%3D%3D; ab.storage.userId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%22d2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0%22%2C%22c%22%3A1711097213422%2C%22l%22%3A1711097213422%7D; ab.storage.sessionId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%22f0599a65-5088-82b3-9089-e1d5286ee5ad%22%2C%22e%22%3A1711102163773%2C%22c%22%3A1711099654839%2C%22l%22%3A1711100363773%7D; ab.storage.deviceId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%22762e89e3-75cf-4bed-ec2d-c7dc7fced657%22%2C%22c%22%3A1711097213423%2C%22l%22%3A1711097213423%7D; agoda.familyMode=Mode=0; agoda.search.01=SHist=1$10779$8490$1$1$1$0$0$1711099648$|1$5414$8490$1$1$2$0$0$1711100356$|4$532093$8490$1$1$2$0$0$$|4$71870$8490$1$1$2$0$0$$&H=8481|0$532093$71870; _ab50group=GroupA; _40-40-20Split=Group40A; utag_main=v_id:018e65578f6e000d5d8ba448bb8a0504604bb00900bd0$_sn:1$_se:29$_ss:0$_st:1711102276708$ses_id:1711097220975%3Bexp-session$_pn:15%3Bexp-session; lastRskxRun=1711097227929; rskxRunCookie=0; rCookie=qpu7p60xr4s53aj4bo4zajlu2f3udy; _ha_aw=GCL.1711100363.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE; _hab_aw=GCL.1711100363.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE; _gid=GA1.2.28862958.1711097226; _gac_UA-6446424-30=1.1711100364.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE; _fbp=fb.1.1711097225963.1923692797; _ga_C07L4VP9DZ=GS1.2.1711099631.2.1.1711100482.48.0.0; __gads=ID=67b7a66e41f1db10:T=1711097225:RT=1711100364:S=ALNI_MaQ4CFngpLi-6-0aTnwyXM9UclBgg; __gpi=UID=00000d52b95a2a0f:T=1711097225:RT=1711100364:S=ALNI_MbzzWyJU7zEyLRiAabcoTgGx63pig; cto_bundle=ATzKM19Ud2FNM1dwWSUyQkh2eGdOemUlMkZScFNOQlNXRCUyQlBrWGswQVc2TlVWJTJGUjJZbnBVZnpOY2xmbkVuY2ZTMkgwNWw3OSUyQkpMcGJpJTJGbVBvSjlRbmtYZXBQVkg1ck8lMkZ4UEQ2Z1Bnd0F3WlhhOHVxMEJxQkl6b3lGeklBaHJmZ0I5eUdycm9ESWFrejY5dDlUdlVYRHdsSlA2TWNXQSUzRCUzRA; _uetsid=c2a40160e82811eeae954114e4cfa07e; _uetvid=c2a41f20e82811eeba84755b2afc03f2',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

json_data = {
    'hotelId': 71870,
    'providerId': 332,
    'demographicId': 0,
    'page': 2,
    'pageSize': 5,
    'sorting': 7,
    'providerIds': [
        332,
    ],
    'isReviewPage': False,
    'isCrawlablePage': True,
    'filters': {
        'language': [],
        'room': [],
    },
    'searchKeyword': '',
    'searchFilters': [],
}

response = requests.post(
    'https://www.agoda.com/api/cronos/property/review/ReviewComments',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"hotelId":71870,"providerId":332,"demographicId":0,"page":2,"pageSize":5,"sorting":7,"providerIds":[332],"isReviewPage":false,"isCrawlablePage":true,"filters":{"language":[],"room":[]},"searchKeyword":"","searchFilters":[]}'
#response = requests.post(
#    'https://www.agoda.com/api/cronos/property/review/ReviewComments',
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)

