import pandas 
import requests

from time import time
from pandas.io.parsers.readers import TextFileReader
from io import StringIO
from requests import Response, Session
from bs4.element import Tag

from src.helpers import Parser, Datetime, Iostream, ConnectionKafka

class BaseCompaniesMarketCap:
    def __init__(self, **kwargs) -> None: 
        self.__kafka: bool = kwargs.get('kafka')

        if(self.__kafka): 
            self.__bootstrap: str = kwargs.get('bootstrap')
            self.__connectionKafka: ConnectionKafka = ConnectionKafka(kwargs.get('topic'), kwargs.get('bootstrap'))

        self.__requests: Session = Session()
        self.__requests.headers.update({
            "Cookie": "usprivacy=1NNN; __gads=ID=d2bc8ce066ad4e3b:T=1713341113:RT=1713421962:S=ALNI_MbdCZq2EgQAZPs7QsKlnBD7EOrg_g; __gpi=UID=00000df024736389:T=1713341113:RT=1713421962:S=ALNI_MZDajjg_YcknVb9sbLcf5NiXvO8rQ; __eoi=ID=3c6979f8bc4d0094:T=1713341113:RT=1713421962:S=AA-AfjYuyE6Ec42cQBOb3PHxMdu6; _cc_id=cd49bcc9a142c107f81a8e815ddf541c; panoramaId_expiry=1713427515031",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"
        })

    def __get_percentage_today(self) -> tuple: 
        def filter(e: Tag) -> dict:
            [class_element] = e['class']
            return {
                'percentage': float(e.get_text().replace('%', '')),
                'status': 'down' if class_element == 'percentage-red' else 'up'
            }
        response: Response = requests.get('https://companiesmarketcap.com/defense-contractors/largest-companies-by-market-cap/')
        soup: Parser = Parser(response.text)

        return (
            {
                "title": soup.select_one('h1').get_text(),
                "companies": int(soup.select_one('.category-stats-bar span').get_text()),
            },
            soup.select('.rh-sm span').map(filter)
        )
    

    def _start(self) -> None: 
        response: Response = self.__requests.get(link := 'https://companiesmarketcap.com/defense-contractors/largest-companies-by-market-cap', params={'download': 'csv'})
        
        df: TextFileReader = pandas.read_csv(StringIO(response.text))
        (all, today) = self.__get_percentage_today()

        results: dict = df.to_dict(orient='records')
        
        link_split: list = link.split('/')
        data: dict = {
            "link": link,
            "domain": link_split[2],
            "tag": link_split[2:],
            "crawling_time": Datetime.now(),
            "crawling_time_epoch": int(time()),
            **all,
            "total_market_cap": int(df['marketcap'].sum()),
            "table": [{
                **result,
                'table': {
                    **today[i]
                }
            } for i, result in enumerate(results)],
            # "path_data_raw": f'S3://ai-pipeline-statistics/data/data_raw/wikipedia/List_of_military_alliances/json/{title}.json',
            # "path_data_clean": f'S3://ai-pipeline-statistics/data/data_clean/wikipedia/List_of_military_alliances/json/{title}.json',
        }

        if(self.__kafka):
            self.__connectionKafka.send(data, name=self.__bootstrap)

        Iostream.write_json(data, f'data/data_raw/companiesmarketcap/json/{Datetime.now()}.json', indent=3)


if(__name__ == '__main__'):
    BaseCompaniesMarketCap()._start()