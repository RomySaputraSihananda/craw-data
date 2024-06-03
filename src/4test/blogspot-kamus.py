import requests
import pandas
import asyncio

from time import time

from src.helpers import Datetime, Iostream, ConnectionS3
from src.library.dataDivtik.wiktionary.wiktionary import Wiktionary
from src.library.dataDivtik.kamuslengkap.kamuslengkap import BaseKamusLengkap
from src.helpers import Parser

filter = lambda x: x.strip().lower().replace(" ", "_")

def start():
    def filter(e):
        return [res for td in e.select('td') if (res := td.get_text().replace('=', '').replace('\n', '').strip())]
    
    data = [e for e in Parser(
        requests.get('https://tutuwawang.blogspot.com/2014/06/kamus-bahasa-hari-hari-ambon.html').text
    ).select('table tr').map(filter) if len(e) == 2]
    return [
            {
                'bahasa_ambon': d[0],
                'bahasa_indonesia': d[1]
            }
            for d in data
        ]
def get_data():
    with open('src/4test/data.txt', 'r') as f:
        def ok(e):
            g = e.split('=', 1)
            return { 
                'bahasa_melayu_riau': g[1].strip(),
                'bahasa_indonesia': g[0].strip()
            }
        return [
            ok(line) for line in f.read().split('\n')
        ]

    
def main(data):
    from .test import start
    result: dict = {
        "link": (link := data['link_kamus_bahasa_daerah']),
        "domain": (link_split := link.split('/'))[2],
        "tag": link_split[2:],
        
        "title": "Kategori:Kata bahasa Komering",
        "data": start(),

        "crawling_time": Datetime.now(),
        "crawling_time_epoch": int(time()),
        "path_data_raw": f'S3://ai-pipeline-raw-data/data/data_descriptive/data_kamus/{(Provinsi := filter(data["Provinsi"]))}/{(nama_bahasa := filter(data["nama_bahasa"]))}/json/{filter(link_split[-1].split(".")[0])}.json'
        # "path_data_raw": [
        #     f'S3://ai-pipeline-raw-data/data/data_descriptive/data_kamus/{(Provinsi := filter(data["Provinsi"]))}/{(nama_bahasa := filter(data["nama_bahasa"]))}/json/{filter(link_split[-1].split(".")[0])}.json',
        #     f'S3://ai-pipeline-raw-data/data/data_descriptive/data_kamus/{(Provinsi := filter(data["Provinsi"]))}/{(nama_bahasa := filter(data["nama_bahasa"]))}/pdf/bahasa_kubu_kbpj.pdf'
        # ]
    }
    # print(result['data'])
    ConnectionS3.upload(result, result["path_data_raw"].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')

    # ConnectionS3.upload(result, result["path_data_raw"][0].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
    # ConnectionS3.upload_content('src/4test/bahasa_kubu_kbpj.pdf', result["path_data_raw"][1].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
    
    # print(result)

if(__name__ == '__main__'):
    main(
        {'Provinsi': 'Sumatera Selatan', 'Nama_Kota': None, 'nama_bahasa': 'Komering', 'link_kamus_bahasa_daerah': 'https://id.wiktionary.org/wiki/Kategori:Kata_bahasa_Komering', 'status_crawl': False, 'note': None, 'path': None}
    )