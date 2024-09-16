if(__name__ == '__main__'):
    data = open('src/library/dataEmoticon/emoticonid/ok.json', 'r').read()
    from json import loads
    from time import time
    print(len(loads(data)))

    from src.helpers import ConnectionS3, Iostream, Datetime
    r = []
    name_old = ''
    for i, d in enumerate(loads(data)):
        if(ada := (file := d["file_statistik"] and d["file_statistik"].split('/')[-1])):
            name_file, format = file.split('.')
        else:
            print(name)

        name = d["nama_dataset"] if d["nama_dataset"] else d['judul']
        if(name_old == name): name = name + '(2)'
        
        name_old = name


        result = {
            "link": (link := 'https://satudata.pertanian.go.id/datasets'),
            "source": (link_split := link.split('/')[:-1])[2],
            'tag': link_split[2:],
            "title": "Daftar Datasets",
            "sub_title": name,
            "range_data": None,
            "create_date": None,
            "update_date": None,
            "desc": None,
            "category": "dataset",
            "sub_category": None,
            'crawling_time': Datetime.now(),
            'crawling_time_epoch': int(time()),
            "table_name": None,
            "country_name": "Indonesia",
            "level": "Nasional",
            "stage": "Crawling data",   
            "update_schedule": "every three months and yearly",
            'data': d,
            'path_data_raw': [
                f's3://ai-pipeline-raw-data/data/data_statistics/satu_data_kementrian_pertanian/dataset/json/{name.strip().lower().replace("/", " or ").replace(" ", "_")}.json',
                *([f's3://ai-pipeline-raw-data/data/data_statistics/satu_data_kementrian_pertanian/dataset/{format}/{file.strip().lower().replace("/", " or ").replace(" ", "_")}'] if ada else [])
            ]
        }       

        ConnectionS3.upload(result, result['path_data_raw'][0].replace('s3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
        
        import requests

        if(ada): 
            ConnectionS3.upload_content(requests.get(d['file_statistik2']).content, result['path_data_raw'][1].replace('s3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
        