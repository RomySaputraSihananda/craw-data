import asyncio

from json import dumps
from enum import Enum
from aiohttp import ClientSession
from functools import reduce
from time import time
from requests import Response, Session

from src.helpers import Datetime, Iostream, ConnectionS3

class Institution(Enum):
    PONTREN = '1'
    PKPPS = '2'
    SPM = '3'
    PDF = '4'
    MDT = '7'
    LPQ = '6'
    MA_HAD_ALY = '5'

class Tahun_Ajaran(Enum):
    GANJIL_2023_2024 = '13'
    GENAP_2022_2023 = '12'
    GANJIL_2022_2023 = '5'
    GENAP_2021_2022 = '4'

class BaseKemenagPonses:
    def __init__(self) -> None:
        self.__requests: Session = Session()
        self.__requests.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'
        })
    
    @staticmethod
    async def encrypt_id_emis(id: int):
        async with ClientSession() as session:
            async with session.get('http://192.168.29.154:6566/v1/encryptIDEmis',
                                   params={
                                       'id': id
                                   }) as response:
                return await response.text()

    async def _get_all_provinces(self, tahun_ajaran: Tahun_Ajaran, institution: Institution = Institution.PONTREN) -> dict:
        response: Response = self.__requests.get('https://api-emis.kemenag.go.id/v1/reports/pontren/institution-statistic',
                                                params={
                                                    'institution_group_id': institution.value,
                                                    'zone_type': 'province',
                                                    'page': '1',
                                                    'per_page': '1000',
                                                    'academic_year_id': tahun_ajaran.value,
                                                })
        response_json: dict = response.json()
        for province in response_json['results']:
            await self._get_by_province(province=province, institution_id=institution, summary_nasional=response_json["metadata"]["summary"], tahun_ajaran=tahun_ajaran)
            # break

    async def _get_by_province(self, **kwargs):
        response: Response = self.__requests.get('https://api-emis.kemenag.go.id/v1/reports/pontren/institution-statistic',
                                                params={
                                                    'institution_group_id': kwargs.get('institution_id').value,
                                                    'zone_type': 'city',
                                                    'province_id': kwargs.get('province')['province_id'],
                                                    'page': '1',
                                                    'per_page': '1000',
                                                    'academic_year_id': kwargs.get('tahun_ajaran').value,
                                                })
        response_json: dict = response.json()
        
        for city in response.json()['results']:
            await self._get_by_city(city=city, summary_province=response_json["metadata"]["summary"], **kwargs)
            # break
    
    async def _get_by_city(self, **kwargs):
        (page, paths)= (1, [])
        while(True):
            response: Response = self.__requests.get('https://api-emis.kemenag.go.id/v1/reports/pontren/institution-statistic', 
                                                    params={
                                                        'institution_group_id': kwargs.get('institution_id').value,
                                                        'zone_type': 'institution',
                                                        'city_id': kwargs.get('city')['city_id'],
                                                        'province_id': kwargs.get('province')['province_id'],
                                                        'page': page,
                                                        'per_page': '5',
                                                        'academic_year_id': kwargs.get('tahun_ajaran').value,
                                                    })
            if(not (results := response.json()['results'])): break

            
            paths.extend(await asyncio.gather(*(self._get_all_detail_institution(institution=institution, **kwargs) for institution in results)))

            page += 1
            # break

        result: dict = {
            "link": (link := 'https://emis.kemenag.go.id/pontren/statistik/pontren'),
            "domain": (link_split := link.split('/'))[2],
            "tag": link_split[2:],
            "crawling_time": Datetime.now(),
            "crawling_time_epoch": int(time()),
            "path_data_raw": [
                f'S3://ai-pipeline-raw-data/data/data_statistics/kemenag/ponpes/{kwargs.get("tahun_ajaran").name.lower()}/{kwargs.get("province")["province_name"].lower().replace(" ", "_")}/{kwargs.get("city")["city_name"].lower().replace(" ", "_")}/json/{kwargs.get("city")["city_name"].lower().replace(" ", "_")}.json',
                await self._get_excel(**kwargs),
                *paths
            ],
        }

        ConnectionS3.upload(result, result['path_data_raw'][0].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')

    async def _get_excel(self, **kwargs) -> None:
        async with ClientSession() as session:
            async with session.get(
                'https://api-emis.kemenag.go.id/v1/reports/pontren/export-institution-statistic',
                params={
                    'institution_group_id': kwargs.get('institution_id').value,
                    'type': 'xls',
                    'academic_year_id': kwargs.get('tahun_ajaran').value,
                    'zone_type': 'institution',
                    'city_id': kwargs.get('city')['city_id'],
                    'province_id': kwargs.get('province')['province_id'],
                }
            ) as response:
                ConnectionS3.upload_content(await response.read(), (path := f'S3://ai-pipeline-raw-data/data/data_statistics/kemenag/ponpes/{kwargs.get("tahun_ajaran").name.lower()}/{kwargs.get("province")["province_name"].lower().replace(" ", "_")}/{kwargs.get("city")["city_name"].lower().replace(" ", "_")}/xlsx/{kwargs.get("city")["city_name"].lower().replace(" ", "_")}.xlsx').replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
                return path


    async def _get_table_institution(self, institution_id: str, academic_year_id: str):
        async with ClientSession() as session:
            async with session.get(f'https://api-emis.kemenag.go.id/v1/institutions/pontren/public/institution-data-info',
                                   params={
                                        'forProfile': '1',
                                        'institution_id': institution_id,
                                        'academic_year_id': academic_year_id,
                                   },
                                   headers={
                                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'
                                   }) as response:
                return (await response.json())['results']
    
    async def _get_detail_institution(self, institution_id: str):
        async with ClientSession() as session:
            async with session.get(f'https://api-emis.kemenag.go.id/v1/institutions/pontren/public/identity/{await self.encrypt_id_emis(institution_id)}',
                                   headers={
                                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'
                                   }) as response:
                return (await response.json())['results']
        
    async def _get_all_detail_institution(self, **kwargs):
        try:
            data: dict = {
                    "link": (link := 'https://emis.kemenag.go.id/pontren/statistik/pontren'),
                    "domain": (link_split := link.split('/'))[2],
                    "tag": link_split[2:],
                    "crawling_time": Datetime.now(),
                    "crawling_time_epoch": int(time()),
                    f'detail_{kwargs.pop("institution_id").name.lower()}': reduce(lambda a, b: dict(a or {}, **(b or {})), await asyncio.gather(*(
                        self._get_detail_institution((institution_id := (institution := kwargs.pop('institution'))['institution_id'])),
                        self._get_table_institution(institution_id, academic_year_id=(tahun_ajaran := kwargs.pop('tahun_ajaran')).value))) 
                    ) | institution,
                    **kwargs,
                    "path_data_raw": f'S3://ai-pipeline-raw-data/data/data_statistics/kemenag/ponpes/{tahun_ajaran.name.lower()}/{kwargs.get("province")["province_name"].lower().replace(" ", "_")}/{kwargs.get("city")["city_name"].lower().replace(" ", "_")}/json/ponpes_detail/{institution_id}.json',
            }

            # Iostream.write_json(data, data['path_data_raw'].replace('S3://ai-pipeline-raw-data/', ''), indent=4)
            ConnectionS3.upload(data, data['path_data_raw'].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')

            return data['path_data_raw']
        except: ...

if(__name__ == '__main__'):
    baseKemenagPonses: BaseKemenagPonses = BaseKemenagPonses() 

    for tahun_ajaran in Tahun_Ajaran:
        asyncio.run(baseKemenagPonses._get_all_provinces(tahun_ajaran))
