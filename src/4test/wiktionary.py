import pandas
from time import time

from src.helpers import Datetime, Iostream, ConnectionS3
from src.library.dataDivtik.wiktionary.wiktionary import Wiktionary

wiktionary = Wiktionary()
def main(data):
    datos = wiktionary._start(link := data['link_kamus_bahasa_daerah'])
    
    if(len(str(datos)) < 1000): return
    filter: function = lambda x: x.strip().lower().replace(" ", "_")
    
    result: dict = {
        "link": link,
        "domain": (link_split := link.split('/'))[2],
        "tag": link_split[2:],
        "crawling_time": Datetime.now(),
        **datos,
        "crawling_time_epoch": int(time()),
        "path_data_raw": f'S3://ai-pipeline-raw-data/data/data_descriptive/data_kamus/{(Provinsi := filter(data["Provinsi"]))}/{(nama_bahasa := filter(data["nama_bahasa"]))}/json/{filter(link_split[-1])}.json'
    }

    # Iostream.write_json(result, result["path_data_raw"].replace('S3://ai-pipeline-raw-data/', ''), indent=4)
    ConnectionS3.upload(result, result["path_data_raw"].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
    print(link)

if(__name__ == '__main__'):
    for data in [data for data in pandas.read_csv('https://docs.google.com/spreadsheets/d/1eEI6tNBQ5O8n6J_qXk-CPZD1EgPxDBcjF3zEtpGtAFU/export?format=csv&gid=394669076').to_dict('records') if 'https://repositori.kemdikbud.go.id/16214/1/Kamus%20Bahasa%20Simalungun%20-%20Indonesia%20Edisi%20Kedua%20Tahun%202016.pdf' in str(data['link_kamus_bahasa_daerah'])]:
        # main(data)
        print(data)
    