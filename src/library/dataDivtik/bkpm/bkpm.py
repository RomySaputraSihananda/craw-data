import os

from time import sleep
from json import loads
from time import time
from concurrent.futures import ThreadPoolExecutor

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
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

    @staticmethod
    def options(output: str = '', **kwargs) -> Options:
        options: Options = Options()
        # if(kwargs.get('headless')): options.add_argument('--headless') 
        options.add_argument("--kiosk-printing")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-save-password-bubble")
        options.add_argument("--disable-extensions")
        options.add_experimental_option("prefs", {
            "savefile.default_directory": os.getcwd() + output,
            "download.default_directory": os.getcwd() + output,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            'profile.default_content_setting_values.automatic_downloads': 1
        })

        return options

    def __wait_element(self, selector: str, timeout: int = 10) -> WebElement:
        return WebDriverWait(self.__driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def __wait_elements(self, selector: str, timeout: int = 10) -> WebElement:
        return WebDriverWait(self.__driver, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
      
    def __wait_element_invisible(self, selector: str, timeout: int = 200) -> WebElement:
        return WebDriverWait(self.__driver, timeout).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))


    def __get_provs(self) -> list:
        sleep(1)
        try:
            self.__wait_element('#tableau_base_widget_LegacyCategoricalQuickFilter_1 > div > div.CFContent > span > div.tabComboBoxNameContainer.tab-ctrl-formatted-fixedsize', 10).click()
        except Exception as e: ...

        return self.__driver.find_elements(By.CSS_SELECTOR, '.tileContainer div[role="listbox"] > div .facetOverflow')
    
    def __get_kabs(self) -> list:
        sleep(1)
        try:
            self.__wait_element('#tableau_base_widget_LegacyCategoricalQuickFilter_0 > div > div.CFContent > span > div.tabComboBoxNameContainer.tab-ctrl-formatted-fixedsize').click()
        except: ...
        
        return self.__driver.find_elements(By.CSS_SELECTOR, '#tableau_base_widget_LegacyCategoricalQuickFilter_0_menu > div.CFInnerContainer.tab-ctrl-formatted-text.tiledContent > div.tileContainer > div >  div .facetOverflow')
        
    def __click_downloads(self, index: int) -> tuple:
        sleep(1)
        self.__wait_element('#download').click()
        self.__wait_element('#viz-viewer-toolbar-download-menu > div:nth-of-type(3)').click()
        self.__wait_element('label[data-tb-test-id="crosstab-options-dialog-radio-csv-Label"]').click()
        sleep(1) 
        self.__wait_element(f'div[data-tb-test-id="sheet-thumbnail-2"] div').click()
        self.__wait_element(f'div[data-tb-test-id="sheet-thumbnail-{index}"] div').click()
        self.__wait_element('button[data-tb-test-id="export-crosstab-export-Button"]').click()
        sleep(3) 


    def start(self) -> None:
        self.__driver: Chrome = Chrome(options=self.options('/data/pma/bpkm/csv', headless=True))

        link: str = 'https://nswi.bkpm.go.id/tableau/show_eis?app_name=InvestasiPer Kabupaten/Kota&content_url=2018_12_DB-Desktop-Apps/DB-per-KABKOT'
        link_split: list = link.split('/')
        
        self.__driver.get(link)
        # self.__driver.get('https://dashboard.bkpm.go.id/views/2018_12_DB-Desktop-Apps/DB-per-KABKOT/9977ec7c-858b-405a-951c-86a7ed74512c/2952c081-9824-4ee5-8951-e35d13a65bb4?%3Adisplay_count=n&%3AshowVizHome=n&%3Aorigin=viz_share_link&%3Aembed=y#1')
        self.__driver.get('https://dashboard.bkpm.go.id/views/2018_12_DB-Desktop-Apps/DB-per-KABKOT/6d4fdf07-c8c2-45a0-97af-1b5d1171ba78/20232024?iframeSizedToWindow=true&:embed=y&:display_spinner=no&:showAppBanner=false&:embed_code_version=3&:loadOrderID=0&:display_count=n&:showVizHome=n&:origin=viz_share_link')
        
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

                        self.__click_downloads(3)
                        self.__click_downloads(0)
                        
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
                            # 'page_info': page_info, 
                            # 'detail_data': detail_data,
                            'path_data_raw': f'S3://ai-pipeline-statistics/data/data_raw/Divtik/bkpm/PMA/{provinsi_name}/json/{kabupaten_name}.json', 
                            'path_data_clean': f'S3://ai-pipeline-statistics/data/data_clean/Divtik/bkpm/PMA/{provinsi_name}/json/{kabupaten_name}.json',   
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
                        
                        # break
                    except Exception as e:
                        continue

                # break
            except Exception as e:
                continue
        sleep(300)
        self.__driver.close()

if(__name__ == '__main__'):
    Bkpm(**{
        # 's3': True
    }).start()
