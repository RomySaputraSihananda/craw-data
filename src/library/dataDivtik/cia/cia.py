import requests

from time import time
from requests import Response
from json import dumps

from src.helpers import Parser, Datetime, Iostream, ConnectionS3

class Cia:
    def __init__(self) -> None:
        response: Response = requests.get(url := 'https://www.cia.gov/the-world-factbook/page-data/references/terrorist-organizations/page-data.json')
         
        for data in response.json()["result"]["data"]["appendix"]["entries"]:
            self.__process_data(data['fields'][1:])

    def __process_data(self, data) -> None:
        def filter(e):
            if (strong := e.find('strong')): strong.replace_with('')
            value: str = e.get_text().strip('– ').strip('- ').strip()
            match(key := strong.get_text().strip()):
                case 'aka':
                    return 'alias', value
                case 'history':
                    return 'history', value
                case 'goals':
                    return 'goals', value
                case 'leadership and organization':
                    return 'leadership', value
                case 'areas of operation':
                    return 'operation', value
                case 'targets, tactics, and weapons':
                    return 'target', value
                case 'strength':
                    return 'strength', value
                case 'financial and other support':
                    return 'financial support', value
                case 'designation':
                    return 'designation', value
                case _:
                    return key, value
        
        soup: Parser = Parser(data[1]["value"])
        data: dict = {
            "link": (link := 'https://www.cia.gov/the-world-factbook/references/terrorist-organizations'),
            "domain": (link_split := link.split('/'))[2],
            "tag": link_split[2:],
            "crawling_time": Datetime.now(),
            "crawling_time_epoch": int(time()),
            'organization': (title := data[0]['value']),
            **dict(soup.select('p').map(filter)),
            "path_data_raw": f'S3://ai-pipeline-statistics/data/data_raw/ciagov/terrorist_organizations/json/{title.replace("/", " or ")}.json',
            "path_data_clean": f'S3://ai-pipeline-statistics/data/data_clean/ciagov/terrorist_organizations/json/{title.replace("/", " or ")}.json'
        }

        ConnectionS3.upload(data, data['path_data_raw'].replace('S3://ai-pipeline-statistics/', ''))

if(__name__ == '__main__'):
    Cia()