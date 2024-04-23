import re
import pandas
import requests

from requests import Response, Session
from json import dumps, loads
from time import time

from src.helpers import Iostream, Decorator, Datetime

class PusiknasPolri():
    def __init__(self) -> None: 
        self.__requests: Session = Session()
        self.__requests.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
        })

        (self.__session, self.__response) = self.__get_session()
        self.__keys: list = (data_columns := (data_segments := self.__response["secondaryInfo"]["presModelMap"]["dataDictionary"]["presModelHolder"]["genDataDictionaryPresModel"]["dataSegments"])[list(data_segments.keys())[0]]["dataColumns"])[1]["dataValues"]
        self.__values: list = data_columns[0]["dataValues"]

    def __process_data(self, response: dict) -> dict:
        try:
            keys: list = (data_columns := (data_segments := response["vqlCmdResponse"]["layoutStatus"]["applicationPresModel"]["dataDictionary"]["dataSegments"])[index := list(data_segments.keys())[0]]["dataColumns"])[1]["dataValues"]
            values: list = data_columns[0]["dataValues"]
        except Exception as e:
            raise e
        
        if(keys == self.__keys): raise Exception('samaaa')

        self.__keys.extend(keys)
        self.__values.extend(values)

        def to_int(x: str) -> int:
            try:
                return int(x.replace(',', '').split('.')[0])
            except Exception as e:
                raise e

        result: dict = {}
        for header in (response := response["vqlCmdResponse"]["layoutStatus"]["applicationPresModel"]["workbookPresModel"]["dashboardPresModel"]["zones"]):
            if("worksheet" in response[header]):
                if(not (name := response[header]["worksheet"]) in result):
                    result[name] = {}
            if("visual" in response[header]["presModelHolder"]):
                try:
                    if(len(response[header]["presModelHolder"]["visual"]["vizData"]["paneColumnsData"]["paneColumnsList"]) < 2):
                            if(len((response[header]["presModelHolder"]["visual"]["vizData"]["paneColumnsData"]["paneColumnsList"][0]["vizPaneColumns"])) > 2):
                                for i, key in enumerate(
                                    response[header]["presModelHolder"]["visual"]["vizData"]["paneColumnsData"]["paneColumnsList"][0]["vizPaneColumns"][2]["valueIndices"]
                                ):
                                    try:
                                        result[name].update({
                                            self.__keys[key]: self.__values[response[header]["presModelHolder"]["visual"]["vizData"]["paneColumnsData"]["paneColumnsList"][0]["vizPaneColumns"][1]["valueIndices"][i]]
                                        })
                                    except Exception as e:
                                        raise e 
                            else:
                                index = response[header]["presModelHolder"]["visual"]["vizData"]["paneColumnsData"]["paneColumnsList"][0]["vizPaneColumns"][1]["aliasIndices"][0]
                                if(index > 0): 
                                    result[name] = self.__values[index]
                                else: 
                                    result[name] = to_int(self.__keys[-index - 1])
                    else:
                        for i, key in enumerate(
                                response[header]["presModelHolder"]["visual"]["vizData"]["paneColumnsData"]["paneColumnsList"][0]["vizPaneColumns"][2]["aliasIndices"]
                            ):
                                try:
                                    result[name].update({
                                        self.__keys[key]: to_int(self.__keys[-response[header]["presModelHolder"]["visual"]["vizData"]["paneColumnsData"]["paneColumnsList"][0]["vizPaneColumns"][3]["aliasIndices"][i] - 1])
                                    })
                                except Exception as e: 
                                    raise e 
                        result[name]['total'] = sum(result[name].values())
                except Exception as e:
                    raise e 

        return result

    def __get_ticket(self) -> str: 
        try:
            print('get ticket')
            response: Response = requests.get('https://pusiknas.polri.go.id/ticket', timeout=10)

            return response.json()['key']
        except:
            return self.__get_ticket()

    def __get_session(self) -> tuple:
        response: Response = self.__requests.get(f'https://pusiknas.polri.go.id/tableau/trusted/{self.__get_ticket()}/views/LakaLantas_16920924926570/STATISTIKALAKALANTAS?:iid=5&:embed=y&:showVizHome=n&:tabs=n&:toolbar=n&:apiID=host0#navType=1&navSrc=Parse')
        print('get session')
        response: Response = self.__requests.post(f'https://pusiknas.polri.go.id/vizql/w/LakaLantas_16920924926570/v/STATISTIKALAKALANTAS/bootstrapSession/sessions/{response.headers["X-Session-Id"]}',
                                                 params={
                                                    "worksheetPortSize":"{\"w\":938,\"h\":650}",
                                                    "dashboardPortSize":"{\"w\":938,\"h\":650}",
                                                    "clientDimension":"{\"w\":938,\"h\":650}",
                                                    "renderMapsClientSide":"true",
                                                    "isBrowserRendering":"true",
                                                    "browserRenderingThreshold":"100",
                                                    "formatDataValueLocally":"false",
                                                    "clientNum":"",
                                                    "navType":"Reload",
                                                    "navSrc":"Parse",
                                                    "devicePixelRatio":"1",
                                                    "clientRenderPixelLimit":"16000000",
                                                    "allowAutogenWorksheetPhoneLayouts":"false",
                                                    "sheet_id":"STATISTIKA%20LAKA%20LANTAS",
                                                    "showParams":"{\"checkpoint\":false,\"refresh\":false,\"refreshUnmodified\":false}",
                                                    "stickySessionKey":"{\"capabilities\":\"7f06f1f82610\",\"dataserverPermissions\":\"fe97e740beff3d5df248b0e467154b3238b1fea5883b933aafb36a6a6261a625\",\"featureFlags\":\"{}\",\"isAuthoring\":false,\"isOfflineMode\":false,\"lastUpdatedAt\":1713489696607,\"unknownParamsHash\":\"\",\"wgSession\":\"kSwjP6PDQmaIowt1pgyvXg\",\"workbookId\":272}",
                                                    "filterTileSize":"200",
                                                    "locale":"en_US",
                                                    "language":"en",
                                                    "verboseMode":"false",
                                                    ":session_feature_flags":"{}",
                                                    "keychain_version":"1"
                                                })
        
        return (response.headers["X-Session-Id"], loads("{" + re.split(r'}\d+;{', response.text)[-1]))

    def _get_by_range(self, **kwargs) -> None:
        print('get range')

        self.__requests.headers.update({
            'Content-Type': 'multipart/form-data; boundary=5qqwMSDC'
        })
        
        response = self.__requests.post(f'https://pusiknas.polri.go.id/vizql/w/LakaLantas_16920924926570/v/STATISTIKALAKALANTAS/sessions/{self.__session}/commands/tabdoc/range-filter',
                                        data="\r\n".join([
                                            "--5qqwMSDC",
                                            "Content-Disposition: form-data; name=\"worksheet\"",
                                            "",
                                            "Tipe Laka Lantas Polda New",
                                            "--5qqwMSDC",
                                            "Content-Disposition: form-data; name=\"dashboard\"",
                                            "",
                                            "STATISTIKA LAKA LANTAS",
                                            "--5qqwMSDC",
                                            "Content-Disposition: form-data; name=\"globalFieldName\"",
                                            "",
                                            "[sqlproxy.00w7op60fqsjlc1c75jn91dbpk22].[none:accident_date:qk]",
                                            "--5qqwMSDC",
                                            "Content-Disposition: form-data; name=\"filterRangeMin\"",
                                            "",
                                            Datetime.excel_serial_date(start_date := kwargs.get('start_date'), format='%m/%d/%Y'),
                                            "--5qqwMSDC",
                                            "Content-Disposition: form-data; name=\"filterRangeMax\"",
                                            "",
                                            Datetime.excel_serial_date(end_date, format='%m/%d/%Y') if (end_date := kwargs.get('end_date', None)) else (end_date_now := Datetime.excel_serial_date_now(format='%m/%d/%Y'))[0],
                                            "--5qqwMSDC",
                                            "Content-Disposition: form-data; name=\"included\"",
                                            "",
                                            "include-range",
                                            "--5qqwMSDC--",
                                            ""
                                        ]))
        
        link_split: list = (link := 'https://pusiknas.polri.go.id/laka_lantas').split('/')

        Iostream.write_json({
            "link": link,
            "domain": link_split[2],
            "tag": link_split[2:],
            "crawling_time": Datetime.now(),
            "crawling_time_epoch": int(time()),
            "date": start_date,
            "data": self.__process_data(response.json())
        }, f"header/{start_date.replace('/', '-')}.json", indent=4)

    def _get_by_date(self, date: str) -> None:
        return self._get_by_range(**{
            'start_date': date,
            'end_date': date
        })
    
def ok(**kwargs):
    for date in pandas.date_range(kwargs.get('start_date'), kwargs.get('end_date')).strftime('%d/%m/%Y'):
        for _ in range(5):
            try:
                PusiknasPolri()._get_by_date(date)
                break
            except:
                PusiknasPolri()._get_by_date(date)
            

if(__name__ == '__main__'):
    # PusiknasPolri()._get_by_range(**{
    #     'start_date': '21/4/2024' ,
    #     'end_date': '21/4/2024'
    # })

    # PusiknasPolri()._get_by_date('4/4/2024')
    
    ok(**{
        'start_date': '3/1/2024' ,
        'end_date': '4/1/2024'
    })