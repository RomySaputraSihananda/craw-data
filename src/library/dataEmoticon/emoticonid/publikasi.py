
from aiohttp import ClientSession
from src.helpers import Parser, ConnectionS3, Datetime

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
                'link': link,
                'domain': (link_split := link.split('/')[:-1])[2],
                'crawling_time': Datetime.now(),
                'crawling_time_epoch': int(time()),
                'title': (title := soup.select_one('.content .row .col p:first-child').get_text().strip()),
                'tag': [*link_split[2:], title],
                'file': (file := soup.select_one('.content .btn.btn-info.btn-sm.rounded')['href']),
                **dict(soup.select('.row.text-center > .col').map(get_detail)),
                'description': soup.select_one('.content .col').get_text().strip().split('( Author )')[-1].strip(),
                'path_data_raw': [
                    f'S3://ai-pipeline-statistics/data/data_raw/data statistic/satu data kementrian pertanian/publikasi/json/{title}.json',
                    f'S3://ai-pipeline-statistics/data/data_raw/data statistic/satu data kementrian pertanian/publikasi/pdf/{(file_name := file.split("/")[-1])}'
                ],
                'path_data_clean': [
                    f'S3://ai-pipeline-statistics/data/data_clean/data statistic/satu data kementrian pertanian/publikasi/json/{title}.json',
                    f'S3://ai-pipeline-statistics/data/data_clean/data statistic/satu data kementrian pertanian/publikasi/pdf/{file_name}'
                ],   
            } 

            ConnectionS3.upload(data, data['path_data_raw'][0].replace('S3://ai-pipeline-statistics/', ''))
        async with session.get(file) as response:
            ConnectionS3.upload_content(await response.read(), data['path_data_raw'][1].replace('S3://ai-pipeline-statistics/', ''))

if(__name__ == '__main__'):
    import asyncio
    async def main():
        i = 0
        while(True):
            response = requests.get(f'https://satudata.pertanian.go.id/datasets/publikasi/{i}')
            print(i)
            cards = Parser(response.text).select('.col-sm-12.pt-2').map(lambda e: e)
            await asyncio.gather(*(process_card(card) for card in cards))
            if(not cards):  break
            i += 5

    asyncio.run(main())
    # BaseEmoticonId().start()