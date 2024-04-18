import pandas 
import requests

from io import StringIO
from requests import Response, Session
from json import dumps, loads
from bs4.element import Tag

from src.helpers import Parser
from src.helpers.parser import Array

class BaseCompaniesMarketCap:
    def __init__(self) -> None: 
        self.__requests: Session = Session()
        self.__requests.headers.update({
            "Cookie": "usprivacy=1NNN; __gads=ID=d2bc8ce066ad4e3b:T=1713341113:RT=1713421962:S=ALNI_MbdCZq2EgQAZPs7QsKlnBD7EOrg_g; __gpi=UID=00000df024736389:T=1713341113:RT=1713421962:S=ALNI_MZDajjg_YcknVb9sbLcf5NiXvO8rQ; __eoi=ID=3c6979f8bc4d0094:T=1713341113:RT=1713421962:S=AA-AfjYuyE6Ec42cQBOb3PHxMdu6; _cc_id=cd49bcc9a142c107f81a8e815ddf541c; panoramaId_expiry=1713427515031",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"
        })

    def __get_percentage_today(self) -> list: 
        def filter(e: Tag) -> dict:
            [class_element] = e['class']
            return {
                'percentage': e.get_text(),
                'status': 'down' if class_element == 'percentage-red' else 'up'
            }
        response: Response = requests.get('https://companiesmarketcap.com/defense-contractors/largest-companies-by-market-cap/')
        soup: Parser = Parser(response.text)

        return soup.select('.rh-sm span').map(filter)

    def _start(self) -> None: 
        response: Response = self.__requests.get('https://companiesmarketcap.com/defense-contractors/largest-companies-by-market-cap?download=csv')
        df = pandas.read_csv(StringIO(response.text))

        result = df.to_dict(orient='records')

        print(result)



if(__name__ == '__main__'):
    BaseCompaniesMarketCap()._start()