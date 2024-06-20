import asyncio
import requests 

from requests import Response
from aiohttp import ClientSession
from json import dumps, loads
from bs4.element import Tag
from functools import reduce
from time import time
from greenstalk import Client

from concurrent.futures import ThreadPoolExecutor

from src.helpers import Parser, Datetime, Iostream, ConnectionS3
from src.helpers.parser import Array

class KemkesRS:
    def __init__(self) -> None:
        self.__beanstalk_use: Client = Client(('192.168.150.21', 11300), use='dev-target-rs')
        self.__beanstalk_watch: Client = Client(('192.168.150.21', 11300), watch='dev-target-rs')

        self.__charts_nasional: dict = asyncio.run(self.get_charts())
        # jumlah_rumah_sakit, rs_tikor = asyncio.run(self.__get_coordinate())
        jumlah_rumah_sakit, rs_tikor = (None, [])
        self.__jumlah_rumah_sakit: list = jumlah_rumah_sakit
        
        data: dict = requests.get('https://sirs.kemkes.go.id/fo/home/rekap_rs_all?id=0').json()['data']
        
        self.__rs: dict = {d['kode']: d for d in data}
        
        for d in rs_tikor: 
            if d['kode'] in self.__rs: self.__rs[d['kode']].update(d)
    
    @staticmethod
    def filter_response(func):
        async def wrap(*args, **kwargs):
            response_json: dict = await func(*args, **kwargs)
            if not (response_json): return None
            if not 'label' in (response_json := response_json[0]):
                return {
                    response_json['text']: {
                        e['name']: e['y']
                        for e in response_json['json']['data']
                    }
                }

            return {
                response_json['text']: {
                    key: response_json['json']['data'][i]
                    for i, key in enumerate(response_json['label']['categories'])
                }
            }

        return wrap
    
    async def get_charts(self, provinsi = 0):
        return reduce(lambda a, b: dict(a, **b), await asyncio.gather(*(
            self.__get_rekap_by_kepemilikan(provinsi),
            self.__get_rekap_by_jenis(provinsi),
            self.__get_rekap_by_kelas(provinsi)
        )))
    
    async def __get_coordinate(self):
        async with ClientSession() as session:
            async with session.get('https://sirs.kemkes.go.id/fo/home/list_prop_noncovid?id=0') as response:
                return loads(await response.text()).values()

    @filter_response
    async def __get_rekap_by_kepemilikan(self, province_id: int = 0):
        async with ClientSession() as session:
            async with session.get('https://sirs.kemkes.go.id/fo/home/rekap_by_kepemilikan?id=%d' % province_id) as response:
                return loads(await response.text())
    
    @filter_response
    async def __get_rekap_by_jenis(self, province_id: int = 0):
        async with ClientSession() as session:
            async with session.get('https://sirs.kemkes.go.id/fo/home/rekap_by_jenis?id=%d' % province_id) as response:
                return loads(await response.text())
    
    @filter_response
    async def __get_rekap_by_kelas(self, province_id: int = 0):
        async with ClientSession() as session:
            async with session.get('https://sirs.kemkes.go.id/fo/home/rekap_by_kelas?id=%d' % province_id) as response:
                return loads(await response.text())

    @staticmethod
    def parse_detail(html) -> dict:
        soup: Parser = Parser(html)
        titles: list = soup.select('.col-md-8 .card-title').map(lambda e: e.get_text())
        
        data = {}
        for i, table in enumerate(soup.select('.col-md-8 table').to_list()): 
            keys: list = Array(table.select('thead tr th')).map(lambda e: e.get_text())
            values: list = Array(table.select('tbody tr')).map(lambda e: [f.get_text() for f in e.select('td')])
            data.update({titles[i]: [{key: value[j].strip() for j, key in enumerate(keys)} for value in values]})
        
        primaries: list = soup.select('.card.card-primary > div').to_list()

        def filter_li(e: Tag):
            if('strong' in [i.name for i in e.findChildren()]):
                return {
                    strong.get_text().strip(): e.select('p')[i].get_text().strip() 
                    for i, strong in enumerate(e.select('strong'))
                }
            
            return {
                e.select_one('b').get_text().replace(':', '').strip(): e.select_one('a').get_text().strip()
            }

        return {
            primaries[0].select_one('h3').get_text(): {
                'image': 'https:' + primaries[1].select_one('.widget-user-header.text-white')['style'].split("url('")[1].split("')")[0].split(':')[-1],
                **reduce(lambda a, b: dict(a, **b), Array(primaries[1].select('ul li')).map(lambda e: filter_li(e))),
            },
            **data
        }
    
    async def _get_all(self):
        for rs in list(self.__rs.values()):
            self.__beanstalk_use.put(dumps(rs))
            
            # Iostream.write_json((data := await self.__get_detail_rs(rs)), data['path_data_raw'].replace('S3://ai-pipeline-raw-data/', ''), indent=4)

    async def _watch_beanstalk(self):
        while(job := self.__beanstalk_watch.reserve(timeout=60)):
            try:
                data: dict = await self.__get_detail_rs(loads(job.body))
                print(data)
                ConnectionS3.upload(data, data['path_data_raw'].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
                self.__beanstalk_watch.delete(job)
            except KeyboardInterrupt:
                exit() 
            except: 
                self.__beanstalk_watch.bury(job)
    
    # async def _watch_beanstalk_thread(self):
    #     with ThreadPoolExecutor(max_workers=10) as executor:
    #         loop = asyncio.get_event_loop()
    #         while True:
    #             job = self.__beanstalk_watch.reserve(timeout=60)

    #             await loop.run_in_executor(executor, self.__get_detail_rs, loads(job.body))

    #             self.__beanstalk_watch.delete(job)

    async def __get_detail_rs(self, rs: dict = None): 
        async with ClientSession() as session:
            async with session.get('https://sirs.kemkes.go.id/fo/home/profile_rs/%s' % rs['kode']) as response:
                data = {
                    "link": (link := str(response.url)),
                    "domain": (link_split := link.split('/'))[2],
                    "tag": link_split[2:],
                    "crawling_time": Datetime.now(),
                    "crawling_time_epoch": int(time()),
                    **rs,
                    **self.parse_detail(await response.text()),
                    'charts_nasional': self.__charts_nasional,
                    'jumlah_rumah_sakit_nasional': self.__jumlah_rumah_sakit,
                    "path_data_raw": f'S3://ai-pipeline-raw-data/data/data_statistics/kemkes/list_rumah_sakit_nasional/2024/json/{rs["nama"].lower().replace(" ", "_")}.json',
                }
                return data

if(__name__ == '__main__'): 
    asyncio.run(KemkesRS()._watch_beanstalk())


# {
#     rekap_nasional: {

#     },
#     rekap_provinsi: {

#     }
# }