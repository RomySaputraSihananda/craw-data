import pandas
import asyncio

from requests import Session
from urllib.parse import unquote
from aiohttp import ClientSession
from time import time
from json import dumps

from src.helpers import Datetime, ConnectionS3
error = [
    {'Provinsi': 'Sumatera Utara', 'Nama_Kota': None, 'nama_bahasa': 'Bahasa Batak Simalungun', 'link_kamus_bahasa_daerah': 'https://repositori.kemdikbud.go.id/16214/1/Kamus%20Bahasa%20Simalungun%20-%20Indonesia%20Edisi%20Kedua%20Tahun%202016.pdf', 'status_crawl': False, 'note': None, 'path': None}
]

async def download(data: dict):
    async with ClientSession() as session:
        async with session.get(link := unquote(data['link_kamus_bahasa_daerah']), 
                                headers={
                                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'
                                },
                                verify_ssl=False) as response:
            try:
                filter: function = lambda x: x.strip().lower().replace(" ", "_")
                name, format = (name_file := filter((link_split := link.split('/'))[-1])).split('.')

                result: dict = {
                    "link": link,
                    "domain": link_split[2],
                    "tag": link_split[2:],
                    "crawling_time": Datetime.now(),
                    "crawling_time_epoch": int(time()),
                    "path_data_raw": [
                        (json_path := f'S3://ai-pipeline-raw-data/data/data_descriptive/data_kamus/{(Provinsi := filter(data["Provinsi"]))}/{(nama_bahasa := filter(data["nama_bahasa"]))}/json/{(name := filter(name))}.json'),
                        (pdf_path := f'S3://ai-pipeline-raw-data/data/data_descriptive/data_kamus/{Provinsi}/{nama_bahasa}/{format}/{name_file}')
                    ]
                }

                ConnectionS3.upload(result, json_path.replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
                ConnectionS3.upload_content(await response.read(), pdf_path.replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
                # return json_path
            except:
                return ''
            
async def main(): 
    # data = await asyncio.gather(*(download(data) for data in pandas.read_csv('src/4test/data.csv').to_dict('records') if data['link_kamus_bahasa_daerah'].strip().endswith('.PDF')))
    data = await asyncio.gather(*(download(data) for data in error if data['link_kamus_bahasa_daerah'].strip().endswith('.pdf')))
    print(
        dumps(data)
    )
if(__name__ == '__main__'):
    asyncio.run(main())