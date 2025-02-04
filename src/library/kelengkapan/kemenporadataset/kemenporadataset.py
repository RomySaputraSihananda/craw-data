import json
import requests

from requests import Session
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from metadata import Metadata
from src.helpers import Datetime, ConnectionS3

clean = lambda x: x.lower().replace(' ', '_').replace(' ', '_').replace('-', '_').replace('/', '_').replace('-', '_')


class KemenporaDataset:
    def __init__(self) -> None:
        self.__session = Session()
        self.__session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        })

    @staticmethod
    def get_soup(html) -> BeautifulSoup:
        return BeautifulSoup(html, 'html.parser')

    @staticmethod
    def get_graph_by_type(data, type) -> dict:
        return [d for d in data['@graph'] if d['@type'] == type]

    def __download(self, file, path):
        match(format := file['schema:encodingFormat'].lower()):
            case 'xlsx' | 'csv': ...
            case 'pdf': path = path.replace('data_statistics', 'data_descriptive')
            case _: return

        final_path = f'{path}/{format}/{clean(file['schema:name'])}'
        # ConnectionS3\
        #     .upload_content(
        #         self.__session.get(
        #             file['schema:url']
        #         ).content, 
        #         final_path.replace('s3://ai-pipeline-raw-data/',''), 
        #         'ai-pipeline-raw-data'
        #     )
        
        return final_path

    def _process_data(self, url):
        data = self._get_detail_data(url)
        
        metadata = Metadata(
            link='https://satudata.rejanglebongkab.go.id' + url,
            tags=[
                'satudata.rejanglebongkab.go.id',
                *url.split('/')
            ],
            source='satudata.rejanglebongkab.go.id',
            title=(title := (dataset := self.get_graph_by_type(data, 'schema:Dataset')[0])['schema:name']),
            create_date=Datetime.utc(dataset['schema:datePublished']),
            update_date=Datetime.utc(dataset['schema:dateModified']),
            data=data,
            desc=dataset.get('schema:description'),
            category=(category := thing[0]['schema:name'] if (thing := self.get_graph_by_type(data, 'schema:Thing')) else 'lainnya'),
            path_data_raw=[
                f's3://ai-pipeline-raw-data/data/data_statistics/kemenpora/dataset/{category}/json/{clean(title)}.json'
            ],
            update_schedule='yearly'
        )

        metadata.path_data_raw.extend([
            self.__download(
                file,
                metadata.path_data_raw[0].split('/json')[0]
            ) for file in self.get_graph_by_type(data, 'schema:DataDownload')
        ]) 
        print(metadata)

        # ConnectionS3\
        #     .upload(
        #         metadata.dict,
        #         metadata.path_data_raw[0].replace('s3://ai-pipeline-raw-data/',''), 
        #         'ai-pipeline-raw-data'
        #     )

    def _get_detail_data(self, url):
        response = self.__session.get(      
            'https://satudata.rejanglebongkab.go.id' + url
        )   
        soup = self.get_soup(response.text)
        return json.loads(soup.select_one('script[type="application/ld+json"]').string)

    def _get_url(self, page):
        response = self.__session.get(
            'https://satudata.rejanglebongkab.go.id/dataset/',
            params={                            
                'page': page
            }
        )
        soup = self.get_soup(response.text)
        return [
            li.select_one('a')["href"] for li in soup.select('.dataset-item')
        ]
    
    def get_data(self):
        urls = self._get_url(1)

        with ThreadPoolExecutor(max_workers=5) as ex:
            futures = []
            for url in urls:
                futures.append(
                    ex.submit(
                        self._process_data,
                        url
                    )
                )

            for future in futures:
                future.result()


if(__name__ == '__main__'):
    KemenporaDataset().get_data()