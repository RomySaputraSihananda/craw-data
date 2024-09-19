import requests
import json

from bs4 import BeautifulSoup
from datetime import datetime
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

from src.helpers import BeanStalk, ConnectionS3
from src.model import Metadata

class Category(Enum):
    UNDANG_UNDANG = 1
    PERATURAN_PEMERINTAH= 2
    PERATURAN_PRESIDEN = 3
    KEPUTUSAN_PRESIDEN = 4
    PERATURAN_MENDAGRI = 5
    KEPUTUSAN_MENDAGRI = 6
    SURAT_EDARAN = 7
    DOKUMEN_HUKUM = 8   
    INSTRUKSI_PRESIDEN = 9
    INSTRUKSI_MENDAGRI = 10
    RUMUSAN_RAKORNAS = 11
    LHKPN = 12
    MATERI_PIMPINAN = 13
    LAPORAN_KINERJA = 14
    SOP = 19
    PHLN = 22

class DukcapilProdukHukum:
    def __init__(self) -> None:
        self.beanstalk = BeanStalk('192.168.150.21', 11300, 'dev-target-dukcapil-produk-hukum')
    
    @staticmethod
    def get_soup(text):
        return BeautifulSoup(text, 'html.parser')
    
    def __download(self, link, path):
        response = requests.get(link)

        if(response.status_code != 200): return

        ConnectionS3.upload_content(response.content, path.replace('s3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')

        return path

    def _get_document(self, id, start, size):
        data = {
            'draw': 0,
            'columns[0][data]': 0,
            'columns[0][name]': '',
            'columns[0][searchable]': 'true',
            'columns[0][orderable]': 'true',
            'columns[0][search][value]': '',
            'columns[0][search][regex]': 'false',
            'columns[1][data]': 1,
            'columns[1][name]': '',
            'columns[1][searchable]': 'true',
            'columns[1][orderable]': 'true',
            'columns[1][search][value]': '',
            'columns[1][search][regex]': 'false',
            'columns[2][data]': 2,  
            'columns[2][name]': '',
            'columns[2][searchable]': 'true',
            'columns[2][orderable]': 'true',
            'columns[2][search][value]': '',
            'columns[2][search][regex]': 'false',
            'columns[3][data]': 3,
            'columns[3][name]': '',
            'columns[3][searchable]': 'true',
            'columns[3][orderable]': 'true',
            'columns[3][search][value]': '',
            'columns[3][search][regex]': 'false',
            'columns[4][data]': 4,
            'columns[4][name]': '',
            'columns[4][searchable]': 'true',
            'columns[4][orderable]': 'true',
            'columns[4][search][value]': '',
            'columns[4][search][regex]': 'false',
            'order[0][column]': 0,
            'order[0][dir]': 'asc',
            'start': start,
            'length': size,
            'search[value]': '',
            'search[regex]': 'false',
            'id_kategori': id.value,
            'keyword': '',
        }

        response = requests.post('https://dukcapil.kemendagri.go.id/download/ajaxlist', data=data)
        data =  response.json()["data"]

        return [
            {e: self.get_soup(d[i]).get_text(strip=True) if not e == 'link' else self.get_soup(d[i]).select_one('a')["href"] for i, e in enumerate(('no', 'nama', 'kategori', 'update_at', 'link'))} for d in data
        ]

    def _send_target(self):
        for category in Category:
            for e in self._get_document(category, 0, 500):
                print(self.beanstalk.use.put(json.dumps(e)))  

    def _get_detail_document(self, link):
        soup = self.get_soup(requests.get(link).text)
        return {
            **{k[0] if len(k) > 1 else 'title': k[1] if len(k) > 1 else k[0] for k in[[f.get_text(strip=True) for f in e.select('div')] for e in soup.select('.card-body > div')]},
            'link': soup.select_one('.card-body a')["href"]
        }

    def _process_data(self, job):
        try:
            body = json.loads(job.body)
            data = self._get_detail_document(body["link"])
            m = Metadata(
                link=body["link"],
                source="dukcapil.kemendagri.go.id",
                tags=[
                    "dukcapil.kemendagri.go.id",
                    "document",
                    body["kategori"]
                ],
                category=body["kategori"],
                update_date=datetime.strptime(body["update_at"], "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S"),
                update_schedule="yearly",
                data=data,
                desc=data["Deskripsi"],
                title=data["title"],
                path_data_raw=[
                    (root := f"s3://ai-pipeline-raw-data/data/data_descriptive/kemendagri/dukcapil/produk_hukum/{body['kategori'].lower().replace(' ', '_')}") + f"/json/{(name := data['title'].lower().replace(' ', '_').replace('-', '_'))}.json",
                ]
            )
            
            if(path_pdf := self.__download(data["link"], root + f"/pdf/{name}.pdf")):
                m.path_data_raw.append(path_pdf)

            ConnectionS3.upload(m.__dict__, m.path_data_raw[0].replace('s3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
            self.beanstalk.watch.delete(job)
        except:
            self.beanstalk.watch.bury(job)

    def start(self):
        # with ThreadPoolExecutor(max_workers=2) as w:
            while(job := self.beanstalk.watch.reserve()):
                self._process_data(job)
            
if(__name__ == '__main__'):
    DukcapilProdukHukum().start()