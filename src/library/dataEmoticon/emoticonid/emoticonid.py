from scrapy import Spider
from typing import Any, Iterable
from scrapy.http import Request, Response
from json import dumps, loads
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.helpers import Datetime, Iostream, ConnectionS3, Parser 
from src.helpers.parser import Array
from scrapy.http import Request, Response
from scrapy.selector.unified import Selector
from time import time, sleep
import requests
from greenstalk import Client

class BaseEmoticonId(Spider):
    start_urls = [
        'https://emoticon.id/kb/perjalanan-tempat/', 
        # 'https://emoticon.id/kb/simbol/', 
        'https://emoticon.id/kb/aktivitas/', 
        'https://emoticon.id/kb/bendera/', 
        'https://emoticon.id/kb/binatang-alam/', 
        'https://emoticon.id/kb/makanan-minuman/', 
        'https://emoticon.id/kb/objek/', 
        'https://emoticon.id/kb/wajah-orang/'
    ]

    def __init__(self, **kwargs: Any):
        self.__s3: bool = kwargs.get('s3')
        super().__init__('emoticon-spider')
        self.__beanstalk_use: Client = Client(('192.168.150.21', 11300), use='dev-target-emoji')
        self.__beanstalk_watch: Client = Client(('192.168.150.21', 11300), watch='dev-target-emoji')
    
    def start_requests(self) -> Iterable[Request]:
        # for url in self.start_urls:
        #     yield Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}, dont_filter=True)

        while((job := self.__beanstalk_watch.reserve())):
            response = Request(job.body, cb_kwargs={'job': job}, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}, dont_filter=True)
            # sleep(5)
            yield response

    def parse(self, response: Response, **kwargs: Any) -> Any:
        job = kwargs.get('job')
    # def __process_emoticon(self, response: Response, **kwargs: Any) -> Any:
        container = response.css('div.pakb-article-content')
        description: list = [p.css('::text').get() for p in response.css('div.pakb-article-content > p')[:2]]
        # keys: list = [h2.css('::text').get() for h2 in container.css('h2')]
        keys: list = ['Contoh penggunaan', 'Informasi emoji', 'Versi platform']
        values: list = (
            [li.css('::text').get() for li in container.css('ul li')],
            {
                tr.css('td:first-child strong::text').get(): {a.css('::text').get(): a.css('::attr(href)').get() for a in tr.css('td:last-child a')} or tr.css('td:last-child::text').get() 
                for tr in container.css('table tbody tr')
            },
            {
                dl.css('dd::text').get().strip(): dl.css('img::attr(src)').get()
                for dl in container.css('dl')
            }
        )

        data: dict = {
            'link': response.url,
            'domain': 'emoticon.id',
            'crawling_time': Datetime.now(),
            'crawling_time_epoch': int(time()),
            'tag': [
                'emoticon.id',
                (category := [a.css('a::text').get() or a.css('span::text').get() for a in response.css('.uk-margin-medium-bottom.uk-breadcrumb.pakb-link.pakb-secondary-color li')][1])
            ],
            'title': (title := response.css('h1::text').get()),
            'data': {
                'description': description,
                **({keys[i]: value for i, value in enumerate(values)} if keys else {})
            },
            'path_data_raw': [
                f'S3://ai-pipeline-statistics/data/data_raw/Emoticon/emoticonid/{category}/{title}/json/{title}.json'
            ]
        } 


        for platform, url in data['data']['Versi platform'].items():
            data['path_data_raw'].append(
                (png_path := f'S3://ai-pipeline-statistics/data/data_raw/Emoticon/emoticonid/{category}/{title}/png/{platform}.png')
            )
            ConnectionS3.upload_content(requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}).content, png_path.replace('S3://ai-pipeline-statistics/', ''))

        ConnectionS3.upload(data, data['path_data_raw'][0].replace('S3://ai-pipeline-statistics/', ''))

        self.__beanstalk_watch.delete(job)

    def __handle_error(self, failure: Response):
        request = failure.request
        if failure.value.response.status != 200:
            self.logger.error(f"Request failed: {request.url}, retrying...")
            yield request.replace(dont_filter=True)

    # def parse(self, response: Response, **kwargs: Any) -> Any: 
    #     for link in (li.css('::attr(href)').get() for li in response.css('.uk-margin-large-top.uk-list.uk-list-large.pakb-list.pakb-primary-color.link-icon-right li a')):
    #         self.__beanstalk_use.put(link)
            # yield response.follow(link, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'}, callback=self.__process_emoticon, errback=self.__handle_error) 

    def start(self, *args, **kwargs) -> None:
        process = CrawlerProcess(get_project_settings())
        process.crawl(BaseEmoticonId)
        return process.start()

if(__name__ == '__main__'): 
    BaseEmoticonId().start()