import os
import asyncio

from dotenv import load_dotenv
from requests import Session, Response
from time import time
from concurrent.futures import ThreadPoolExecutor
from aiohttp import ClientSession
from click import style
from typing import final

from src.helpers import Iostream, Datetime, ConnectionS3

load_dotenv()

class BaseGlassDoor:
    def __init__(self, **kwargs) -> None:
        self.__s3: bool = kwargs.get('s3') 
        self.__clean: bool = kwargs.get('clean')
        self.__requests: Session = Session()
        self.__requests.headers.update({
            'cookie': os.getenv('COOKIE_GLASSDOOR'),
            'gd-csrf-token': os.getenv('CSRF_TOKEN_GLASSDOOR'),
            'user-agent': 'Mozilla/5.0 (Linux; Android 9; Pixel 2 Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/121.0.6167.101 Mobile Safari/537.36',
        })
    
    @final
    async def __process_review(self, data_final: dict, paths: list, log: dict, data: dict, review_detail: dict) -> None:
        try:
            with ThreadPoolExecutor() as executor:
                data_final: dict = Iostream.dict_to_deep(data_final)
                try:
                    if(self.__s3):
                        executor.map(lambda path: ConnectionS3.upload(data_final, path), paths)
                    else:
                        executor.map(lambda path: Iostream.write_json(data_final, path), paths)
                except Exception as e:
                    raise e
                
            Iostream.info_log(log, review_detail["reviewId"], 'success', name=__name__)
                
            log['total_success'] += 1
            Iostream.update_log(log, name=__name__)
        
        except Exception as e:
            Iostream.info_log(log, review_detail["reviewId"], 'failed', error=e, name=__name__)

            log['total_failed'] += 1
            Iostream.update_log(log, name=__name__)
    
    @final
    def __requests_graphql(self, body: dict) -> Response:
        return self.__requests.post('https://www.glassdoor.com/graph', json=body)

    @final
    async def __get_reviews(self, employer_id: int, page: int) -> tuple:
        async with ClientSession() as session:
            async with session.post('https://www.glassdoor.com/graph',
                                    headers={
                                        'cookie': os.getenv('COOKIE_GLASSDOOR'),
                                        'gd-csrf-token': os.getenv('CSRF_TOKEN_GLASSDOOR'),
                                        'user-agent': 'Mozilla/5.0 (Linux; Android 9; Pixel 2 Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/121.0.6167.101 Mobile Safari/537.36',
                                    },
                                    json={
                                        "operationName": "EIReviewsPageGraphQueryRG",
                                        "variables": {
                                        "onlyCurrentEmployees": False,
                                        "employerId": employer_id,
                                        "jobTitle": None,
                                        "location": {
                                            "countryId": None,
                                            "stateId": None,
                                            "metroId": None,
                                            "cityId": None
                                        },
                                        "employmentStatuses": [],
                                        "goc": None,
                                        "highlight": None,
                                        "page": page,
                                        "sort": "RELEVANCE",
                                        "applyDefaultCriteria": True,
                                        "worldwideFilter": False,
                                        "language": "eng",
                                        "preferredTldId": 0,
                                        "dynamicProfileId": 4505142,
                                        "useRowProfileTldForRatings": True
                                        },
                                        "query": "query EIReviewsPageGraphQueryRG($onlyCurrentEmployees: Boolean, $employerId: Int!, $jobTitle: JobTitleIdent, $location: LocationIdent, $employmentStatuses: [EmploymentStatusEnum], $goc: GOCIdent, $highlight: HighlightTerm, $page: Int!, $sort: ReviewsSortOrderEnum, $applyDefaultCriteria: Boolean, $worldwideFilter: Boolean, $language: String, $preferredTldId: Int, $isRowProfileEnabled: Boolean, $dynamicProfileId: Int, $useRowProfileTldForRatings: Boolean) {\n  employerReviews: employerReviewsRG(\n    employerReviewsInput: {onlyCurrentEmployees: $onlyCurrentEmployees, employer: {id: $employerId}, jobTitle: $jobTitle, location: $location, goc: $goc, employmentStatuses: $employmentStatuses, highlight: $highlight, sort: $sort, page: {num: $page, size: 1000}, applyDefaultCriteria: $applyDefaultCriteria, worldwideFilter: $worldwideFilter, language: $language, preferredTldId: $preferredTldId, isRowProfileEnabled: $isRowProfileEnabled, dynamicProfileId: $dynamicProfileId, useRowProfileTldForRatings: $useRowProfileTldForRatings}\n  ) {\n    filteredReviewsCountByLang {\n      count\n      isoLanguage\n      __typename\n    }\n    employer {\n      legalActionBadges {\n        id\n        headerText\n        bodyText\n        __typename\n      }\n      bestPlacesToWork(onlyCurrent: true) {\n        bannerImageUrl\n        id\n        isCurrent\n        timePeriod\n        __typename\n      }\n      bestProfile {\n        id\n        __typename\n      }\n      ceo {\n        id\n        name\n        __typename\n      }\n      employerManagedContent(\n        parameters: [{employerId: $employerId, divisionProfileId: $dynamicProfileId}]\n      ) {\n        isContentPaidForTld\n        __typename\n      }\n      id\n      largeLogoUrl: squareLogoUrl(size: LARGE)\n      links {\n        jobsUrl\n        reviewsUrl\n        faqUrl\n        __typename\n      }\n      regularLogoUrl: squareLogoUrl(size: REGULAR)\n      shortName\n      squareLogoUrl\n      website\n      __typename\n    }\n    queryLocation {\n      id\n      type\n      shortName\n      longName\n      __typename\n    }\n    queryJobTitle {\n      id\n      text\n      __typename\n    }\n    currentPage\n    numberOfPages\n    lastReviewDateTime\n    allReviewsCount\n    ratedReviewsCount\n    filteredReviewsCount\n    ratings {\n      overallRating\n      reviewCount\n      ceoRating\n      recommendToFriendRating\n      cultureAndValuesRating\n      diversityAndInclusionRating\n      careerOpportunitiesRating\n      workLifeBalanceRating\n      seniorManagementRating\n      compensationAndBenefitsRating\n      businessOutlookRating\n      ceoRatingsCount\n      ratedCeo {\n        id\n        name\n        title\n        regularPhoto: photoUrl(size: REGULAR)\n        largePhoto: photoUrl(size: LARGE)\n        currentBestCeoAward {\n          displayName\n          timePeriod\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    reviews {\n      isLegal\n      reviewId\n      reviewDateTime\n      ratingOverall\n      ratingCeo\n      ratingBusinessOutlook\n      ratingWorkLifeBalance\n      ratingCultureAndValues\n      ratingDiversityAndInclusion\n      ratingSeniorLeadership\n      ratingRecommendToFriend\n      ratingCareerOpportunities\n      ratingCompensationAndBenefits\n      employer {\n        id\n        shortName\n        regularLogoUrl: squareLogoUrl(size: REGULAR)\n        largeLogoUrl: squareLogoUrl(size: LARGE)\n        __typename\n      }\n      isCurrentJob\n      lengthOfEmployment\n      employmentStatus\n      jobEndingYear\n      jobTitle {\n        id\n        text\n        __typename\n      }\n      location {\n        id\n        type\n        name\n        __typename\n      }\n      originalLanguageId\n      pros\n      prosOriginal\n      cons\n      consOriginal\n      summary\n      summaryOriginal\n      advice\n      adviceOriginal\n      isLanguageMismatch\n      countHelpful\n      countNotHelpful\n      employerResponses {\n        id\n        response\n        userJobTitle\n        responseDateTime(format: ISO)\n        countHelpful\n        countNotHelpful\n        responseOriginal\n        languageId\n        originalLanguageId\n        translationMethod\n        __typename\n      }\n      featured\n      isCovid19\n      topLevelDomainId\n      languageId\n      translationMethod\n      __typename\n    }\n    ratingCountDistribution {\n      overall {\n        _5\n        _4\n        _3\n        _2\n        _1\n        __typename\n      }\n      cultureAndValues {\n        _5\n        _4\n        _3\n        _2\n        _1\n        __typename\n      }\n      careerOpportunities {\n        _5\n        _4\n        _3\n        _2\n        _1\n        __typename\n      }\n      workLifeBalance {\n        _5\n        _4\n        _3\n        _2\n        _1\n        __typename\n      }\n      seniorManagement {\n        _5\n        _4\n        _3\n        _2\n        _1\n        __typename\n      }\n      compensationAndBenefits {\n        _5\n        _4\n        _3\n        _2\n        _1\n        __typename\n      }\n      diversityAndInclusion {\n        _5\n        _4\n        _3\n        _2\n        _1\n        __typename\n      }\n      recommendToFriend {\n        WONT_RECOMMEND\n        RECOMMEND\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  pageViewSummary {\n    totalCount\n    __typename\n  }\n  reviewLocationsV2(employer: {id: $employerId}) {\n    locations {\n      atlasType\n      id\n      name\n      __typename\n    }\n    employerHQLocation {\n      atlasType\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n}\n"
                                    }) as response:
                    
                    response_json: dict = await response.json()
                    data: dict = response_json['data']['employerReviews']
                    
                    reviews: list = data['reviews']

                    del data['reviews']

                    return (data, reviews)
    
    @final
    def __get_employers(self, page: int) -> list:
        response: Response = self.__requests_graphql({
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
                'pageRequested': page,
                'preferredTldId': 1,
                'sGocIds': [],
                'sectors': [],
            },
            'query': 'query ExplorerEmployerSearchGraphQuery($employerSearchRangeFilters: [EmployerSearchRangeFilter], $industries: [IndustryIdent], $jobTitle: String, $location: UgcSearchV2LocationIdent, $pageRequested: Int, $preferredTldId: Int, $sGocIds: [Int], $sectors: [SectorIdent]) {\n  employerSearchV2(\n    employerSearchRangeFilters: $employerSearchRangeFilters\n    industries: $industries\n    jobTitle: $jobTitle\n    location: $location\n    pageRequested: $pageRequested\n    preferredTldId: $preferredTldId\n    sGocIds: $sGocIds\n    sectors: $sectors\n  ) {\n    employerResults {\n      demographicRatings {\n        category\n        categoryRatings {\n          categoryValue\n          ratings {\n            overallRating\n            __typename\n          }\n          __typename\n        }\n      }\n      employer {\n        bestProfile {\n          id\n          __typename\n        }\n        id\n        shortName\n        ratings {\n          overallRating\n          careerOpportunitiesRating\n          compensationAndBenefitsRating\n          cultureAndValuesRating\n          diversityAndInclusionRating\n          seniorManagementRating\n          workLifeBalanceRating\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    numOfPagesAvailable\n    numOfRecordsAvailable\n    __typename\n  }\n}\n',
        })
        
        return [employer['employer'] for employer in response.json()['data']['employerSearchV2']['employerResults']]

    
    @final
    async def _get_detail_by_employer_id(self, employer_id: int) -> dict:
        async with ClientSession() as session:
            async with session.post('https://www.glassdoor.com/graph',
                                headers={
                                    'cookie': os.getenv('COOKIE_GLASSDOOR'),
                                    'gd-csrf-token': os.getenv('CSRF_TOKEN_GLASSDOOR'),
                                    'user-agent': 'Mozilla/5.0 (Linux; Android 9; Pixel 2 Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/121.0.6167.101 Mobile Safari/537.36',
                                },
                                json={
                                    'operationName': 'EmployerBaseDataQuery',
                                    'variables': {
                                        'employerId': employer_id,
                                        'isLoggedIn': True,
                                        'isROWProfile': False,
                                    },
                                    'query': 'query EmployerBaseDataQuery($employerId: Int!, $isLoggedIn: Boolean!, $isROWProfile: Boolean!) {\n  employer(id: $employerId) {\n    id\n    shortName\n    website(useRow: $isROWProfile)\n    type\n    revenue(useRow: $isROWProfile)\n    headquarters(useRow: $isROWProfile)\n    size(useRow: $isROWProfile)\n    stock\n    squareLogoUrl(size: SMALL)\n    officeAddresses {\n      id\n      __typename\n    }\n    primaryIndustry {\n      industryId\n      industryName\n      sectorId\n      __typename\n    }\n    yearFounded\n    overview {\n      description\n      mission\n      __typename\n    }\n    links {\n      manageoLinkData {\n        url\n        urlText\n        \nemployerSpecificText\n        __typename\n      }\n      overviewUrl\n      faqUrl\n      \n      __typename\n    }\n    bestPlacesToWorkAwards: bestPlacesToWork(onlyCurrent: false, limit: 30) {\n      id\n      name\n      rank\n      timePeriod\n      __typename\n    }\n    legalActionBadges {\n      headerText\n      bodyText\n      __typename\n    }\n    competitors {\n      shortName\n      __typename\n    }\n    __typename\n  }\n  getCompanyFollowsForUser @include(if: $isLoggedIn) {\n    employer {\n      id\n      __typename\n    }\n    follow\n    __typename\n  }\n}\n',
                                }) as response:
                
                response_json: dict = await response.json()
                data: dict = response_json['data']['employer']

                link: str = f'https://www.glassdoor.com{data["links"]["overviewUrl"]}'
                link_split: list = link.split('/')

                headers: dict = {
                    "link": link,
                    "domain": link_split[2],
                    "tag": link_split[2:],
                    "crawling_time": Datetime.now(),
                    "crawling_time_epoch": int(time()),
                    'employer_detail': data,
                    'category_reviews': 'Data review perusahaan',
                    "path_data_raw": f'S3://ai-pipeline-statistics/data/data_raw/data_review/glassdoor/{data["shortName"]}/json/detail.json',
                    "path_data_clean": f'S3://ai-pipeline-statistics/data/data_clean/data_review/glassdoor/{data["shortName"]}/json/detail.json',
                }

                paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [headers["path_data_raw"]]] 
                if self.__clean:
                    paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [headers["path_data_raw"], headers["path_data_clean"]]] 

                with ThreadPoolExecutor() as executor:
                    headers: dict = Iostream.dict_to_deep(headers)
                    try:
                        if(self.__s3):
                            executor.map(lambda path: ConnectionS3.upload(headers, path), paths)
                        else:
                            executor.map(lambda path: Iostream.write_json(headers, path), paths)
                    except Exception as e:
                        raise e
                
                log: dict = {
                    "Crawlling_time": Datetime.now(),
                    "id_project": None,
                    "project": "Data Intelligence",
                    "sub_project": "data review",
                    "source_name": headers['domain'],
                    "sub_source_name": data["shortName"],
                    "id_sub_source": str(employer_id),
                    "total_data": 0,
                    "total_success": 0,
                    "total_failed": 0,
                    "status": "Process",
                    "assign": "romy",
                }
                Iostream.write_log(log, name=__name__)
                
                (page, sum) = (1, 0)
                while(True):
                    (employer_detail, reviews) = await self.__get_reviews(employer_id, page)

                    sum += len(reviews)
                    if(not log['total_data']): log['total_data'] = employer_detail['filteredReviewsCount']

                    for review_detail in reviews:
                        data_final: dict ={
                            **headers,
                            'employer_detail': {
                                **data, **employer_detail 
                            },
                            'review_detail': review_detail,
                            "path_data_raw": f'S3://ai-pipeline-statistics/data/data_raw/data_review/glassdoor/{data["shortName"]}/json/data_review/{review_detail["reviewId"]}.json',
                            "path_data_clean": f'S3://ai-pipeline-statistics/data/data_clean/data_review/glassdoor/{data["shortName"]}/json/data_review/{review_detail["reviewId"]}.json',
                        } 

                        paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data_final["path_data_raw"]]] 
                        if self.__clean:
                            paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data_final["path_data_raw"], data_final["path_data_clean"]]] 
                        
                        await self.__process_review(data_final, paths, log, data, review_detail)

                    if(sum == employer_detail['filteredReviewsCount']): break
                    page += 1

                log['status'] = 'Done'
                Iostream.update_log(log, name=__name__)

    @final
    async def _get_detail_by_page(self, page: int) -> bool: 
        employers: list = self.__get_employers(page)
        if(not employers): return False
        for employer in employers:
            await self._get_detail_by_employer_id(employer['id'])
        return True

    @final
    async def _get_all_detail(self) -> None:
        page: int = 1
        while(True):
            success: bool = await self._get_detail_by_page(page)

            if(not success): break

            page += 1

if(__name__ == '__main__'):
    glassdoor: BaseGlassDoor = BaseGlassDoor()
    glassdoor._get_detail_by_employer_id(1050335)
    # glassdoor._get_all_detail(1)
