import gdown
import os

from requests import Session, Response
from json import dumps
from typing import Generator
from time import time
from urllib.parse import unquote

from src.helpers import Iostream, Datetime, ConnectionS3

from .provinceEnum import ProvinceEnum

class BaseBawasluKerawanan:
    def __init__(self) -> None:
        self.__requests: Session = Session()
        self.__requests.headers.update({
            'ActivityId': 'ef25aaa3-3d0b-e48e-3169-0f4af20f5c9f',
            'RequestId': 'd2427529-46b8-e147-6b6a-886a09931f2c',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'X-PowerBI-ResourceKey': '9a3fd331-b6df-4481-8c8f-76779e436459',
        })

    def __download(self, title: str, sub_title: str, links: str) -> Generator: 
        for link in os.listdir(links):
            _, format = (file_name := link.split('/')[-1]).rsplit('.', 1)
            ConnectionS3.upload_content(os.path.join(links, link), (path := f'S3://ai-pipeline-raw-data/data/data_statistics/bawaslu/download_ikp_2024/{title}/{sub_title}/{format}/{file_name.replace(" ", "_").lower()}').replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
            yield path

    def _get_download(self) -> None:
        for data in (
            ('buku_ikp_pemilu&pemilihan_serentak_2024', 'buku_ikp', '/home/romy/Desktop/dasor-皇/craw-data/datod/1'), 
            ('launching_ikp_pemilu&pemilihan_serentak_2024', 'paparan_ikp', '/home/romy/Desktop/dasor-皇/craw-data/datod/2'), 
            ('launching_ikp_pemilu&pemilihan_serentak_2024', 'pers_release_ikp', '/home/romy/Desktop/dasor-皇/craw-data/datod/3'), 
            ('launching_ikp_pemilu&pemilihan_serentak_2024', 'ringkasan_rksekutif_ikp', '/home/romy/Desktop/dasor-皇/craw-data/datod/4'),
            ('data_tabel_ikp_pemilu_dan_ikp_pemilihan_serentak_2024', 'tabel_excell_ikp', '/home/romy/Desktop/dasor-皇/craw-data/datod/5')
        ):

            ConnectionS3.upload((result := {
                "link": (link := 'https://sipekapilu.bawaslu.go.id/download'),
                "domain": (link_split := link.split('/'))[2],
                "tag": link_split[2:],
                "crawling_time": Datetime.now(),
                "crawling_time_epoch": int(time()),
                'title': (title := data[0]).replace('_', ' ').title(),
                'sub_title': (sub_title := data[1]).replace('_', ' ').title(), 
                "path_data_raw": [
                    f'S3://ai-pipeline-raw-data/data/data_statistics/bawaslu/download_ikp_2024/{title}/json/{sub_title.replace(" ", "_").lower()}.json',
                    *list(self.__download(*data))
                ]
            }), result['path_data_raw'][0].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')


    def _get_by_province(self, province: ProvinceEnum) -> None:
        response: Response = self.__requests.post('https://wabi-south-east-asia-b-primary-api.analysis.windows.net/public/reports/querydata',     
                                                params={
                                                    'synchronous': 'true',
                                                },
                                                json={
                                                    'version': '1.0.0',
                                                    'queries': [
                                                        {
                                                            'Query': {
                                                                'Commands': [
                                                                    {
                                                                        'SemanticQueryDataShapeCommand': {
                                                                            'Query': {
                                                                                'Version': 2,
                                                                                'From': [
                                                                                    {
                                                                                        'Name': 'i1',
                                                                                        'Entity': 'IKP Provinsi (2)',
                                                                                        'Type': 0,
                                                                                    },
                                                                                ],
                                                                                'Select': [
                                                                                    {
                                                                                        'Column': {
                                                                                            'Expression': {
                                                                                                'SourceRef': {
                                                                                                    'Source': 'i1',
                                                                                                },
                                                                                            },
                                                                                            'Property': 'PROVINSI',
                                                                                        },
                                                                                        'Name': 'PROVINSI',
                                                                                    },
                                                                                    {
                                                                                        'Column': {
                                                                                            'Expression': {
                                                                                                'SourceRef': {
                                                                                                    'Source': 'i1',
                                                                                                },
                                                                                            },
                                                                                            'Property': 'Kategori IKP',
                                                                                        },
                                                                                        'Name': 'Kategori IKP',
                                                                                    },
                                                                                    {
                                                                                        'Aggregation': {
                                                                                            'Expression': {
                                                                                                'Column': {
                                                                                                    'Expression': {
                                                                                                        'SourceRef': {
                                                                                                            'Source': 'i1',
                                                                                                        },
                                                                                                    },
                                                                                                    'Property': 'Skor IKP 2024 ',
                                                                                                },
                                                                                            },
                                                                                            'Function': 0,
                                                                                        },
                                                                                        'Name': 'Skor IKP 2024',
                                                                                    },
                                                                                    {
                                                                                        'Aggregation': {
                                                                                            'Expression': {
                                                                                                'Column': {
                                                                                                    'Expression': {
                                                                                                        'SourceRef': {
                                                                                                            'Source': 'i1',
                                                                                                        },
                                                                                                    },
                                                                                                    'Property': 'Skor Dimensi Sosial Politik',
                                                                                                },
                                                                                            },
                                                                                            'Function': 0,
                                                                                        },
                                                                                        'Name': 'Skor Dimensi Sosial Politik',
                                                                                    },
                                                                                    {
                                                                                        'Aggregation': {
                                                                                            'Expression': {
                                                                                                'Column': {
                                                                                                    'Expression': {
                                                                                                        'SourceRef': {
                                                                                                            'Source': 'i1',
                                                                                                        },
                                                                                                    },
                                                                                                    'Property': 'Skor Dimensi Penyelenggaraan Pemilu',
                                                                                                },
                                                                                            },
                                                                                            'Function': 0,
                                                                                        },
                                                                                        'Name': 'Skor Dimensi Penyelenggaraan Pemilu',
                                                                                    },
                                                                                    {
                                                                                        'Aggregation': {
                                                                                            'Expression': {
                                                                                                'Column': {
                                                                                                    'Expression': {
                                                                                                        'SourceRef': {
                                                                                                            'Source': 'i1',
                                                                                                        },
                                                                                                    },
                                                                                                    'Property': 'Skor Dimensi Kontestasi',
                                                                                                },
                                                                                            },
                                                                                            'Function': 0,
                                                                                        },
                                                                                        'Name': 'Skor Dimensi Kontestasi',
                                                                                    },
                                                                                    {
                                                                                        'Aggregation': {
                                                                                            'Expression': {
                                                                                                'Column': {
                                                                                                    'Expression': {
                                                                                                        'SourceRef': {
                                                                                                            'Source': 'i1',
                                                                                                        },
                                                                                                    },
                                                                                                    'Property': 'Skor Dimensi Partisipasi',
                                                                                                },
                                                                                            },
                                                                                            'Function': 0,
                                                                                        },
                                                                                        'Name': 'Skor Dimensi Partisipasi',
                                                                                    },
                                                                                ],
                                                                                
                                                                                'Where': [
                                                                                    {
                                                                                        'Condition': {
                                                                                            'In': {
                                                                                                'Expressions': [
                                                                                                    {
                                                                                                        'Column': {
                                                                                                            'Expression': {
                                                                                                                'SourceRef': {
                                                                                                                    'Source': 'i1',
                                                                                                                },
                                                                                                            },
                                                                                                            'Property': 'PROVINSI',
                                                                                                        },
                                                                                                    },
                                                                                                ],
                                                                                                'Values': [
                                                                                                    [
                                                                                                        {
                                                                                                            'Literal': {
                                                                                                                'Value': f"'{province.value}'",
                                                                                                            },
                                                                                                        },
                                                                                                    ],
                                                                                                ],
                                                                                            },
                                                                                        },
                                                                                    },
                                                                                ],
                                                                            },
                                                                            'Binding': {
                                                                                'Primary': {
                                                                                    'Groupings': [
                                                                                        {
                                                                                            'Projections': [
                                                                                                0,
                                                                                                2,
                                                                                                3,
                                                                                                4,
                                                                                                5,
                                                                                                6,
                                                                                            ],
                                                                                        },
                                                                                    ],
                                                                                },
                                                                                'Secondary': {
                                                                                    'Groupings': [
                                                                                        {
                                                                                            'Projections': [
                                                                                                1,
                                                                                            ],
                                                                                        },
                                                                                    ],
                                                                                },
                                                                                'DataReduction': {
                                                                                    'DataVolume': 4,
                                                                                    'Primary': {
                                                                                        'Top': {},
                                                                                    },
                                                                                    'Secondary': {
                                                                                        'Top': {},
                                                                                    },
                                                                                },
                                                                                'SuppressedJoinPredicates': [
                                                                                    2,
                                                                                    3,
                                                                                    4,
                                                                                    5,
                                                                                    6,
                                                                                ],
                                                                                'Version': 1,
                                                                            },
                                                                            'ExecutionMetricsKind': 1,
                                                                        },
                                                                    },
                                                                ],
                                                            },
                                                            'QueryId': '',
                                                            'ApplicationContext': {
                                                                'DatasetId': '96fa2498-e59f-422f-ba3e-c3a2125daa0f',
                                                                'Sources': [
                                                                    {
                                                                        'ReportId': 'a6a1b926-33f8-4d98-af81-853ead59e8e6',
                                                                        'VisualId': '981a5194702b535c0713',
                                                                    },
                                                                ],
                                                            },
                                                        },
                                                    ],
                                                    'cancelQueries': [],
                                                    'modelId': 1407678,
                                                },
                                            )
        
        data: dict = response.json()["results"][0]["result"]["data"]
        keys: list = [key['Name'] for key in data["descriptor"]["Select"]]
        values: list = [(data := data["dsr"]["DS"][0])["PH"][0]["DM0"][0]["G0"], data["SH"][0]["DM1"][0]["G1"], *data["PH"][0]["DM0"][0]["X"][0]["C"]]

        ConnectionS3.upload((result := {
            "link": (link := 'https://sipekapilu.bawaslu.go.id/data-visualization'),
            "domain": (link_split := link.split('/'))[2],
            "tag": link_split[2:],
            "crawling_time": Datetime.now(),
            "crawling_time_epoch": int(time()),
            'data': {
                key: values[i]
                for i, key in enumerate(keys)
            },
            "path_data_raw": f'S3://ai-pipeline-raw-data/data/data_statistics/bawaslu/data_visualisasi_ikp_2024/json/{province.name.lower()}.json'
        }), result['path_data_raw'].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')

    def _get_provinces(self) -> Generator:
        for province in ProvinceEnum:
            self._get_by_province(province)



if(__name__ == '__main__'): BaseBawasluKerawanan()._get_provinces()