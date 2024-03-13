import re
import urllib3
import requests
import asyncio

from json import loads
from time import time
from aiohttp import ClientSession
from concurrent.futures import ThreadPoolExecutor

from requests import Response, Session

from src.helpers import Parser, Datetime, Iostream, ConnectionS3, logging, ConnectionKafka

urllib3.disable_warnings()

class BaseCekbpom:
    def __init__(self, **kwargs) -> None:
        self.__s3: bool = kwargs.get('s3')
        self.__kafka: bool = kwargs.get('kafka')
        self.__clean: bool = kwargs.get('clean')

        if(self.__kafka): 
            self.__bootstrap: str = kwargs.get('bootstrap')
            self.__connectionKafka: ConnectionKafka = ConnectionKafka(kwargs.get('topic'), kwargs.get('bootstrap'))

        self.__requests: Session = Session() 
        self.__headers: dict = {
            'Cookie': 'webreg=f3rs64qmrr4k7lln0cud4virv480jdca',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Pixel 2 Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/121.0.6167.101 Mobile Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.__requests.headers.update(self.__headers)

        (self.__count_data_all_produk, self.__product_first) = self.get_count_data_all_produk()

    @staticmethod 
    def get_count_data_all_produk() -> tuple:
        response: Response = requests.get('https://cekbpom.pom.go.id/search_home_produk')
        content: str = response.text

        return (
            int(re.findall(r"count_data_all_produk = '(\d+)'", content)[0]),
            re.findall(r'onclick="get_detail\(\'(.*?)\*(\d+)\'\)"', content)
        )

    async def _get_product_by_page(self, page: int, data: dict, log: dict = None) -> bool:
        try:
            async with ClientSession() as session:
                async with session.post('https://cekbpom.pom.go.id/prev_next_pagination_all_produk', 
                                        headers=self.__headers,
                                        data={
                                            'st_filter': '1',
                                            'input_search': '',
                                            'from_home_flag': 'Y',
                                            'offset': (page - 1) * 10 + 1,
                                            'next_prev': page * 10,
                                            'count_data_all_produk': self.__count_data_all_produk,
                                            'marked': 'next',
                                        }, timeout=30) as response:
                    response_json: dict = loads(await response.text())

                    data_all_produk: list = response_json['data_all_produk']

                    if(not data_all_produk): return False 

                    if(self.__product_first):
                        log['total_data'] += len(self.__product_first)
                        await asyncio.gather(*(self._get_detail_by_product_id(*product, data, log) for product in self.__product_first))
                        self.__product_first = None

                    if(not all): log['total_data'] += len(data_all_produk)
                    await asyncio.gather(*(self._get_detail_by_product_id(product['PRODUCT_ID'], product['APPLICATION_ID'], data, log) for product in data_all_produk))

                    if(not all): 
                        log['status'] = 'Done'
                        Iostream.update_log(log, name=__name__)
 
                    return True
        except Exception as e:
            logging.error(f'Error Time Out page {page}')
            logging.error(e)
            return await self._get_product_by_page(page, data, log)
            
    
    async def _get_detail_by_product_id(self, product_id: str, aplication_id: str, data: dict, log: dict) -> None:
        link: str = 'https://cekbpom.pom.go.id/search_home_produk'
        link_split: list = link.split('/')
        try:
            async with ClientSession() as session:
                async with session.post('https://cekbpom.pom.go.id/get_detail_produk_obat',
                                        headers=self.__headers,
                                        data={
                                            'product_id': product_id,
                                            'aplication_id': aplication_id
                                        }, verify_ssl=False, timeout=30) as response:

                    soup: Parser = Parser(await response.text())

                    keys: list = soup.select('.form-field-caption').map(lambda element: re.sub(r'\s+', ' ', element.text.replace('\n', '')).lower().replace(' ', '_'))
                    values: list = soup.select('.form-field-input div').map(lambda element: re.sub(r'\s+', ' ', element.text.replace('\n', '')).strip(' '))
                    
                    for i, key in enumerate(keys):
                        if(key == "_" or key == "" or key == " "):
                            try:
                                data[keys[i - 1]] = [data[keys[i - 1]], [value.strip(' ') for value in values[i].split('- ')] if '-' in values[i] else values[i]]
                                current_key = keys[i - 1]
                            except Exception as e:
                                data[current_key].append([value.strip(' ') for value in values[i].split('- ')] if '-' in values[i] else values[i])
                        else:
                            try:
                                data[key] = Datetime.format(values[i], "%d-%m-%Y")
                            except Exception:
                                if(re.search(r'-\s', values[i])):
                                    value_split = [value.strip(' ') for value in values[i].split('- ')]
                                    if("" in value_split): 
                                        data[key] = value_split[1:]
                                    else:
                                        data[key] = value_split
                                else:
                                    data[key] = values[i]

                    data.update({
                        'path_data_raw': f'S3://ai-pipeline-statistics/data/data_raw/bpom/product/{data["produk"]}/json/{product_id}.json', 
                        'path_data_clean': f'S3://ai-pipeline-statistics/data/data_clean/bpom/product/{data["produk"]}/json/{product_id}.json',   
                    })
                    paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"]]] 
                    
                    if(self.__clean):
                        paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"], data["path_data_clean"]]] 
                    
                    data['tag'] = [*data['tag'], data["produk"]]
                    data: dict = Iostream.dict_to_deep(data)
                    
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
                    
                    Iostream.info_log(log, product_id, 'success', name=__name__)
                
                    log['total_success'] += 1
                    Iostream.update_log(log, name=__name__)
                    data['tag'] = link_split[2:]
        except Exception as e:
            Iostream.info_log(log, f'{product_id};{aplication_id}', 'failed', error=e, name=__name__)

            log['total_failed'] += 1
            Iostream.update_log(log, name=__name__)
        
    async def _get_all(self, start: int = 1):
        link: str = 'https://cekbpom.pom.go.id/search_home_produk'
        link_split: list = link.split('/')
        data: dict = {
                'link': link,
                'domain': link_split[2],
                'tag': link_split[2:],
                'crawling_time': Datetime.now(),
                'crawling_time_epoch': int(time()),
        }

        log: dict = {
            "Crawlling_time": Datetime.now(),
            "id_project": None,
            "project": "Data Intelligence",
            "sub_project": "data divtik",
            "source_name": data['domain'],
            "sub_source_name": 'product',
            "id_sub_source": None,
            "total_data": self.__count_data_all_produk if all else 0,
            "total_success": start * 10,
            "total_failed": 0,
            "status": "Process",
            "assign": "romy",
        }
        Iostream.write_log(log, name=__name__)
        
        page: int = start
        while(True):
            success: bool = await asyncio.gather(*(self._get_product_by_page(i, data, log) for i in range(page, page + 2)))

            if(False in success): break
            
            page += 2

        log['status'] = 'Done'
        Iostream.update_log(log, name=__name__)
    
    def _retry_error(self):
        log_errors: list = Iostream.get_log_error(name=__name__)
        
        for log_error in [log_error['id_data'] for log_error in log_errors]:
            # [product_id, aplication_id] = log_error.split(';')
            [product_id, aplication_id] = log_error.split(';')

            print(product_id)

if(__name__ == '__main__'):
    baseCekbpom: BaseCekbpom = BaseCekbpom()
    asyncio.run(baseCekbpom._get_product_by_page(2))
    # baseCekbpom._retry_error()