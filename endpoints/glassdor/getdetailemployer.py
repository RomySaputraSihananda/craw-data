import requests
import os
from dotenv import load_dotenv
load_dotenv()
headers = {
    # 'authority': 'www.glassdoor.com',
    # 'accept': '*/*',
    # 'accept-language': 'en-US,en;q=0.9',
    # 'apollographql-client-name': 'company.explorer',
    # 'apollographql-client-version': '3.20.8',
    # 'content-type': 'application/json',
    'cookie': os.getenv('COOKIE_GLASSDOOR'),
    'gd-csrf-token': 'VSd4dewZtsI0joOi2jZRtg:umzE8PaSomTHQ2ssaFVGp_VEFa1OEK0mIpz373zTu3-178ZNe7VgBGK7WO82bMMtJveDbtdyP7f-tApX1pnF0Q:cTncOac90ti8Q_JD27WKG2scZF9Q5_I9ZQ6FjjiAlDM',
    # 'origin': 'https://www.glassdoor.com',
    # 'referer': 'https://www.glassdoor.com/',
    # 'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    # 'sec-ch-ua-arch': '"x86"',
    # 'sec-ch-ua-bitness': '"64"',
    # 'sec-ch-ua-full-version': '"120.0.6099.109"',
    # 'sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.109", "Google Chrome";v="120.0.6099.109"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-model': '""',
    # 'sec-ch-ua-platform': '"Linux"',
    # 'sec-ch-ua-platform-version': '"6.5.8"',
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

json_data = [
    {
        'operationName': 'EmployerBaseDataQuery',
        'variables': {
            'employerId': 9079,
            'isLoggedIn': True,
            'isROWProfile': False,
        },
        'query': 'query EmployerBaseDataQuery($employerId: Int!, $isLoggedIn: Boolean!, $isROWProfile: Boolean!) {\n  employer(id: $employerId) {\n    id\n    shortName\n    website(useRow: $isROWProfile)\n    type\n    revenue(useRow: $isROWProfile)\n    headquarters(useRow: $isROWProfile)\n    size(useRow: $isROWProfile)\n    stock\n    squareLogoUrl(size: SMALL)\n    officeAddresses {\n      id\n      __typename\n    }\n    primaryIndustry {\n      industryId\n      industryName\n      sectorId\n      __typename\n    }\n    yearFounded\n    overview {\n      description\n      mission\n      __typename\n    }\n    links {\n      manageoLinkData {\n        url\n        urlText\n        employerSpecificText\n        __typename\n      }\n      faqUrl\n      __typename\n    }\n    bestPlacesToWorkAwards: bestPlacesToWork(onlyCurrent: false, limit: 30) {\n      id\n      name\n      rank\n      timePeriod\n      __typename\n    }\n    legalActionBadges {\n      headerText\n      bodyText\n      __typename\n    }\n    competitors {\n      shortName\n      __typename\n    }\n    __typename\n  }\n  getCompanyFollowsForUser @include(if: $isLoggedIn) {\n    employer {\n      id\n      __typename\n    }\n    follow\n    __typename\n  }\n}\n',
    },
    {
        'operationName': 'RecordPageView',
        'variables': {
            'employerId': '9079',
            'pageIdent': 'INFOSITE_OVERVIEW',
        },
        'query': 'mutation RecordPageView($employerId: String!, $pageIdent: String!) {\n  recordPageView(\n    pageIdent: $pageIdent\n    metaData: {key: "employerId", value: $employerId}\n  ) {\n    totalCount\n    __typename\n  }\n}\n',
    },
]


from json import dumps

response = requests.post('https://www.glassdoor.com/graph', headers=headers, json=json_data)
print(dumps(response.json(), indent=4))
