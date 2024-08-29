import json
import asyncio

from httpx import AsyncClient
from bs4 import BeautifulSoup
from greenstalk import Client
from time import time

from src.helpers import Datetime, ConnectionS3, Iostream

class KemendikbudPeraturan:    
    def __init__(self) -> None:
        self.__asession: AsyncClient = AsyncClient(verify=False)
        self.__beanstalk_use: Client = Client(('192.168.150.21', 11300), use='dev-target-kemendikbud-peraturan')
        self.__beanstalk_watch: Client = Client(('192.168.150.21', 11300), watch='dev-target-kemendikbud-peraturan')

    async def __download(self, file, root, judul):
        response = await self.__asession.get(file)
        ConnectionS3.upload_content(response.content, (path := f'{root}pdf/{judul}.pdf').replace('s3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
        return path

    async def _get_detail(self, id):
        response = await self.__asession.get(
            'https://jdih.kemdikbud.go.id/detail_peraturan',
            params={
                'main': id
            }
        )

        soup = BeautifulSoup(response.text, 'html.parser')
        data = {
            td[0].get_text().strip(): td[1].get_text().strip() for tr in soup.select('.table tbody tr') if (td := tr.find_all_next('td'))
        }

        clean = lambda x: x.lower().strip().replace('/', '_').replace('-', '_').replace(' ', '_')

        result: dict = {
            "link": (link := response.url.__str__()),
            "domain": (link_split := link.split('/'))[2],
            "tag": [
                *link_split[2:],
                'kemdikbud'
            ],
            'file': (file := soup.select_one('.float-right a')["href"]),
            **data,
            "crawling_time": Datetime.now(),
            "crawling_time_epoch": int(time()),
            "path_data_raw": [
                (root := f's3://ai-pipeline-raw-data/data/data_descriptive/peraturan_undang_undang/jdih_kemdikbud_go_id/{clean(data["Tematik"])}/') + f'json/{clean(data["Judul"])}.json',
                await self.__download(file, root, clean(data["Judul"]))
            ]
        }

        ConnectionS3.upload(result, result["path_data_raw"][0].replace('s3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
    
    async def _get_all_detail(self):
        while(job := self.__beanstalk_watch.reserve()):
            try:
                await asyncio.gather(*(self._get_detail(id) for id in json.loads(job.body)))
                self.__beanstalk_watch.delete(job)
            except:
                self.__beanstalk_watch.bury(job)

    async def _send_target(self, page = 1):
        while(True):
            response = await self.__asession.post(
                'https://jdih.kemdikbud.go.id/get_peraturan', 
                data={
                    'page': page,
                }
            ) 

            soup = BeautifulSoup(response.text, 'html.parser')
            ids = [input["value"] for input in soup.select('input[name="id_peraturan"]')]
            if(not ids): break
            print(self.__beanstalk_use.put(json.dumps(ids)))    
            
            page += 1

if(__name__ == '__main__'):
    asyncio.run(
        KemendikbudPeraturan()\
            ._get_all_detail()
            # ._get_detail("3414")
            # ._get_all_detail([
            #     "3429",
            #     "3430",
            #     "3428", 
            #     "3426",
            #     "3427",
            #     "3416",
            #     "3414",
            #     "3421",
            #     "3413",
            #     "3423"
            # ])
    )