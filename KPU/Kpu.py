from logging import handlers
import logging
from loguru import logger
import requests
import asyncio
import click
from requests import Session
import s3fs
import os
# from loguru import logger

from aiohttp import ClientSession
from enum import Enum
from datetime import datetime
from time import time
from json import dumps

class Province(Enum):
    ACEH = "11"
    BALI = "51"
    BANTEN = "36"
    BENGKULU = "17"
    DAERAH_ISTIMEWA_YOGYAKARTA = "34"
    DKI_JAKARTA = "31"
    GORONTALO = "75"
    JAMBI = "15"
    JAWA_BARAT = "32"
    JAWA_TENGAH = "33"
    JAWA_TIMUR = "35"
    KALIMANTAN_BARAT = "61"
    KALIMANTAN_SELATAN = "63"
    KALIMANTAN_TENGAH = "62"
    KALIMANTAN_TIMUR = "64"
    KALIMANTAN_UTARA = "65"
    KEPULAUAN_BANGKA_BELITUNG = "19"
    KEPULAUAN_RIAU = "21"
    LAMPUNG = "18"
    LUAR_NEGERI = "99"
    MALUKU = "81"
    MALUKU_UTARA = "82"
    NUSA_TENGGARA_BARAT = "52"
    NUSA_TENGGARA_TIMUR = "53"
    PAPUA = "91"
    PAPUA_BARAT = "92"
    PAPUA_BARAT_DAYA = "96"
    PAPUA_PEGUNUNGAN = "95"
    PAPUA_SELATAN = "93"
    PAPUA_TENGAH = "94"
    RIAU = "14"
    SULAWESI_BARAT = "76"
    SULAWESI_SELATAN = "73"
    SULAWESI_TENGAH = "72"
    SULAWESI_TENGGARA = "74"
    SULAWESI_UTARA = "71"
    SUMATERA_BARAT = "13"
    SUMATERA_SELATAN = "16"
    SUMATERA_UTARA = "12"

class TypePemilu(Enum):
    Hasil_Hitung_Suara_DPR = 'pdpr;pilegdpr'
    Hasil_Hitung_Suara_DPRD_PROV = 'pdprdp;pilegdprd_prov'
    Hasil_Hitung_Suara_DPRD_KAB = 'pdprdk;pilegdprd_kab'
    Hasil_Hitung_Suara_DPD = 'pdpd;pemilu_dpd'

class Kpu():
    def __init__(self, type_pemilu: TypePemilu) -> None:
        self.__requests = Session()
        self.__type_pemilu = type_pemilu

        self.__s3 = s3fs.core.S3FileSystem(**{
                'key': 'GLZG2JTWDFFSCQVE7TSQ',
                'secret': 'VjTXOpbhGvYjDJDAt2PNgbxPKjYA4p4B7Btmm4Tw',
                'endpoint_url': 'http://192.168.180.9:8000',
                'anon': False,
                'asynchronous': True
        })

        self.__s3.connect_timeout = 10
    
    @staticmethod
    def filter_name_kode(func):
        def wrap(*args, **kwargs):
            datas = func(*args, **kwargs)
            return [(data['nama'], data['kode']) for data in datas]
        return wrap
    
    async def download(self, tps_image, name_image):
        async with ClientSession() as session:
            async with session.get(tps_image) as response:
                with self.__s3.open(name_image, 'wb') as file:
                    await file.write(await response.read())
                    print(f"Success save {name_image} in s3.")
        
    @filter_name_kode 
    def __get_kabupaten(self, kode_provinsi):
        response = self.__requests.get(f'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{kode_provinsi}.json')
        return response.json()

    @filter_name_kode 
    def __get_kecamatan(self, kode_provinsi, kode_kabupaten):
        response = self.__requests.get(f'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{kode_provinsi}/{kode_kabupaten}.json')
        return response.json()

    @filter_name_kode 
    def __get_desa(self, kode_provinsi, kode_kabupaten, kode_kecamatan):
        response = self.__requests.get(f'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{kode_provinsi}/{kode_kabupaten}/{kode_kecamatan}.json')
        return response.json()

    @filter_name_kode 
    def __get_tps(self, kode_provinsi, kode_kabupaten, kode_kecamatan, kode_desa):
        response = self.__requests.get(f'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{kode_provinsi}/{kode_kabupaten}/{kode_kecamatan}/{kode_desa}.json')
        return response.json()
    
    async def __get_tps_images(self, kode_provinsi, kode_kabupaten, kode_kecamatan, kode_desa, kode_tps):
        async with ClientSession() as session:
            async with session.get(f'https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/{self.__type_pemilu.value.split(";")[0]}/{kode_provinsi}/{kode_kabupaten}/{kode_kecamatan}/{kode_desa}/{kode_tps}.json') as response:
                response_json: dict = await response.json()
                return response_json['images']
            
    async def get_detail_by_province(self, provinsi: Province):
        print(provinsi.name)
        # await asyncio.gather(*(self.get_detail_by_kabupaten(nama_kabupaten, kode_kabupaten, provinsi) for nama_kabupaten, kode_kabupaten in self.__get_kabupaten(provinsi.value)))
        for nama_kabupaten, kode_kabupaten in self.__get_kabupaten(provinsi.value):
            await self.get_detail_by_kabupaten(nama_kabupaten, kode_kabupaten, provinsi)
    
    async def get_detail_by_kabupaten(self, nama_kabupaten, kode_kabupaten, provinsi: Province):
        print(provinsi.name, nama_kabupaten)
        # await asyncio.gather(*(self.get_detail_by_kecamatan(nama_kecamatan, kode_kecamatan, nama_kabupaten, kode_kabupaten, provinsi) for nama_kecamatan, kode_kecamatan in self.__get_kecamatan(provinsi.value, kode_kabupaten)))
        for nama_kecamatan, kode_kecamatan in self.__get_kecamatan(provinsi.value, kode_kabupaten):
            await self.get_detail_by_kecamatan(nama_kecamatan, kode_kecamatan, nama_kabupaten, kode_kabupaten, provinsi)

    async def get_detail_by_kecamatan(self, nama_kecamatan, kode_kecamatan, nama_kabupaten, kode_kabupaten, provinsi: Province):
        print(provinsi.name, nama_kabupaten, nama_kecamatan)
        # await asyncio.gather(*(self.get_detail_by_desa(nama_desa, kode_desa, nama_kecamatan, kode_kecamatan, nama_kabupaten, kode_kabupaten, provinsi) for nama_desa, kode_desa in self.__get_desa(provinsi.value, kode_kabupaten, kode_kecamatan)))
        for nama_desa, kode_desa in self.__get_desa(provinsi.value, kode_kabupaten, kode_kecamatan):
            await self.get_detail_by_desa(nama_desa, kode_desa, nama_kecamatan, kode_kecamatan, nama_kabupaten, kode_kabupaten, provinsi)
        
    async def get_detail_by_desa(self, nama_desa, kode_desa, nama_kecamatan, kode_kecamatan, nama_kabupaten, kode_kabupaten, provinsi: Province):
        print(provinsi.name, nama_kabupaten, nama_kecamatan, nama_desa)
        # await asyncio.gather(*(self.get_detail_by_tps(nama_tps, kode_tps, nama_desa, kode_desa, nama_kecamatan, kode_kecamatan, nama_kabupaten, kode_kabupaten, provinsi) for nama_tps, kode_tps in self.__get_tps(provinsi.value, kode_kabupaten, kode_kecamatan, kode_desa)))    
        for nama_tps, kode_tps in self.__get_tps(provinsi.value, kode_kabupaten, kode_kecamatan, kode_desa):
            await self.get_detail_by_tps(nama_tps, kode_tps, nama_desa, kode_desa, nama_kecamatan, kode_kecamatan, nama_kabupaten, kode_kabupaten, provinsi)
    async def get_detail_by_tps(self, nama_tps, kode_tps, nama_desa, kode_desa, nama_kecamatan, kode_kecamatan, nama_kabupaten, kode_kabupaten, provinsi: Province):
        print(provinsi.name, nama_kabupaten, nama_kecamatan, nama_desa, nama_tps)
        tps_images = await self.__get_tps_images(kode_provinsi := provinsi.value, kode_kabupaten, kode_kecamatan, kode_desa, kode_tps)
        nama_json = f"s3://ai-pipeline-statistics/data/data_raw/KPU/{self.__type_pemilu.name.replace('_', ' ')}/image/{provinsi.name.replace('_',' ')}/{nama_kabupaten}/{nama_kecamatan}/{nama_desa}/{nama_tps}"
        try:
            name_images = []
            tasks = []
            for i, tps_image in enumerate(tps_images, start=1):
                if not tps_image:
                    logging.error(f'no image found in https://pemilu2024.kpu.go.id/{self.__type_pemilu.value.split(";")[1]}/hitung-suara/wilayah/{kode_provinsi}/{kode_kabupaten}/{kode_kecamatan}/{kode_desa}/{kode_tps} key {tps_image}')
                    continue

                name_images.append((name_image := nama_json + f"/gambar({i}).jpg"))
                tasks.append(self.download(tps_image, name_image))
            await asyncio.gather(*tasks)
        except Exception as e:
            logging.error(e)
                
        try: 
            metadata = {
                'link': f'https://pemilu2024.kpu.go.id/{self.__type_pemilu.value.split(";")[1]}/hitung-suara/wilayah/{kode_provinsi}/{kode_kabupaten}/{kode_kecamatan}/{kode_desa}/{kode_tps}',
                'domain': 'kpu.go.id',
                'tag': [
                    'kpu',
                    'hasil hitung suara'
                ],
                'province': provinsi.name.replace('_',' '),
                'city': nama_kabupaten,
                'district': nama_kecamatan,
                'subdistrict': nama_desa,
                'tps': nama_tps,
                'path_data_raw': [*name_images, (nama_json := f'{nama_json}/metadata.json')],
                'crawling_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'crawling_time_epoch': int(time())
            }
        
            with self.__s3.open(nama_json, 'w') as file:
                await file.write(
                    dumps(
                        metadata,
                        indent=4
                    )
                )
            print(f"Success save {nama_json} in s3.")
        except Exception as e:
            raise e
            logger.error(e)

@click.command()
@click.argument('provinsi', metavar='Provinsi', type=click.Choice(Province._member_names_))
@click.argument('type', metavar='Type', type=click.Choice(TypePemilu._member_names_))
def main(**kwargs):
    path = f'{os.getcwd()}/{(type := kwargs.get("type"))}/{(provinsi := kwargs.get("provinsi"))}.log'
    
    if (not os.path.exists(data := os.path.dirname(path))): os.makedirs(data)
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [ %(levelname)s ] :: %(message)s',
                datefmt="%Y-%m-%dT%H:%M:%S", handlers=[
        handlers.RotatingFileHandler(path),
        logging.StreamHandler()
    ])

    asyncio.run(
        Kpu(
            TypePemilu[type]
        )
        .get_detail_by_province(
            Province[provinsi]
        )
    )

if(__name__ == '__main__'):
    main()