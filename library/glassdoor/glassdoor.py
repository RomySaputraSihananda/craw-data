import os

from dotenv import load_dotenv
from requests import Session, Response

load_dotenv()

class BaseGlassDoor:
    def __init__(self) -> None:
        self.__requests: Session = Session()
        self.__requests.headers.update({
            'cookie': os.getenv('COOKIE_GLASSDOOR'),
            'gd-csrf-token': os.getenv('CSRF_TOKEN_GLASSDOOR'),
            'user-agent': 'Mozilla/5.0 (Linux; Android 9; Pixel 2 Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/121.0.6167.101 Mobile Safari/537.36',
        })

    def _get_detail_by_employer_id(self, employer_id: int) -> None:
        response: Response = self.__requests.post('https://www.glassdoor.com/graph', 
                                                 json=[
                                                        {
                                                            'operationName': 'EmployerBaseDataQuery',
                                                            'variables': {
                                                                'employerId': employer_id,
                                                                'isLoggedIn': True,
                                                                'isROWProfile': False,
                                                            },
                                                            'query': 'query EmployerBaseDataQuery($employerId: Int!, $isLoggedIn: Boolean!, $isROWProfile: Boolean!) {\n  employer(id: $employerId) {\n    id\n    shortName\n    website(useRow: $isROWProfile)\n    type\n    revenue(useRow: $isROWProfile)\n    headquarters(useRow: $isROWProfile)\n    size(useRow: $isROWProfile)\n    stock\n    squareLogoUrl(size: SMALL)\n    officeAddresses {\n      id\n      __typename\n    }\n    primaryIndustry {\n      industryId\n      industryName\n      sectorId\n      __typename\n    }\n    yearFounded\n    overview {\n      description\n      mission\n      __typename\n    }\n    links {\n      manageoLinkData {\n        url\n        urlText\n        employerSpecificText\n        __typename\n      }\n      faqUrl\n      __typename\n    }\n    bestPlacesToWorkAwards: bestPlacesToWork(onlyCurrent: false, limit: 30) {\n      id\n      name\n      rank\n      timePeriod\n      __typename\n    }\n    legalActionBadges {\n      headerText\n      bodyText\n      __typename\n    }\n    competitors {\n      shortName\n      __typename\n    }\n    __typename\n  }\n  getCompanyFollowsForUser @include(if: $isLoggedIn) {\n    employer {\n      id\n      __typename\n    }\n    follow\n    __typename\n  }\n}\n',
                                                        },
                                                        {
                                                            'operationName': 'RecordPageView',
                                                            'variables': {
                                                                'employerId': employer_id,
                                                                'pageIdent': 'INFOSITE_OVERVIEW',
                                                            },
                                                            'query': 'mutation RecordPageView($employerId: String!, $pageIdent: String!) {\n  recordPageView(\n    pageIdent: $pageIdent\n    metaData: {key: "employerId", value: $employerId}\n  ) {\n    totalCount\n    __typename\n  }\n}\n',
                                                        },
                                                    ])
        print(response)

if(__name__ == '__main__'):
    glassdoor: BaseGlassDoor = BaseGlassDoor()
    glassdoor._get_detail_by_employer_id(466601)
