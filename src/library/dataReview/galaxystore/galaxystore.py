import xmltodict

from requests import Response, Session 
from json import dumps
from time import time

from src.helpers import Datetime

bodies = [
  """<?xml version="1.0" encoding="UTF-8"?><SamsungProtocol networkType="0" version2="0" lang="EN" openApiVersion="28" deviceModel="SM-G998B" storeFilter="themeDeviceModel=SM-G998B_TM||OTFVersion=8000000||gearDeviceModel=SM-G998B_SM-R800||gOSVersion=4.0.0" mcc="450" mnc="00" csc="CPW" odcVersion="4.5.21.6" version="6.5" filter="1" odcType="01" systemId="1604973510099" sessionId="10a4ee19e202011101104" logId="XXX" userMode="0">
    <request name="normalCategoryList" id="2225" numParam="4" transactionId="10a4ee19e011">
      <param name="needKidsCategoryYN">Y</param>
      <param name="imgWidth">135</param>
      <param name="imgHeight">135</param>
      <param name="upLevelCategoryKeyword">Games</param>
    </request>
  </SamsungProtocol>""",
  """<?xml version="1.0" encoding="UTF-8"?><SamsungProtocol networkType="0" version2="0" lang="EN" openApiVersion="28" deviceModel="SM-G998B" storeFilter="themeDeviceModel=SM-G998B_TM||OTFVersion=8000000||gearDeviceModel=SM-G998B_SM-R800||gOSVersion=4.0.0" mcc="450" mnc="00" csc="CPW" odcVersion="4.5.21.6" version="6.5" filter="1" odcType="01" systemId="1604973510099" sessionId="10a4ee19e202011101104" logId="XXX" userMode="0">
    <request name="normalCategoryList" id="2225" numParam="4" transactionId="10a4ee19e011">
        <param name="needKidsCategoryYN">Y</param>
        <param name="imgWidth">135</param>
        <param name="imgHeight">135</param>
        <param name="gameCateYN">N</param>
    </request>
    </SamsungProtocol>"""
]

class BaseGalaxystore:
    def __init__(self) -> None:
        self.__requests: Session = Session()
        self.__requests.headers.update({
            "Content-Type": "application/xml",
            "X-country-channel-code": "id-odc",
        })

    def __get_reviews_by_start(self, content_id: str, start: int) -> list | None:
        response: Response = self.__requests.get(f'https://galaxystore.samsung.com/api/commentList/contentId={content_id}&startNum={start}')

        response_json: dict = response.json()

        if(not response_json['commentList']): return

        return response_json['commentList']

    def __get_games_by_category(self, category_name: str, category_id: str) -> list:
        response: Response = self.__requests.post("https://galaxystore.samsung.com/storeserver/ods.as?id=categoryProductList2Notc",
                                                    data=f"""<?xml version="1.0" encoding="UTF-8"?>
                                                            <SamsungProtocol networkType="0" version2="0" lang="EN" openApiVersion="28" deviceModel="SM-G998B" storeFilter="themeDeviceModel=SM-G998B_TM||OTFVersion=8000000||gearDeviceModel=SM-G998B_SM-R800||gOSVersion=4.0.0" mcc="310" mnc="03" csc="MWD" odcVersion="9.9.30.9" version="6.5" filter="1" odcType="01" systemId="1604973510099" sessionId="10a4ee19e202011101104" logId="XXX" userMode="0">   
                                                                <request name="categoryProductList2Notc" id="2030" numParam="10" transactionId="10a4ee19e126"> 
                                                                    <param name="imgWidth">135</param>
                                                                    <param name="startNum">1</param>
                                                                    <param name="imgHeight">135</param>
                                                                    <param name="alignOrder">bestselling</param>
                                                                    <param name="contentType">All</param>
                                                                    <param name="endNum">500</param>
                                                                    <param name="categoryName">{category_name}</param>
                                                                    <param name="categoryID">{category_id}</param>
                                                                    <param name="srcType">01</param>
                                                                    <param name="status">0</param>
                                                                </request>
                                                            </SamsungProtocol>""")
        response_json: dict = xmltodict.parse(response.text)
        games: list = [e['value'][17]['#text'] for e in response_json['SamsungProtocol']['response']['list']]

        return games 
    
    def __get_detail_by_game_id(self, game_id: str) -> None:
        response: Response = self.__requests.get(f'https://galaxystore.samsung.com/api/detail/{game_id}')
        response_json: dict = response.json()

        if('errCode' in response_json): return False

        (detail_main, app_id, screenshot, seller_info, comment_list_total_count) = (response_json['DetailMain'], response_json['appId'], response_json['Screenshot'], response_json['SellerInfo'], response_json['commentListTotalCount'])

        link: str = f'https://galaxystore.samsung.com/detail/{app_id}'
        link_split: list = link.split('/')

        log: dict = {
                'Crawlling_time': Datetime.now(),
                'id_project': None,
                'project': "Data Intelligence",
                'sub_project': "data review",
                'source_name': link_split[2],
                'sub_source_name': detail_main['contentName'],
                'id_sub_source': app_id,
                'total_data': 0,
                'total_success': 0,
                'total_failed': 0,
                'status': "Process",
                'assign': "romy",
        }

        headers: dict = {

            'link': link,
            'domain': link_split[2],
            'tag': link_split[2:],
            'crawling_time': Datetime.now(),
            'crawling_time_epoch': int(time()),
            'reviews_name': detail_main['contentName'],
            'description_reviews': detail_main['contentDescription'],
            'description_new_reviews': detail_main['contentNewDescription'],
            'publisher_reviews': detail_main['sellerName'],
            'publisher_info_reviews': {
                'seller_trade_name': seller_info['sellerTradeName'],
                'representation': seller_info['representation'],
                'seller_site': seller_info['sellerSite'],
                'first_name': seller_info['firstName'],
                'last_name': seller_info['lastName'],
                'seller_number': seller_info['sellerNumber'],
                'first_seller_address': seller_info['firstSellerAddress'],
                'second_seller_address': seller_info['secondSellerAddress'],
                'registration_number': seller_info['registrationNumber'],
                'report_number': seller_info['reportNumber'],
            },
            'limit_age_reviews': int(detail_main['limitAgeCd']),
            'size_in_mb_reviews': float(detail_main['contentBinarySize'].replace(" MB", "")),
            'content_binary_version_reviews': detail_main['contentBinaryVersion'],
            'local_price_rp_reviews': int(detail_main['localPrice'].replace("Rp", "").replace(",", "")),
            'permissions_required_reviews': detail_main['permissionList'],
            'screenshots_reviews': [ss['originalScrnShtUrl'] for ss in screenshot['scrnShtUrlList']],
            'location_reviews': None,
            'category_reviews': "application",
            'total_reviews': int(comment_list_total_count),
            'reviews_rating': {
            'total_rating': float(detail_main['ratingNumber']),
            'detail_total_rating': None,
            },
            'path_data_raw': 'S3://ai-pipeline-statistics/data/data_raw/data_review/galaxystore_samsung/${title}/json/detail.json',
            'path_data_clean': 'S3://ai-pipeline-statistics/data/data_clean/data_review/galaxystore_samsung/${title}/json/detail.json',
        }
        
        start: int = 1
        while(reviews := self.__get_reviews_by_start(detail_main['contentId'], start)):
            if(not reviews): break
            log['total_data'] += len(reviews)
            start += 15

    def __get_by_body(self, body: str) -> None:
        response: Response = self.__requests.post('https://galaxystore.samsung.com/storeserver/ods.as?id=normalCategoryList', data=body)
        
        response_json: dict = xmltodict.parse(response.text)
        categories = [[e['value'][2]['#text'], e['value'][0]['#text']] for e in response_json['SamsungProtocol']['response']['list']]

        for category in categories:
            game_ids: list = self.__get_games_by_category(*category)
            self.__get_detail_by_game_id(game_ids[0])
            break

    
    def start(self):
        self.__get_by_body(bodies[0])
        

if(__name__ == '__main__'):
    baseGalaxystore: BaseGalaxystore = BaseGalaxystore()
    baseGalaxystore.start()