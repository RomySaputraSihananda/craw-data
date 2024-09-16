
from aiohttp import ClientSession
from src.helpers import Parser, ConnectionS3, Datetime, Iostream

from time import time

import requests

def get_detail(e):
    name, key = e.select('p')
    return name.get_text(), key.get_text()

async def process_card(card):
    link = card.select_one('.col-sm-12.pt-2 a:first-child')['href']
    async with ClientSession() as session:
        async with session.get(link) as response:
            soup: Parser = Parser(await response.text())

            data = {
                "link": link,
                "source": (link_split := link.split('/')[:-1])[2],
                'tag': link_split[2:],
                "title": (title := soup.select_one('.content .row .col p:first-child').get_text().strip()),
                "sub_title": None,
                "range_data": None,
                "create_date": None,
                "update_date": None,
                "desc": soup.select_one('.content .col').get_text().strip().split('( Author )')[-1].strip(),
                "category": "publikasi",
                "sub_category": None,
                'crawling_time': Datetime.now(),
                'crawling_time_epoch': int(time()),
                "table_name": None,
                "country_name": "Indonesia",
                "level": "Nasional",
                "stage": "Crawling data",
                "update_schedule": "every three months and yearly",
                'data': {
                    'file': (file := soup.select_one('.content .btn.btn-info.btn-sm.rounded')['href']),
                    **dict(soup.select('.row.text-center > .col').map(get_detail))
                },
                'path_data_raw': [
                    f's3://ai-pipeline-raw-data/data/data_statistics/satu_data_kementrian_pertanian/publikasi/json/{title.strip().lower().replace("/", " or ").replace(" ", "_")}.json',
                    f's3://ai-pipeline-raw-data/data/data_statistics/satu_data_kementrian_pertanian/publikasi/pdf/{(file_name := file.split("/")[-1]).lower().replace(" ", "_")}'
                ]
            }   

            ConnectionS3.upload(data, data['path_data_raw'][0].replace('s3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
            async with session.get(file) as response:
                ConnectionS3.upload_content(await response.read(), data['path_data_raw'][1].replace('s3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')


if(__name__ == '__main__'):
    import asyncio
    async def main():
        i = 150     
        while(True):
            response = requests.get(f'https://satudata.pertanian.go.id/datasets/publikasi/{i}')
            print(i)
            cards = Parser(response.text).select('.col-sm-12.pt-2').map(lambda e: e)
            await asyncio.gather(*(process_card(card) for card in cards))
            if(not cards):  break
            i += 5

    asyncio.run(main())
    # BaseEmoticonId().start()