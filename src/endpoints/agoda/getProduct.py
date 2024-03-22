

import requests

cookies = {
    'agoda.landings': '1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7||hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|19----1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7|EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE|hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|20----1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7|EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE|hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|99',
    'agoda.analytics': 'Id=1759663807146755370&Signature=3831058715177103895&Expiry=1711101323860',
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
    'agoda.consent': 'ID||2024-03-22 08:46:48Z',
    '_gcl_aw': 'GCL.1711097224.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE',
    '_gcl_au': '1.1.913130779.1711097211',
    '_ga_T408Z268D2': 'GS1.1.1711097210.1.1.1711097725.0.0.1525321318',
    '_ga': 'GA1.2.1816605990.1711097211',
    'FPID': 'FPID2.2.dl5Al7XRNkZWXCxvNet1hQLPWYuBLUT4WYjODVwcrj0%3D.1711097211',
    'FPLC': 'AzMc0Z83T9eFMBgX39%2BZYEXz4xJkVgRWLDnrAogM41szJZ6EGfpsx55LcLfGWyPIFurYFfyD9UfSTHEEr6at%2BkBrD94nef9Q7AjB%2Fqn7dTtseIrIKn9tKARPslsxdw%3D%3D',
    'ab.storage.userId.d999de98-30bc-4346-8124-a15900a101ae': '%7B%22g%22%3A%22d2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0%22%2C%22c%22%3A1711097213422%2C%22l%22%3A1711097213422%7D',
    'ab.storage.sessionId.d999de98-30bc-4346-8124-a15900a101ae': '%7B%22g%22%3A%22bf268215-8fc3-10a5-ca5c-9ad38aa7ab25%22%2C%22e%22%3A1711099028196%2C%22c%22%3A1711097213423%2C%22l%22%3A1711097228196%7D',
    'ab.storage.deviceId.d999de98-30bc-4346-8124-a15900a101ae': '%7B%22g%22%3A%22762e89e3-75cf-4bed-ec2d-c7dc7fced657%22%2C%22c%22%3A1711097213423%2C%22l%22%3A1711097213423%7D',
    'agoda.familyMode': 'Mode=0',
    'agoda.search.01': 'SHist=1$5414$8490$1$1$2$0$0$1711097723$$0&H=',
    '_ab50group': 'GroupA',
    '_40-40-20Split': 'Group40A',
    'utag_main': 'v_id:018e65578f6e000d5d8ba448bb8a0504604bb00900bd0$_sn:1$_se:6$_ss:0$_st:1711099525798$ses_id:1711097220975%3Bexp-session$_pn:2%3Bexp-session',
    'lastRskxRun': '1711097227929',
    'rskxRunCookie': '0',
    'rCookie': 'qpu7p60xr4s53aj4bo4zajlu2f3udy',
    '_ha_aw': 'GCL.1711097225.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE',
    '_hab_aw': 'GCL.1711097225.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE',
    '_gid': 'GA1.2.28862958.1711097226',
    '_gac_UA-6446424-30': '1.1711097226.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE',
    '_uetsid': 'c2a40160e82811eeae954114e4cfa07e',
    '_uetvid': 'c2a41f20e82811eeba84755b2afc03f2',
    '_fbp': 'fb.1.1711097225963.1923692797',
    '_ga_C07L4VP9DZ': 'GS1.2.1711097226.1.0.1711097226.60.0.0',
    '__gads': 'ID=67b7a66e41f1db10:T=1711097225:RT=1711097225:S=ALNI_MaQ4CFngpLi-6-0aTnwyXM9UclBgg',
    '__gpi': 'UID=00000d52b95a2a0f:T=1711097225:RT=1711097225:S=ALNI_MbzzWyJU7zEyLRiAabcoTgGx63pig',
    'cto_bundle': 'ygTCtl9Ud2FNM1dwWSUyQkh2eGdOemUlMkZScFNOQTN6NW01TUlXRE5TcEZPYXA2Z2ElMkJ4TWloT0ZQQUlvVHRDdCUyQnVsUEFFdUI4SHRKbEdCbTclMkY0TWglMkZnUkl1NVA0SCUyRmklMkJFdHdQZmxDZTA3cGVSS0Q1SmJhU1RIQlV6RU9GVVhYT243R1prciUyQlIlMkJDV2dBeXFNVTVQTU5QZTRpcUJYZyUzRCUzRA',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.agoda.com/search?guid=ed81f485-725d-4b8b-80e9-b66784fcdb1e&asq=aV3fIKFTJBGl9z%2FHkkPKtJufa9Vwpz6XltTHq4n%2B9gOoYWnc1lzpx1CJNDqaRMvYVcOIQB7qTZcoKPmREzQuJvpOJF18I2z9kM8pXdZT33RVWhh2b%2FcP3YiYXrYm2ttkr6QDs48C6hOjLzuYUvlEgOm%2B3QacrQMDUE7JkJAfzu2HyAFLyCDQBimDzm3foBMgrr7xO7rV1TXsNvFBK8vGuA%3D%3D&city=5414&tick=638467192125&locale=en-us&ckuid=d2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0&prid=0&gclid=EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE&currency=IDR&correlationId=8a3cb2ef-297d-4625-ab9a-a907cc073fd7&analyticsSessionId=1759663807146755370&pageTypeId=1&realLanguageId=1&languageId=1&origin=ID&cid=1891460&tag=f71b0106-fb42-0cf2-b13e-84355fbe83c7&userId=d2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=25&currencyCode=IDR&htmlLanguage=en-us&cultureInfoName=en-us&machineName=sg-pc-6g-acm-web-user-7ff798594-vrd7r&trafficGroupId=5&sessionId=hwz4ybyt0vqbbcb3morfkfek&trafficSubGroupId=122&aid=82361&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&browserFamily=Firefox&cdnDomain=agoda.net&checkIn=2024-03-31&checkOut=2024-04-01&rooms=1&adults=2&children=0&priceCur=IDR&los=1&textToSearch=Malang&travellerType=1&familyMode=off&ds=en8tWMNuMxqNWXE8&productType=-1',
    'content-type': 'application/json',
    'AG-LANGUAGE-LOCALE': 'en-us',
    'ag-debug-override-origin': 'ID',
    'AG-REQUEST-ID': '30cdaf22-f278-4cec-ad5c-363817eb6113',
    'AG-RETRY-ATTEMPT': '0',
    'AG-REQUEST-ATTEMPT': '1',
    'AG-PAGE-TYPE-ID': '103',
    'AG-CORRELATION-ID': 'bf2266db-3ce0-4dbd-a40e-52551f03d383',
    'AG-ANALYTICS-SESSION-ID': '1759663807146755370',
    'Access-Control-Max-Age': '7200',
    'Origin': 'https://www.agoda.com',
    'Connection': 'keep-alive',
    # 'Cookie': 'agoda.landings=1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7||hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|19----1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7|EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE|hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|20----1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7|EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE|hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|99; agoda.analytics=Id=1759663807146755370&Signature=3831058715177103895&Expiry=1711101323860; ASP.NET_SessionId=hwz4ybyt0vqbbcb3morfkfek; agoda.version.03=CookieId=7628156b-a104-42e8-8c31-1877034bbb88&TItems=2$1891460$03-22-2024 15:46$04-21-2024 15:46$f71b0106-fb42-0cf2-b13e-84355fbe83c7&DLang=en-us&CurLabel=IDR; agoda.firstclicks=1891460||f71b0106-fb42-0cf2-b13e-84355fbe83c7||2024-03-22T15:46:47||hwz4ybyt0vqbbcb3morfkfek||{"IsPaid":true,"gclid":"","Type":""}; agoda.user.03=UserId=d2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0; agoda.lastclicks=1891460||f71b0106-fb42-0cf2-b13e-84355fbe83c7||2024-03-22T15:46:47||hwz4ybyt0vqbbcb3morfkfek||{"IsPaid":true,"gclid":"EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE","Type":""}; agoda.prius=PriusID=0&PointsMaxTraffic=Agoda; agoda.attr.03=ATItems=1891460$03-22-2024 15:46$f71b0106-fb42-0cf2-b13e-84355fbe83c7; agoda.price.01=PriceView=1; xsrf_token=CfDJ8Dkuqwv-0VhLoFfD8dw7lYyW3DV2i_AgBuSaJO-ms2PzSot77dQp1a8XJA7LtTpj_G6i_PdMHhPB2zYNikT3BVfLJ6MraBpPHEE6jzIc_ThUJ58yUqHk9vlW420jboLdiXVmiKAgnE_tV_L5BRGvuuY; tealiumEnable=true; deviceId=03a52854-f95d-479d-bf1d-73552986527e; agoda.consent=ID||2024-03-22 08:46:48Z; _gcl_aw=GCL.1711097224.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE; _gcl_au=1.1.913130779.1711097211; _ga_T408Z268D2=GS1.1.1711097210.1.1.1711097725.0.0.1525321318; _ga=GA1.2.1816605990.1711097211; FPID=FPID2.2.dl5Al7XRNkZWXCxvNet1hQLPWYuBLUT4WYjODVwcrj0%3D.1711097211; FPLC=AzMc0Z83T9eFMBgX39%2BZYEXz4xJkVgRWLDnrAogM41szJZ6EGfpsx55LcLfGWyPIFurYFfyD9UfSTHEEr6at%2BkBrD94nef9Q7AjB%2Fqn7dTtseIrIKn9tKARPslsxdw%3D%3D; ab.storage.userId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%22d2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0%22%2C%22c%22%3A1711097213422%2C%22l%22%3A1711097213422%7D; ab.storage.sessionId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%22bf268215-8fc3-10a5-ca5c-9ad38aa7ab25%22%2C%22e%22%3A1711099028196%2C%22c%22%3A1711097213423%2C%22l%22%3A1711097228196%7D; ab.storage.deviceId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%22762e89e3-75cf-4bed-ec2d-c7dc7fced657%22%2C%22c%22%3A1711097213423%2C%22l%22%3A1711097213423%7D; agoda.familyMode=Mode=0; agoda.search.01=SHist=1$5414$8490$1$1$2$0$0$1711097723$$0&H=; _ab50group=GroupA; _40-40-20Split=Group40A; utag_main=v_id:018e65578f6e000d5d8ba448bb8a0504604bb00900bd0$_sn:1$_se:6$_ss:0$_st:1711099525798$ses_id:1711097220975%3Bexp-session$_pn:2%3Bexp-session; lastRskxRun=1711097227929; rskxRunCookie=0; rCookie=qpu7p60xr4s53aj4bo4zajlu2f3udy; _ha_aw=GCL.1711097225.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE; _hab_aw=GCL.1711097225.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE; _gid=GA1.2.28862958.1711097226; _gac_UA-6446424-30=1.1711097226.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE; _uetsid=c2a40160e82811eeae954114e4cfa07e; _uetvid=c2a41f20e82811eeba84755b2afc03f2; _fbp=fb.1.1711097225963.1923692797; _ga_C07L4VP9DZ=GS1.2.1711097226.1.0.1711097226.60.0.0; __gads=ID=67b7a66e41f1db10:T=1711097225:RT=1711097225:S=ALNI_MaQ4CFngpLi-6-0aTnwyXM9UclBgg; __gpi=UID=00000d52b95a2a0f:T=1711097225:RT=1711097225:S=ALNI_MbzzWyJU7zEyLRiAabcoTgGx63pig; cto_bundle=ygTCtl9Ud2FNM1dwWSUyQkh2eGdOemUlMkZScFNOQTN6NW01TUlXRE5TcEZPYXA2Z2ElMkJ4TWloT0ZQQUlvVHRDdCUyQnVsUEFFdUI4SHRKbEdCbTclMkY0TWglMkZnUkl1NVA0SCUyRmklMkJFdHdQZmxDZTA3cGVSS0Q1SmJhU1RIQlV6RU9GVVhYT243R1prciUyQlIlMkJDV2dBeXFNVTVQTU5QZTRpcUJYZyUzRCUzRA',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

json_data = {
    'operationName': 'citySearch',
    'variables': {
        'CitySearchRequest': {
            'cityId': 5414,
            'searchRequest': {
                'searchCriteria': {
                    'isAllowBookOnRequest': True,
                    'bookingDate': '2024-03-22T08:55:26.034Z',
                    'checkInDate': '2024-03-30T17:00:00.000Z',
                    'localCheckInDate': '2024-03-31',
                    'los': 1,
                    'rooms': 1,
                    'adults': 2,
                    'children': 0,
                    'childAges': [],
                    'ratePlans': [],
                    'featureFlagRequest': {
                        'fetchNamesForTealium': True,
                        'fiveStarDealOfTheDay': True,
                        'isAllowBookOnRequest': False,
                        'showUnAvailable': True,
                        'showRemainingProperties': True,
                        'isMultiHotelSearch': False,
                        'enableAgencySupplyForPackages': True,
                        'flags': [
                            {
                                'feature': 'FamilyChildFriendlyPopularFilter',
                                'enable': True,
                            },
                            {
                                'feature': 'FamilyChildFriendlyPropertyTypeFilter',
                                'enable': True,
                            },
                            {
                                'feature': 'FamilyMode',
                                'enable': False,
                            },
                        ],
                        'enablePageToken': True,
                        'enableDealsOfTheDayFilter': False,
                        'isEnableSupplierFinancialInfo': False,
                        'ignoreRequestedNumberOfRoomsForNha': False,
                        'isFlexibleMultiRoomSearch': False,
                    },
                    'isUserLoggedIn': False,
                    'currency': 'IDR',
                    'travellerType': 'Couple',
                    'isAPSPeek': False,
                    'enableOpaqueChannel': False,
                    'isEnabledPartnerChannelSelection': None,
                    'sorting': {
                        'sortField': 'Ranking',
                        'sortOrder': 'Desc',
                        'sortParams': None,
                    },
                    'requiredBasis': 'PRPN',
                    'requiredPrice': 'Exclusive',
                    'suggestionLimit': 0,
                    'synchronous': False,
                    'supplierPullMetadataRequest': None,
                    'isRoomSuggestionRequested': False,
                    'isAPORequest': False,
                    'hasAPOFilter': False,
                },
                'searchContext': {
                    'userId': 'd2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0',
                    'memberId': 0,
                    'locale': 'en-us',
                    'cid': 1891460,
                    'origin': 'ID',
                    'platform': 1,
                    'deviceTypeId': 1,
                    'experiments': {
                        'forceByVariant': None,
                        'forceByExperiment': [
                            {
                                'id': 'UMRAH-B2B',
                                'variant': 'B',
                            },
                            {
                                'id': 'UMRAH-B2C-REGIONAL',
                                'variant': 'B',
                            },
                            {
                                'id': 'UMRAH-B2C',
                                'variant': 'Z',
                            },
                            {
                                'id': 'JGCW-204',
                                'variant': 'B',
                            },
                        ],
                    },
                    'isRetry': False,
                    'showCMS': False,
                    'storeFrontId': 3,
                    'pageTypeId': 103,
                    'whiteLabelKey': None,
                    'ipAddress': '139.255.221.98',
                    'endpointSearchType': 'CitySearch',
                    'trackSteps': None,
                    'searchId': '394407b5-c69a-4bf0-bb48-829d55c22e1d',
                },
                'matrix': None,
                'matrixGroup': [
                    {
                        'matrixGroup': 'NumberOfBedrooms',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'LandmarkIds',
                        'size': 10,
                    },
                    {
                        'matrixGroup': 'GroupedBedTypes',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'RoomBenefits',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'AtmosphereIds',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'PopularForFamily',
                        'size': 5,
                    },
                    {
                        'matrixGroup': 'RoomAmenities',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'AffordableCategory',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'HotelFacilities',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'BeachAccessTypeIds',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'StarRating',
                        'size': 20,
                    },
                    {
                        'matrixGroup': 'KidsStayForFree',
                        'size': 5,
                    },
                    {
                        'matrixGroup': 'AllGuestReviewBreakdown',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'MetroSubwayStationLandmarkIds',
                        'size': 20,
                    },
                    {
                        'matrixGroup': 'CityCenterDistance',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'ProductType',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'TripPurpose',
                        'size': 5,
                    },
                    {
                        'matrixGroup': 'BusStationLandmarkIds',
                        'size': 20,
                    },
                    {
                        'matrixGroup': 'IsSustainableTravel',
                        'size': 2,
                    },
                    {
                        'matrixGroup': 'ReviewLocationScore',
                        'size': 3,
                    },
                    {
                        'matrixGroup': 'LandmarkSubTypeCategoryIds',
                        'size': 20,
                    },
                    {
                        'matrixGroup': 'ReviewScore',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'AccommodationType',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'PaymentOptions',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'TrainStationLandmarkIds',
                        'size': 20,
                    },
                    {
                        'matrixGroup': 'HotelAreaId',
                        'size': 100,
                    },
                    {
                        'matrixGroup': 'HotelChainId',
                        'size': 10,
                    },
                    {
                        'matrixGroup': 'RecommendedByDestinationCity',
                        'size': 10,
                    },
                    {
                        'matrixGroup': 'Deals',
                        'size': 100,
                    },
                ],
                'filterRequest': {
                    'idsFilters': [],
                    'rangeFilters': [],
                    'textFilters': [],
                },
                'page': {
                    'pageSize': 100,
                    'pageNumber': 2,
                    "pageToken": "AEuwCCAES5wIK5AKLvZwV+t6/FbqQ3hWlzIMB2KYijeoR1N+/DNnmJ4H1GP28IL6xBPHVFNjVEcfCOpH3H5aggg/936EKrL0i+8mSCamuvQTQihnOkg+SyhTakg/flh+T/50OvtSBDtGUGc/LGLj5L7qUD8SgwgnurTj1zw2n05YDnoQD/bEEkv+dDonvR+j7vRXJk/sO0ebzDsfMEfaIogeaig6a0ogDioaaELPeRqb3qwGdtKsH0u68AtOO2g3+027o8LkSrsSYEPSFpAP+sQSCoOEC7ZKJEebusgaXqyGdrb4B6LmbBIChYIj7Bf/b0w+R3iDT14IR/4COA6eV+QLh8kiErg/X/vIS59f4AojiEdCpEen6/QLD1xHcgXrrvyDJ4rAD2Zb0BKX+kATRmNQE15iGDp2n4BLZkOQCoIoO6cOEC/yxBJWb5BGTlvoNs5ekA4GepAv/0NUEiYqeA4vqkhDVz4gDlejODqmYOBoECAEQaA=="
                },
                'apoRequest': {
                    'apoPageSize': 10,
                },
                'searchHistory': None,
                'searchDetailRequest': {
                    'priceHistogramBins': 50,
                },
                'isTrimmedResponseRequested': False,
                'featuredAgodaHomesRequest': None,
                'featuredLuxuryHotelsRequest': None,
                'highlyRatedAgodaHomesRequest': {
                    'numberOfAgodaHomes': 30,
                    'minimumReviewScore': 7.5,
                    'minimumReviewCount': 3,
                    'accommodationTypes': [
                        28,
                        29,
                        30,
                        102,
                        103,
                        106,
                        107,
                        108,
                        109,
                        110,
                        114,
                        115,
                        120,
                        131,
                    ],
                    'sortVersion': 0,
                },
                'extraAgodaHomesRequest': None,
                'extraHotels': {
                    'extraHotelIds': [],
                    'enableFiltersForExtraHotels': False,
                },
                'packaging': None,
                'flexibleSearchRequest': {
                    'fromDate': '2024-03-22',
                    'toDate': '2024-04-30',
                    'alternativeDateSize': 4,
                    'isFullFlexibleDateSearch': False,
                },
                'rankingRequest': {
                    'isNhaKeywordSearch': False,
                },
                'rocketmilesRequestV2': None,
                'featuredPulsePropertiesRequest': {
                    'numberOfPulseProperties': 15,
                },
            },
        },
        'ContentSummaryRequest': {
            'context': {
                'rawUserId': 'd2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0',
                'memberId': 0,
                'userOrigin': 'ID',
                'locale': 'en-us',
                'forceExperimentsByIdNew': [
                    {
                        'key': 'UMRAH-B2B',
                        'value': 'B',
                    },
                    {
                        'key': 'UMRAH-B2C-REGIONAL',
                        'value': 'B',
                    },
                    {
                        'key': 'UMRAH-B2C',
                        'value': 'Z',
                    },
                    {
                        'key': 'JGCW-204',
                        'value': 'B',
                    },
                ],
                'apo': False,
                'searchCriteria': {
                    'cityId': 5414,
                },
                'platform': {
                    'id': 1,
                },
                'storeFrontId': 3,
                'cid': '1891460',
                'occupancy': {
                    'numberOfAdults': 2,
                    'numberOfChildren': 0,
                    'travelerType': 2,
                    'checkIn': '2024-03-30T17:00:00.000Z',
                },
                'deviceTypeId': 1,
                'whiteLabelKey': '',
                'correlationId': '',
            },
            'summary': {
                'highlightedFeaturesOrderPriority': None,
                'includeHotelCharacter': True,
            },
            'reviews': {
                'commentary': None,
                'demographics': {
                    'providerIds': None,
                    'filter': {
                        'defaultProviderOnly': True,
                    },
                },
                'summaries': {
                    'providerIds': None,
                    'apo': True,
                    'limit': 1,
                    'travellerType': 2,
                },
                'cumulative': {
                    'providerIds': None,
                },
                'filters': None,
            },
            'images': {
                'page': None,
                'maxWidth': 0,
                'maxHeight': 0,
                'imageSizes': None,
                'indexOffset': None,
            },
            'rooms': {
                'images': None,
                'featureLimit': 0,
                'filterCriteria': None,
                'includeMissing': False,
                'includeSoldOut': False,
                'includeDmcRoomId': False,
                'soldOutRoomCriteria': None,
                'showRoomSize': True,
                'showRoomFacilities': True,
                'showRoomName': False,
            },
            'nonHotelAccommodation': True,
            'engagement': True,
            'highlights': {
                'maxNumberOfItems': 0,
                'images': {
                    'imageSizes': [
                        {
                            'key': 'full',
                            'size': {
                                'width': 0,
                                'height': 0,
                            },
                        },
                    ],
                },
            },
            'personalizedInformation': True,
            'localInformation': {
                'images': None,
            },
            'features': None,
            'rateCategories': True,
            'contentRateCategories': {
                'escapeRateCategories': {},
            },
            'synopsis': True,
        },
        'PricingSummaryRequest': {
            'cheapestOnly': True,
            'context': {
                'isAllowBookOnRequest': True,
                'abTests': [
                    {
                        'testId': 9021,
                        'abUser': 'B',
                    },
                    {
                        'testId': 9023,
                        'abUser': 'B',
                    },
                    {
                        'testId': 9024,
                        'abUser': 'B',
                    },
                    {
                        'testId': 9025,
                        'abUser': 'B',
                    },
                    {
                        'testId': 9027,
                        'abUser': 'B',
                    },
                    {
                        'testId': 9029,
                        'abUser': 'B',
                    },
                ],
                'clientInfo': {
                    'cid': 1891460,
                    'languageId': 1,
                    'languageUse': 1,
                    'origin': 'ID',
                    'platform': 1,
                    'searchId': '394407b5-c69a-4bf0-bb48-829d55c22e1d',
                    'storefront': 3,
                    'userId': 'd2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0',
                    'ipAddress': '139.255.221.98',
                },
                'experiment': [
                    {
                        'name': 'UMRAH-B2B',
                        'variant': 'B',
                    },
                    {
                        'name': 'UMRAH-B2C-REGIONAL',
                        'variant': 'B',
                    },
                    {
                        'name': 'UMRAH-B2C',
                        'variant': 'Z',
                    },
                    {
                        'name': 'JGCW-204',
                        'variant': 'B',
                    },
                ],
                'sessionInfo': {
                    'isLogin': False,
                    'memberId': 0,
                    'sessionId': 1,
                },
                'packaging': None,
            },
            'isSSR': True,
            'pricing': {
                'bookingDate': '2024-03-22T08:55:26.025Z',
                'checkIn': '2024-03-30T17:00:00.000Z',
                'checkout': '2024-03-31T17:00:00.000Z',
                'localCheckInDate': '2024-03-31',
                'localCheckoutDate': '2024-04-01',
                'currency': 'IDR',
                'details': {
                    'cheapestPriceOnly': False,
                    'itemBreakdown': False,
                    'priceBreakdown': False,
                },
                'featureFlag': [
                    'ClientDiscount',
                    'PriceHistory',
                    'VipPlatinum',
                    'RatePlanPromosCumulative',
                    'PromosCumulative',
                    'CouponSellEx',
                    'MixAndSave',
                    'APSPeek',
                    'StackChannelDiscount',
                    'AutoApplyPromos',
                    'EnableAgencySupplyForPackages',
                    'EnableCashback',
                    'CreditCardPromotionPeek',
                    'EnableCofundedCashback',
                    'DispatchGoLocalForInternational',
                    'EnableGoToTravelCampaign',
                    'EnablePriceTrend',
                ],
                'features': {
                    'crossOutRate': False,
                    'isAPSPeek': False,
                    'isAllOcc': False,
                    'isApsEnabled': False,
                    'isIncludeUsdAndLocalCurrency': False,
                    'isMSE': True,
                    'isRPM2Included': True,
                    'maxSuggestions': 0,
                    'isEnableSupplierFinancialInfo': False,
                    'isLoggingAuctionData': False,
                    'newRateModel': False,
                    'overrideOccupancy': False,
                    'filterCheapestRoomEscapesPackage': False,
                    'priusId': 0,
                    'synchronous': False,
                    'enableRichContentOffer': True,
                    'showCouponAmountInUserCurrency': False,
                    'disableEscapesPackage': False,
                    'enablePushDayUseRates': False,
                    'enableDayUseCor': False,
                },
                'filters': {
                    'cheapestRoomFilters': [],
                    'filterAPO': False,
                    'ratePlans': [
                        1,
                    ],
                    'secretDealOnly': False,
                    'suppliers': [],
                    'nosOfBedrooms': [],
                },
                'includedPriceInfo': False,
                'occupancy': {
                    'adults': 2,
                    'children': 0,
                    'childAges': [],
                    'rooms': 1,
                    'childrenTypes': [],
                },
                'supplierPullMetadata': {
                    'requiredPrecheckAccuracyLevel': 0,
                },
                'mseHotelIds': [],
                'ppLandingHotelIds': [],
                'searchedHotelIds': [],
                'paymentId': -1,
                'externalLoyaltyRequest': None,
            },
            'suggestedPrice': 'Exclusive',
        },
        'PriceStreamMetaLabRequest': {
            'attributesId': [
                8,
                1,
                18,
                7,
                11,
                2,
                3,
            ],
        },
    },
    'query': 'query citySearch($CitySearchRequest: CitySearchRequest!, $ContentSummaryRequest: ContentSummaryRequest!, $PricingSummaryRequest: PricingRequestParameters, $PriceStreamMetaLabRequest: PriceStreamMetaLabRequest) {\n  citySearch(CitySearchRequest: $CitySearchRequest) {\n    featuredPulseProperties(ContentSummaryRequest: $ContentSummaryRequest, PricingSummaryRequest: $PricingSummaryRequest) {\n      propertyId\n      propertyResultType\n      pricing {\n        pulseCampaignMetadata {\n          promotionTypeId\n          webCampaignId\n          campaignTypeId\n          campaignBadgeText\n          campaignBadgeDescText\n          dealExpiryTime\n          showPulseMerchandise\n        }\n        isAvailable\n        isReady\n        offers {\n          roomOffers {\n            room {\n              pricing {\n                currency\n                price {\n                  perNight {\n                    exclusive {\n                      crossedOutPrice\n                      display\n                    }\n                    inclusive {\n                      crossedOutPrice\n                      display\n                    }\n                  }\n                  perRoomPerNight {\n                    exclusive {\n                      crossedOutPrice\n                      display\n                    }\n                    inclusive {\n                      crossedOutPrice\n                      display\n                    }\n                  }\n                }\n              }\n            }\n          }\n        }\n      }\n      content {\n        reviews {\n          contentReview {\n            isDefault\n            providerId\n            cumulative {\n              reviewCount\n              score\n            }\n          }\n          cumulative {\n            reviewCount\n            score\n          }\n        }\n        images {\n          hotelImages {\n            urls {\n              value\n            }\n          }\n        }\n        informationSummary {\n          hasHostExperience\n          displayName\n          rating\n          propertyLinks {\n            propertyPage\n          }\n          address {\n            country {\n              id\n            }\n            area {\n              name\n            }\n            city {\n              name\n            }\n          }\n          nhaSummary {\n            hostType\n          }\n        }\n      }\n    }\n    searchResult {\n      sortMatrix {\n        result {\n          fieldId\n          sorting {\n            sortField\n            sortOrder\n            sortParams {\n              id\n            }\n          }\n          display {\n            name\n          }\n          childMatrix {\n            fieldId\n            sorting {\n              sortField\n              sortOrder\n              sortParams {\n                id\n              }\n            }\n            display {\n              name\n            }\n            childMatrix {\n              fieldId\n              sorting {\n                sortField\n                sortOrder\n                sortParams {\n                  id\n                }\n              }\n              display {\n                name\n              }\n            }\n          }\n        }\n      }\n      searchInfo {\n        flexibleSearch {\n          currentDate {\n            checkIn\n            price\n          }\n          alternativeDates {\n            checkIn\n            price\n          }\n        }\n        hasSecretDeal\n        isComplete\n        totalFilteredHotels\n        hasEscapesPackage\n        searchStatus {\n          searchCriteria {\n            checkIn\n          }\n          searchStatus\n        }\n        objectInfo {\n          objectName\n          cityName\n          cityEnglishName\n          countryId\n          countryEnglishName\n          mapLatitude\n          mapLongitude\n          mapZoomLevel\n          wlPreferredCityName\n          wlPreferredCountryName\n          cityId\n          cityCenterPolygon {\n            geoPoints {\n              lon\n              lat\n            }\n            touristAreaCenterPoint {\n              lon\n              lat\n            }\n          }\n        }\n      }\n      urgencyDetail {\n        urgencyScore\n      }\n      histogram {\n        bins {\n          numOfElements\n          upperBound {\n            perNightPerRoom\n            perPax\n          }\n        }\n      }\n      nhaProbability\n    }\n    properties(ContentSummaryRequest: $ContentSummaryRequest, PricingSummaryRequest: $PricingSummaryRequest, PriceStreamMetaLabRequest: $PriceStreamMetaLabRequest) {\n      propertyId\n      sponsoredDetail {\n        sponsoredType\n        trackingData\n        isShowSponsoredFlag\n      }\n      propertyResultType\n      content {\n        informationSummary {\n          hotelCharacter {\n            hotelTag {\n              name\n              symbol\n            }\n            hotelView {\n              name\n              symbol\n            }\n          }\n          propertyLinks {\n            propertyPage\n          }\n          atmospheres {\n            id\n            name\n          }\n          isSustainableTravel\n          localeName\n          defaultName\n          displayName\n          accommodationType\n          awardYear\n          hasHostExperience\n          nhaSummary {\n            hostPropertyCount\n          }\n          address {\n            countryCode\n            country {\n              id\n              name\n            }\n            city {\n              id\n              name\n            }\n            area {\n              id\n              name\n            }\n          }\n          propertyType\n          rating\n          agodaGuaranteeProgram\n          remarks {\n            renovationInfo {\n              renovationType\n              year\n            }\n          }\n          spokenLanguages {\n            id\n          }\n          geoInfo {\n            latitude\n            longitude\n          }\n        }\n        propertyEngagement {\n          lastBooking\n          peopleLooking\n        }\n        nonHotelAccommodation {\n          masterRooms {\n            noOfBathrooms\n            noOfBedrooms\n            noOfBeds\n            roomSizeSqm\n            highlightedFacilities\n          }\n          hostLevel {\n            id\n            name\n          }\n          supportedLongStay\n        }\n        facilities {\n          id\n        }\n        images {\n          hotelImages {\n            id\n            caption\n            providerId\n            urls {\n              key\n              value\n            }\n          }\n        }\n        reviews {\n          contentReview {\n            isDefault\n            providerId\n            demographics {\n              groups {\n                id\n                grades {\n                  id\n                  score\n                }\n              }\n            }\n            summaries {\n              recommendationScores {\n                recommendationScore\n              }\n              snippets {\n                countryId\n                countryCode\n                countryName\n                date\n                demographicId\n                demographicName\n                reviewer\n                reviewRating\n                snippet\n              }\n            }\n            cumulative {\n              reviewCount\n              score\n            }\n          }\n          cumulative {\n            reviewCount\n            score\n          }\n          cumulativeForHost {\n            hostAvgHotelReviewRating\n            hostHotelReviewTotalCount\n          }\n        }\n        familyFeatures {\n          hasChildrenFreePolicy\n          isFamilyRoom\n          hasMoreThanOneBedroom\n          isInterConnectingRoom\n          isInfantCottageAvailable\n          hasKidsPool\n          hasKidsClub\n        }\n        personalizedInformation {\n          childrenFreePolicy {\n            fromAge\n            toAge\n          }\n        }\n        localInformation {\n          landmarks {\n            transportation {\n              landmarkName\n              distanceInM\n            }\n            topLandmark {\n              landmarkName\n              distanceInM\n            }\n            beach {\n              landmarkName\n              distanceInM\n            }\n          }\n          hasAirportTransfer\n        }\n        highlight {\n          cityCenter {\n            distanceFromCityCenter\n          }\n          favoriteFeatures {\n            features {\n              id\n              title\n              category\n            }\n          }\n          hasNearbyPublicTransportation\n        }\n        rateCategories {\n          escapeRateCategories {\n            rateCategoryId\n            localizedRateCategoryName\n          }\n        }\n      }\n      soldOut {\n        soldOutPrice {\n          averagePrice\n        }\n      }\n      pricing {\n        pulseCampaignMetadata {\n          promotionTypeId\n          webCampaignId\n          campaignTypeId\n          campaignBadgeText\n          campaignBadgeDescText\n          dealExpiryTime\n          showPulseMerchandise\n        }\n        isAvailable\n        isReady\n        benefits\n        cheapestRoomOffer {\n          agodaCash {\n            showBadge\n            giftcardGuid\n            dayToEarn\n            earnId\n            percentage\n            expiryDay\n          }\n          cashback {\n            cashbackGuid\n            showPostCashbackPrice\n            cashbackVersion\n            percentage\n            earnId\n            dayToEarn\n            expiryDay\n            cashbackType\n            appliedCampaignName\n          }\n        }\n        isEasyCancel\n        isInsiderDeal\n        isMultiHotelEligible\n        suggestPriceType {\n          suggestPrice\n        }\n        roomBundle {\n          bundleId\n          bundleType\n          saveAmount {\n            perNight {\n              ...Frag6902j0b2gca1jfd5c905\n            }\n          }\n        }\n        pointmax {\n          channelId\n          point\n        }\n        priceChange {\n          changePercentage\n          searchDate\n        }\n        payment {\n          cancellation {\n            cancellationType\n            freeCancellationDate\n          }\n          payLater {\n            isEligible\n          }\n          payAtHotel {\n            isEligible\n          }\n          noCreditCard {\n            isEligible\n          }\n          taxReceipt {\n            isEligible\n          }\n        }\n        cheapestStayPackageRatePlans {\n          stayPackageType\n          ratePlanId\n        }\n        pricingMessages {\n          location\n          ids\n        }\n        suppliersSummaries {\n          id\n          supplierHotelId\n        }\n        supplierInfo {\n          id\n          name\n          isAgodaBand\n        }\n        childPolicy {\n          freeChildren\n        }\n        offers {\n          roomOffers {\n            room {\n              extraPriceInfo {\n                displayPriceWithSurchargesPRPN\n                corDisplayPriceWithSurchargesPRPN\n              }\n              availableRooms\n              isPromoEligible\n              promotions {\n                typeId\n                promotionDiscount {\n                  value\n                }\n                isRatePlanAsPromotion\n                cmsTypeId\n                description\n              }\n              bookingDuration {\n                unit\n                value\n              }\n              supplierId\n              corSummary {\n                hasCor\n                corType\n                isOriginal\n                hasOwnCOR\n                isBlacklistedCor\n              }\n              localVoucher {\n                currencyCode\n                amount\n              }\n              pricing {\n                currency\n                price {\n                  perNight {\n                    exclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      originalPrice\n                    }\n                    inclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      originalPrice\n                    }\n                  }\n                  perBook {\n                    exclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      originalPrice\n                      autoAppliedPromoDiscount\n                    }\n                    inclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      originalPrice\n                      autoAppliedPromoDiscount\n                    }\n                  }\n                  perRoomPerNight {\n                    exclusive {\n                      display\n                      crossedOutPrice\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      pseudoCouponPrice\n                      originalPrice\n                      loyaltyOfferSummary {\n                        basePrice {\n                          exclusive\n                          allInclusive\n                        }\n                        status\n                        offers {\n                          identifier\n                          status\n                          burn {\n                            points\n                            payableAmount\n                          }\n                          earn {\n                            points\n                          }\n                          offerType\n                          isSelected\n                        }\n                      }\n                    }\n                    inclusive {\n                      display\n                      crossedOutPrice\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      pseudoCouponPrice\n                      originalPrice\n                      loyaltyOfferSummary {\n                        basePrice {\n                          exclusive\n                          allInclusive\n                        }\n                        status\n                        offers {\n                          identifier\n                          status\n                          burn {\n                            points\n                            payableAmount\n                          }\n                          earn {\n                            points\n                          }\n                          offerType\n                          isSelected\n                        }\n                      }\n                    }\n                  }\n                  totalDiscount\n                  priceAfterAppliedAgodaCash {\n                    perBook {\n                      ...Fragih856fgi287ec49egf33\n                    }\n                    perRoomPerNight {\n                      ...Fragih856fgi287ec49egf33\n                    }\n                  }\n                }\n                apsPeek {\n                  perRoomPerNight {\n                    ...Frag6902j0b2gca1jfd5c905\n                  }\n                }\n                promotionPricePeek {\n                  display {\n                    perBook {\n                      ...Frag6902j0b2gca1jfd5c905\n                    }\n                    perRoomPerNight {\n                      ...Frag6902j0b2gca1jfd5c905\n                    }\n                    perNight {\n                      ...Frag6902j0b2gca1jfd5c905\n                    }\n                  }\n                  discountType\n                  promotionCodeType\n                  promotionCode\n                  promoAppliedOnFinalPrice\n                  childPromotions {\n                    campaignId\n                  }\n                  campaignName\n                }\n                channelDiscountSummary {\n                  channelDiscountBreakdown {\n                    display\n                    discountPercent\n                    channelId\n                  }\n                }\n                promotionsCumulative {\n                  promotionCumulativeType\n                  amountPercentage\n                  minNightsStay\n                }\n              }\n              uid\n              payment {\n                cancellation {\n                  cancellationType\n                }\n              }\n              discount {\n                deals\n                channelDiscount\n              }\n              saveUpTo {\n                perRoomPerNight\n              }\n              benefits {\n                id\n                targetType\n              }\n              channel {\n                id\n              }\n              mseRoomSummaries {\n                supplierId\n                subSupplierId\n                pricingSummaries {\n                  currency\n                  channelDiscountSummary {\n                    channelDiscountBreakdown {\n                      channelId\n                      discountPercent\n                      display\n                    }\n                  }\n                  price {\n                    perRoomPerNight {\n                      exclusive {\n                        display\n                      }\n                      inclusive {\n                        display\n                      }\n                    }\n                  }\n                }\n              }\n              cashback {\n                cashbackGuid\n                showPostCashbackPrice\n                cashbackVersion\n                percentage\n                earnId\n                dayToEarn\n                expiryDay\n                cashbackType\n                appliedCampaignName\n              }\n              agodaCash {\n                showBadge\n                giftcardGuid\n                dayToEarn\n                expiryDay\n                percentage\n              }\n              corInfo {\n                corBreakdown {\n                  taxExPN {\n                    ...Frage60a5384bab7h9023989\n                  }\n                  taxInPN {\n                    ...Frage60a5384bab7h9023989\n                  }\n                  taxExPRPN {\n                    ...Frage60a5384bab7h9023989\n                  }\n                  taxInPRPN {\n                    ...Frage60a5384bab7h9023989\n                  }\n                }\n                corInfo {\n                  corType\n                }\n              }\n              loyaltyDisplay {\n                items\n              }\n              capacity {\n                extraBedsAvailable\n              }\n              pricingMessages {\n                formatted {\n                  location\n                  texts {\n                    index\n                    text\n                  }\n                }\n              }\n              campaign {\n                selected {\n                  campaignId\n                  promotionId\n                  messages {\n                    campaignName\n                    title\n                    titleWithDiscount\n                    description\n                    linkOutText\n                    url\n                  }\n                }\n              }\n              stayPackageType\n            }\n          }\n        }\n      }\n      metaLab {\n        attributes {\n          attributeId\n          dataType\n          value\n          version\n        }\n      }\n      enrichment {\n        topSellingPoint {\n          tspType\n          value\n        }\n        pricingBadges {\n          badges\n        }\n        uniqueSellingPoint {\n          rank\n          segment\n          uspType\n          uspPropertyType\n        }\n        bookingHistory {\n          bookingCount {\n            count\n            timeFrame\n          }\n        }\n        showReviewSnippet\n        isPopular\n        roomInformation {\n          cheapestRoomSizeSqm\n          facilities {\n            id\n            propertyFacilityName\n            symbol\n          }\n        }\n      }\n    }\n    searchEnrichment {\n      suppliersInformation {\n        supplierId\n        supplierName\n        isAgodaBand\n      }\n      pageToken\n    }\n    aggregation {\n      matrixGroupResults {\n        matrixGroup\n        matrixItemResults {\n          id\n          name\n          count\n          filterKey\n          filterRequestType\n          extraDataResults {\n            text\n            matrixExtraDataType\n          }\n        }\n      }\n    }\n  }\n}\n\nfragment Fragih856fgi287ec49egf33 on DisplayPrice {\n  exclusive\n  allInclusive\n}\n\nfragment Frag6902j0b2gca1jfd5c905 on DFDisplayPrice {\n  exclusive\n  allInclusive\n}\n\nfragment Frage60a5384bab7h9023989 on DFCorBreakdownItem {\n  price\n  id\n}\n',
}

response = requests.post('https://www.agoda.com/graphql/search', cookies=cookies, headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"operationName":"citySearch","variables":{"CitySearchRequest":{"cityId":5414,"searchRequest":{"searchCriteria":{"isAllowBookOnRequest":true,"bookingDate":"2024-03-22T08:55:26.034Z","checkInDate":"2024-03-30T17:00:00.000Z","localCheckInDate":"2024-03-31","los":1,"rooms":1,"adults":2,"children":0,"childAges":[],"ratePlans":[],"featureFlagRequest":{"fetchNamesForTealium":true,"fiveStarDealOfTheDay":true,"isAllowBookOnRequest":false,"showUnAvailable":true,"showRemainingProperties":true,"isMultiHotelSearch":false,"enableAgencySupplyForPackages":true,"flags":[{"feature":"FamilyChildFriendlyPopularFilter","enable":true},{"feature":"FamilyChildFriendlyPropertyTypeFilter","enable":true},{"feature":"FamilyMode","enable":false}],"enablePageToken":true,"enableDealsOfTheDayFilter":false,"isEnableSupplierFinancialInfo":false,"ignoreRequestedNumberOfRoomsForNha":false,"isFlexibleMultiRoomSearch":false},"isUserLoggedIn":false,"currency":"IDR","travellerType":"Couple","isAPSPeek":false,"enableOpaqueChannel":false,"isEnabledPartnerChannelSelection":null,"sorting":{"sortField":"Ranking","sortOrder":"Desc","sortParams":null},"requiredBasis":"PRPN","requiredPrice":"Exclusive","suggestionLimit":0,"synchronous":false,"supplierPullMetadataRequest":null,"isRoomSuggestionRequested":false,"isAPORequest":false,"hasAPOFilter":false},"searchContext":{"userId":"d2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0","memberId":0,"locale":"en-us","cid":1891460,"origin":"ID","platform":1,"deviceTypeId":1,"experiments":{"forceByVariant":null,"forceByExperiment":[{"id":"UMRAH-B2B","variant":"B"},{"id":"UMRAH-B2C-REGIONAL","variant":"B"},{"id":"UMRAH-B2C","variant":"Z"},{"id":"JGCW-204","variant":"B"}]},"isRetry":false,"showCMS":false,"storeFrontId":3,"pageTypeId":103,"whiteLabelKey":null,"ipAddress":"139.255.221.98","endpointSearchType":"CitySearch","trackSteps":null,"searchId":"394407b5-c69a-4bf0-bb48-829d55c22e1d"},"matrix":null,"matrixGroup":[{"matrixGroup":"NumberOfBedrooms","size":100},{"matrixGroup":"LandmarkIds","size":10},{"matrixGroup":"GroupedBedTypes","size":100},{"matrixGroup":"RoomBenefits","size":100},{"matrixGroup":"AtmosphereIds","size":100},{"matrixGroup":"PopularForFamily","size":5},{"matrixGroup":"RoomAmenities","size":100},{"matrixGroup":"AffordableCategory","size":100},{"matrixGroup":"HotelFacilities","size":100},{"matrixGroup":"BeachAccessTypeIds","size":100},{"matrixGroup":"StarRating","size":20},{"matrixGroup":"KidsStayForFree","size":5},{"matrixGroup":"AllGuestReviewBreakdown","size":100},{"matrixGroup":"MetroSubwayStationLandmarkIds","size":20},{"matrixGroup":"CityCenterDistance","size":100},{"matrixGroup":"ProductType","size":100},{"matrixGroup":"TripPurpose","size":5},{"matrixGroup":"BusStationLandmarkIds","size":20},{"matrixGroup":"IsSustainableTravel","size":2},{"matrixGroup":"ReviewLocationScore","size":3},{"matrixGroup":"LandmarkSubTypeCategoryIds","size":20},{"matrixGroup":"ReviewScore","size":100},{"matrixGroup":"AccommodationType","size":100},{"matrixGroup":"PaymentOptions","size":100},{"matrixGroup":"TrainStationLandmarkIds","size":20},{"matrixGroup":"HotelAreaId","size":100},{"matrixGroup":"HotelChainId","size":10},{"matrixGroup":"RecommendedByDestinationCity","size":10},{"matrixGroup":"Deals","size":100}],"filterRequest":{"idsFilters":[],"rangeFilters":[],"textFilters":[]},"page":{"pageSize":45,"pageNumber":1,"pageToken":""},"apoRequest":{"apoPageSize":10},"searchHistory":null,"searchDetailRequest":{"priceHistogramBins":50},"isTrimmedResponseRequested":false,"featuredAgodaHomesRequest":null,"featuredLuxuryHotelsRequest":null,"highlyRatedAgodaHomesRequest":{"numberOfAgodaHomes":30,"minimumReviewScore":7.5,"minimumReviewCount":3,"accommodationTypes":[28,29,30,102,103,106,107,108,109,110,114,115,120,131],"sortVersion":0},"extraAgodaHomesRequest":null,"extraHotels":{"extraHotelIds":[],"enableFiltersForExtraHotels":false},"packaging":null,"flexibleSearchRequest":{"fromDate":"2024-03-22","toDate":"2024-04-30","alternativeDateSize":4,"isFullFlexibleDateSearch":false},"rankingRequest":{"isNhaKeywordSearch":false},"rocketmilesRequestV2":null,"featuredPulsePropertiesRequest":{"numberOfPulseProperties":15}}},"ContentSummaryRequest":{"context":{"rawUserId":"d2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0","memberId":0,"userOrigin":"ID","locale":"en-us","forceExperimentsByIdNew":[{"key":"UMRAH-B2B","value":"B"},{"key":"UMRAH-B2C-REGIONAL","value":"B"},{"key":"UMRAH-B2C","value":"Z"},{"key":"JGCW-204","value":"B"}],"apo":false,"searchCriteria":{"cityId":5414},"platform":{"id":1},"storeFrontId":3,"cid":"1891460","occupancy":{"numberOfAdults":2,"numberOfChildren":0,"travelerType":2,"checkIn":"2024-03-30T17:00:00.000Z"},"deviceTypeId":1,"whiteLabelKey":"","correlationId":""},"summary":{"highlightedFeaturesOrderPriority":null,"includeHotelCharacter":true},"reviews":{"commentary":null,"demographics":{"providerIds":null,"filter":{"defaultProviderOnly":true}},"summaries":{"providerIds":null,"apo":true,"limit":1,"travellerType":2},"cumulative":{"providerIds":null},"filters":null},"images":{"page":null,"maxWidth":0,"maxHeight":0,"imageSizes":null,"indexOffset":null},"rooms":{"images":null,"featureLimit":0,"filterCriteria":null,"includeMissing":false,"includeSoldOut":false,"includeDmcRoomId":false,"soldOutRoomCriteria":null,"showRoomSize":true,"showRoomFacilities":true,"showRoomName":false},"nonHotelAccommodation":true,"engagement":true,"highlights":{"maxNumberOfItems":0,"images":{"imageSizes":[{"key":"full","size":{"width":0,"height":0}}]}},"personalizedInformation":true,"localInformation":{"images":null},"features":null,"rateCategories":true,"contentRateCategories":{"escapeRateCategories":{}},"synopsis":true},"PricingSummaryRequest":{"cheapestOnly":true,"context":{"isAllowBookOnRequest":true,"abTests":[{"testId":9021,"abUser":"B"},{"testId":9023,"abUser":"B"},{"testId":9024,"abUser":"B"},{"testId":9025,"abUser":"B"},{"testId":9027,"abUser":"B"},{"testId":9029,"abUser":"B"}],"clientInfo":{"cid":1891460,"languageId":1,"languageUse":1,"origin":"ID","platform":1,"searchId":"394407b5-c69a-4bf0-bb48-829d55c22e1d","storefront":3,"userId":"d2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0","ipAddress":"139.255.221.98"},"experiment":[{"name":"UMRAH-B2B","variant":"B"},{"name":"UMRAH-B2C-REGIONAL","variant":"B"},{"name":"UMRAH-B2C","variant":"Z"},{"name":"JGCW-204","variant":"B"}],"sessionInfo":{"isLogin":false,"memberId":0,"sessionId":1},"packaging":null},"isSSR":true,"pricing":{"bookingDate":"2024-03-22T08:55:26.025Z","checkIn":"2024-03-30T17:00:00.000Z","checkout":"2024-03-31T17:00:00.000Z","localCheckInDate":"2024-03-31","localCheckoutDate":"2024-04-01","currency":"IDR","details":{"cheapestPriceOnly":false,"itemBreakdown":false,"priceBreakdown":false},"featureFlag":["ClientDiscount","PriceHistory","VipPlatinum","RatePlanPromosCumulative","PromosCumulative","CouponSellEx","MixAndSave","APSPeek","StackChannelDiscount","AutoApplyPromos","EnableAgencySupplyForPackages","EnableCashback","CreditCardPromotionPeek","EnableCofundedCashback","DispatchGoLocalForInternational","EnableGoToTravelCampaign","EnablePriceTrend"],"features":{"crossOutRate":false,"isAPSPeek":false,"isAllOcc":false,"isApsEnabled":false,"isIncludeUsdAndLocalCurrency":false,"isMSE":true,"isRPM2Included":true,"maxSuggestions":0,"isEnableSupplierFinancialInfo":false,"isLoggingAuctionData":false,"newRateModel":false,"overrideOccupancy":false,"filterCheapestRoomEscapesPackage":false,"priusId":0,"synchronous":false,"enableRichContentOffer":true,"showCouponAmountInUserCurrency":false,"disableEscapesPackage":false,"enablePushDayUseRates":false,"enableDayUseCor":false},"filters":{"cheapestRoomFilters":[],"filterAPO":false,"ratePlans":[1],"secretDealOnly":false,"suppliers":[],"nosOfBedrooms":[]},"includedPriceInfo":false,"occupancy":{"adults":2,"children":0,"childAges":[],"rooms":1,"childrenTypes":[]},"supplierPullMetadata":{"requiredPrecheckAccuracyLevel":0},"mseHotelIds":[],"ppLandingHotelIds":[],"searchedHotelIds":[],"paymentId":-1,"externalLoyaltyRequest":null},"suggestedPrice":"Exclusive"},"PriceStreamMetaLabRequest":{"attributesId":[8,1,18,7,11,2,3]}},"query":"query citySearch($CitySearchRequest: CitySearchRequest!, $ContentSummaryRequest: ContentSummaryRequest!, $PricingSummaryRequest: PricingRequestParameters, $PriceStreamMetaLabRequest: PriceStreamMetaLabRequest) {\\n  citySearch(CitySearchRequest: $CitySearchRequest) {\\n    featuredPulseProperties(ContentSummaryRequest: $ContentSummaryRequest, PricingSummaryRequest: $PricingSummaryRequest) {\\n      propertyId\\n      propertyResultType\\n      pricing {\\n        pulseCampaignMetadata {\\n          promotionTypeId\\n          webCampaignId\\n          campaignTypeId\\n          campaignBadgeText\\n          campaignBadgeDescText\\n          dealExpiryTime\\n          showPulseMerchandise\\n        }\\n        isAvailable\\n        isReady\\n        offers {\\n          roomOffers {\\n            room {\\n              pricing {\\n                currency\\n                price {\\n                  perNight {\\n                    exclusive {\\n                      crossedOutPrice\\n                      display\\n                    }\\n                    inclusive {\\n                      crossedOutPrice\\n                      display\\n                    }\\n                  }\\n                  perRoomPerNight {\\n                    exclusive {\\n                      crossedOutPrice\\n                      display\\n                    }\\n                    inclusive {\\n                      crossedOutPrice\\n                      display\\n                    }\\n                  }\\n                }\\n              }\\n            }\\n          }\\n        }\\n      }\\n      content {\\n        reviews {\\n          contentReview {\\n            isDefault\\n            providerId\\n            cumulative {\\n              reviewCount\\n              score\\n            }\\n          }\\n          cumulative {\\n            reviewCount\\n            score\\n          }\\n        }\\n        images {\\n          hotelImages {\\n            urls {\\n              value\\n            }\\n          }\\n        }\\n        informationSummary {\\n          hasHostExperience\\n          displayName\\n          rating\\n          propertyLinks {\\n            propertyPage\\n          }\\n          address {\\n            country {\\n              id\\n            }\\n            area {\\n              name\\n            }\\n            city {\\n              name\\n            }\\n          }\\n          nhaSummary {\\n            hostType\\n          }\\n        }\\n      }\\n    }\\n    searchResult {\\n      sortMatrix {\\n        result {\\n          fieldId\\n          sorting {\\n            sortField\\n            sortOrder\\n            sortParams {\\n              id\\n            }\\n          }\\n          display {\\n            name\\n          }\\n          childMatrix {\\n            fieldId\\n            sorting {\\n              sortField\\n              sortOrder\\n              sortParams {\\n                id\\n              }\\n            }\\n            display {\\n              name\\n            }\\n            childMatrix {\\n              fieldId\\n              sorting {\\n                sortField\\n                sortOrder\\n                sortParams {\\n                  id\\n                }\\n              }\\n              display {\\n                name\\n              }\\n            }\\n          }\\n        }\\n      }\\n      searchInfo {\\n        flexibleSearch {\\n          currentDate {\\n            checkIn\\n            price\\n          }\\n          alternativeDates {\\n            checkIn\\n            price\\n          }\\n        }\\n        hasSecretDeal\\n        isComplete\\n        totalFilteredHotels\\n        hasEscapesPackage\\n        searchStatus {\\n          searchCriteria {\\n            checkIn\\n          }\\n          searchStatus\\n        }\\n        objectInfo {\\n          objectName\\n          cityName\\n          cityEnglishName\\n          countryId\\n          countryEnglishName\\n          mapLatitude\\n          mapLongitude\\n          mapZoomLevel\\n          wlPreferredCityName\\n          wlPreferredCountryName\\n          cityId\\n          cityCenterPolygon {\\n            geoPoints {\\n              lon\\n              lat\\n            }\\n            touristAreaCenterPoint {\\n              lon\\n              lat\\n            }\\n          }\\n        }\\n      }\\n      urgencyDetail {\\n        urgencyScore\\n      }\\n      histogram {\\n        bins {\\n          numOfElements\\n          upperBound {\\n            perNightPerRoom\\n            perPax\\n          }\\n        }\\n      }\\n      nhaProbability\\n    }\\n    properties(ContentSummaryRequest: $ContentSummaryRequest, PricingSummaryRequest: $PricingSummaryRequest, PriceStreamMetaLabRequest: $PriceStreamMetaLabRequest) {\\n      propertyId\\n      sponsoredDetail {\\n        sponsoredType\\n        trackingData\\n        isShowSponsoredFlag\\n      }\\n      propertyResultType\\n      content {\\n        informationSummary {\\n          hotelCharacter {\\n            hotelTag {\\n              name\\n              symbol\\n            }\\n            hotelView {\\n              name\\n              symbol\\n            }\\n          }\\n          propertyLinks {\\n            propertyPage\\n          }\\n          atmospheres {\\n            id\\n            name\\n          }\\n          isSustainableTravel\\n          localeName\\n          defaultName\\n          displayName\\n          accommodationType\\n          awardYear\\n          hasHostExperience\\n          nhaSummary {\\n            hostPropertyCount\\n          }\\n          address {\\n            countryCode\\n            country {\\n              id\\n              name\\n            }\\n            city {\\n              id\\n              name\\n            }\\n            area {\\n              id\\n              name\\n            }\\n          }\\n          propertyType\\n          rating\\n          agodaGuaranteeProgram\\n          remarks {\\n            renovationInfo {\\n              renovationType\\n              year\\n            }\\n          }\\n          spokenLanguages {\\n            id\\n          }\\n          geoInfo {\\n            latitude\\n            longitude\\n          }\\n        }\\n        propertyEngagement {\\n          lastBooking\\n          peopleLooking\\n        }\\n        nonHotelAccommodation {\\n          masterRooms {\\n            noOfBathrooms\\n            noOfBedrooms\\n            noOfBeds\\n            roomSizeSqm\\n            highlightedFacilities\\n          }\\n          hostLevel {\\n            id\\n            name\\n          }\\n          supportedLongStay\\n        }\\n        facilities {\\n          id\\n        }\\n        images {\\n          hotelImages {\\n            id\\n            caption\\n            providerId\\n            urls {\\n              key\\n              value\\n            }\\n          }\\n        }\\n        reviews {\\n          contentReview {\\n            isDefault\\n            providerId\\n            demographics {\\n              groups {\\n                id\\n                grades {\\n                  id\\n                  score\\n                }\\n              }\\n            }\\n            summaries {\\n              recommendationScores {\\n                recommendationScore\\n              }\\n              snippets {\\n                countryId\\n                countryCode\\n                countryName\\n                date\\n                demographicId\\n                demographicName\\n                reviewer\\n                reviewRating\\n                snippet\\n              }\\n            }\\n            cumulative {\\n              reviewCount\\n              score\\n            }\\n          }\\n          cumulative {\\n            reviewCount\\n            score\\n          }\\n          cumulativeForHost {\\n            hostAvgHotelReviewRating\\n            hostHotelReviewTotalCount\\n          }\\n        }\\n        familyFeatures {\\n          hasChildrenFreePolicy\\n          isFamilyRoom\\n          hasMoreThanOneBedroom\\n          isInterConnectingRoom\\n          isInfantCottageAvailable\\n          hasKidsPool\\n          hasKidsClub\\n        }\\n        personalizedInformation {\\n          childrenFreePolicy {\\n            fromAge\\n            toAge\\n          }\\n        }\\n        localInformation {\\n          landmarks {\\n            transportation {\\n              landmarkName\\n              distanceInM\\n            }\\n            topLandmark {\\n              landmarkName\\n              distanceInM\\n            }\\n            beach {\\n              landmarkName\\n              distanceInM\\n            }\\n          }\\n          hasAirportTransfer\\n        }\\n        highlight {\\n          cityCenter {\\n            distanceFromCityCenter\\n          }\\n          favoriteFeatures {\\n            features {\\n              id\\n              title\\n              category\\n            }\\n          }\\n          hasNearbyPublicTransportation\\n        }\\n        rateCategories {\\n          escapeRateCategories {\\n            rateCategoryId\\n            localizedRateCategoryName\\n          }\\n        }\\n      }\\n      soldOut {\\n        soldOutPrice {\\n          averagePrice\\n        }\\n      }\\n      pricing {\\n        pulseCampaignMetadata {\\n          promotionTypeId\\n          webCampaignId\\n          campaignTypeId\\n          campaignBadgeText\\n          campaignBadgeDescText\\n          dealExpiryTime\\n          showPulseMerchandise\\n        }\\n        isAvailable\\n        isReady\\n        benefits\\n        cheapestRoomOffer {\\n          agodaCash {\\n            showBadge\\n            giftcardGuid\\n            dayToEarn\\n            earnId\\n            percentage\\n            expiryDay\\n          }\\n          cashback {\\n            cashbackGuid\\n            showPostCashbackPrice\\n            cashbackVersion\\n            percentage\\n            earnId\\n            dayToEarn\\n            expiryDay\\n            cashbackType\\n            appliedCampaignName\\n          }\\n        }\\n        isEasyCancel\\n        isInsiderDeal\\n        isMultiHotelEligible\\n        suggestPriceType {\\n          suggestPrice\\n        }\\n        roomBundle {\\n          bundleId\\n          bundleType\\n          saveAmount {\\n            perNight {\\n              ...Frag6902j0b2gca1jfd5c905\\n            }\\n          }\\n        }\\n        pointmax {\\n          channelId\\n          point\\n        }\\n        priceChange {\\n          changePercentage\\n          searchDate\\n        }\\n        payment {\\n          cancellation {\\n            cancellationType\\n            freeCancellationDate\\n          }\\n          payLater {\\n            isEligible\\n          }\\n          payAtHotel {\\n            isEligible\\n          }\\n          noCreditCard {\\n            isEligible\\n          }\\n          taxReceipt {\\n            isEligible\\n          }\\n        }\\n        cheapestStayPackageRatePlans {\\n          stayPackageType\\n          ratePlanId\\n        }\\n        pricingMessages {\\n          location\\n          ids\\n        }\\n        suppliersSummaries {\\n          id\\n          supplierHotelId\\n        }\\n        supplierInfo {\\n          id\\n          name\\n          isAgodaBand\\n        }\\n        childPolicy {\\n          freeChildren\\n        }\\n        offers {\\n          roomOffers {\\n            room {\\n              extraPriceInfo {\\n                displayPriceWithSurchargesPRPN\\n                corDisplayPriceWithSurchargesPRPN\\n              }\\n              availableRooms\\n              isPromoEligible\\n              promotions {\\n                typeId\\n                promotionDiscount {\\n                  value\\n                }\\n                isRatePlanAsPromotion\\n                cmsTypeId\\n                description\\n              }\\n              bookingDuration {\\n                unit\\n                value\\n              }\\n              supplierId\\n              corSummary {\\n                hasCor\\n                corType\\n                isOriginal\\n                hasOwnCOR\\n                isBlacklistedCor\\n              }\\n              localVoucher {\\n                currencyCode\\n                amount\\n              }\\n              pricing {\\n                currency\\n                price {\\n                  perNight {\\n                    exclusive {\\n                      display\\n                      cashbackPrice\\n                      displayAfterCashback\\n                      originalPrice\\n                    }\\n                    inclusive {\\n                      display\\n                      cashbackPrice\\n                      displayAfterCashback\\n                      originalPrice\\n                    }\\n                  }\\n                  perBook {\\n                    exclusive {\\n                      display\\n                      cashbackPrice\\n                      displayAfterCashback\\n                      rebatePrice\\n                      originalPrice\\n                      autoAppliedPromoDiscount\\n                    }\\n                    inclusive {\\n                      display\\n                      cashbackPrice\\n                      displayAfterCashback\\n                      rebatePrice\\n                      originalPrice\\n                      autoAppliedPromoDiscount\\n                    }\\n                  }\\n                  perRoomPerNight {\\n                    exclusive {\\n                      display\\n                      crossedOutPrice\\n                      cashbackPrice\\n                      displayAfterCashback\\n                      rebatePrice\\n                      pseudoCouponPrice\\n                      originalPrice\\n                      loyaltyOfferSummary {\\n                        basePrice {\\n                          exclusive\\n                          allInclusive\\n                        }\\n                        status\\n                        offers {\\n                          identifier\\n                          status\\n                          burn {\\n                            points\\n                            payableAmount\\n                          }\\n                          earn {\\n                            points\\n                          }\\n                          offerType\\n                          isSelected\\n                        }\\n                      }\\n                    }\\n                    inclusive {\\n                      display\\n                      crossedOutPrice\\n                      cashbackPrice\\n                      displayAfterCashback\\n                      rebatePrice\\n                      pseudoCouponPrice\\n                      originalPrice\\n                      loyaltyOfferSummary {\\n                        basePrice {\\n                          exclusive\\n                          allInclusive\\n                        }\\n                        status\\n                        offers {\\n                          identifier\\n                          status\\n                          burn {\\n                            points\\n                            payableAmount\\n                          }\\n                          earn {\\n                            points\\n                          }\\n                          offerType\\n                          isSelected\\n                        }\\n                      }\\n                    }\\n                  }\\n                  totalDiscount\\n                  priceAfterAppliedAgodaCash {\\n                    perBook {\\n                      ...Fragih856fgi287ec49egf33\\n                    }\\n                    perRoomPerNight {\\n                      ...Fragih856fgi287ec49egf33\\n                    }\\n                  }\\n                }\\n                apsPeek {\\n                  perRoomPerNight {\\n                    ...Frag6902j0b2gca1jfd5c905\\n                  }\\n                }\\n                promotionPricePeek {\\n                  display {\\n                    perBook {\\n                      ...Frag6902j0b2gca1jfd5c905\\n                    }\\n                    perRoomPerNight {\\n                      ...Frag6902j0b2gca1jfd5c905\\n                    }\\n                    perNight {\\n                      ...Frag6902j0b2gca1jfd5c905\\n                    }\\n                  }\\n                  discountType\\n                  promotionCodeType\\n                  promotionCode\\n                  promoAppliedOnFinalPrice\\n                  childPromotions {\\n                    campaignId\\n                  }\\n                  campaignName\\n                }\\n                channelDiscountSummary {\\n                  channelDiscountBreakdown {\\n                    display\\n                    discountPercent\\n                    channelId\\n                  }\\n                }\\n                promotionsCumulative {\\n                  promotionCumulativeType\\n                  amountPercentage\\n                  minNightsStay\\n                }\\n              }\\n              uid\\n              payment {\\n                cancellation {\\n                  cancellationType\\n                }\\n              }\\n              discount {\\n                deals\\n                channelDiscount\\n              }\\n              saveUpTo {\\n                perRoomPerNight\\n              }\\n              benefits {\\n                id\\n                targetType\\n              }\\n              channel {\\n                id\\n              }\\n              mseRoomSummaries {\\n                supplierId\\n                subSupplierId\\n                pricingSummaries {\\n                  currency\\n                  channelDiscountSummary {\\n                    channelDiscountBreakdown {\\n                      channelId\\n                      discountPercent\\n                      display\\n                    }\\n                  }\\n                  price {\\n                    perRoomPerNight {\\n                      exclusive {\\n                        display\\n                      }\\n                      inclusive {\\n                        display\\n                      }\\n                    }\\n                  }\\n                }\\n              }\\n              cashback {\\n                cashbackGuid\\n                showPostCashbackPrice\\n                cashbackVersion\\n                percentage\\n                earnId\\n                dayToEarn\\n                expiryDay\\n                cashbackType\\n                appliedCampaignName\\n              }\\n              agodaCash {\\n                showBadge\\n                giftcardGuid\\n                dayToEarn\\n                expiryDay\\n                percentage\\n              }\\n              corInfo {\\n                corBreakdown {\\n                  taxExPN {\\n                    ...Frage60a5384bab7h9023989\\n                  }\\n                  taxInPN {\\n                    ...Frage60a5384bab7h9023989\\n                  }\\n                  taxExPRPN {\\n                    ...Frage60a5384bab7h9023989\\n                  }\\n                  taxInPRPN {\\n                    ...Frage60a5384bab7h9023989\\n                  }\\n                }\\n                corInfo {\\n                  corType\\n                }\\n              }\\n              loyaltyDisplay {\\n                items\\n              }\\n              capacity {\\n                extraBedsAvailable\\n              }\\n              pricingMessages {\\n                formatted {\\n                  location\\n                  texts {\\n                    index\\n                    text\\n                  }\\n                }\\n              }\\n              campaign {\\n                selected {\\n                  campaignId\\n                  promotionId\\n                  messages {\\n                    campaignName\\n                    title\\n                    titleWithDiscount\\n                    description\\n                    linkOutText\\n                    url\\n                  }\\n                }\\n              }\\n              stayPackageType\\n            }\\n          }\\n        }\\n      }\\n      metaLab {\\n        attributes {\\n          attributeId\\n          dataType\\n          value\\n          version\\n        }\\n      }\\n      enrichment {\\n        topSellingPoint {\\n          tspType\\n          value\\n        }\\n        pricingBadges {\\n          badges\\n        }\\n        uniqueSellingPoint {\\n          rank\\n          segment\\n          uspType\\n          uspPropertyType\\n        }\\n        bookingHistory {\\n          bookingCount {\\n            count\\n            timeFrame\\n          }\\n        }\\n        showReviewSnippet\\n        isPopular\\n        roomInformation {\\n          cheapestRoomSizeSqm\\n          facilities {\\n            id\\n            propertyFacilityName\\n            symbol\\n          }\\n        }\\n      }\\n    }\\n    searchEnrichment {\\n      suppliersInformation {\\n        supplierId\\n        supplierName\\n        isAgodaBand\\n      }\\n      pageToken\\n    }\\n    aggregation {\\n      matrixGroupResults {\\n        matrixGroup\\n        matrixItemResults {\\n          id\\n          name\\n          count\\n          filterKey\\n          filterRequestType\\n          extraDataResults {\\n            text\\n            matrixExtraDataType\\n          }\\n        }\\n      }\\n    }\\n  }\\n}\\n\\nfragment Fragih856fgi287ec49egf33 on DisplayPrice {\\n  exclusive\\n  allInclusive\\n}\\n\\nfragment Frag6902j0b2gca1jfd5c905 on DFDisplayPrice {\\n  exclusive\\n  allInclusive\\n}\\n\\nfragment Frage60a5384bab7h9023989 on DFCorBreakdownItem {\\n  price\\n  id\\n}\\n"}'
#response = requests.post('https://www.agoda.com/graphql/search', cookies=cookies, headers=headers, data=data)

import json

print(json.dumps(response.json(), indent=4))