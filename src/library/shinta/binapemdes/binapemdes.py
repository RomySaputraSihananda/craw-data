import asyncio
import json

from requests import Session   
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from redis import Redis
from time import time
from greenstalk import Client
from concurrent.futures import ThreadPoolExecutor, as_completed     
from loguru import logger
from .urls import urls, datas

class BinaPemdes:
    def __init__(self) -> None:
        self.__beanstalk_use: Client = Client(('192.168.150.21', 11300), use='dev-target-binapemdes')   
        self.__beanstalk_watch: Client = Client(('192.168.150.21', 11300), watch='dev-target-binapemdes')
        self.__session: Session = Session() 
        self.__session.headers.update({
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
        self.__session.get('https://prodeskel.binapemdes.kemendagri.go.id/default/?nm_run_menu=1&nm_apl_menu=mpublik&script_case_init=1&script_case_session=')

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

    def _get_table(self, obj, page = 1, size = 15, job=None):
        try:
            clean = lambda x: x.lower().replace(' ', '_').replace('-', '_').replace('/', '_')
            db = clean('db:binapemdes:%s:%s' % ((category:= obj["category"]), (sub_category := obj["sub_category"]))) 
            logger.info(f'start {db,  page}')
            response = self.__session.get(
                obj["url"]
            )
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

            try:
                data = get_data(page, size)
            except:
                self.__get_cookies()
                data = get_data(page, size)
                
            for d in data:
                self.__redis.rpush(db, json.dumps(d))

            logger.success(f'{db, page}')
            # self.__beanstalk_watch.delete(job)        
        except BaseException as e:
            logger.error(f'{db, page, e}')
            # self.__beanstalk_watch.bury(job)

    def _get_tables(self):
        max_workers = 5
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            while(job := self.__beanstalk_watch.reserve()):
                data = json.loads(job.body)        
                future = executor.submit(self._get_table, data, data["page"], 15, job)
                futures.append(future)

                if len(futures) >= max_workers:
                    for future in as_completed(futures):
                        futures.remove(future)

    def _send_target(self):
        def send(data):     
            if(isinstance(data["page"], str)): return
            for i in range(1, data["page"] + 1):
                print(self.__beanstalk_use.put(json.dumps({**data, 'page': i}), ttr=999999999, priority=1))
        with ThreadPoolExecutor(max_workers=2               ) as executor:          
            for data in datas:
                executor.submit(send, data)

if(__name__ == '__main__'):
    BinaPemdes()._send_target() 