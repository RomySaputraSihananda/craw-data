import asyncio
import requests

from httpx import AsyncClient
from bs4 import BeautifulSoup

from concurrent.futures import ThreadPoolExecutor
from metadata import Metadata

from src.helpers import ConnectionS3

class BknRegulasi:
    def __init__(self) -> None:
        self.__assesion = AsyncClient()
    
    @staticmethod
    def parse_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        return [
            {
                'title': (a := article.select_one('h2 a')).get_text(strip=True),
                'link': a["href"],
                'desc': article.select_one('p').get_text(strip=True),
                'category': article.select_one('.wpex-mb-15 a').get_text(strip=True),
                'link_document': article.select('a')[-1]["href"]
            } for article in soup.select('article')
        ]

    async def get_data(self, page):
        root = 'https://www.bkn.go.id/regulasi/'
        response = await self.__assesion.get(
            '%spage/%d/' % (root, page) if page > 1 else root
        )
        if(response.status_code == 404): return

        return self.parse_data(response.text)
    
    def _download_data(self, data: Metadata):
        try:
            ConnectionS3.upload_content(
                requests.get(url if not (url := data.data["link_document"]).startswith('/') else f'https://www.bkn.go.id/{url}').content,
                data.path_data_raw[1].replace('s3://ai-pipeline-raw-data/', ''),
                'ai-pipeline-raw-data'
            )
        except: ...
    async def _process_datas(self,  datas):
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for data in datas:
                metadata = Metadata(
                    link=data["link"],
                    source='www.bkn.go.id',
                    tags=[
                        'www.bkn.go.id',
                        'unggahan',
                        'Data Peraturan BKN',
                        'peraturan',
                        'regulasi'
                    ],
                    update_schedule='yearly',
                    stage='Kelengkapan data',
                    desc=data['desc'],
                    path_data_raw=[
                        f"s3://ai-pipeline-raw-data/data/data_descriptive/bkn/regulasi/{data['category'].lower().replace(' ', '_').replace('-', '_').replace('/', '_')}/json/{data['title'].lower().replace(' ', '_').replace('-', '_').replace('/', '_')}.json",
                        f"s3://ai-pipeline-raw-data/data/data_descriptive/bkn/regulasi/{data['category'].lower().replace(' ', '_').replace('-', '_').replace('/', '_')}/pdf/{data['title'].lower().replace(' ', '_').replace('-', '_').replace('/', '_')}.pdf"
                    ],
                    data=data, 
                    category='regulasi',
                    sub_category=data['category'],
                    title='Regulasi',
                    sub_title=data['title']
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

    async def start(self):
        page = 1
        while(True):
            datas = await self.get_data(page)
            if(not datas): break
            await self._process_datas(datas)
            page += 1
            # break

if(__name__ == '__main__'):
    b = BknRegulasi()
    asyncio.run(b.start())