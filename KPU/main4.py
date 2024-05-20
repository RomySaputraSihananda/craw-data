from logging import handlers
import logging
from loguru import logger
import requests
from requests import Session
import s3fs
# from loguru import logger

from aiohttp import ClientSession
from enum import Enum
from datetime import datetime
from time import time
from json import dumps

logging.basicConfig(level=logging.INFO, format='%(asctime)s [ %(levelname)s ] :: %(message)s',
                datefmt="%Y-%m-%dT%H:%M:%S", handlers=[
    handlers.RotatingFileHandler(f'pilegdpr_log/KEPULAUAN_RIAU.log'),
    logging.StreamHandler()
])

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
        # self.__s3 = s3fs.core.S3FileSystem(**{
        #         'key': 'GLZG2JTWDFFSCQVE7TSQ',
        #         'secret': 'VjTXOpbhGvYjDJDAt2PNgbxPKjYA4p4B7Btmm4Tw',
        #         'endpoint_url': 'http://192.168.180.9:8000',
        #         'anon': False,
        #         'asynchronous': True
        # })

        # self.__s3.connect_timeout = 10
    
    @staticmethod
    def filter_name_kode(func):
        def wrap(*args, **kwargs):
            datas = func(*args, **kwargs)
            return [(data['nama'], data['kode']) for data in datas]
        return wrap
    
    def download(self, tps_image, name_image):
        with self.__s3.open(name_image, 'wb') as file:
            file.write(self.__requests.get(tps_image).content)
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
    
    def __get_tps_images(self, kode_provinsi, kode_kabupaten, kode_kecamatan, kode_desa, kode_tps):
        response = self.__requests.get(link := f'https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/{self.__type_pemilu.value.split(";")[0]}/{kode_provinsi}/{kode_kabupaten}/{kode_kecamatan}/{kode_desa}/{kode_tps}.json')
        
        return response.json()['images']
    
    def get_detail_by_province(self, provinsi: Province): 
        banyak_kabupaten = self.__get_kabupaten(kode_provinsi := provinsi.value)
        for nama_kabupaten, kode_kabupaten in banyak_kabupaten:
            banyak_kecamatan = self.__get_kecamatan(kode_provinsi, kode_kabupaten)
            for nama_kecamatan, kode_kecamatan in banyak_kecamatan:
                banyak_desa = self.__get_desa(kode_provinsi, kode_kabupaten, kode_kecamatan)
                for nama_desa, kode_desa in banyak_desa:
                    banyak_tps = self.__get_tps(kode_provinsi, kode_kabupaten, kode_kecamatan, kode_desa)
                    for nama_tps, kode_tps in banyak_tps:
                        tps_images = self.__get_tps_images(kode_provinsi, kode_kabupaten, kode_kecamatan, kode_desa, kode_tps)
                        try:
                            name_images = []
                            for i, tps_image in enumerate(tps_images, start=1):
                                if(not tps_image): 
                                    logging.error(f'not image found in https://pemilu2024.kpu.go.id/{self.__type_pemilu.value.split(";")[1]}/hitung-suara/wilayah/{kode_provinsi}/{kode_kabupaten}/{kode_kecamatan}/{kode_desa}/{kode_tps}')
                                    continue
                                name_images.append((name_image := (nama_json := f"s3://ai-pipeline-statistics/data/data_raw/KPU/{self.__type_pemilu.name.replace("_", " ")}/image/{provinsi.name.replace('_',' ')}/{nama_kabupaten}/{nama_kecamatan}/{nama_desa}/{nama_tps}") + f"/gambar({i}).jpg"))
                                
                                self.download(tps_image, name_image)
                        except Exception as e:
                            print(e)
                            logging.error(f'not image found in https://pemilu2024.kpu.go.id/{self.__type_pemilu.value.split(";")[1]}/hitung-suara/wilayah/{kode_provinsi}/{kode_kabupaten}/{kode_kecamatan}/{kode_desa}/{kode_tps}')
                            continue
                                
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
                            print(
                                dumps(
                                    metadata,
                                    indent=4
                                )
                            )
                        
                            # with self.__s3.open(nama_json, 'w') as file:
                            #     file.write(
                            #         dumps(
                            #             metadata,
                            #             indent=4
                            #         )
                            #     )
                            # print(f"Success save {nama_json} in s3.")
                        except Exception as e:
                            logger.error(e)
if(__name__ == '__main__'):
    import asyncio
    Kpu(TypePemilu.Hasil_Hitung_Suara_DPD).get_detail_by_province(Province.KEPULAUAN_RIAU)