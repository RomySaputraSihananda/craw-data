
import requests

from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from typing import Any
from time import time

from src.helpers import ConnectionS3, Datetime, Iostream

class BaseSatuDataPertanianInfografis(Spider):
    start_urls = ['https://satudata.pertanian.go.id/datasets/infografis']

    def __init__(self, **kwargs: Any):
        super().__init__('pertanian-infografis', **kwargs)

    def start(self, *args, **kwargs) -> None:
        process = CrawlerProcess(get_project_settings())    
        process.crawl(BaseSatuDataPertanianInfografis)

        return process.start()
    
    def __download_image(self, urls: str):
        for url in urls:
            _, format = (file := url.split('/')[-1]).split('.') 

            if((response := requests.get(url)).status_code == 200):
                ConnectionS3.upload_content(response.content, (path := f's3://ai-pipeline-raw-data/data/data_statistics/satu_data_kementrian_pertanian/infografis/{format}/{file.lower().replace(" ", "_")}').replace('s3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
                yield path

    def parse(self, response, **kwargs: Any) -> Any:
        for card in response.css('.text-center'):
            data = {
                "link": (link := 'https://satudata.pertanian.go.id/datasets/infografis'),
                "source": (link_split := link.split('/')[:-1])[2],
                'tag': [*link_split[2:], 'infografis'],
                "title": 'Daftar Infografis',
                "sub_title": (title := card.css('::text').getall()[-1].strip()),
                "range_data": None,
                "create_date": None,
                "update_date": None,
                "desc": "Infografis adalah informasi yang disajikan dalam bentuk grafik agar lebih mudah dipahami.",
                "category": "infografis",
                "sub_category": None,
                'crawling_time': Datetime.now(),
                'crawling_time_epoch': int(time()),
                "table_name": None,
                "country_name": "Indonesia",
                "level": "Nasional",
                "stage": "Crawling data",
                "update_schedule": "every three months and yearly",
                'data': {
                    'img_urls': (img_urls := [
                        card.css('img::attr(src)').get(),
                        *['https://satudata.pertanian.go.id/assets/docs/infografis/' + img['photo'] for img in requests.get('https://satudata.pertanian.go.id/galeri/photo/' + card.css('.text-center .link-box.rounded:last-child a::attr(data-id)').get()).json()]
                    ])
                },      
                'path_data_raw': [
                    f's3://ai-pipeline-raw-data/data/data_statistics/satu_data_kementrian_pertanian/infografis/json/{title.lower().replace(" ", "_")}.json',
                    *list(self.__download_image(img_urls))
                ],
            }

            ConnectionS3.upload(data, data['path_data_raw'][0].replace('s3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
            print(data)

if(__name__ == '__main__'):
    BaseSatuDataPertanianInfografis().start()
