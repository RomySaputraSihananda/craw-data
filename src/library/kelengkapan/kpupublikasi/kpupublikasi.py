import os

from metadata import Metadata
from concurrent.futures import ThreadPoolExecutor
from src.helpers import ConnectionS3

data = [{'name': 'Laporan Tahunan 2023', 'link': 'https://kppu.go.id/wp-content/uploads/2024/07/Bundle-Laporan-Tahunan-KPPU-2023.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2024/05/Cover-Laporan-Tahunan-2023.png'}, {'name': 'Laporan Lima Tahun\n2018 – 2023', 'link': 'https://kppu.go.id/wp-content/uploads/2024/01/Laporan-Lima-Tahun-KPPU-2018-2023.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2024/01/Cover-Laporan-Lima-Tahun-KPPU-2018-2023.png'}, {'name': 'Laporan Tahunan 2022', 'link': 'https://kppu.go.id/wp-content/uploads/2023/08/Laporan-Tahunan-KPPU-2022.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2023/08/Cover-Laporan-Tahunan-KPPU-2022.jpg'}, {'name': 'Laporan Tahunan 2021', 'link': 'https://kppu.go.id/wp-content/uploads/2022/05/Laporan-Tahunan-KPPU-2021.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2022/04/Cover-Laporan-Tahunan-KPPU-2021.jpg'}, {'name': 'Laporan Tahunan 2020', 'link': 'https://kppu.go.id/wp-content/uploads/2021/04/Laporan-Tahunan-KPPU-2020.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2021/04/Cover-Laporan-Tahunan-KPPU-2020-scaled.jpg'}, {'name':'Laporan Tahunan 2019', 'link': 'https://kppu.go.id/wp-content/uploads/2020/06/Laporan-Tahunan-KPPU-2019_ok.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2020/06/Cover-Laporan-Tahunan-2019-Compressed.jpg'}, {'name':'Laporan Tahunan 2018', 'link': 'https://kppu.go.id/wp-content/uploads/2020/06/Laporan-Tahunan-2018.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2020/06/Cover-Laporan-Tahunan-2018-Compressed.jpg'}, {'name': 'Laporan Kinerja 2017', 'link': 'https://kppu.go.id/wp-content/uploads/2020/03/Laporan_Tahunan_KPPU_2017.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2020/06/Cover-Laporan-Kinerja-KPPU-2017-Compressed.jpg'}, {'name': 'Laporan Tahunan 2016', 'link': 'https://kppu.go.id/wp-content/uploads/2020/03/Laporan_Tahunan_KPPU_2016.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2020/06/Cover-Laporan-Tahunan-2016-Compressed.jpg'}, {'name': 'LaporanTahunan 2015', 'link': 'https://kppu.go.id/wp-content/uploads/2016/12/SPREAD-LAPORAN-TAHUNAN-KPPU-2015.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2020/06/Cover-Laporan-Tahunan-2015-Compressed-scaled.jpg'}, {'name': 'Laporan Tahunan 2014', 'link': 'https://kppu.go.id/wp-content/uploads/2020/03/LAPORAN-TAHUNAN-KPPU-2014.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2020/06/Cover-Laporan-Tahunan-2014-Compressed.jpg'}, {'name': 'Laporan Tahunan 2013', 'link': 'https://kppu.go.id/wp-content/uploads/2020/03/Laporan-Tahun-2013.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2020/06/Cover-Laporan-Tahunan-2013-Compressed.jpg'}, {'name': 'Laporan Kinerja 2012', 'link': 'https://kppu.go.id/wp-content/uploads/2020/03/Laporan-Tahun-2012.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2020/06/Cover-Laporan-Kinerja-KPPU-2012-Compressed.jpg'}, {'name': 'Laporan Tahun 2011', 'link': 'https://kppu.go.id/wp-content/uploads/2020/03/LAPORAN-KPPU_2011.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2020/06/Cover-Laporan-Tahun-2011.jpg'}, {'name': 'Laporan Tahun 2010', 'link': 'https://kppu.go.id/wp-content/uploads/2020/03/laporan-tahun-2010_180511.pdf', 'img':'https://kppu.go.id/wp-content/uploads/2020/06/Cover-Laporan-Tahun-2010-Compressed.jpg'}, {'name': 'Laporan Tahun 2009', 'link': 'https://kppu.go.id/wp-content/uploads/2020/03/laporan-kppu-2009-230511.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2020/06/Cover-Laporan-Tahun-2009-Compressed.jpg'}, {'name': 'Laporan Tahun 2008', 'link': 'https://kppu.go.id/wp-content/uploads/2015/07/Laporan-Tahun-2008.pdf', 'img': 'https://kppu.go.id/wp-content/uploads/2020/06/Cover-Laporan-Tahun-2008-Compressed.jpg'}]

class KpuPublikasi:
    def __init__(self) -> None:
        self.data = [{
            **d,
            'path': '/home/sc-rommy/Documents/kpu/' + d['link'].split('/')[-1]
        } for d in data]

    def send(self):
        clean = lambda x: x.lower().replace(' ', '_').replace(' ', '_').replace('-', '_').replace('/', '_').replace('-', '_')
        with ThreadPoolExecutor(max_workers=5) as ex:
            futures = []
            for data in self.data:
                path = data.pop('path')
                metadata = Metadata(
                    link='https://kppu.go.id/laporan-tahunan/',
                    source='kppu.go.id',
                    tags=[
                        'kppu.go.id',
                        'laporan-tahunan',
                    ],
                    sub_title=data['name'],
                    update_schedule='yearly',
                    stage='Kelengkapan data',   
                    path_data_raw=[
                        f"s3://ai-pipeline-raw-data/data/data_descriptive/kpu/laporan_tahunan/json/{clean(data['name'])}.json",
                        f"s3://ai-pipeline-raw-data/data/data_descriptive/kpu/laporan_tahunan/pdf/{clean(data['name'])}.pdf ",
                    ],
                    data=data, 
                    category='laporan-tahunan',
                    title='Laporan Tahunan',
                )
                futures.append(
                    ex.submit(
                        ConnectionS3.upload,
                        metadata.json,
                        metadata.path_data_raw[0].replace('s3://ai-pipeline-raw-data/', ''),
                        'ai-pipeline-raw-data'
                    )
                )
                futures.append(
                    ex.submit(
                        ConnectionS3.upload_content,
                        path,
                        metadata.path_data_raw[1].replace('s3://ai-pipeline-raw-data/', ''),
                        'ai-pipeline-raw-data'
                    )
                )
            for future in futures:
                future.result()

if(__name__ == '__main__'): KpuPublikasi().send()