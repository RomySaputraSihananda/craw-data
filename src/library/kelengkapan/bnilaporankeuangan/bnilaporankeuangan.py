import requests
import json

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from src.helpers import Iostream, ConnectionS3
from src.model import Metadata

clean = lambda x: x.lower().replace(' ', '_').replace(' ', '_').replace('-', '_').replace('/', '_').replace('-', '_')
class BniLaporanKeuangan:
    def __init__(self) -> None:
        soup = BeautifulSoup(
            requests.get('https://www.bni.co.id/id-id/investor/laporan-keuangan').text,
            'html.parser'
        )

        containers = soup.select('.resp-tabs-container > div')[:1]      
        category = ['Tahunan', 'Triwulan', 'Bulanan', 'Lainnya'][:1]
        datas = [
            {
                'sub_category': [heading.get_text(strip=True) for heading in container.select('.panel-heading h4')], 
                'value': [self.parser_value(body) for body in container.select('.panel-body')]
            } for container in containers
        ]
        for i, data in enumerate(datas):
            for j, sub_category in enumerate(data['sub_category'][1:]):
                d = {
                    'category': category[i],
                    'sub_category': sub_category,
                    'data': data['value'][1:][j]
                }
                metadata = Metadata(
                    link='https://www.bni.co.id/id-id/investor/laporan-keuangan',
                    source='www.bni.co.id',
                    update_schedule='yeary, every three months, dan monthly',
                    tags=[
                        'www.bni.co.id',
                        'investor',
                        'laporan-keuangan',
                        d['category'],
                        d['sub_category'],
                    ],
                    path_data_raw=[
                        f's3://ai-pipeline-raw-data/data/data_descriptive/bni/laporan_keuangan/{clean(d["category"])}/json/{clean(d["sub_category"])}.json',
                    ],
                    title='Laporan Keuangan',
                    category=d['category'],
                    sub_category=d['sub_category'],
                    data=d,
                    table_name='Laporan Posisi Keuangan(Rp Miliar)'
                )

                self.process_data(metadata)

    @staticmethod
    def parser_value(soup: BeautifulSoup):
        if(cards := soup.select('.icon-box03.box03-new')):
            return [
                {
                    "files": [
                        {
                            'name': card.select_one('p').get_text(strip=True),
                            'tahun': card.select_one('h2').get_text(strip=True),
                            'link': 'https://www.bni.co.id' +  card.select_one('a')["href"],
                            'image': 'https://www.bni.co.id' + card.select_one('img')["data-src"]
                        } for card in cards
                    ]
                }
            ]
        if(table := soup.select_one('.table-responsive table')):
            return {
                'name': 'Laporan Posisi Keuangan(Rp Miliar)'
            }
            return [[[td.get_text() for td in tr.select('td')] for tr in tbody.select('tr')] for tbody in table.select('tbody')]
        if(container := soup.select('h4')):  
            names = [h4.get_text(strip=True) for h4 in container]
            return [
                    {
                        'files': [
                            {
                                'link': 'https://www.bni.co.id' + li["href"],
                                'name': li.get_text(strip=True)
                            }
                            for li in ul.select('li a')
                        ],
                        'category': names[i]
                    } for i, ul in enumerate(soup.select('ul'))
                ]
        
        if(container := soup.select('.list_style7.listbninostyle li')):
            return  [
                {   
                    "files": [
                        {
                            'name': li.get_text(strip=True), 
                            'link': 'https://www.bni.co.id' + li.select_one('a')["href"]
                        } for li in container 
                    ]
                }
            ]

    def __download(self, file, path): 
        final_path = f'{path}/pdf/{clean(file["name"])}.pdf'
        ConnectionS3.upload_content(requests.get(file['link']).content, final_path.replace('s3://ai-pipeline-raw-data/',''), 'ai-pipeline-raw-data')
        return final_path

    def process_data(self, metadata: Metadata):
        # with ThreadPoolExecutor(max_workers=5) as ex:
        #     futures = []
        #     for data in metadata.data["data"]:
        #         for file in data["files"]:
        #             futures.append(
        #                 ex.submit(
        #                     self.__download, 
        #                     file,
        #                     metadata.path_data_raw[0].split('/json')[0]
        #                 )
        #             )
        #     path_pdf = [future.result() for future in futures]
        # metadata.path_data_raw.extend(path_pdf)
        a = f"{metadata.path_data_raw[0].split('/json')[0]}/xlsx/{clean("Laporan Posisi Keuangan(Rp Miliar)")}.xlsx"
        ConnectionS3.upload_content('/home/sc-rommy/Documents/kpu/Laporan Posisi Keuangan(Rp Miliar).xlsx', a.replace('s3://ai-pipeline-raw-data/',''), 'ai-pipeline-raw-data')
        metadata.path_data_raw.append(a)            
        # Iostream.write_json(metadata.dict, metadata.path_data_raw[0].replace('s3://ai-pipeline-raw-data/',''))
        ConnectionS3.upload(metadata.dict, metadata.path_data_raw[0].replace('s3://ai-pipeline-raw-data/',''), 'ai-pipeline-raw-data')

if(__name__ == '__main__'): BniLaporanKeuangan()