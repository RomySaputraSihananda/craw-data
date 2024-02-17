import os
import re
import urllib3
import requests
import asyncio

from json import dumps
from time import time
from aiohttp import ClientSession
from concurrent.futures import ThreadPoolExecutor

from requests import Response, Session
from helpers import Parser, Datetime, Iostream, ConnectionS3

urllib3.disable_warnings()

class BaseCekbpom:
    def __init__(self, **kwargs) -> None:
        self.__s3: bool = kwargs.get('s3')
        self.__clean: bool = kwargs.get('clean')
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

    async def _get_product_by_page(self, page: int) -> bool:
        response: Response = self.__requests.post('https://cekbpom.pom.go.id/prev_next_pagination_all_produk', 
                                                    data={
                                                        'st_filter': '1',
                                                        'input_search': '',
                                                        'from_home_flag': 'Y',
                                                        'offset': (page - 1) * 10 + 1,
                                                        'next_prev': page * 10,
                                                        'count_data_all_produk': self.__count_data_all_produk,
                                                        'marked': 'next',
                                                    })
        data_all_produk: list = response.json()['data_all_produk']

        if(not data_all_produk): return False 

        if(self.__product_first):
            await asyncio.gather(*(self._get_detail_by_product_id(*product) for product in self.__product_first))
            self.__product_first = None

        
        await asyncio.gather(*(self._get_detail_by_product_id(product['PRODUCT_ID'], product['APPLICATION_ID']) for product in data_all_produk))

        return True
    
    async def _get_detail_by_product_id(self, product_id: str, aplication_id: str) -> None:
        async with ClientSession() as session:
            async with session.post('https://cekbpom.pom.go.id/get_detail_produk_obat',
                                    headers=self.__headers,
                                    data={
                                        'product_id': product_id,
                                        'aplication_id': aplication_id
                                    }, verify_ssl=False) as response:

                soup: Parser = Parser(await response.text())

                keys: list = soup.select('.form-field-caption').map(lambda element: re.sub(r'\s+', ' ', element.text.replace('\n', '')).lower().replace(' ', '_'))
                values: list = soup.select('.form-field-input div').map(lambda element: re.sub(r'\s+', ' ', element.text.replace('\n', '')).strip(' '))

                link: str = 'https://cekbpom.pom.go.id/search_home_produk'
                link_split: list = link.split('/')

                data: dict = {
                        'link': link,
                        'domain': link_split[2],
                        'tag': link_split[2:],
                        'crawling_time': Datetime.now(),
                        'crawling_time_epoch': int(time()),
                }
                for i, key in enumerate(keys):
                    if(key == "_" or key == "" or key == " "):
                        data[keys[i -1]] = [data[keys[i -1]], values[i]]
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
                    'path_data_raw': f'S3://ai-pipeline-statistics/data/data_raw/data_divtik/bpom/product/{data["produk"]}/json/{product_id}.json',   
                    'path_data_clean': f'S3://ai-pipeline-statistics/data/data_clean/data_divtik/bpom/product/{data["produk"]}/json/{product_id}.json',   
                })
                paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"]]] 
                
                if(self.__clean):
                    paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"], data["path_data_clean"]]] 
                
                with ThreadPoolExecutor() as executor:
                    data: dict = Iostream.dict_to_deep(data)
                    try:
                        if(self.__s3):
                            executor.map(lambda path: ConnectionS3.upload(data, path), paths)
                        else:
                            executor.map(lambda path: Iostream.write_json(data, path), paths)
                    except Exception as e:
                        raise e    
        
    def _get_all(self):
        page: int = 1
        while(True):
            print(page)
            success: bool = asyncio.run(self._get_product_by_page(page))

            if(not success): break
            
            page += 1
            

if(__name__ == '__main__'):
    baseCekbpom: BaseCekbpom = BaseCekbpom()
    asyncio.run(baseCekbpom._get_product_by_page(1))
    # baseCekbpom._get_all()