import asyncio
import requests

from concurrent.futures import ThreadPoolExecutor
from metadata import Metadata 
from httpx import AsyncClient
from bs4 import BeautifulSoup
from enum import Enum

from src.helpers import ConnectionS3

class Category(Enum):
    LAPORAN_KEUANGAN = 'laporan-keuangan'
    LAPORAN_KEBERLANJUTAN = 'laporan-keberlanjutan'
    LAPORAN_TAHUNAN = 'laporan-tahunan'


class Peruri:
    def __init__(self, category: Category) -> None:
        self.__assesion = AsyncClient()
        self.category: Category = category

    @staticmethod
    def parse_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select_one('h1').get_text(strip=True)
        return [
            {   
                'sub_title': (h4 := s.select_one('h4')).get_text(strip=True),
                'title': title,
                'desc': s.select_one('li').get_text(strip=True),
                'link_document': h4.select_one('a')["href"]
            } for s in soup.select('.item')
        ]
    
    def _download_data(self, data: Metadata):
        print('download =======')
        try:
            ConnectionS3.upload_content(
                requests.get(url if not (url := data.data["link_document"]).startswith('/') else f'https://www.bkn.go.id/{url}').content,
                data.path_data_raw[1].replace('s3://ai-pipeline-raw-data/', ''),
                'ai-pipeline-raw-data'
            )
        except: ...

    async def get_data(self, page):
        response = await self.__assesion.get(
            'https://www.peruri.co.id/hubungan-investor/%s' % self.category.value,
            params={
                'page': page
            }
        )
        return self.parse_data(response.text)
    
    def _process_datas(self, datas):
        clean = lambda x: x.lower().replace(' ', '_').replace(' ', '_').replace('-', '_').replace('/', '_').replace('-', '_')
        with ThreadPoolExecutor(max_workers=5   ) as executor:
            futures = []
            for data in datas:
                metadata = Metadata(
                    link='https://www.peruri.co.id/hubungan-investor/%s' % self.category.value,
                    source='www.peruri.co.id',
                    tags=[
                        'www.peruri.co.id',
                        'hubungan-investor',
                        self.category.value
                    ],
                    update_schedule='yearly',   
                    stage='Kelengkapan data',
                    desc=data['desc'],
                    path_data_raw=[
                        f"s3://ai-pipeline-raw-data/data/data_descriptive/peruri/hubungan_investor/{clean(self.category.value)}/json/{clean(data['sub_title'])}.json",
                        f"s3://ai-pipeline-raw-data/data/data_descriptive/peruri/hubungan_investor/{clean(self.category.value)}/pdf/{clean(data['sub_title'])}.pdf"
                    ],
                    data=data, 
                    category='hubungan-investor',
                    sub_category=self.category.value,
                    title=data['title'],
                    sub_title=data['sub_title']
                )                       
                futures.append(
                    executor.submit(
                        ConnectionS3.upload,
                        metadata.dict,
                        metadata.path_data_raw[0].replace('s3://ai-pipeline-raw-data/', ''),
                        'ai-pipeline-raw-data'
                    )
                )
                futures.append(
                    executor.submit(
                        self._download_data,
                        metadata,
                    )
                )

            for future in futures:
                future.result()

    async def get_all(self):
        page = 1
        while(True):
            datas = await self.get_data(page)
            if(not datas): break
            self._process_datas(datas)
            page += 1

if(__name__ == '__main__'):
    for cat in Category:
        p = Peruri(cat)  
        asyncio.run(p.get_all())