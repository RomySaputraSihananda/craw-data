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
            'Cookie': 'lotame_domain_check=pertanian.go.id;_cc_id=4e006a7ade03fd4b2eb5853083e57138;_ga_V1F3WXCYQT=GS1.1.1714378104.2.0.1714378104.60.0.229850642;_gid=GA1.3.1673470873.1714364665;cf_use_ob=443;panoramaIdType=panoDevice;cf_clearance=g9.AbL1TKIsl_RLP3VTEuHlKwNeLsIf_dlp4WaO9MPE-1714380895-1.0.1.1-7QVI8nqYnQeJZpWZAWnv9pm8I8UYeVWiCOXtpfLQYTKQN51Vyc_57o0XzF2PIJvm3TNcalEbfmKKr0iDKzb96w;_ga=GA1.3.841809683.1714033655;_gat_gtag_UA_107417379_1=1;panoramaId=c81add31d09f396e316ea2d533ec185ca02ce9a7fcf1a3517d34d3483b529018;_gat_gtag_UA_123405247_1=1;__dtsu=6D001714033644628FB4E565E5B91530;_ga_8Q4BMH31EM=GS1.1.1714378113.14.1.1714381048.0.0.0;_ga_M9SFY5S827=GS1.1.1714378110.13.1.1714380930.0.0.0;cf_ob_info=520:87be11f03e2b5ea0:CGK;ci_session=a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%227263766c5fe9fe12837c7254c5e6b448%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A11%3A%2210.24.11.10%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A50%3A%22Mozilla%2F5.0%20%28X11%3B%20Linux%20x86_64%3B%20rv%3A124.0%29%20Gecko%2F20%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1714380904%3B%7D6c03da89cb88a3e20ea8e124a9d57617;panoramaId_expiry=1714982895056'
        })
    
    @staticmethod
    @Decorator.check_path
    async def write_data_frame(data_frame: DataFrame, path: str, info: dict, **kwargs) -> tuple:
        await asyncio.to_thread(data_frame.to_excel,  (rill_path := path.replace('S3://ai-pipeline-statistics/', '')), index=False)
        print(rill_path)
        # ConnectionS3.upload_content(rill_path, rill_path)
        return path, info
    
    @staticmethod
    def send_metadata(func: Callable[..., None]) -> Callable[..., None]:
        @wraps(func)
        async def wrapper(self, *args: Any, **kwargs: Any) -> None:
            try:
                [data] = await func(self, *args, **kwargs)
                
                (path, info) = data

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
                    "data": info,
                    "crawling_time": Datetime.now(),
                    "crawling_time_epoch": int(time()),
                    "path_data_raw": [path, (json_path := path.split('xlxs/')[0] + "json/metadata.json")],
                }

                Iostream.write_json(data, json_path.replace('S3://ai-pipeline-statistics/', ''), indent=4)
            except Exception as e:
                raise e
            # ConnectionS3.upload(data, json_path.replace('S3://ai-pipeline-statistics/', ''))
        return wrapper

    def __get_provinces(self) -> list:
        return self.__requests.get('https://bdsp2.pertanian.go.id/bdsp/id/lokasi/getProv').json()
    
    def __get_kabupaten(self, fkode_prop: str) -> list:
        return self.__requests.post('https://bdsp2.pertanian.go.id/bdsp/id/lokasi/getKab',
                                    headers=self.__requests.headers,
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
        except IndexError as e:
            raise e
        except Exception as e:
            await asyncio.sleep(5)
            return await self.__get_komoditas(**kwargs)
    
    
    async def __get_indikator(self, **kwargs) -> list:
        try:
            async with ClientSession() as session:
                async with session.post('https://bdsp2.pertanian.go.id/bdsp/id/indikator/getIndiByKomSubsek',
                                        data={
                                            'subsektorcd': kwargs.get('subsector').value,
                                            'komcd': kwargs.get('komoditas')["fkomcd"]
                                        }) as response:
            
                    return await asyncio.gather(*(self.__get_satuan(indikator=indikator, **kwargs) for indikator in loads(await response.text())))
        except IndexError as e:
            raise e
        except Exception as e:
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
            
                    return await asyncio.gather(*(self.__get_result(satuan=satuan, **kwargs) for satuan in loads(await response.text())))
        except IndexError as e:
            raise e
        except Exception as e:
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
            
                    soup: Parser = Parser(test := await response.text())
                    header: list = Array((table := soup.select_one('table')).select('thead tr td')).map(lambda e: e.get_text())
                    values: list = Array(table.select('tbody tr')).map(lambda e: [f.get_text() for f in e.select('td')])
                    footer: list = Array(table.select('tfoot tr td')).map(lambda e: e.get_text())


                    info: dict = {
                        key: soup.select('.col-md-4').map(lambda x: x.get_text().replace(':', '').strip())[i]
                        for i, key in enumerate(soup.select('.col-md-2').map(lambda x: x.get_text().strip()))
                    }

                    data_frame: DataFrame = DataFrame(columns=header, data=[*values, [len(values) + 1, *footer]])

                    path: str = f'S3://ai-pipeline-statistics/data/data_raw/bdsp/{provinsi_name.replace("/", " or ")}/{subsector_name.replace("/", " or ")}/{komoditas_name.replace("/", " or ")}/{indikator_name.replace("/", " or ")}/xlxs/{satuan_name.replace("/", " or ")}.xlsx'

                    return await self.write_data_frame(data_frame, path, info, **kwargs)

        except Exception as e:
            await asyncio.sleep(10)
            await self.__get_result(**kwargs)

    
    async def _get_by_subsector(self, subsector: Subsector, provinsi: dict):
        return await self.__get_komoditas(subsector=subsector, provinsi=provinsi)
    
    async def _get_all(self) -> None:
        for provinsi in self.__get_provinces():
            print(provinsi)
        for subsector in Subsector:
            print(subsector)


if(__name__ == '__main__'):
    asyncio.run(BaseBdsp()._get_all())

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

