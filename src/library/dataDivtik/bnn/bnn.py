import scrapy
import requests
import asyncio
import aiofiles
from typing import Any
from aiohttp import ClientSession
from scrapy import Spider
from scrapy.http import Response
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from src.helpers import Decorator, ConnectionS3

class Bnn(Spider):
    name = 'bnn-spider'
    start_urls = ['https://puslitdatin.bnn.go.id/hasil-lit-idr/']
    
    @staticmethod
    @Decorator.check_path
    async def download(url: str, path: str) -> None:
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200: return
                ConnectionS3.upload_content(await response.read(), f'{path}{url.split("/")[-1]}')
                # async with aiofiles.open(f'{path}{url.split("/")[-1]}', 'wb') as file:
                #     await file.write(await response.read())
    
    async def __downloads(self, urls: list, tahun: str, category: str) -> None:
        return await asyncio.gather(*(asyncio.create_task(self.download(url, f'data/data_raw/bnn/{category.replace("tab-", "")}/{tahun}/pdf/')) for url in urls))

    def parse(self, response: Response, **kwargs: Any) -> Any:
        categories = list(response.css('.wpb_tab.ui-tabs-panel.wpb_ui-tabs-hide.clearfix'))
        key_categories: list = [category.css('div::attr(id)').get() for category in categories]

        for i, category in enumerate(categories):
            tahun_text: str = ''
            for tahun in category.css('.wpb_row.vc_row-fluid.vc_row.inner_row'):

                if(tahun_new := tahun.css('div span strong::text').get()):
                    tahun_text: str = tahun_new

                if(not (urls := list(link.get() for link in tahun.css('div a::attr(href)')))): continue
                asyncio.run(self.__downloads(urls, tahun_text, key_categories[i]))
    
    def start(self):
        process = CrawlerProcess(get_project_settings())
        process.crawl(Bnn)
        process.start()

if(__name__ == '__main__'):
    Bnn().start()
