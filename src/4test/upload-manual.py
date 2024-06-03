import requests
import pandas
import asyncio
from json import loads
from time import time

from src.helpers import Datetime, Iostream, ConnectionS3
from src.library.dataDivtik.wiktionary.wiktionary import Wiktionary
from src.library.dataDivtik.kamuslengkap.kamuslengkap import BaseKamusLengkap
from src.helpers import Parser

filter = lambda x: x.strip().lower().replace(" ", "_")

def get_data(url):
    for data in [data for data in pandas.read_csv('https://docs.google.com/spreadsheets/d/1eEI6tNBQ5O8n6J_qXk-CPZD1EgPxDBcjF3zEtpGtAFU/export?format=csv&gid=394669076').to_dict('records') if url in str(data['link_kamus_bahasa_daerah'])]:
        return data

def main(url):
    data = get_data(url)
    if(not data): return
    with open('src/4test/manual.json', 'r') as f:
        manual = loads(f.read())
    result: dict = {
        "link": (link := data['link_kamus_bahasa_daerah']),
        "domain": (link_split := link.split('/'))[2],
        "tag": link_split[2:],

        **manual,

        "crawling_time": Datetime.now(),
        "crawling_time_epoch": int(time()),
        "path_data_raw": f'S3://ai-pipeline-raw-data/data/data_descriptive/data_kamus/{(Provinsi := filter(data["Provinsi"]))}/{(nama_bahasa := filter(data["nama_bahasa"]))}/json/{filter(link_split[-1].split(".")[0])}.json'
    }
    ConnectionS3.upload(result, result["path_data_raw"].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
if(__name__ == '__main__'): 
    main('https://dologhuluanjaya.blogspot.com/2012/11/kamus-bahasa-simalungun-indonesia.html')