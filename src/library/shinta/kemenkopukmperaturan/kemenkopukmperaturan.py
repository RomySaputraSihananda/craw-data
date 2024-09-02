import json
import asyncio

from httpx import AsyncClient
from bs4 import BeautifulSoup
from greenstalk import Client
from time import time

from src.helpers import Datetime, ConnectionS3

class KemenkopukmPeraturan  :
    BASE_URL = 'https://jdih.kemenkopukm.go.id'
    def __init__(self) -> None:
        self.__assesion: AsyncClient = AsyncClient(verify=False)
        self.__beanstalk_use: Client = Client(('192.168.150.21', 11300), use='dev-target-kemenkopukm-peraturan')
        self.__beanstalk_watch: Client = Client(('192.168.150.21', 11300), watch='dev-target-kemenkopukm-peraturan')

    async def __download(self, file, root, judul):
        (key, url) = file
        response = await self.__assesion.get(url)
        ConnectionS3.upload_content(response.content, (path := f'{root}pdf/{judul}{"_abstrak" if key == "Abstrak" else ""}.pdf').replace('s3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
        return path

    async def _get_page(self, page):
        response = await self.__assesion.get(
            '%s/doc/peraturan/' % self.BASE_URL,
            params={
                'page': (page - 1) * 12 + 1
            }
        )

        soup = BeautifulSoup(response.text, 'html.parser')
        return [
            self.BASE_URL + a["href"] for a in soup.select('#blog h2 a')
        ]

    async def _get_detail(self, url):
        response = await self.__assesion.get(
            url
        )

        clean = lambda x: x.lower().strip().replace('/', '_').replace('-', '_').replace(' ', '_')

        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.select_one('article')
        container = article.select('.clearfix.row.mt-2 > div')

        iframe = (file_container := container.pop(0)).select_one('iframe')["src"]

        file = {
            a.get_text().strip(): self.BASE_URL + a["href"] for a in file_container.select('a')
        }

        if('Flipbook' in file): del file["Flipbook"]

        meta = container.pop(0).select_one('table') 
        metadata = {
            key.get_text().strip(): value.get_text().strip()  for key, value in [tr.select('td') for tr in meta.select('tbody tr')]
        }

        def parse_table(table):
            return [
                {
                    th.get_text(): values[i] if len(values := [td.get_text() for td in tr.select('td')]) > 1 else values[0] for i, th in enumerate(table.select('thead tr th'))
                } for tr in table.select('tbody tr')
            ]

        result = {
            "link": (link := response.url.__str__()),
            "domain": (link_split := link.split('/'))[2],
                                "tag": [
                *link_split[2:],
                'kemenkopukm'
            ],
            **metadata,
            'file': file,
            'iframe': iframe,
            'status': meta.select_one('thead tr th:last-child span').get_text(),
            'info': {
                table.select_one('h4').get_text(): parse_table(table.select_one('table')) for table in container
            },
            "crawling_time": Datetime.now(),
            "crawling_time_epoch": int(time()),
            "path_data_raw": [
                (root := f's3://ai-pipeline-raw-data/data/data_descriptive/peraturan_undang_undang/jdih_kemenkopukm_go_id/{clean(metadata["Jenis/Bentuk Peraturan"])}/') + f'json/{clean(metadata["Judul"])}.json',
                *await asyncio.gather(*(self.__download(a, root, clean(metadata["Judul"])) for a in file.items()))
            ]
        }
        ConnectionS3.upload(result, result["path_data_raw"][0].replace('s3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')

    async def _push_link(self):
        page = 1
        while(True):
            urls = await self._get_page(page)
            if(not urls): break

            self.__beanstalk_use.put(json.dumps(urls))

            page += 1

    async def _perform(self):
        # await self._get_detail('https://jdih.kemenkopukm.go.id/doc/detail/doc-1130-v_peraturan')
        while(job := self.__beanstalk_watch.peek_buried()):
            try:
                print(job)
                # for url in json.loads(job.body):
                #     await self._get_detail(url)
                # self.__beanstalk_watch.delete(job)
            except Exception as e:
                raise e
                # self.__beanstalk_watch.bury(job)

if(__name__ == '__main__'):
    asyncio.run(
        KemenkopukmPeraturan()\
            ._perform()
    )