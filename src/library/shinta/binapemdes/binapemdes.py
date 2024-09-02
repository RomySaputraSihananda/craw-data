import asyncio
import json

from requests import Session   
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from redis import Redis
from time import time
from greenstalk import Client

from src.helpers import Datetime, Iostream

from .urls import urls

class BinaPemdes:
    def __init__(self) -> None:
        self.__beanstalk_use: Client = Client(('192.168.150.21', 11300), use='dev-target-rs')
        self.__beanstalk_watch: Client = Client(('192.168.150.21', 11300), watch='dev-target-rs')

        self.__session: Session = Session()
        self.__session.headers.update({
            # 'Cookie': 'PHPSESSID=;',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
        })

        self.__get_cookies()

        self.__redis: Redis = Redis(
            '192.168.20.175',
            db=2,
            decode_responses=True
        )
    @staticmethod
    def fill_missing_data(data):
        for i, d in enumerate(data):
            for key in d:
                if(not d[key]):
                    d[key] = data[i - 1][key]
        return data

    @staticmethod
    def parse_table(html):
        clean = lambda x: x.get_text().strip().replace('\\r', '').replace('\\n', '')
        
        soup = BeautifulSoup(html, 'html.parser')
        tr = soup.select('table tr')
        
        keys = [clean(td) for td in tr.pop(0).select('td')]
        keys[0] = 'no'
        data = [{keys[i]: clean(td) for i, td in enumerate(t.select('td'))} for t in tr]
        try:
            return BinaPemdes.fill_missing_data(data)
        except: return data

    def __get_cookies(self):
        res = self.__session.get('https://prodeskel.binapemdes.kemendagri.go.id/default/?nm_run_menu=1&nm_apl_menu=mpublik&script_case_init=1&script_case_session=')

    def _get_table_paging(self, url, page, soup, size = 50):
        response = self.__session.post(
            url,
            data={
                'nmgp_opcao': 'ajax_navigate',
                'opc': 'muda_qt_linhas' if page == 1 else 'rec', 
                'parm': size if page == 1 else size * (page - 1) + 1,
                **{
                    input.get('name'): input.get('value') 
                    for input in soup.select_one('form[name="F6"]').select('input')
                },
                'script_case_session': self.__session.cookies.get('PHPSESSID')
            },
            timeout=500
        )
        [value] = [s["value"] for s in response.json()["setValue"] if s["field"] == "sc_grid_body"]
        
        return self.parse_table(value)
    
    def _get_data_redis(self):
        ...

    def _test(self):...
        # result: dict = {
        #         "link": (link := obj["url"]),
        #         "domain": (link_split := link.split('/'))[2],
        #         "tag": [
        #             *link_split[2:],
        #             (title := 'KEMENTERIAN DALAM NEGERI DIREKTORAT JENDERAL PEMBERDAYAAN MASYARAKAT DAN DESA BATAS WILAYAH'),
        #             category,
        #             sub_category
        #         ],
        #         "title": title,
        #         "category": category,
        #         "sub_category": sub_category,
        #         'data': data,
        #         "crawling_time": Datetime.now(),
        #         "crawling_time_epoch": int(time()),
        #         "path_data_raw": f's3://ai-pipeline-raw-data/data/data_statistics/kemendagri/prodeskel_bina_pemdes/{clean(category)}/json/{clean(sub_category)}.json'
        #     }
            
        #     Iostream.write_json(
        #         result,
        #         result["path_data_raw"].replace('s3://ai-pipeline-raw-data/', ''),
        #         indent=4
        #     )

    def _get_table(self, obj, page = 1, size = 15):
        response = self.__session.get(
            obj["url"]
        )

        print(response)
        print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')

        form = soup.find('form')    
        url = urljoin("https://prodeskel.binapemdes.kemendagri.go.id", form.get('action'))
        a = self.__session.post(
            url, 
            data={
                input.get('name'): input.get('value') 
                for input in form.select('input')
            }
        ).text

        def get_data(page, size):
            return self._get_table_paging(
                url, 
                page, 
                BeautifulSoup(
                    a,'html.parser'   
                ), 
                size
            )     

        while(True):
            try:
                data = get_data(page, size)
            except:
                self.__get_cookies()
                data = get_data(page, size)
            
            clean = lambda x: x.lower().replace(' ', '_').replace('-', '_').replace('/', '_')
            db = clean('db:binapemdes:%s:%s' % ((category:= obj["category"]), (sub_category := obj["sub_category"]))) 

            for d in data:
                self.__redis.rpush(db, json.dumps(d))

            print(f'[{page}]', db, len(data))

            if(len(data) < size): break
            
            page += 1

    def _get_tables(self):
        while(job := self.__beanstalk_watch.reserve()):
            try:
                self._get_table(json.loads(job.body))
                self.__beanstalk_watch.delete(job)
            except:
                self.__beanstalk_watch.bury(job)

    def _send_target(self):
        for url in urls:
            print(url)
            self.__beanstalk_use.put(json.dumps(url))

if(__name__ == '__main__'):
    BinaPemdes()._get_tables()
    # BinaPemdes.parse_table(open('/home/sc-rommy/Desktop/dasor-皇/craw-data/test.html', 'r').read())