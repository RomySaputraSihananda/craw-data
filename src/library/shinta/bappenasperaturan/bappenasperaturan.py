# bappenasperaturan
# 0, 10, 20     
import asyncio
import json

from time import time 
from httpx import AsyncClient
from bs4 import BeautifulSoup
from greenstalk import Client 
from concurrent.futures import ThreadPoolExecutor       

from .urls import urls

from src.helpers import Datetime, ConnectionS3

class BappenasPeraturan:
    def __init__(self) -> None:
        self.__asession = AsyncClient()
        self.__beanstalk_use: Client = Client(('192.168.150.21', 11300), use='dev-target-bappenas-peraturan')
        self.__beanstalk_watch: Client = Client(('192.168.150.21', 11300), watch='dev-target-bappenas-peraturan')

    async def __download(self, file, root, judul):
        type, url = file
        response = await self.__asession.get(url)
        ConnectionS3.upload_content(response.content, (path := f'{root}pdf/{judul}_{type}.pdf').replace('s3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
        return path

    async def _get_cards(self, url):
        type = url.split('/')[-1]
        page = 1
        while(True):
            response = await self.__asession.get(
                '%s/%d' % (url, (page - 1) * 10)
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            for a in (card := soup.select('#tabsdetail > div > div a.document-title')):
                yield {
                    'type': type,   
                    'link': a["href"]
                }

            if(not card): break

            page += 1

    async def _get_all(self):
        for url in urls:
            async for card in self._get_cards(url):
                print(self.__beanstalk_use.put(json.dumps(card)))
    
    async def _get_detail(self, link, type):
        response = await self.__asession.get(    
            link
        )

        clean = lambda x: x.lower().strip().replace('/', '_').replace('-', '_').replace(' ', '_')
        soup = BeautifulSoup(response.text, 'html.parser')

        data = {
            **{
                (td := tr.select('td div'))[0].get_text().strip(): [l.get_text().strip() for l in li] if (li := td[1].select('li')) else td[1].get_text().strip() for tr in soup.select('table tbody tr')
            },
            'Judul': soup.select_one('h4').get_text().strip(),
            'description': soup.select_one('.mb-20 > span').get_text().strip(),
            'subjek': [span.get_text().strip() for span in soup.select('.m-0 > span')],
            'file': {file["id"].replace('tab-', ''): embed["src"].replace('#toolbar=0', '') if (embed := file.select_one('embed')) else file.get_text().strip() for file in soup.select('.mb-4 > div[role="tabpanel"]')}
        }

        result: dict = {
            "link": (link := response.url.__str__()),
            "domain": (link_split := link.split('/'))[2],
            "tag": [
                *link_split[2:],
                'bappenas',
                type
            ],
            **data,
            "crawling_time": Datetime.now(),
            "crawling_time_epoch": int(time()),
            "path_data_raw": [
                (root := f's3://ai-pipeline-raw-data/data/data_descriptive/peraturan_undang_undang/jdih_bappenas_go_id/{clean(type)}/') + f'json/{clean(data["Judul"])}.json',
                *await asyncio.gather(*(self.__download(file, root, clean(data["Judul"])) for file in data["file"].items() if 'http' in file[1]))
            ]
        }

        ConnectionS3.upload(result, result["path_data_raw"][0].replace('s3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')

    async def _get_all_detail(self):
        while(job := self.__beanstalk_watch.peek_buried()):
            try:            
                await self._get_detail(**json.loads(job.body))
                self.__beanstalk_watch.delete(job)
            except BaseException as e:
                self.__beanstalk_watch.bury(job)

if(__name__ == '__main__'):
    # asyncio.run(BappenasPeraturan()._get_detail('https://jdih.bappenas.go.id/peraturan/detailperaturan/153/undang-undang-nomor-2-tahun-2015'))
    asyncio.run(
        BappenasPeraturan()\
            ._get_all_detail()
            # ._get_detail(
            #     **{
            #         "type": "uud1945",
            #         "link": "https://jdih.bappenas.go.id/peraturan/detailperaturan/1267/undang-undang-dasar-1945-nomor--tahun-2020"
            #     }
            # )
)

