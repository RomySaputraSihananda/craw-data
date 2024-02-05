import requests
import os
from dotenv import load_dotenv

load_dotenv()
headers = {
    'authority': 'www.glassdoor.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'apollographql-client-name': 'company.explorer',
    'apollographql-client-version': '3.20.8',
    'content-type': 'application/json',
    'cookie': os.getenv('COOKIE_GLASSDOOR'),
    'gd-csrf-token': 'VSd4dewZtsI0joOi2jZRtg:umzE8PaSomTHQ2ssaFVGp_VEFa1OEK0mIpz373zTu3-178ZNe7VgBGK7WO82bMMtJveDbtdyP7f-tApX1pnF0Q:cTncOac90ti8Q_JD27WKG2scZF9Q5_I9ZQ6FjjiAlDM',
    'origin': 'https://www.glassdoor.com',
    'referer': 'https://www.glassdoor.com/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"120.0.6099.109"',
    'sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.109", "Google Chrome";v="120.0.6099.109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Linux"',
    'sec-ch-ua-platform-version': '"6.5.8"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

json_data = [
    {
        'operationName': 'ExplorerEmployerSearchGraphQuery',
        'variables': {
            'employerSearchRangeFilters': [
                {
                    'filterType': 'RATING_OVERALL',
                    'maxInclusive': 5,
                    'minInclusive': 3.5,
                },
            ],
            'industries': [],
            'jobTitle': '',
            'location': {
                'locationId': 2709872,
                'locationType': "C"
            },
            'pageRequested': 1,
            'preferredTldId': 1,
            'sGocIds': [],
            'sectors': [],
        },
        'query': 'query ExplorerEmployerSearchGraphQuery($employerSearchRangeFilters: [EmployerSearchRangeFilter], $industries: [IndustryIdent], $jobTitle: String, $location: UgcSearchV2LocationIdent, $pageRequested: Int, $preferredTldId: Int, $sGocIds: [Int], $sectors: [SectorIdent]) {\n  employerSearchV2(\n    employerSearchRangeFilters: $employerSearchRangeFilters\n    industries: $industries\n    jobTitle: $jobTitle\n    location: $location\n    pageRequested: $pageRequested\n    preferredTldId: $preferredTldId\n    sGocIds: $sGocIds\n    sectors: $sectors\n  ) {\n    employerResults {\n      demographicRatings {\n        category\n        categoryRatings {\n          categoryValue\n          ratings {\n            overallRating\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      employer {\n        bestProfile {\n          id\n          __typename\n        }\n        id\n        shortName\n        ratings {\n          overallRating\n          careerOpportunitiesRating\n          compensationAndBenefitsRating\n          cultureAndValuesRating\n          diversityAndInclusionRating\n          seniorManagementRating\n          workLifeBalanceRating\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    numOfPagesAvailable\n    numOfRecordsAvailable\n    __typename\n  }\n}\n',
    },
]

from json import dumps

response = requests.post('https://www.glassdoor.com/graph', headers=headers, json=json_data)
data = response.json()[0]['data']['employerSearchV2']['employerResults']

for i in data:
    print(i['employer']['shortName'], i['employer']['bestProfile']['id'])
