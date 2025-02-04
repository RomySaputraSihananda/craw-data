import requests

from bs4 import BeautifulSoup
from metadata import Metadata
from src.helpers import ConnectionS3

clean = lambda x: x.lower().replace(' ', '_').replace(' ', '_').replace('-', '_').replace('/', '_').replace('-', '_')

class BphmigasLaporan:
    def __init__(self) -> None:
        self.datas = [
            [
                "LAPORAN KINERJA 2023 BPH MIGAS",
                "https://www.bphmigas.go.id/laporan-kinerja/laporan-kinerja-2023-bph-migas/"
            ],
            [
                "LAPORAN KINERJA 2022 BADAN PENGATUR HILIR MINYAK DAN GAS BUMI",
                "https://www.bphmigas.go.id/laporan-kinerja/laporan-kinerja-2022-badan-pengatur-hilir-minyak-dan-gas-bumi/"
            ],
            [
                "LAPORAN KINERJA 2021 BADAN PENGATUR HILIR MINYAK DAN GAS BUMI",
                "https://www.bphmigas.go.id/laporan-kinerja/laporan-kinerja-2021-badan-pengatur-hilir-minyak-dan-gas-bumi/"
            ],
            [
                "Laporan Kinerja BPH Migas 2020",
                "https://www.bphmigas.go.id/laporan-kinerja/laporan-kinerja-bph-migas-2020/"
            ],
            [
                "Laporan Kinerja BPH Migas Tahun 2019",
                "https://www.bphmigas.go.id/laporan-kinerja/laporan-kinerja-bph-migas-tahun-2019/"
            ],
            [
                "Laporan Kinerja BPH Migas Tahun 2018",
                "https://www.bphmigas.go.id/laporan-kinerja/laporan-kinerja-bph-migas-tahun-2018/"
            ]
        ]
    
    def __download(self, link, path):
        ConnectionS3\
            .upload_content(
                requests.get(
                    link,
                    verify=False
                ).content, 
                path.replace('s3://ai-pipeline-raw-data/',''), 
                'ai-pipeline-raw-data'
            )
        
        return path

    def send(self):
        for name, link in self.datas:
            response = requests.get(link, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            link_pdf = soup.select_one('iframe')["data-src"].split('file=')[-1]
            metadata = Metadata(
                link=link,
                source='www.bphmigas.go.id',
                tags=[
                    'www.bphmigas.go.id',
                    'LAPORAN KINERJA'
                ],
                title=name,
                data={
                    'name': name,
                    'link_document': link_pdf,
                    'link': link
                },
                desc='Badan Pengatur Hilir Minyak dan Gas Bumi',
                category='laporan-kinerja',
                path_data_raw=[
                    f's3://ai-pipeline-raw-data/data/data_descriptive/bph_migas/laporan_kinerja/json/{clean(name)}.json'
                ],
                update_schedule='yearly'
            )

            metadata.path_data_raw.append(
                self.__download(
                    link,
                    metadata.path_data_raw[0].split('/json')[0] + f'/pdf/{clean(name)}.pdf'
                )
            )
            ConnectionS3\
                .upload(
                    metadata.dict,
                    metadata.path_data_raw[0].replace('s3://ai-pipeline-raw-data/',''), 
                    'ai-pipeline-raw-data'
                )

if(__name__ == '__main__'):
    BphmigasLaporan().send()