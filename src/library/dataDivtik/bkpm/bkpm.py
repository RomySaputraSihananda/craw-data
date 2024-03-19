from time import sleep
from json import loads
from time import time
from concurrent.futures import ThreadPoolExecutor

from seleniumwire.utils import decode
from seleniumwire.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.helpers import Iostream, Datetime, ConnectionS3

class Bkpm:
    def __init__(self, **kwargs) -> None:
        self.__s3: bool = kwargs.get('s3')
        self.__kafka: bool = kwargs.get('kafka')
        self.__clean: bool = kwargs.get('clean')

        self.__options: ChromeOptions = ChromeOptions()
        # self.__options.add_argument('--headless')
        self.__options.add_argument("--kiosk-printing")
        self.__options.add_argument("--disable-popup-blocking")
        self.__options.add_argument("--disable-notifications")
        self.__options.add_argument("--disable-web-security")
        self.__options.add_argument("--allow-running-insecure-content")
        self.__options.add_argument("--disable-save-password-bubble")
        self.__options.add_argument("--disable-extensions")

    @staticmethod
    def process_data(data) -> tuple:
        values: list = data['viewDataTablePagePresModel']['dataDictionary']['dataSegments']['0']['dataColumns'][0]['dataValues']
        page_info: dict = data['viewDataTablePagePresModel']['pageInfo']

        keys: list = [
            key | data['viewDataTablePagePresModel']['viewDataColumnValuesPresModels'][i] 
            for i, key in enumerate(data['underlyingDataTableColumns'])
        ]

        data = []
        for key in keys:
            for j, v in enumerate(key['formatValIdxs']):
                try:
                    data[j].update({
                        key['fieldCaption']: values[v] if v > 0 else None
                    })
                except:
                    data.append({
                        key['fieldCaption']: values[v] if v > 0 else None
                    })
        
        return (page_info, data)

    def __wait_element(self, selector: str, timeout: int = 10) -> WebElement:
        return WebDriverWait(self.__driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    
    def __wait_element_invisible(self, selector: str, timeout: int = 200) -> WebElement:
        return WebDriverWait(self.__driver, timeout).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))


    def __get_provs(self) -> list:
        try:
            self.__wait_element('#tableau_base_widget_LegacyCategoricalQuickFilter_1 > div > div.CFContent > span > div.tabComboBoxNameContainer.tab-ctrl-formatted-fixedsize', 10).click()
        except: ...

        return self.__driver.find_elements(By.CSS_SELECTOR, '.tileContainer div[role="listbox"] > div .facetOverflow')
    
    def __get_kabs(self) -> list:
        try:
            self.__wait_element('#tableau_base_widget_LegacyCategoricalQuickFilter_0 > div > div.CFContent > span > div.tabComboBoxNameContainer.tab-ctrl-formatted-fixedsize').click()
        except: ...
        
        return self.__driver.find_elements(By.CSS_SELECTOR, '#tableau_base_widget_LegacyCategoricalQuickFilter_0_menu > div.CFInnerContainer.tab-ctrl-formatted-text.tiledContent > div.tileContainer > div >  div .facetOverflow')
        
    def __click_downloads(self) -> tuple:
        sleep(1)
        self.__wait_element('#download').click()
        self.__wait_element('#viz-viewer-toolbar-download-menu > div:nth-of-type(2)').click()
        
        sleep(3)
        self.__wait_element('html > body > div:nth-of-type(7) > div > div > div > div > div:nth-of-type(3) > div > div > button').click()
        
        [ data ] = [request for request in self.__driver.requests if request.url.find('get-view-data-dialog-tab-pres-model') > 0]

        del self.__driver.requests

        return self.process_data(loads(decode(data.response.body, data.response.headers.get('Content-Encoding', 'identity')))['vqlCmdResponse']['cmdResultList'][0]['commandReturn']['viewDataDialogTabPresModel'])
    
    def start(self) -> None:
        self.__driver: Chrome = Chrome(options=self.__options)

        link: str = 'https://nswi.bkpm.go.id/tableau/show_eis?app_name=InvestasiPer Kabupaten/Kota&content_url=2018_12_DB-Desktop-Apps/DB-per-KABKOT'
        link_split: list = link.split('/')
        
        self.__driver.get(link)
        self.__driver.get('https://dashboard.bkpm.go.id/views/2018_12_DB-Desktop-Apps/DB-per-KABKOT/9977ec7c-858b-405a-951c-86a7ed74512c/2952c081-9824-4ee5-8951-e35d13a65bb4?%3Adisplay_count=n&%3AshowVizHome=n&%3Aorigin=viz_share_link&%3Aembed=y#1')


        for i in range(len(self.__get_provs())):
            try:
                provinsi_element: WebElement = self.__get_provs()[i]
                provinsi_name: str = provinsi_element.text.replace(' ', '_')

                provinsi_element.click()

                for j in range(len(self.__get_kabs())):
                    try:
                        kabupaten_element: WebElement = self.__get_kabs()[j]
                        kabupaten_name: str = kabupaten_element.text.replace(' ', '_')

                        kabupaten_element.click()

                        (page_info, detail_data) = self.__click_downloads()
                        
                        data: dict = {
                            'link': link,
                            'domain': link_split[2],
                            'crawling_time': Datetime.now(),
                            'crawling_time_epoch': int(time()),
                            'tag': [
                                'nswi',
                                'bkpm',
                                'Investasi Per Kabupaten / Kota', 
                                'tableau', 
                                'DB-per-KABKOT', 
                                '2018_12_DB-Desktop-Apps',
                                provinsi_name, 
                                kabupaten_name
                            ],
                            'page_info': page_info, 
                            'detail_data': detail_data,
                            'path_data_raw': f'S3://ai-pipeline-statistics/data/data_raw/Divtik/bkpm/{provinsi_name}/json/{kabupaten_name}.json', 
                            'path_data_clean': f'S3://ai-pipeline-statistics/data/data_clean/Divtik/bkpm/{provinsi_name}/json/{kabupaten_name}.json',   
                        }
                        paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"]]] 
                        
                        if(self.__clean):
                            paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"], data["path_data_clean"]]] 
                        
                        if(self.__kafka):
                            self.__connectionKafka.send(data, name=self.__bootstrap)

                        with ThreadPoolExecutor() as executor:
                            try:
                                if(self.__s3):
                                    executor.map(lambda path: ConnectionS3.upload(data, path), paths)
                                else:
                                    executor.map(lambda path: Iostream.write_json(data, path), paths)
                            except Exception as e:
                                raise e
                        
                        break
                    except Exception as e:
                        continue

                break
            except Exception as e:
                continue
        
        self.__driver.close()

if(__name__ == '__main__'):
    Bkpm(**{
        's3': True
    }).start()
    