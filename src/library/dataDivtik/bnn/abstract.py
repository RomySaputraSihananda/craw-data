from abc import ABC, abstractmethod
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from .bnn import BaseBnn

class AbstractBnn(ABC):
    @abstractmethod
    def start(self, *args, **kwargs) -> None:
        process = CrawlerProcess(get_project_settings())
        process.crawl(BaseBnn)
        return process.start()