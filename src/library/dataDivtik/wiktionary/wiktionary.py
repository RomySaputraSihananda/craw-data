from requests import Session, Response
from json import dumps
from bs4.element import Tag
from src.helpers import Parser

class Wiktionary:
    def __init__(self) -> None:
        self.__requests: Session = Session()
        self.__requests.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Referer': 'https://www.google.com/',
            'Cookie': 'WMF-Last-Access=29-May-2024; WMF-Last-Access-Global=29-May-2024; idwiktionarymwclientpreferences=vector-feature-toc-pinned-clientpref-0; GeoIP=ID:BT:Tangerang:-6.18:106.63:v4; NetworkProbeLimit=0.001; idwiktionarymwuser-sessionId=bcc69ceedc7f3cb95885',
        })
    
    @staticmethod
    def get_table(table: Tag):
        trs: list = table.select('tr')
        keys: list = [th.get_text().strip() for th in trs[0].select('th')]
        values: list = [[td.get_text().strip() for td in tr.select('td')] for tr in trs[1:]]
        
        return [
            {
                key: value[i]
                for i, key in enumerate(keys)
            }
            for value in values
        ]
    
    @staticmethod
    def get_ul_ol(ul: Tag):
        return [li.get_text().strip() for li in ul.select('li')]
    
    def _start(self, url: str) -> dict:
        response: Response = self.__requests.get(url)
        self.__soup: Parser = Parser(response.text)
        title = self.__soup.select_one('#firstHeading').get_text()
        if(len(containers := self.__soup.select('#mw-content-text > div').to_list()[:-1]) > 1): return
        childerns = [child for child in list(containers[0].children) if type(child) == Tag][1:]
        data = {}
        for i, childern in enumerate(childerns):
            if(childern.name == 'h2'):
                value: None = None
                match((tag := childerns[i + 1]).name):
                    case 'table':
                        value = self.get_table(tag)
                    case 'ul':
                        value = self.get_ul_ol(tag)
                    case 'div':
                        value = self.get_ul_ol(tag.select_one('ol'))

                data.update({
                    childern.select_one('span').get_text().strip(): value
                })

        return {
            'title': title,
            'data': data
        }
        

if(__name__ == '__main__'): 
    Wiktionary()._start()
    # Wiktionary()._start('https://id.wiktionary.org/wiki/Kategori:Kata_bahasa_Komering')
    # https://id.wiktionary.org/