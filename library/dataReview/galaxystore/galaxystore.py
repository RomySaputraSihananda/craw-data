import xmltodict

from requests import Response, Session 
from json import dumps
from helpers import Parser, Datetime, Iostream, ConnectionS3, logging

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
        link: str = f'https://galaxystore.samsung.com/detail/{response_json["appId"]}'
        link_split: list = link.split('/')
        log: dict = {
                'Crawlling_time': Datetime.now(),
                'id_project': None,
                'project': "Data Intelligence",
                'sub_project': "data review",
                'source_name': link_split[2],
                'sub_source_name': DetailMain['contentName'],
                'id_sub_source': response_json["appId"],
                'total_data': len(reviews),
                'total_success': 0,
                'total_failed': 0,
                'status': "Process",
                'assign': "romy",
        }


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