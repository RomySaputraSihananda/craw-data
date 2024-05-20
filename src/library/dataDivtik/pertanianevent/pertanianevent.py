import requests

from time import time
from requests import Response
from collections import defaultdict
from datetime import datetime
from json import dumps
from calendar import month_name
from src.helpers import Iostream, Datetime, ConnectionS3

class BasePertanianEvent():
    def __init__(self) -> None:
        response: Response = requests.get('https://pertanian.go.id/home/event_api.php')
        old_data: list = response.json()

        self.__data: defaultdict = defaultdict(list)
        for e in old_data:
            title, agenda = e['title'].split('<br/>')
            self.__data[(date := e['startDate'])[:7]].append(
                Iostream.dict_to_deep({
                    "link": (link := 'https://pertanian.go.id/home/?show=page&act=view&id=76'),
                    "domain": (link_split := link.split('/'))[2],
                    "tag": [*link_split[2:], "Agenda Kementerian Pertanian"],
                    "crawling_time": Datetime.now(),
                    "crawling_time_epoch": int(time()),
                    'title': title,
                    'agenda': agenda,
                    'date': date,
                    "path_data_raw": f'S3://ai-pipeline-raw-data/data/data_descriptive/pertaniangoid/data_event/{(date_split := date.split("-"))[0]}/{month_name[int(date_split[1])].lower()}/json/{date_split[-1]}.json',
                })
            )

    def _get_by_year_month(self, year: int = None, month: int = None, **kwargs):
        for e in (data := self.__data[date if (date := kwargs.get('date')) else datetime(year, month, 1).strftime('%Y-%m')]):
            # Iostream.write_json(e, e['path_data_raw'].replace('S3://ai-pipeline-raw-data/', ''), indent=4)
            ConnectionS3.upload(e, e['path_data_raw'].replace('S3://ai-pipeline-raw-data/', ''), bucket='ai-pipeline-raw-data')
        return data

    def _get_by_year(self, year: int):
        for month in range(1, 12 + 1):
            self._get_by_year_month(year, month)

if(__name__ == '__main__'):
    d = BasePertanianEvent()
    d._get_by_year(2021)
    d._get_by_year(2020)
