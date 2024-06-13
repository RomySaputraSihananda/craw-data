import asyncio

from aiohttp import ClientSession
from json import dumps, loads
from enum import Enum
from requests import Session, Response
from typing import Callable, Any, final, Generator
from functools import wraps
from time import time
from greenstalk import Client
from concurrent.futures import ThreadPoolExecutor, wait

from src.helpers import Parser, Datetime, Iostream, Decorator, ConnectionS3

from .categoryEnum import AcaraKadinEnum, DataDanStatistikEnum, MediaEnum, PengumumanEnum, ProgramEnum, RegulasiBisnisEnum, SolusiBisnisEnum, TentangKadinEnum

class KadinProgram:
    def __init__(self) -> None: 
        self.__beanstalk_use: Client = Client(('192.168.150.21', 11300), use='dev-target-kadin-regulasi')
        self.__beanstalk_watch: Client = Client(('192.168.150.21', 11300), watch='dev-target-kadin-regulasi')
        self.__requests: Session = Session();
        self.__requests.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'
        })

    @staticmethod
    def parse_description(func: Callable[..., None]) -> Callable[..., None]:
        @wraps(func)
        async def wrapper(self, *args: Any, **kwargs: Any) -> None:
            data: Any = await func(self, *args, **kwargs)
            soup: Parser = Parser(data["content"]["rendered"])
            
            data["content"]['images'] = soup.select('img').map(lambda e: e['src'])
            data["content"]['text'] = [t for t in [t.strip() for t in soup.get_text().split('\n')] if t]
            data["content"]["pdf"] = [a for a in soup.select('a').map(lambda e: e['href']) if a.endswith('.pdf')]
            
            return data
        return wrapper

    @staticmethod
    def parse_result(name_data: str = 'data_descriptive') -> Callable[..., None]:
        def decorator(func: Callable[..., None]) -> Callable[..., None]:
            @wraps(func)
            def wrapper(self, *args: Any, **kwargs: Any) -> None:
                data: dict = func(self, args[0])
                if(kwargs.get('write')):
                    result: dict = {
                        "link": (link := (enum := args[0]).value),
                        "domain": (link_split := link.split('/'))[2],
                        "tag": link_split[2:],
                        **data,
                        "crawling_time": Datetime.now(),
                        "crawling_time_epoch": int(time()),
                        "path_data_raw": [
                            f'S3://ai-pipeline-raw-data/data/{name_data}/kadin/{enum.identity}/json/{enum.name.lower()}.json',
                            *asyncio.run(self.__download_files([*(content := data["content"])["images"], *content["pdf"]], enum_identity=enum.identity))
                        ]
                    }
                    # Iostream.write_json(result, result['path_data_raw'][0].replace('S3://ai-pipeline-raw-data/', ''), indent=4)
                    ConnectionS3.upload(result, result['path_data_raw'][0].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
                    return result
                return data
            return wrapper
        return decorator

    def __get_id(self, enum: Enum) -> str:
        return Parser(self.__requests.get(enum.value).text).select_one('link[rel="shortlink"]')['href'].split('=')[-1]
    
    async def __download_files(self, urls: list, **kwargs) -> list:
        return await asyncio.gather(*(self.__download_file(url, **kwargs) for url in urls))

    async def __download_file(self, url: str, **kwargs) -> str:
        async with ClientSession() as session:
            async with session.get(url, headers=self.__requests.headers) as response:
                _, format = (file_name := url.rsplit('/', 1)[-1]).rsplit('.', 1)

                # ConnectionS3.upload_content(await response.read(), (path := f'S3://ai-pipeline-raw-data/data/data_gambar/kadin/{kwargs.get("enum_identity")}/{format}/{file_name}').replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
                ConnectionS3.upload_content(await response.read(), (path := f'S3://ai-pipeline-raw-data/data/{"data_descriptive" if format == "pdf" else  "data_gambar"}/kadin/{kwargs.get("enum_identity")}/{format}/{file_name}').replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
                
                return path

    def _get_data_by_enum(self, enum: Enum):
        if(enum == AcaraKadinEnum): return self._get_all_acara()
        if(enum == DataDanStatistikEnum): return self._get_all_data_dan_statistik()
        if(enum == MediaEnum): return self._get_all_media()
        if(enum == PengumumanEnum): return self._get_all_pengumuman()
        if(enum == ProgramEnum): return self._get_all_program()
        if(enum == RegulasiBisnisEnum): return self._get_all_regulasi_bisnis()
        if(enum == SolusiBisnisEnum): return self._get_all_solusi_bisnis()
        if(enum == TentangKadinEnum): return self._get_all_tentang_kadin()
    
    
    @parse_description
    async def __get_detail(self, id: str, **kwargs: Any) -> dict:
        async with ClientSession() as session:
            async with session.get(f'https://kadin.id/wp-json/wp/v2/{kwargs.get("type", "pages")}/{id}', headers=self.__requests.headers) as response:
                return await response.json()
    
    @parse_result()
    def _get_tentang_kadin(self, acara: AcaraKadinEnum, **kwargs) -> dict:
        return asyncio.run(self.__get_detail(self.__get_id(acara)))

    @parse_result()
    def _get_solusi_bisnis(self, solusi_bisnis: SolusiBisnisEnum, **kwargs) -> dict:
        return asyncio.run(self.__get_detail(self.__get_id(solusi_bisnis)))

    @parse_result()
    def _get_media(self, media: MediaEnum, **kwargs) -> dict:
        return asyncio.run(self.__get_detail(self.__get_id(media)))

    @parse_result()
    def _get_pengumuman(self, pengumuman: PengumumanEnum, **kwargs) -> dict:
        return asyncio.run(self.__get_detail(self.__get_id(pengumuman)))

    def _get_link_regulasi_bisnis(self, **kwargs) -> dict:
        response: Response = self.__requests.get('https://peraturan.go.id/cariglobal',
                                                params={
                                                    'PeraturanSearch[idglobal]': '',
                                                    'page': kwargs.get('page', 1)
                                                })
        return Parser(response.text).select('div.row div.col-lg-8 div.row div.col-md-12 div.strip.grid div.wrapper p a').map(lambda e: 'https://peraturan.go.id' + e['href'])
    
    async def _get_detail_regulasi_bisnis(self, url, **kwargs) -> dict:
        async with ClientSession() as session:
            async with session.get(url, headers=self.__requests.headers) as response:
                def filter_data(e) -> tuple:
                    th, td = e.children
                    if(files := td.select('a')): 
                        return (th.get_text().strip(), ['https://peraturan.go.id' + file['href'] for file in files])
                    return (th.get_text().strip(), td.get_text().strip())
                
                soup: Parser = Parser(await response.text())
                return {
                    'link': url,
                    'title': soup.select_one('h1').get_text().strip(),
                    **{key: value for key, value in [*soup.select('#w2 tr').map(filter_data), *soup.select('#reviews .card').map((lambda e: (e.select_one('h6').get_text().strip(), [li.get_text().strip() for li in e.select('ul li')])))]},
                }
        
    @parse_result('data_statistics')
    def _get_data_dan_statistik(self, data_dan_statistik: DataDanStatistikEnum, **kwargs) -> dict:
        return asyncio.run(self.__get_detail(self.__get_id(data_dan_statistik)))
    
    @parse_result()
    def _get_program(self, program: ProgramEnum, **kwargs) -> dict: 
        return asyncio.run(self.__get_detail(self.__get_id(program)))
    
    async def _get_acara(self, **kwargs) -> dict:
        response = self.__requests.post('https://kadin.id/acara-kadin/', 
                                        params={
                                            'nocache': '1718098915',
                                        }, 
                                        data={
                                            'action': 'jet_engine_ajax',
                                            'handler': 'listing_load_more',
                                            'query[query_id]': '63',
                                            'query[filtered_query][jet_smart_filters]': 'jet-engine/default',
                                            'query[filtered_query][suppress_filters]': 'false',
                                            'query[filtered_query][meta_query][0][key]': 'acara-mulai',
                                            'query[filtered_query][meta_query][0][value][]': [
                                                '1704067200',
                                                '1735689599',
                                            ],
                                            'query[filtered_query][meta_query][0][compare]': 'BETWEEN',
                                            'query[filtered_query][meta_query][0][type]': 'NUMERIC',
                                            'query[filtered_query][meta_query][acara mulai][_id]': '12393',
                                            'query[filtered_query][meta_query][acara mulai][collapsed]': 'false',
                                            'query[filtered_query][meta_query][acara mulai][key]': 'acara-mulai',
                                            'query[filtered_query][meta_query][acara mulai][type]': 'NUMERIC',
                                            'query[filtered_query][meta_query][acara mulai][clause_name]': 'acara mulai',
                                            'query[filtered_query][meta_query][acara mulai][compare]': 'EXISTS',
                                            'widget_settings[lisitng_id]': '3317',
                                            'widget_settings[posts_num]': '6',
                                            'widget_settings[columns]': '1',
                                            'widget_settings[columns_tablet]': '1',
                                            'widget_settings[columns_mobile]': '1',
                                            'widget_settings[is_archive_template]': '',
                                            'widget_settings[post_status][]': 'publish',
                                            'widget_settings[use_random_posts_num]': '',
                                            'widget_settings[max_posts_num]': '9',
                                            'widget_settings[not_found_message]': 'No data was found',
                                            'widget_settings[is_masonry]': 'false',
                                            'widget_settings[equal_columns_height]': '',
                                            'widget_settings[use_load_more]': 'yes',
                                            'widget_settings[load_more_id]': 'load-more-acara',
                                            'widget_settings[load_more_type]': 'click',
                                            'widget_settings[use_custom_post_types]': '',
                                            'widget_settings[hide_widget_if]': '',
                                            'widget_settings[carousel_enabled]': '',
                                            'widget_settings[slides_to_scroll]': '1',
                                            'widget_settings[arrows]': 'true',
                                            'widget_settings[arrow_icon]': 'fa fa-angle-left',
                                            'widget_settings[dots]': '',
                                            'widget_settings[autoplay]': 'true',
                                            'widget_settings[autoplay_speed]': '5000',
                                            'widget_settings[infinite]': 'true',
                                            'widget_settings[center_mode]': '',
                                            'widget_settings[effect]': 'slide',
                                            'widget_settings[speed]': '500',
                                            'widget_settings[inject_alternative_items]': '',
                                            'widget_settings[scroll_slider_enabled]': '',
                                            'widget_settings[scroll_slider_on][]': [
                                                'desktop',
                                                'tablet',
                                                'mobile',
                                            ],
                                            'widget_settings[custom_query]': 'yes',
                                            'widget_settings[custom_query_id]': '63',
                                            'widget_settings[_element_id]': '',
                                            'page_settings[post_id]': 'false',
                                            'page_settings[queried_id]': 'false',
                                            'page_settings[element_id]': 'false',
                                            'page_settings[page]': kwargs.get('page', 1),
                                            'listing_type': 'false',
                                            'isEditMode': 'false',
                                            'addedPostCSS[]': '3317',
                                        })
        return await asyncio.gather(*(self.__get_detail(id, type='acara') for id in Parser(response.json()['data']['html']).select('a').map(lambda e: e['href'].rsplit("#")[-1])))

    def _get_all_tentang_kadin(self, **kwargs) -> Generator:
        for tentang in TentangKadinEnum:
            yield self._get_tentang_kadin(tentang, **kwargs)

    def _get_all_solusi_bisnis(self, **kwargs) -> Generator:
        for solusi_bisnis in SolusiBisnisEnum:
            yield self._get_solusi_bisnis(solusi_bisnis, **kwargs)

    def _get_all_media(self, **kwargs) -> Generator:
        for media in MediaEnum:
            yield self._get_media(media, **kwargs)

    def _get_all_pengumuman(self, **kwargs) -> Generator:
        for pengumuman in PengumumanEnum:
            yield self._get_pengumuman(pengumuman, **kwargs)

    async def _get_all_regulasi_bisnis(self, **kwargs) -> Generator:
        page: int = 1
        while(True):
            links: list = self._get_link_regulasi_bisnis(page=page)
            self.__beanstalk_use.put(dumps({'page': page, 'links': links}, indent=4))
            print('send.... page %d' % page)
            if(len(links) < 10): break
            page += 1
    
    async def _watch_regulasi_bisnis(self, **kwargs):
        print('running...')
        while(job := self.__beanstalk_watch.reserve(timeout=60)):
            try:
                for data in await asyncio.gather(*(self._get_detail_regulasi_bisnis(link) for link in loads(job.body)['links'])):
                    result: dict = {
                        "domain": (link_split := data['link'].split('/'))[2],
                        "tag": link_split[2:],
                        "crawling_time": Datetime.now(),
                        **data,
                        "crawling_time_epoch": int(time()),
                        "path_data_raw": [
                            f'S3://ai-pipeline-raw-data/data/data_descriptive/kadin/regulasi_bisnis/json/{link_split[-1].lower().replace("-", "_").replace("/", " or ").replace(" ", "_")}.json',
                            *await self.__download_files(data["Dokumen Peraturan"], enum_identity=RegulasiBisnisEnum.REGULASI_BISNIS.identity)
                        ]
                    }
                    # Iostream.write_json(result, result['path_data_raw'][0].replace('S3://ai-pipeline-raw-data/', ''), indent=4)
                    ConnectionS3.upload(result, result['path_data_raw'][0].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')

                self.__beanstalk_watch.delete(job)
            except KeyboardInterrupt:
                exit() 
            except: 
                self.__beanstalk_watch.bury(job)

    async def _watch_regulasi_bisnis_thread(self, **kwargs):
        def wrapper(func):
            return asyncio.run(func)
        
        with ThreadPoolExecutor(max_workers=(max_workers := kwargs.get('max_workers'))) as executor:
            executor.map(wrapper, (self._watch_regulasi_bisnis() for _ in range(max_workers)))

    def _get_all_data_dan_statistik(self, **kwargs) -> Generator:
        for data_dan_statistik in DataDanStatistikEnum:
            yield self._get_data_dan_statistik(data_dan_statistik, **kwargs)
    
    def _get_all_acara(self, **kwargs) -> Generator:
        page: int = 1
        while(True):
            datas: dict = asyncio.run(self._get_acara(page=page, **kwargs))
            if(not datas): break
            for data in datas:
                if(kwargs.get('write')):
                    result: dict = {
                        "link": (link := data['link']),
                        "domain": (link_split := link.split('/')[:-1])[2],
                        "tag": link_split[2:],
                        **data,
                        "crawling_time": Datetime.now(),
                        "crawling_time_epoch": int(time()),
                        "path_data_raw": #[
                            f'S3://ai-pipeline-raw-data/data/data_descriptive/kadin/acara/json/{link_split[-1].lower().replace("-", "_")}.json',
                            # *asyncio.run(self.__download_files([*(content := data["content"])["images"], *content["pdf"]], enum_identity=enum.identity))
                        # ]
                    }
                    # Iostream.write_json(result, result['path_data_raw'].replace('S3://ai-pipeline-raw-data/', ''), indent=4)
                    ConnectionS3.upload(result, result['path_data_raw'].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')

            # yield data
            page += 1

    def _get_all_program(self, **kwargs) -> Generator: 
        for program in ProgramEnum:
            yield self._get_program(program, **kwargs)


if(__name__ == '__main__'):
    kadinProgram: KadinProgram = KadinProgram()
    asyncio.run(kadinProgram._watch_regulasi_bisnis_thread(max_workers=3))

    # print(list(kadinProgram._get_regulasi_bisnis(write=True)))

    # for enum in  [AcaraKadinEnum, DataDanStatistikEnum, MediaEnum, PengumumanEnum, ProgramEnum, RegulasiBisnisEnum, SolusiBisnisEnum, TentangKadinEnum]:
    #     data = kadinProgram._get_data_by_enum(enum)
