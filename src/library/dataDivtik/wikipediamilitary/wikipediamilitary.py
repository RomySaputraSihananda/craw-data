import requests 

from requests import Response
from json import dumps
from time import time
from bs4.element import Tag

from src.helpers import Parser, Datetime, Iostream, ConnectionS3
from src.helpers.parser import Array

class BaseWikipediaMilitary:
    def __init__(self) -> None: ...

    def __get_background_ijo(self, table: Tag) -> list:
        def filter(e: Tag):
            if(e.select('span')): return Array(e.select('a')).map(lambda e: e.get_text())
            
            return e.get_text().strip().split('[')[0]
        
        body_table: Tag = table.select_one('tbody')
        
        keys: list = Array(body_table.select('tr th')).map(lambda e: e.get_text().strip())
        values: list = Array(body_table.select('tr[style="background:#afe6ba"]')).map(lambda e: Array(e.select('td')).map(filter))
        
        return [
            { key: value[i] for i, key in enumerate(keys) }
            for value in values
        ]
    
    def _start(self) -> None: 
        response: Response = requests.get(link := 'https://en.wikipedia.org/wiki/List_of_military_alliances')
        soup: Parser = Parser(response.text)
        
        link_split: list = link.split('/')

        titles: list = soup.select('.mw-headline').map(lambda e: e.get_text())[1:-4]
        tables: list = soup.select('.wikitable').map(lambda e: e)[1:-1]

        for i, title in enumerate(titles):
            clean_table: list = self.__get_background_ijo(tables[i]) 
            data: dict = {
                    "link": link,
                    "domain": link_split[2],
                    "tag": [*link_split[2:], title, *list(dict.fromkeys([clean['Years'] for clean in clean_table]))],
                    "table": clean_table,
                    "crawling_time": Datetime.now(),
                    "crawling_time_epoch": int(time()),
                    "path_data_raw": f'S3://ai-pipeline-statistics/data/data_raw/wikipedia/List_of_military_alliances/json/{title}.json',
                    "path_data_clean": f'S3://ai-pipeline-statistics/data/data_clean/wikipedia/List_of_military_alliances/json/{title}.json',
            }

            if(clean_table):
                ConnectionS3.upload(data, data['path_data_raw'].replace('S3://ai-pipeline-statistics/', ''))

if(__name__ == '__main__'):
    BaseWikipediaMilitary()._start()