import requests
from bs4 import BeautifulSoup 
from metadata import Metadata
from concurrent.futures import ThreadPoolExecutor, Future
from src.helpers import ConnectionS3, Iostream

clean = lambda x: x.lower().replace(' ', '_').replace(' ', '_').replace('-', '_').replace('/', '_').replace('-', '_')

class KemendesaPublikasi:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_soup(html) -> BeautifulSoup:
        return BeautifulSoup(html, 'html.parser')
    
    @staticmethod
    def get_format(link):
        name, format = (file_name := link.split('/')[-1]).rsplit('.', 1)
        return {
            'name': name,
            'format': format,
            'file_name': file_name
        }
    
    def __download(self, img, path):
        final_path = f'{path}/{clean(img["format"])}/{clean(img["file_name"])}'
        ConnectionS3.upload_content(requests.get(img['link'], verify=False).content, final_path.replace('s3://ai-pipeline-raw-data/',''), 'ai-pipeline-raw-data')
        return final_path

    def _get_cards(self, page):
        response = requests.get(
            'https://kemendesa.go.id/berita/content/infografis_kdpdtt',
            params={
                    'key': '',
                    'per_page': (page - 1) * 9,
                },
            verify=False
        )   
        soup = self.get_soup(response.text)

        return [
                {
                    'link': a["href"],
                    'title': a["title"]
                } for a in soup.select('.thumbnail a')
            ]
    
    def _process_card(self, card):
        print('starrttttoooooooooo')
        response = requests.get(
            (link := card['link']),
            verify=False
        )   
        soup = self.get_soup(response.text)
        metadata = Metadata(
            link=link,
            source=(link_split := link.split('/')[2:])[0],
            tags=[
                *link_split,
                'publikasi',
                'infografis'
            ],
            title=card['title'],
            update_schedule='non-periodic', 
            category='infografis',
            path_data_raw=[
                f's3://ai-pipeline-raw-data/data/data_descriptive/kemendesa/infografis/json/{clean(card["title"])}.json'
            ],
            data={
                **card,
                'images': [
                    {
                        'link': (link_img := img['src']),
                        **self.get_format(link_img)
                    } for img in soup.select('.infografis img')
                ]
            },
        )
        metadata.path_data_raw.extend(
            [
                self.__download(
                    image,
                    metadata.path_data_raw[0].split('/json')[0]
                ) for image in metadata.data["images"]
            ]
        )

        ConnectionS3.upload(metadata.dict, metadata.path_data_raw[0].replace('s3://ai-pipeline-raw-data/',''), 'ai-pipeline-raw-data')
        # Iostream.write_json(metadata.dict, metadata.path_data_raw[0].replace('s3://ai-pipeline-raw-data/',''))

    def get_data(self):
        page = 1
        while(True):
            cards = self._get_cards(page)
            if(not cards): break
            with ThreadPoolExecutor(max_workers=5) as ex:
                futures: list[Future] = []
                for card in cards:
                    futures.append(
                        ex.submit(
                            self._process_card,
                            card
                        )
                    )
                
                for future in futures:
                    future.result()

            page += 1


if(__name__ == '__main__'):
    KemendesaPublikasi().get_data()