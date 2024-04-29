import asyncio
import requests

from time import time
from pandas import DataFrame
from json import dumps, loads
from requests import Session, Response
from aiohttp import ClientSession
from functools import wraps
from typing import Callable, Any, final

from .subsector import Subsector

from src.helpers import Parser, Decorator, Datetime, Iostream, ConnectionS3
from src.helpers.parser import Array

class BaseBdsp():
    def __init__(self) -> None:
        self.__requests: Session = Session() 
        self.__requests.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
            'Content-Type': 'application/x-www-form-urlencoded',

        })
    
    @staticmethod
    @Decorator.check_path
    async def write_data_frame(data_frame: DataFrame, path: str, **kwargs) -> tuple:
        await asyncio.to_thread(data_frame.to_excel,  (rill_path := path.replace('S3://ai-pipeline-statistics/', '')), index=False)
        # ConnectionS3.upload_content(rill_path, rill_path)
        return (path, kwargs.get('info'))
    
    @staticmethod
    def send_metadata(func: Callable[..., None]) -> Callable[..., None]:
        @wraps(func)
        async def wrapper(self, *args: Any, **kwargs: Any) -> None:
            data = await func(self, *args, **kwargs)

            path, info = data
            print(info)

            data: dict = {
                "link": (link := "https://11ap.pertanian.go.id/portalstatistik/bdsp/lokasi"),
                "domain": (link_split := link.split('/'))[2],
                "tag": [
                    *link_split[2:], 
                    kwargs.get('indikator')['findinm'],
                    kwargs.get('komoditas')['fkomnm'],
                    kwargs.get('subsector').name,
                    kwargs.get('provinsi')['nama_prop']
                ],
                "": info,
                "crawling_time": Datetime.now(),
                "crawling_time_epoch": int(time()),
                "path_data_raw": [*path, (json_path := path[0].split('xlxs/')[0] + "json/metadata.json")],
            }

            Iostream.write_json(data, json_path.replace('S3://ai-pipeline-statistics/', ''), indent=4)
            # ConnectionS3.upload(data, json_path.replace('S3://ai-pipeline-statistics/', ''))
        return wrapper

    def __get_provinces(self) -> list:
        return self.__requests.get('https://bdsp2.pertanian.go.id/bdsp/id/lokasi/getProv').json()
    
    def __get_kabupaten(self, fkode_prop: str) -> list:
        return self.__requests.post('https://bdsp2.pertanian.go.id/bdsp/id/lokasi/getKab',
                                    data={
                                        'fkode_prop': fkode_prop
                                    }).json()
        
    async def __get_komoditas(self, **kwargs) -> list:
        try:
            async with ClientSession() as session:
                async with session.post('https://bdsp2.pertanian.go.id/bdsp/id/komoditas/getKomBySubsektor',
                                data={
                                    'subsektorcd': kwargs.get('subsector').value
                                }) as response:
            
                    return await asyncio.gather(*(self.__get_indikator(komoditas=komoditas, **kwargs) for komoditas in loads(await response.text())))
        except:
            await asyncio.sleep(5)
            return await self.__get_komoditas(**kwargs)
    
    
    async def __get_indikator(self, **kwargs) -> list:
        try:
            async with ClientSession() as session:
                async with session.post('https://bdsp2.pertanian.go.id/bdsp/id/indikator/getIndiByKomSubsek',
                                        headers=self.__requests.headers,
                                        data={
                                            'subsektorcd': kwargs.get('subsector').value,
                                            'komcd': kwargs.get('komoditas')["fkomcd"]
                                        }) as response:
            
                    return await asyncio.gather(*(self.__get_satuan(indikator=indikator, **kwargs) for indikator in loads(await response.text())))
        except:
            await asyncio.sleep(7)
            return await self.__get_indikator(**kwargs)
    
    @send_metadata
    async def __get_satuan(self, **kwargs) -> list:
        try:
            async with ClientSession() as session:
                async with session.post('https://bdsp2.pertanian.go.id/bdsp/id/satuan/getSatuan',
                                        headers=self.__requests.headers,
                                        data={
                                            'subsektorcd': kwargs.get('subsector').value,
                                            'komcd': kwargs.get('komoditas')["fkomcd"],
                                            'indikatorcd': kwargs.get('indikator')["findicd"]
                                        }) as response:
            
                    data = await asyncio.gather(*(self.__get_result(satuan=satuan, **kwargs) for satuan in loads(await response.text())))
                    return data
        except:
            await asyncio.sleep(8)
            return await self.__get_satuan(**kwargs)

    async def __get_result(self, **kwargs) -> str:
        try:
            async with ClientSession() as session:
                async with session.post('https://bdsp2.pertanian.go.id/bdsp/id/lokasi/result',
                                        headers=self.__requests.headers,
                                        data={
                                            'subsektorcd': (subsector := kwargs.get('subsector')).value,
                                            'subsektornm': (subsector_name := subsector.name).replace('_', ' ').title(),
                                            'komoditas': (komoditas := kwargs.get('komoditas'))["fkomcd"],
                                            'komoditasnm': (komoditas_name := komoditas["fkomnm"]),
                                            'indikator': (indikator := kwargs.get('indikator'))["findicd"],
                                            'indikatornm': (indikator_name := indikator["findinm"]),
                                            'level': '03',
                                            'levelnm': 'Kabupaten',
                                            'prov': (provinsi := kwargs.get('provinsi'))['fkode_prop'],
                                            'provnm': (provinsi_name := provinsi["nama_prop"]),
                                            'sts_angka': '6',
                                            'sts_angkanm': 'Angka Tetap',
                                            'sumb_data': '00',
                                            'sumb_datanm': '-- Pilih Sumber Data --',
                                            'tahunAwal': '1970',
                                            'tahunAkhir': '2024',
                                            'satuan': (satuan := kwargs.get('satuan'))["fkeyid"],
                                            'satuannm': (satuan_name := satuan["fsatuan"]),
                                            'judul': 'lokasi',
                                        }
                                    ) as response:
            
                    soup: Parser = Parser(await response.text())
                    header: list = Array((table := soup.select_one('table')).select('thead tr td')).map(lambda e: e.get_text())
                    values: list = Array(table.select('tbody tr')).map(lambda e: [f.get_text() for f in e.select('td')])
                    footer: list = Array(table.select('tfoot tr td')).map(lambda e: e.get_text())


                    info: dict = {
                        key: soup.select('.col-md-4').map(lambda x: x.get_text().replace(':', '').strip())[i]
                        for i, key in enumerate(soup.select('.col-md-2').map(lambda x: x.get_text().strip()))
                    }

                    data_frame: DataFrame = DataFrame(columns=header, data=[*values, [len(values) + 1, *footer]])

                    path: str = f'S3://ai-pipeline-statistics/data/data_raw/bdsp/{provinsi_name.replace("/", " or ")}/{subsector_name.replace("/", " or ")}/{komoditas_name.replace("/", " or ")}/{indikator_name.replace("/", " or ")}/xlxs/{satuan_name.replace("/", " or ")}.xlsx'

                    return await self.write_data_frame(data_frame, path, info=info, **kwargs)

        except Exception as e:
            await asyncio.sleep(10)
            await self.__get_result(**kwargs)

    
    async def start(self, subsector):
        provinsi = {
            "fkode_prop": "35",
            "nama_prop": "Jawa Timur"
        }

        data = await self.__get_komoditas(subsector=subsector, provinsi=provinsi)

if(__name__ == '__main__'):
    asyncio.run(BaseBdsp().start(Subsector.HORTIKULTURA))

    # import requests

    # headers = 

    # data = 

    # response = requests.post(
    #     'https://bdsp2.pertanian.go.id/bdsp/id/site/writeexcel/resultToExcel',
    #     headers=headers,
    #     data=data,
    # )

    # with open('test.xls', 'wb') as file:
    #         file.write(response.content)

