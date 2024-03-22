

import requests

cookies = {
    'agoda.landings': '1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7||hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|19----1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7|EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE|hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|20----1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7|EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE|hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|99',
    'agoda.analytics': 'Id=1759663807146755370&Signature=7745457525434028397&Expiry=1711104060608',
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
    '_ga_T408Z268D2': 'GS1.1.1711097210.1.1.1711100476.0.0.1525321318',
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
    'utag_main': 'v_id:018e65578f6e000d5d8ba448bb8a0504604bb00900bd0$_sn:1$_se:28$_ss:0$_st:1711102265239$ses_id:1711097220975%3Bexp-session$_pn:14%3Bexp-session',
    'lastRskxRun': '1711097227929',
    'rskxRunCookie': '0',
    'rCookie': 'qpu7p60xr4s53aj4bo4zajlu2f3udy',
    '_ha_aw': 'GCL.1711100363.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE',
    '_hab_aw': 'GCL.1711100363.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE',
    '_gid': 'GA1.2.28862958.1711097226',
    '_gac_UA-6446424-30': '1.1711100364.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE',
    '_fbp': 'fb.1.1711097225963.1923692797',
    '_ga_C07L4VP9DZ': 'GS1.2.1711099631.2.1.1711100470.60.0.0',
    '__gads': 'ID=67b7a66e41f1db10:T=1711097225:RT=1711100364:S=ALNI_MaQ4CFngpLi-6-0aTnwyXM9UclBgg',
    '__gpi': 'UID=00000d52b95a2a0f:T=1711097225:RT=1711100364:S=ALNI_MbzzWyJU7zEyLRiAabcoTgGx63pig',
    'cto_bundle': 'ZBCH219Ud2FNM1dwWSUyQkh2eGdOemUlMkZScFNOSGxWZWxra3JNeE9lOWJKQW41dDNNU1drd1p1eWRrbFg1SUg0eXYlMkZDMkE4N0Z2c0xCWVQ5JTJCRzVRekVreXB2MVVZTUsxd2RoR0pDSmdZWXpPQSUyQjJJSjViV2VkOUtwRlVXdlZsSnBXT2NXemlEUnJ1Z2RydkhFWXdSczlWSmIlMkJCMXclM0QlM0Q',
    '_uetsid': 'c2a40160e82811eeae954114e4cfa07e',
    '_uetvid': 'c2a41f20e82811eeba84755b2afc03f2',
    '_gat_t3': '1',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.agoda.com/hotel-santika-premiere-malang/hotel/malang-id.html?finalPriceView=1&isShowMobileAppPrice=false&cid=1891460&numberOfBedrooms=&familyMode=false&adults=2&children=0&rooms=1&maxRooms=0&checkIn=2024-03-31&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=1&showReviewSubmissionEntry=false&currencyCode=IDR&isFreeOccSearch=false&tag=f71b0106-fb42-0cf2-b13e-84355fbe83c7&isCityHaveAsq=false&los=1&searchrequestid=fe94e148-c808-423d-949f-35ba5ec53590&ds=en8tWMNuMxqNWXE8',
    'content-type': 'application/json',
    'AG-LANGUAGE-LOCALE': 'en-us',
    'ag-debug-override-origin': 'ID',
    'AG-REQUEST-ID': '425449c1-1069-4c89-bec0-c3ee221300a6',
    'AG-RETRY-ATTEMPT': '0',
    'AG-REQUEST-ATTEMPT': '1',
    'AG-PAGE-TYPE-ID': '7',
    'AG-CORRELATION-ID': 'c3ce60af-faa4-4405-a3ae-80fc7a77c2a0',
    'AG-ANALYTICS-SESSION-ID': '1759663807146755370',
    'Access-Control-Max-Age': '7200',
    'AG-FORCE-EXPERIMENTS': 'TEXT-10548,B',
    'Origin': 'https://www.agoda.com',
    'Connection': 'keep-alive',
    # 'Cookie': 'agoda.landings=1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7||hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|19----1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7|EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE|hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|20----1891460|f71b0106-fb42-0cf2-b13e-84355fbe83c7|EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE|hwz4ybyt0vqbbcb3morfkfek|2024-03-22T15:46:47|True|99; agoda.analytics=Id=1759663807146755370&Signature=7745457525434028397&Expiry=1711104060608; ASP.NET_SessionId=hwz4ybyt0vqbbcb3morfkfek; agoda.version.03=CookieId=7628156b-a104-42e8-8c31-1877034bbb88&TItems=2$1891460$03-22-2024 15:46$04-21-2024 15:46$f71b0106-fb42-0cf2-b13e-84355fbe83c7&DLang=en-us&CurLabel=IDR; agoda.firstclicks=1891460||f71b0106-fb42-0cf2-b13e-84355fbe83c7||2024-03-22T15:46:47||hwz4ybyt0vqbbcb3morfkfek||{"IsPaid":true,"gclid":"","Type":""}; agoda.user.03=UserId=d2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0; agoda.lastclicks=1891460||f71b0106-fb42-0cf2-b13e-84355fbe83c7||2024-03-22T15:46:47||hwz4ybyt0vqbbcb3morfkfek||{"IsPaid":true,"gclid":"EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE","Type":""}; agoda.prius=PriusID=0&PointsMaxTraffic=Agoda; agoda.attr.03=ATItems=1891460$03-22-2024 15:46$f71b0106-fb42-0cf2-b13e-84355fbe83c7; agoda.price.01=PriceView=1; xsrf_token=CfDJ8Dkuqwv-0VhLoFfD8dw7lYyW3DV2i_AgBuSaJO-ms2PzSot77dQp1a8XJA7LtTpj_G6i_PdMHhPB2zYNikT3BVfLJ6MraBpPHEE6jzIc_ThUJ58yUqHk9vlW420jboLdiXVmiKAgnE_tV_L5BRGvuuY; tealiumEnable=true; deviceId=03a52854-f95d-479d-bf1d-73552986527e; agoda.consent=ID||2024-03-22 09:27:06Z; _gcl_aw=GCL.1711100363.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE; _gcl_au=1.1.913130779.1711097211; _ga_T408Z268D2=GS1.1.1711097210.1.1.1711100476.0.0.1525321318; _ga=GA1.2.1816605990.1711097211; FPID=FPID2.2.dl5Al7XRNkZWXCxvNet1hQLPWYuBLUT4WYjODVwcrj0%3D.1711097211; FPLC=AzMc0Z83T9eFMBgX39%2BZYEXz4xJkVgRWLDnrAogM41szJZ6EGfpsx55LcLfGWyPIFurYFfyD9UfSTHEEr6at%2BkBrD94nef9Q7AjB%2Fqn7dTtseIrIKn9tKARPslsxdw%3D%3D; ab.storage.userId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%22d2bd8d3b-5ae5-4210-bbad-5b69c26a1ee0%22%2C%22c%22%3A1711097213422%2C%22l%22%3A1711097213422%7D; ab.storage.sessionId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%22f0599a65-5088-82b3-9089-e1d5286ee5ad%22%2C%22e%22%3A1711102163773%2C%22c%22%3A1711099654839%2C%22l%22%3A1711100363773%7D; ab.storage.deviceId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%22762e89e3-75cf-4bed-ec2d-c7dc7fced657%22%2C%22c%22%3A1711097213423%2C%22l%22%3A1711097213423%7D; agoda.familyMode=Mode=0; agoda.search.01=SHist=1$10779$8490$1$1$1$0$0$1711099648$|1$5414$8490$1$1$2$0$0$1711100356$|4$532093$8490$1$1$2$0$0$$|4$71870$8490$1$1$2$0$0$$&H=8481|0$532093$71870; _ab50group=GroupA; _40-40-20Split=Group40A; utag_main=v_id:018e65578f6e000d5d8ba448bb8a0504604bb00900bd0$_sn:1$_se:28$_ss:0$_st:1711102265239$ses_id:1711097220975%3Bexp-session$_pn:14%3Bexp-session; lastRskxRun=1711097227929; rskxRunCookie=0; rCookie=qpu7p60xr4s53aj4bo4zajlu2f3udy; _ha_aw=GCL.1711100363.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE; _hab_aw=GCL.1711100363.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE; _gid=GA1.2.28862958.1711097226; _gac_UA-6446424-30=1.1711100364.EAIaIQobChMIyYKD6b2HhQMVdqhmAh05GgClEAAYASAAEgICz_D_BwE; _fbp=fb.1.1711097225963.1923692797; _ga_C07L4VP9DZ=GS1.2.1711099631.2.1.1711100470.60.0.0; __gads=ID=67b7a66e41f1db10:T=1711097225:RT=1711100364:S=ALNI_MaQ4CFngpLi-6-0aTnwyXM9UclBgg; __gpi=UID=00000d52b95a2a0f:T=1711097225:RT=1711100364:S=ALNI_MbzzWyJU7zEyLRiAabcoTgGx63pig; cto_bundle=ZBCH219Ud2FNM1dwWSUyQkh2eGdOemUlMkZScFNOSGxWZWxra3JNeE9lOWJKQW41dDNNU1drd1p1eWRrbFg1SUg0eXYlMkZDMkE4N0Z2c0xCWVQ5JTJCRzVRekVreXB2MVVZTUsxd2RoR0pDSmdZWXpPQSUyQjJJSjViV2VkOUtwRlVXdlZsSnBXT2NXemlEUnJ1Z2RydkhFWXdSczlWSmIlMkJCMXclM0QlM0Q; _uetsid=c2a40160e82811eeae954114e4cfa07e; _uetvid=c2a41f20e82811eeba84755b2afc03f2; _gat_t3=1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

json_data = {
    'operationName': 'propertyDetailsSearch',
    'variables': {
        'PropertyDetailsRequest': {
            'propertyIds': [
                71870,
            ],
        },
        'ContentImagesRequest': {
            'imageSizes': [
                {
                    'key': 'main',
                    'size': {
                        'width': 1024,
                        'height': 768,
                    },
                },
                {
                    'key': 'gallery_preview',
                    'size': {
                        'width': 450,
                        'height': 450,
                    },
                },
                {
                    'key': 'thumbnail',
                    'size': {
                        'width': 80,
                        'height': 60,
                    },
                },
                {
                    'key': 'thumbnail-2x',
                    'size': {
                        'width': 160,
                        'height': 120,
                    },
                },
            ],
            'isApo': False,
            'isUseNewImageCaption': True,
        },
        'ContentReviewSummariesRequest': {
            'providerIds': [
                332,
                3038,
                27901,
                28999,
                29100,
                27999,
                27980,
                27989,
                29014,
            ],
            'occupancyRequest': {
                'numberOfAdults': 2,
                'numberOfChildren': 0,
                'travelerType': 1,
                'lengthOfStay': 1,
                'checkIn': '2024-03-30T17:00:00.000Z',
            },
            'contentReviewPositiveMentionsRequest': {
                'facilityClassesLimit': 3,
                'facilityClassesSentimentLimit': 3,
            },
            'contentReviewSnippetsRequest': {
                'overrideLimit': 20,
            },
            'isApo': False,
        },
        'ContentReviewScoreRequest': {
            'demographics': {
                'filter': {
                    'defaultProviderOnly': True,
                },
            },
            'providerIds': [],
        },
        'ContentInformationSummaryRequest': {
            'isApo': False,
        },
        'ContentHighlightsRequest': {
            'includeAtfPropertyHighlights': True,
            'maxNumberOfItems': 5,
            'occupancyRequest': {
                'numberOfAdults': 2,
                'numberOfChildren': 0,
                'travelerType': 2,
            },
            'images': {
                'imageSizes': [
                    {
                        'key': 'main',
                        'size': {
                            'width': 360,
                            'height': 270,
                        },
                    },
                ],
            },
        },
        'ContentLocalInformationRequest': {
            'showWalkablePlaces': True,
            'images': {
                'imageSizes': [
                    {
                        'key': 'main',
                        'size': {
                            'width': 360,
                            'height': 270,
                        },
                    },
                ],
            },
        },
        'ContentInformationRequest': {
            'isApo': False,
            'characteristicTopicsLimit': 3,
            'showDynamicShortDescription': True,
        },
        'ContentFeaturesRequest': {
            'includeFacilityHighlights': True,
            'occupancyRequest': {
                'numberOfAdults': 2,
                'numberOfChildren': 0,
                'travelerType': 1,
                'lengthOfStay': 1,
            },
            'images': {
                'imageSizes': [
                    {
                        'key': 'original',
                        'size': {
                            'width': 360,
                            'height': 270,
                        },
                    },
                ],
            },
        },
        'PriceStreamMetaLabRequest': {
            'attributesId': [
                8,
                2,
                3,
                7,
                18,
            ],
        },
    },
    'query': 'query propertyDetailsSearch($PropertyDetailsRequest: PropertyDetailsRequest!, $ContentImagesRequest: ContentImagesRequest!, $ContentReviewSummariesRequest: ContentReviewSummariesRequest, $ContentReviewScoreRequest: ContentReviewScoreRequest, $ContentInformationSummaryRequest: ContentInformationSummaryRequest, $ContentHighlightsRequest: ContentHighlightsRequest, $ContentLocalInformationRequest: ContentLocalInformationRequest, $ContentInformationRequest: ContentInformationRequest, $ContentFeaturesRequest: ContentFeaturesRequest, $PriceStreamMetaLabRequest: PriceStreamMetaLabRequest!) {\n  propertyDetailsSearch(PropertyDetailsRequest: $PropertyDetailsRequest) {\n    propertyDetails {\n      propertyId\n      propertyMetaInfo {\n        propertyMetaRanking {\n          numberOfProperty\n          metrics {\n            metricName\n            rank\n            absoluteValue\n          }\n        }\n      }\n      contentDetail {\n        propertyId\n        contentImages(ContentImagesRequest: $ContentImagesRequest) {\n          hotelImages {\n            caption\n            groupEntityId\n            groupId\n            id\n            providerId\n            typeId\n            uploadedDate\n            highResolutionSizes\n            urls {\n              key\n              value\n            }\n          }\n          videos {\n            id\n            location\n          }\n          matterports {\n            id\n            orderId\n            roomTypeId\n            thumbnailUrl\n            url\n          }\n        }\n        contentReviewSummaries(ContentReviewSummariesRequest: $ContentReviewSummariesRequest) {\n          snippets {\n            snippetId\n            countryCode\n            countryId\n            countryName\n            date\n            demographicId\n            demographicName\n            reviewer\n            reviewRating\n            snippet\n            topics {\n              score\n              topicId\n            }\n          }\n          recommendationScores {\n            frequentTravellerRecommendationScore\n            recommendationScore\n          }\n          positiveMentions {\n            categories {\n              id\n              name\n              score\n            }\n            facilityClassesSentiment {\n              facilityIds\n              id\n              name\n              noOfPositiveMentioned\n            }\n            facilityClasses {\n              facilityIds\n              id\n              name\n              noOfMentioned\n            }\n          }\n        }\n        contentReviewScore(ContentReviewScoreRequest: $ContentReviewScoreRequest) {\n          combinedReviewScore {\n            cumulative {\n              maxScore\n              reviewCount\n              score\n            }\n            cumulativeForHost {\n              reviewCount\n            }\n          }\n          providerReviewScore {\n            isDefault\n            providerId\n            trendingScore {\n              past14DaysUplift\n              past30DaysUplift\n            }\n            cumulative {\n              maxScore\n              reviewCount\n              score\n            }\n            demographics {\n              allGuest {\n                id\n                scoreDistribution {\n                  id\n                  reviewCount\n                }\n                reviewCount\n                grades {\n                  id\n                  score\n                  cityAverage\n                  subGrades {\n                    score\n                    name\n                  }\n                }\n              }\n            }\n          }\n          thirdPartyReviewScore {\n            providerId\n            grades {\n              id\n              score\n            }\n          }\n        }\n        contentSummary(ContentInformationSummaryRequest: $ContentInformationSummaryRequest) {\n          propertyId\n          displayName\n          defaultName\n          localeName\n          accommodation {\n            accommodationType\n            accommodationName\n          }\n          propertyType\n          address {\n            address1\n            address2\n            countryCode\n            area {\n              id\n              name\n            }\n            city {\n              id\n              name\n            }\n            country {\n              id\n              name\n            }\n            postalCode\n            stateInfo {\n              id\n            }\n          }\n          awardsAndAccolades {\n            goldCircleAward {\n              year\n            }\n            advanceGuaranteeProgram {\n              logo\n              description\n            }\n          }\n          remarks {\n            renovationInfo {\n              year\n              renovationType\n            }\n          }\n          hasHostExperience\n          geoInfo {\n            latitude\n            longitude\n          }\n          rating\n          asqType\n          asqInfos {\n            asqTypeId\n          }\n        }\n        contentEngagement {\n          peopleLooking\n          todayBooking\n        }\n        contentHighlights(ContentHighlightsRequest: $ContentHighlightsRequest) {\n          favoriteFeatures {\n            category\n            id\n            images {\n              id\n              urls {\n                key\n                value\n              }\n            }\n            name\n            symbol\n            tooltip\n          }\n          locationHighlightMessage {\n            title\n          }\n          locationHighlights {\n            distanceKm\n            highlightType\n            message\n          }\n          locations {\n            tooltip\n            symbol\n            name\n            images {\n              id\n              urls {\n                key\n                value\n              }\n            }\n          }\n          atfPropertyHighlights {\n            id\n            name\n            symbol\n            icon\n            category\n            images {\n              id\n              urls {\n                key\n                value\n              }\n            }\n            tooltip\n          }\n        }\n        contentLocalInformation(ContentLocalInformationRequest: $ContentLocalInformationRequest) {\n          walkablePlaces {\n            title\n            totalCount\n            description\n            walkableCategories {\n              categoryName\n              totalCount\n              topPlaces {\n                name\n                distanceInKm\n                images {\n                  urls {\n                    value\n                  }\n                }\n                landMarkGroup {\n                  name\n                  sortOrder\n                }\n              }\n            }\n          }\n          nearbyProperties {\n            categoryName\n            categorySymbol\n            id\n            places {\n              abbr\n              distanceInKm\n              duration\n              durationIcon\n              geoInfo {\n                latitude\n                longitude\n                obfuscatedLat\n                obfuscatedLong\n              }\n              images {\n                urls {\n                  value\n                  key\n                }\n                id\n              }\n              landmarkId\n              name\n              typeId\n              typeName\n            }\n          }\n          cuisines {\n            id\n            images {\n              urls {\n                value\n                key\n              }\n              id\n            }\n            name\n            restaurants {\n              cuisinesOffered\n              distance\n              id\n              name\n            }\n          }\n          locationSubscore {\n            airportScore\n            poiScore\n            transportationScore\n          }\n          nearbyPlaces {\n            abbr\n            distanceInKm\n            duration\n            durationIcon\n            geoInfo {\n              latitude\n              longitude\n              obfuscatedLat\n              obfuscatedLong\n            }\n            images {\n              urls {\n                value\n                key\n              }\n              id\n            }\n            landmarkId\n            name\n            typeId\n            typeName\n            landMarkGroup {\n              name\n              sortOrder\n            }\n          }\n          nearbyShops {\n            abbr\n            distanceInKm\n            duration\n            durationIcon\n            geoInfo {\n              latitude\n              longitude\n              obfuscatedLat\n              obfuscatedLong\n            }\n            images {\n              urls {\n                value\n                key\n              }\n              id\n            }\n            landmarkId\n            name\n            typeId\n            typeName\n          }\n          popularLandmarkNumber\n          topPlaces {\n            abbr\n            distanceInKm\n            duration\n            durationIcon\n            geoInfo {\n              latitude\n              longitude\n              obfuscatedLat\n              obfuscatedLong\n            }\n            images {\n              urls {\n                value\n                key\n              }\n              id\n            }\n            landmarkId\n            name\n            typeId\n            typeName\n            landMarkGroup {\n              name\n              sortOrder\n            }\n          }\n        }\n        contentInformation(ContentInformationRequest: $ContentInformationRequest) {\n          usefulInfoGroups {\n            id\n            usefulInfo {\n              id\n              description\n            }\n          }\n          certificate {\n            name\n            imageUrl\n            description\n          }\n          staffVaccinationInfo {\n            details\n            status\n          }\n          messaging {\n            responsiveRate\n            isAllowedPreBooking\n          }\n          description {\n            short\n          }\n          notes {\n            criticalNotes\n          }\n          sustainabilityInfo {\n            isSustainableTravel\n            practiceCategories {\n              categoryId\n              categoryName\n              practices {\n                practiceId\n                practiceName\n              }\n            }\n          }\n        }\n        contentFeatures(ContentFeaturesRequest: $ContentFeaturesRequest) {\n          featureGroups {\n            features {\n              available\n              featureName\n              featureNameLocalizationList {\n                locale\n                value\n              }\n              id\n              order\n              symbol\n              images {\n                id\n                urls {\n                  key\n                  value\n                }\n                groupId\n                groupEntityId\n                typeId\n                uploadedDate\n                providerId\n                caption\n                highResolutionSizes\n              }\n            }\n            id\n            name\n            order\n            symbol\n          }\n          hotelFacilities {\n            id\n            name\n          }\n          summary {\n            chineseFriendly\n            staycationFacilityIds {\n              activities\n              drinkingAndDining\n              sportAndEntertainment\n              wellness\n            }\n            hygienePlusFacilities {\n              healthAndMedical\n              safetyFeature\n              preventiveEquipment\n            }\n          }\n          facilityHighlights {\n            facilityId\n            facilityName\n            images {\n              id\n              urls {\n                key\n                value\n              }\n              groupId\n              groupEntityId\n              typeId\n              uploadedDate\n              providerId\n              caption\n              highResolutionSizes\n            }\n          }\n        }\n        hostProfile {\n          displayName\n          picture\n          averageReviewScore\n          totalReviews\n          hostLevel\n          responseRate\n          responseTimeSeconds\n          properties {\n            id\n            bookings\n            reviewAvg\n            reviewCount\n          }\n          userId\n        }\n      }\n      metaLab(PriceStreamMetaLabRequest: $PriceStreamMetaLabRequest) {\n        propertyAttributes {\n          attributeId\n          dataType\n          value\n          version\n        }\n      }\n    }\n  }\n}\n',
}

response = requests.post('https://www.agoda.com/graphql/property', cookies=cookies, headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"operationName":"propertyDetailsSearch","variables":{"PropertyDetailsRequest":{"propertyIds":[71870]},"ContentImagesRequest":{"imageSizes":[{"key":"main","size":{"width":1024,"height":768}},{"key":"gallery_preview","size":{"width":450,"height":450}},{"key":"thumbnail","size":{"width":80,"height":60}},{"key":"thumbnail-2x","size":{"width":160,"height":120}}],"isApo":false,"isUseNewImageCaption":true},"ContentReviewSummariesRequest":{"providerIds":[332,3038,27901,28999,29100,27999,27980,27989,29014],"occupancyRequest":{"numberOfAdults":2,"numberOfChildren":0,"travelerType":1,"lengthOfStay":1,"checkIn":"2024-03-30T17:00:00.000Z"},"contentReviewPositiveMentionsRequest":{"facilityClassesLimit":3,"facilityClassesSentimentLimit":3},"contentReviewSnippetsRequest":{"overrideLimit":20},"isApo":false},"ContentReviewScoreRequest":{"demographics":{"filter":{"defaultProviderOnly":true}},"providerIds":[]},"ContentInformationSummaryRequest":{"isApo":false},"ContentHighlightsRequest":{"includeAtfPropertyHighlights":true,"maxNumberOfItems":5,"occupancyRequest":{"numberOfAdults":2,"numberOfChildren":0,"travelerType":2},"images":{"imageSizes":[{"key":"main","size":{"width":360,"height":270}}]}},"ContentLocalInformationRequest":{"showWalkablePlaces":true,"images":{"imageSizes":[{"key":"main","size":{"width":360,"height":270}}]}},"ContentInformationRequest":{"isApo":false,"characteristicTopicsLimit":3,"showDynamicShortDescription":true},"ContentFeaturesRequest":{"includeFacilityHighlights":true,"occupancyRequest":{"numberOfAdults":2,"numberOfChildren":0,"travelerType":1,"lengthOfStay":1},"images":{"imageSizes":[{"key":"original","size":{"width":360,"height":270}}]}},"PriceStreamMetaLabRequest":{"attributesId":[8,2,3,7,18]}},"query":"query propertyDetailsSearch($PropertyDetailsRequest: PropertyDetailsRequest!, $ContentImagesRequest: ContentImagesRequest!, $ContentReviewSummariesRequest: ContentReviewSummariesRequest, $ContentReviewScoreRequest: ContentReviewScoreRequest, $ContentInformationSummaryRequest: ContentInformationSummaryRequest, $ContentHighlightsRequest: ContentHighlightsRequest, $ContentLocalInformationRequest: ContentLocalInformationRequest, $ContentInformationRequest: ContentInformationRequest, $ContentFeaturesRequest: ContentFeaturesRequest, $PriceStreamMetaLabRequest: PriceStreamMetaLabRequest!) {\\n  propertyDetailsSearch(PropertyDetailsRequest: $PropertyDetailsRequest) {\\n    propertyDetails {\\n      propertyId\\n      propertyMetaInfo {\\n        propertyMetaRanking {\\n          numberOfProperty\\n          metrics {\\n            metricName\\n            rank\\n            absoluteValue\\n          }\\n        }\\n      }\\n      contentDetail {\\n        propertyId\\n        contentImages(ContentImagesRequest: $ContentImagesRequest) {\\n          hotelImages {\\n            caption\\n            groupEntityId\\n            groupId\\n            id\\n            providerId\\n            typeId\\n            uploadedDate\\n            highResolutionSizes\\n            urls {\\n              key\\n              value\\n            }\\n          }\\n          videos {\\n            id\\n            location\\n          }\\n          matterports {\\n            id\\n            orderId\\n            roomTypeId\\n            thumbnailUrl\\n            url\\n          }\\n        }\\n        contentReviewSummaries(ContentReviewSummariesRequest: $ContentReviewSummariesRequest) {\\n          snippets {\\n            snippetId\\n            countryCode\\n            countryId\\n            countryName\\n            date\\n            demographicId\\n            demographicName\\n            reviewer\\n            reviewRating\\n            snippet\\n            topics {\\n              score\\n              topicId\\n            }\\n          }\\n          recommendationScores {\\n            frequentTravellerRecommendationScore\\n            recommendationScore\\n          }\\n          positiveMentions {\\n            categories {\\n              id\\n              name\\n              score\\n            }\\n            facilityClassesSentiment {\\n              facilityIds\\n              id\\n              name\\n              noOfPositiveMentioned\\n            }\\n            facilityClasses {\\n              facilityIds\\n              id\\n              name\\n              noOfMentioned\\n            }\\n          }\\n        }\\n        contentReviewScore(ContentReviewScoreRequest: $ContentReviewScoreRequest) {\\n          combinedReviewScore {\\n            cumulative {\\n              maxScore\\n              reviewCount\\n              score\\n            }\\n            cumulativeForHost {\\n              reviewCount\\n            }\\n          }\\n          providerReviewScore {\\n            isDefault\\n            providerId\\n            trendingScore {\\n              past14DaysUplift\\n              past30DaysUplift\\n            }\\n            cumulative {\\n              maxScore\\n              reviewCount\\n              score\\n            }\\n            demographics {\\n              allGuest {\\n                id\\n                scoreDistribution {\\n                  id\\n                  reviewCount\\n                }\\n                reviewCount\\n                grades {\\n                  id\\n                  score\\n                  cityAverage\\n                  subGrades {\\n                    score\\n                    name\\n                  }\\n                }\\n              }\\n            }\\n          }\\n          thirdPartyReviewScore {\\n            providerId\\n            grades {\\n              id\\n              score\\n            }\\n          }\\n        }\\n        contentSummary(ContentInformationSummaryRequest: $ContentInformationSummaryRequest) {\\n          propertyId\\n          displayName\\n          defaultName\\n          localeName\\n          accommodation {\\n            accommodationType\\n            accommodationName\\n          }\\n          propertyType\\n          address {\\n            address1\\n            address2\\n            countryCode\\n            area {\\n              id\\n              name\\n            }\\n            city {\\n              id\\n              name\\n            }\\n            country {\\n              id\\n              name\\n            }\\n            postalCode\\n            stateInfo {\\n              id\\n            }\\n          }\\n          awardsAndAccolades {\\n            goldCircleAward {\\n              year\\n            }\\n            advanceGuaranteeProgram {\\n              logo\\n              description\\n            }\\n          }\\n          remarks {\\n            renovationInfo {\\n              year\\n              renovationType\\n            }\\n          }\\n          hasHostExperience\\n          geoInfo {\\n            latitude\\n            longitude\\n          }\\n          rating\\n          asqType\\n          asqInfos {\\n            asqTypeId\\n          }\\n        }\\n        contentEngagement {\\n          peopleLooking\\n          todayBooking\\n        }\\n        contentHighlights(ContentHighlightsRequest: $ContentHighlightsRequest) {\\n          favoriteFeatures {\\n            category\\n            id\\n            images {\\n              id\\n              urls {\\n                key\\n                value\\n              }\\n            }\\n            name\\n            symbol\\n            tooltip\\n          }\\n          locationHighlightMessage {\\n            title\\n          }\\n          locationHighlights {\\n            distanceKm\\n            highlightType\\n            message\\n          }\\n          locations {\\n            tooltip\\n            symbol\\n            name\\n            images {\\n              id\\n              urls {\\n                key\\n                value\\n              }\\n            }\\n          }\\n          atfPropertyHighlights {\\n            id\\n            name\\n            symbol\\n            icon\\n            category\\n            images {\\n              id\\n              urls {\\n                key\\n                value\\n              }\\n            }\\n            tooltip\\n          }\\n        }\\n        contentLocalInformation(ContentLocalInformationRequest: $ContentLocalInformationRequest) {\\n          walkablePlaces {\\n            title\\n            totalCount\\n            description\\n            walkableCategories {\\n              categoryName\\n              totalCount\\n              topPlaces {\\n                name\\n                distanceInKm\\n                images {\\n                  urls {\\n                    value\\n                  }\\n                }\\n                landMarkGroup {\\n                  name\\n                  sortOrder\\n                }\\n              }\\n            }\\n          }\\n          nearbyProperties {\\n            categoryName\\n            categorySymbol\\n            id\\n            places {\\n              abbr\\n              distanceInKm\\n              duration\\n              durationIcon\\n              geoInfo {\\n                latitude\\n                longitude\\n                obfuscatedLat\\n                obfuscatedLong\\n              }\\n              images {\\n                urls {\\n                  value\\n                  key\\n                }\\n                id\\n              }\\n              landmarkId\\n              name\\n              typeId\\n              typeName\\n            }\\n          }\\n          cuisines {\\n            id\\n            images {\\n              urls {\\n                value\\n                key\\n              }\\n              id\\n            }\\n            name\\n            restaurants {\\n              cuisinesOffered\\n              distance\\n              id\\n              name\\n            }\\n          }\\n          locationSubscore {\\n            airportScore\\n            poiScore\\n            transportationScore\\n          }\\n          nearbyPlaces {\\n            abbr\\n            distanceInKm\\n            duration\\n            durationIcon\\n            geoInfo {\\n              latitude\\n              longitude\\n              obfuscatedLat\\n              obfuscatedLong\\n            }\\n            images {\\n              urls {\\n                value\\n                key\\n              }\\n              id\\n            }\\n            landmarkId\\n            name\\n            typeId\\n            typeName\\n            landMarkGroup {\\n              name\\n              sortOrder\\n            }\\n          }\\n          nearbyShops {\\n            abbr\\n            distanceInKm\\n            duration\\n            durationIcon\\n            geoInfo {\\n              latitude\\n              longitude\\n              obfuscatedLat\\n              obfuscatedLong\\n            }\\n            images {\\n              urls {\\n                value\\n                key\\n              }\\n              id\\n            }\\n            landmarkId\\n            name\\n            typeId\\n            typeName\\n          }\\n          popularLandmarkNumber\\n          topPlaces {\\n            abbr\\n            distanceInKm\\n            duration\\n            durationIcon\\n            geoInfo {\\n              latitude\\n              longitude\\n              obfuscatedLat\\n              obfuscatedLong\\n            }\\n            images {\\n              urls {\\n                value\\n                key\\n              }\\n              id\\n            }\\n            landmarkId\\n            name\\n            typeId\\n            typeName\\n            landMarkGroup {\\n              name\\n              sortOrder\\n            }\\n          }\\n        }\\n        contentInformation(ContentInformationRequest: $ContentInformationRequest) {\\n          usefulInfoGroups {\\n            id\\n            usefulInfo {\\n              id\\n              description\\n            }\\n          }\\n          certificate {\\n            name\\n            imageUrl\\n            description\\n          }\\n          staffVaccinationInfo {\\n            details\\n            status\\n          }\\n          messaging {\\n            responsiveRate\\n            isAllowedPreBooking\\n          }\\n          description {\\n            short\\n          }\\n          notes {\\n            criticalNotes\\n          }\\n          sustainabilityInfo {\\n            isSustainableTravel\\n            practiceCategories {\\n              categoryId\\n              categoryName\\n              practices {\\n                practiceId\\n                practiceName\\n              }\\n            }\\n          }\\n        }\\n        contentFeatures(ContentFeaturesRequest: $ContentFeaturesRequest) {\\n          featureGroups {\\n            features {\\n              available\\n              featureName\\n              featureNameLocalizationList {\\n                locale\\n                value\\n              }\\n              id\\n              order\\n              symbol\\n              images {\\n                id\\n                urls {\\n                  key\\n                  value\\n                }\\n                groupId\\n                groupEntityId\\n                typeId\\n                uploadedDate\\n                providerId\\n                caption\\n                highResolutionSizes\\n              }\\n            }\\n            id\\n            name\\n            order\\n            symbol\\n          }\\n          hotelFacilities {\\n            id\\n            name\\n          }\\n          summary {\\n            chineseFriendly\\n            staycationFacilityIds {\\n              activities\\n              drinkingAndDining\\n              sportAndEntertainment\\n              wellness\\n            }\\n            hygienePlusFacilities {\\n              healthAndMedical\\n              safetyFeature\\n              preventiveEquipment\\n            }\\n          }\\n          facilityHighlights {\\n            facilityId\\n            facilityName\\n            images {\\n              id\\n              urls {\\n                key\\n                value\\n              }\\n              groupId\\n              groupEntityId\\n              typeId\\n              uploadedDate\\n              providerId\\n              caption\\n              highResolutionSizes\\n            }\\n          }\\n        }\\n        hostProfile {\\n          displayName\\n          picture\\n          averageReviewScore\\n          totalReviews\\n          hostLevel\\n          responseRate\\n          responseTimeSeconds\\n          properties {\\n            id\\n            bookings\\n            reviewAvg\\n            reviewCount\\n          }\\n          userId\\n        }\\n      }\\n      metaLab(PriceStreamMetaLabRequest: $PriceStreamMetaLabRequest) {\\n        propertyAttributes {\\n          attributeId\\n          dataType\\n          value\\n          version\\n        }\\n      }\\n    }\\n  }\\n}\\n"}'
#response = requests.post('https://www.agoda.com/graphql/property', cookies=cookies, headers=headers, data=data)

