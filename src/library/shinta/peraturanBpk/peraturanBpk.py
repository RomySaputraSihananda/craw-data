import asyncio

from requests import Response, Session
from aiohttp import ClientSession
from time import time, sleep

from urllib.parse import unquote

from src.helpers import Parser, ConnectionS3, Datetime

class BasePeraturanBpk:
    def __init__(self) -> None:
        self.__requests: Session = Session()
        self.__requests.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }) 
    
    async def __download_file(self, url: str, **kwargs) -> str:
        try:
            async with ClientSession() as session:
                async with session.get(url, headers=self.__requests.headers) as response:
                    ConnectionS3.upload_content(await response.read(), (path := f'S3://ai-pipeline-raw-data/data/data_descriptive/bpk/data_rencana_pembangunan_jangka_menengah/pdf/{unquote(url).split("/")[-1].replace(" ", "_").lower()}').replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
                    
                    return path
                
        except Exception as e:
            print(e)

    async def __get_detail_peraturan(self, url: str, **kwargs) -> dict:
        async with ClientSession() as session:
            async with session.get(url, headers=self.__requests.headers) as response:
                soup: Parser = Parser(await response.text())
                return (data := {
                    'title': soup.select_one('.bg-gd-bpk-2.mb-8 h1').get_text().strip(),
                    'sub_title': soup.select_one('.bg-gd-bpk-2.mb-8 h4').get_text().strip(),
                    'materi_pokok': tag.get_text().strip() if (tag := soup.select_one('.card.mb-8 > div > p')) else '',
                    'metadata': {key.strip(): value.strip() for key, value in soup.select('.container.fs-6 > .py-4.ms-n2 > div').map(lambda e: [f.get_text() for f in e.select('div')])},
                    'abstrak': {
                        'paragraph': soup.select('#abstrak .modal-body > div p').map(lambda e: e.get_text().strip()),
                        'table': {key.strip(): value for key, value in soup.select('#abstrak .modal-body > div table tr').map(lambda e: [e.select_one('td').get_text().replace(":", ""), [li.get_text().strip() for li in e.select('ul > li')]])}
                    },
                    'files': soup.select('a[data-kategori="Peraturan"]').map(lambda e: 'https://peraturan.bpk.go.id' + e['href']),
                    'status': soup.select('.card.mb-6 div.row.g-4.g-xl-9.mb-8 ol li').map(lambda e: e.get_text().strip()),
                }, await asyncio.gather(*(self.__download_file(file) for file in data['files'])))
    async def _get_peraturan(self, **kwargs) -> list:
        response: Response = self.__requests.get('https://peraturan.bpk.go.id/Search',
                                            params={
                                                'keywords': '',
                                                'tentang': 'Rencana Pembangunan jangka menengah',
                                                'nomor': '',
                                                'tahun': [
                                                    2023,
                                                    2022,
                                                    2021,
                                                    2020,
                                                    2019,
                                                    2018,
                                                    2017,
                                                    2016,
                                                ],
                                                'jenis': 19,
                                                'p': kwargs.get('page', 1),
                                            })
        urls: list = Parser(response.text).select('.rounded-4 > .row.mb-8 a.fs-1.fw-bold').map(lambda e: 'https://peraturan.bpk.go.id' + e['href']) 
        datas: list = await asyncio.gather(*(self.__get_detail_peraturan(url) for url in urls))

        if(kwargs.get('write', None)):
            for i, url in enumerate(urls):
                data, paths = datas[i]
                result: dict = {
                    "link": url,
                    "domain": (link_split := url.split('/'))[2],
                    "tag": link_split[2:],
                    "crawling_time": Datetime.now(),
                    **data,
                    "crawling_time_epoch": int(time()),
                    "path_data_raw": [
                        f'S3://ai-pipeline-raw-data/data/data_descriptive/bpk/data_rencana_pembangunan_jangka_menengah/json/{data["title"].replace(" ", "_").lower()}.json',
                        *paths
                    ]
                }

                ConnectionS3.upload(result, result['path_data_raw'][0].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
        
        return datas
        
    async def _get_all(self, **kwargs) -> list:
        page: int = 1
        datas: list = [] 
        while(True):
            data: list = await self._get_peraturan(page=page, **kwargs)
            if(not data): break
            datas.extend(data)
            page += 1
            sleep(5)
        return datas


if(__name__ == '__main__'): asyncio.run(BasePeraturanBpk()._get_all(write=True))
