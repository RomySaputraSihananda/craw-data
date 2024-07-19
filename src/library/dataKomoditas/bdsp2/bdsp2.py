# s3://ai-pipeline-raw-data/data/data_statistics/pertaniangoid/[nama_data]/[format_type]
import asyncio
import os

from time import time
from pandas import DataFrame
from json import dumps, loads
from functools import wraps
from typing import Callable, Any, final
from httpx import AsyncClient, Response
from greenstalk import Client

from .subsector import Subsector

from src.helpers import Parser, Decorator, Datetime, Iostream, ConnectionS3
from src.helpers.parser import Array

class BaseBdsp2:
    def __init__(self) -> None:
        self.__aseesion: AsyncClient = AsyncClient()
        self.__aseesion.headers.update({
            'Cookie': 'ci_session=a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22ee8bb89899370a96b0c875be93db2439%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A11%3A%2210.24.11.10%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A50%3A%22Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%3B%20rv%3A109.0%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1721377186%3B%7Dd3a363a6cd107d7c0aead196820b173c; twk_uuid_62a2ed2eb0d10b6f3e76a00a=%7B%22uuid%22%3A%221.WrwvJkdCf4895cH1cwC9JCzHoOY9yf7r7kQoenb4xpaKouPaznzqTBIjA72qiQkPfgBbNGrlaBEFAn4MqXv0t0VJ4Avb0o4nECEHPqXxWu0Em53qYVPdSCLRo%22%2C%22version%22%3A3%2C%22domain%22%3A%22pertanian.go.id%22%2C%22ts%22%3A1721375781295%7D; cf_clearance=OykT2oS1NKBVBqwE_RCdIBKJo4XcCR7a.2TuwASBrQg-1721377630-1.0.1.1-a246Qw2R5ZVFHkxNdcVeoYnE4W1LZfSwRwibesYjeYeGsVuA1doPeErPmJkcETtmmj_7Z7zwzcGFjg1N6vVlYA',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
        })

        self.__beanstalk_use: Client = Client(('192.168.150.21', 11300), use='dev-target-komoditas')
        self.__beanstalk_watch: Client = Client(('192.168.150.21', 11300), watch='dev-target-komoditas')
    
    @staticmethod
    async def write_data_frame(data_frame: DataFrame, path: str, **kwargs) -> tuple:
        rill_path = path.replace('S3://ai-pipeline-raw-data/', '')
        if not os.path.isdir(rill_path):
            os.makedirs(os.path.dirname(rill_path))

        data_frame.to_excel(rill_path, index=False)

        ConnectionS3.upload_content(rill_path, rill_path, 'ai-pipeline-raw-data')
        # os.remove(rill_path)

        return path           
    
    @staticmethod
    def build_data(**kwargs):
        return {
            "subsektor": (subsector := kwargs.get('subsector')).value,
            "subsektorcd": subsector.value,
            "subsektornm": subsector.name.title().replace('_', ' '),

            "indikator": (indikator := kwargs.get('indikator'))['findicd'],
            "indikatornm": indikator['findinm'],
            
            "prov": (provinsi := kwargs.get('provinsi'))['fkode_prop'],
            "provnm": provinsi['nama_prop'],

            "kab": (kabupaten := kwargs.get('kabupaten'))['fkode_kab'],
            "kabnm": kabupaten['nama_kab'],
            
            "level": "03",
            "levelnm": "Kabupaten",
            "satuan": "--",
            "satuannm": "-- Pilih Satuan --",   
            "sts_angka": "6",
            "sts_angkanm": "Angka Tetap",
            "sumb_data": "00",
            "sumb_datanm": "-- Pilih Sumber Data --",
            "tahunAwal": "1970",
            "tahunAkhir": "2024",
        }
    
    async def __get_indikator(self, subsector):
        return (
                await self.__aseesion.post(
                    'https://bdsp2.pertanian.go.id/bdsp/id/subsektor/getIndiBySubsektor',
                    data={  
                        'subsektorcd': subsector.value,
                    }
                )
            ).json()
    
    async def __get_provinces(self) -> list:
        return (
            await self.__aseesion.get('https://bdsp2.pertanian.go.id/bdsp/id/lokasi/getProv')
        ).json()
    
    async def __get_kabupaten(self, fkode_prop: str) -> list:
        return (
            await self.__aseesion.post(
                'https://bdsp2.pertanian.go.id/bdsp/id/lokasi/getKab',
                data={
                    'fkode_prop': fkode_prop
                }
            )
        ).json()

    async def _get_result(self, data):
        response: Response = await self.__aseesion.post(
            'https://bdsp2.pertanian.go.id/bdsp/id/komoditas/result',
            data=data
        )

        soup: Parser = Parser(response.text)
        header: list = Array((table := soup.select_one('table')).select('thead tr td')).map(lambda e: e.get_text())
        values: list = Array(table.select('tbody tr')).map(lambda e: [f.get_text() for f in e.select('td')])

        data_frame: DataFrame = DataFrame(columns=header, data=values)
        path = f'S3://ai-pipeline-raw-data/data/data_statistics/komoditas/pertaniangoid/' + '/'.join([data['provnm'], data['kabnm'], data['subsektornm'], 'xlsx', data['indikatornm']]).lower().replace(' ', '_').replace('.', '') + '.xlsx'

        return await self.write_data_frame(data_frame, path)

    async def start(self):
        indikators = await asyncio.gather(*(self.__get_indikator(sub) for sub in Subsector))
        provinces = await self.__get_provinces()
        kabupaten = await asyncio.gather(*(self.__get_kabupaten(province['fkode_prop']) for province in provinces))

        for i, subsector in enumerate(Subsector):
            for indikator in indikators[i]:
                for j, province in enumerate(provinces):
                    for kab in kabupatens if (kabupatens := kabupaten[j]) else []:
                        self.__beanstalk_use.put(
                            data := dumps(
                                self.build_data(
                                    subsector=subsector,
                                    indikator=indikator,
                                    provinsi=province,
                                    kabupaten=kab
                                ),
                                indent=4
                            )
                        )
                        print(data)
    async def consume(self):
        while(job := self.__beanstalk_watch.reserve()):
            try:
                data = loads(job.body)
                await self._get_result(data)
                self.__beanstalk_watch.delete()
            except:
                from time import sleep
                sleep(5)
                self.__beanstalk_watch.bury(job)

if(__name__ == '__main__'):
    baseBdsp2: BaseBdsp2 = BaseBdsp2()
    result = asyncio.run(
        # baseBdsp2._get_result(
        #     {'subsektor': '01', 'subsektorcd': '01', 'subsektornm': 'Tanaman Pangan', 'indikator': '0103', 'indikatornm': 'LUAS PANEN', 'prov': '11', 'provnm': 'Aceh', 'kab': '01', 'kabnm': 'Kab. Simeulue', 'level': '03', 'levelnm': 'Kabupaten', 'satuan': '--', 'satuannm': '-- Pilih Satuan --', 'sts_angka': '6', 'sts_angkanm': 'Angka Tetap', 'sumb_data': '00', 'sumb_datanm': '-- Pilih Sumber Data --', 'tahunAwal': '1970', 'tahunAkhir': '2024'}
        # )
        # baseBdsp2.start()
        baseBdsp2.consume()
    )