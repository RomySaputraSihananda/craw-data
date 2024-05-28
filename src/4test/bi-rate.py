import requests
from calendar import month_name
from json import dumps
from src.helpers import ConnectionKafka
def fetch(date):
    month, year = date.split('/')

    res = requests.get(f'http://server.ubuntu.ph:8088/api/v2/data_tingkat_suku_bunga_bulanan',
                 params={
                    'start_date': date,
                    'end_date': date
                 })
    if res.status_code != 200: return

    return{
        "link": "https://www.bi.go.id/id/statistik/informasi-kurs/transaksi-bi/default.aspx",
        "domain": "www.bi.go.id",
        "tag": [
            "BI-Rate",
            "BI",
            "Bank Indonesia",
            "www.bi.go.id"
        ],
        "data": res.json(),
        "path_data_raw": f"S3://ai-pipeline-statistics/data/data_raw/bank_indonesia/bi_rate/statistik/json/{month_name[int(month)]} {year}.json",
        "crawling_time_epoch": 1715847634935,
        "crawling_time": "2024-05-16 15:20:34"
    }

connectionKafka: ConnectionKafka = ConnectionKafka(bootstrap_servers='kafka01.research.ai,kafka02.research.ai,kafka03.research.ai', topic='data-knowledge-repo-general_4')

if(__name__ == '__main__'):
    for i in range(2016, 2024 + 1):
        for j in range(1, 12 + 1):
            data = fetch(f'{"0" if j < 10 else ""}{j}/{i}')
            if(data):
                connectionKafka.send(data)