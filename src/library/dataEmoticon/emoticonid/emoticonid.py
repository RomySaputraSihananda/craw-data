from scrapy import Spider
from typing import Any
from scrapy.http import Request, Response
from json import dumps, loads
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.helpers import Datetime, Iostream, ConnectionS3, Parser 
from src.helpers.parser import Array
from scrapy.selector.unified import Selector
from time import time
import requests

class BaseEmoticonId(Spider):
    start_urls = ['https://emoticon.id/']

    def __init__(self, **kwargs: Any):
        self.__s3: bool = kwargs.get('s3')
        super().__init__('emoticon-spider')

    # def parse(self, response: Response, **kwargs: Any) -> Any:
    def __process_emoticon(self, response: Response, **kwargs: Any) -> Any:
        container = response.css('div.pakb-article-content')
        description: list = [p.css('::text').get() for p in response.css('div.pakb-article-content > p')[:2]]
        keys: list = [h2.css('::text').get() for h2 in container.css('h2')]
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
            'link': (link := response.url),
            'domain': (link_split := link.split('/')[:-1])[2],
            'crawling_time': Datetime.now(),
            'crawling_time_epoch': int(time()),
            'tag': [
                'emoticon.id',
                (category := [a.css('a::text').get() or a.css('span::text').get() for a in response.css('.uk-margin-medium-bottom.uk-breadcrumb.pakb-link.pakb-secondary-color li')][1])
            ],
            'title': (title := response.css('h1::text').get()),
            'data': {
                'description': description,
                **{keys[i]: value for i, value in enumerate(values)}
            },
            'path_data_raw': f'S3://ai-pipeline-statistics/data/data_raw/Emoticon/emoticonid/{category}/json/{title}.json', 
            'path_data_clean': f'S3://ai-pipeline-statistics/data/data_clean/Emoticon/emoticonid/{category}/json/{title}.json',   
        } 

        Iostream.write_json(data, data['path_data_raw'].replace('S3://ai-pipeline-statistics/', ''), indent=4)


    def __process_card(self, response: Response, **kwargs: Any) -> Any: 
        for link in (li.css('::attr(href)').get() for li in response.css('.uk-margin-large-top.uk-list.uk-list-large.pakb-list.pakb-primary-color.link-icon-right li a')):
            yield response.follow(link, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'}, callback=self.__process_emoticon, errback=self.__handle_error) 

    def __handle_error(self, failure: Response):
        request = failure.request
        if failure.value.response.status != 200:
            self.logger.error(f"Request failed: {request.url}, retrying...")
            yield request.replace(dont_filter=True)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        links: list = [card.css('::attr(href)').get() for card in response.css('.uk-card.uk-card-small.uk-card-body.uk-border-rounded.uk-inline.uk-text-center a')]
        symbol: Any = links.pop(1)

        for link in links:
            yield response.follow(link, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'}, callback=self.__process_card, errback=self.__handle_error)

    def start(self, *args, **kwargs) -> None:
        process = CrawlerProcess(get_project_settings())
        process.crawl(BaseEmoticonId)
        return process.start()

if(__name__ == '__main__'): BaseEmoticonId().start()