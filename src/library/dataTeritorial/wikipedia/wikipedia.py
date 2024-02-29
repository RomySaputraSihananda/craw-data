__author__ = 'Gumilar Ganjar Permana'

import re
import asyncio

from time import time
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from concurrent.futures import ThreadPoolExecutor

from src.helpers import Iostream, Datetime, ConnectionS3
from .kabupaten import KabupatenEnum

class BaseWikipedia:
    def __init__(self, **kwargs) -> None:
        self.__s3: bool = kwargs.get('s3')
        self.__kafka: bool = kwargs.get('kafka')
        self.__clean: bool = kwargs.get('clean')
    
    @staticmethod
    def __clean_text(text: str) -> str:
        clean_text: str = re.sub(r'(\n)?\[.*\](\n)?', ' ', text).replace(' • ', ' ').replace(' ', ' ').strip(' ')
        if(match := re.findall(r'Rp\.?\s*([+-]?\s*\d{1,3}(?:\.\d{3})*)(?:,\d+)?', clean_text)):
            return int("".join(match).replace('.', ''))
        elif '\n' in clean_text:
            return [clean for clean in clean_text.split('\n') if clean]
        elif '), ' in clean_text:
            clean_texts: list = [clean for clean in clean_text.split('), ') if clean]
            return [f'{clean})' if "(" in clean else clean for clean in clean_texts]
        
        return clean_text
    
    def __proccess_data(self, page_source: str):
        soup: BeautifulSoup = BeautifulSoup(page_source, 'html.parser')
        rows: list  = soup.select('.infobox.ib-settlement.vcard tbody tr')

        data: dict = {}
        for row in rows:
            try:
                data.update({
                    self.__clean_text(row.find('th').get_text()): self.__clean_text(row.find('td').get_text()) if not row.select('li') else [self.__clean_text(li.get_text()) for li in row.select('li')]
                })
            except:
                if(images := row.select('img')):
                    for image in images:
                        value: str = 'https:' + image.attrs['src'] if not 'https:' in image.attrs['src'] else image.attrs['src']
                        key: str = value if not 'alt' in image.attrs else image.attrs['alt']
                        key: str = re.sub(r'\d+px-', '', value.split('/')[-1].split('.')[0]) if not key or 'https' in key else key
                        data: dict = {
                            **data,
                            'images': data['images'] | {key: value} if 'images' in data else {key: value},
                        }
        return data

    async def _get_wikipedia_detail_by_location(self, location: KabupatenEnum) -> dict:
        link: str = location.value
        link_split: list = link.split('/')
        async with ClientSession() as session:
            async with session.get(link) as response:
                
                data: dict = self.__proccess_data(await response.text())
                data: dict = {
                    "link": link,
                    "domain": link_split[2],
                    "tag": link_split[2:],
                    "crawling_time": Datetime.now(),
                    "crawling_time_epoch": int(time()),
                    **data,
                    "path_data_raw": f'S3://ai-pipeline-statistics/data/data_raw/wikipedia/data teritorial/json/{data["Provinsi"].replace(" ", "_")}/{location.name.title()}.json',
                    "path_data_clean": f'S3://ai-pipeline-statistics/data/data_clean/wikipedia/data teritorial/json/{data["Provinsi"].replace(" ", "_")}/{location.name.title()}.json',
                }

                paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"]]] 
                
                if(self.__clean):
                    paths: list = [path.replace('S3://ai-pipeline-statistics/', '') for path in [data["path_data_raw"], data["path_data_clean"]]] 
                    
                data: dict = Iostream.dict_to_deep(data)
                
                if(self.__kafka):
                    # self.__connectionKafka.send(self.__topik, data, name=self.__bootstrap)
                    ...
                else:
                    with ThreadPoolExecutor() as executor:
                        try:
                            if(self.__s3):
                                executor.map(lambda path: ConnectionS3.upload(data, path), paths)
                            else:
                                executor.map(lambda path: Iostream.write_json(data, path), paths)
                        except Exception as e:
                            raise e    

    async def _get_all_location(self) -> None:
        await asyncio.gather(*(self._get_wikipedia_detail_by_location(kabupaten) for kabupaten in KabupatenEnum))

if(__name__ == '__main__'):
    asyncio.run(BaseWikipedia()._get_all_location())
    # asyncio.run(WikipediaCrawler()._get_wikipedia_detail_by_location(KabupatenEnum.KABUPATEN_BANTAENG))