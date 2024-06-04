import asyncio
import re

from requests import Session, Response
from json import dumps
from os.path import join
from time import time
from aiohttp import ClientSession
from aiofiles import open

from .enums import ProfilEnum, StatistikEnum

from src.helpers import Parser, Datetime, Iostream, ConnectionS3

class BaseKemenparekraf:
    def __init__(self) -> None:
        self.__requests: Session = Session()
        self.__requests.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
        }) 

    @staticmethod
    def build_dict(url: str) -> dict:
        if(isinstance(url, dict)): return url
        extension  = (file_name := url.split('/')[-1]).split('.', )[-1]
        return {
            'path': url,
            'extension': extension,
            'file_name': file_name
        } 

    async def __download_files(self, data: dict, **kwargs) -> list:
        if(kwargs.get('enum').__class__ == StatistikEnum):
            return await asyncio.gather(*(self.__download_file(file, **kwargs) for file in [*data['files'], data['featured_image']] if file))
        return await asyncio.gather(*(self.__download_file(self.build_dict(file), **kwargs) for file in [re.findall(r'https?://.*?.pdf', data['content'])[0], data['image_url'], data['cover']] if file))

    async def __download_file(self, data: dict, **kwargs) -> str:
        try:
            type = 'data_descriptive'
            match(extension := data['extension'].lower()):
                case 'xlsx' | 'csv':
                    type = 'data_statistics'
                case 'png' | 'jpg' | 'jpeg':
                    type = 'data_gambar'
                case '_': ...
            async with ClientSession() as session:
                async with session.get(data['path'], headers=self.__requests.headers) as response:
                    ConnectionS3.upload_content(await response.read(), (path := f'S3://ai-pipeline-raw-data/data/{type}/kemenparekraf/{"statistik" if (enum := kwargs.get("enum")).__class__ == StatistikEnum else "profil"}/{enum.value["slug"].replace("-", "_").lower()}/{extension}/{data["file_name"].replace(" ", "_").lower()}').replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
                    return path

        except Exception as e:
            print(e)
            print(data)

    async def __get_detail_profile(self, data: dict):
        async with ClientSession() as session:
                async with session.get(join('https://api2.kemenparekraf.go.id/api/v1/articles', data['slug'])) as response:
                    return (await response.json())['data'] | data
        
    async def _get_statistics(self, statistik: StatistikEnum, **kwargs) -> list:
        response: Response = self.__requests.get('https://api2.kemenparekraf.go.id/api/v1/statistics/posts',
            params={
                'pageSize': kwargs.get('size', 10),
                'query': '',
                'filterData': dumps({"category_id": (statistik_value := statistik.value)['categoryFilter']}),
                'order_by': 'published_at',
                'order_dir': 'desc',
                'pageIndex': kwargs.get('page', 1) - 1,
            },
        )
        def process_data(data):
            data['description'] = Parser(data['description']).get_text().strip()
            return data
        
        if not (datas := response.json()['data']): return
            
        datas: list = [process_data(data) for data in datas]
        
        if(kwargs.get('write')):
            for data in datas:
                result: dict = {
                    "link": (link := join('https://www.kemenparekraf.go.id', filter := statistik_value['slug'], name := data['slug'])),
                    "domain": (link_split := link.split('/'))[2],
                    "tag": link_split[2:],
                    "crawling_time": Datetime.now(),
                    **data,
                    "crawling_time_epoch": int(time()),
                    "path_data_raw": [
                        f'S3://ai-pipeline-raw-data/data/data_descriptive/kemenparekraf/statistik/{filter.replace("-", "_").lower()}/json/{name.replace("-", "_").lower()}.json',
                        *await self.__download_files(data, enum=statistik)
                    ]
                }

                ConnectionS3.upload(result, result['path_data_raw'][0].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
        
        return datas
    
    async def _get_by_statistic(self, statistik: StatistikEnum, **kwargs) -> list:
        (datas, i) = ([], 1) 
        while(True):
            data: list = await self._get_statistics(statistik=statistik, page=i, **kwargs) 
            if(not data): break
            datas.extend(data)
            i += 1
        return datas
    
    async def _get_all_statistics(self, **kwargs):
        return [await self._get_by_statistic(statistik=statistik, **kwargs) for statistik in StatistikEnum]
    
    async def _get_profiles(self, profile: ProfilEnum, **kwargs) -> list:
        response: Response = self.__requests.get('https://api2.kemenparekraf.go.id/api/v1/articles',
            params={
                'pageSize': kwargs.get('size', 10),
                'query': '',
                'filterData': dumps({"category_id": (profile_value := profile.value)['categoriesFilter']}),
                'order_by': 'published_at',
                'order_dir': 'desc',
                'pageIndex': kwargs.get('page', 1) - 1,
            },
        )
        
        if not (datas := response.json()['data']): return

        datas: list = await asyncio.gather(*(self.__get_detail_profile(data) for data in datas))
        
        
        if(kwargs.get('write')):
            for data in datas:
                del data["relatedArticles"]
                result: dict = {
                    "link": (link := join('https://www.kemenparekraf.go.id', filter := profile_value['slug'], name := data['slug'])),
                    "domain": (link_split := link.split('/'))[2],
                    "tag": link_split[2:],
                    "crawling_time": Datetime.now(),
                    **data,
                    "crawling_time_epoch": int(time()),
                    "path_data_raw": [
                        f'S3://ai-pipeline-raw-data/data/data_descriptive/kemenparekraf/profil/{filter.replace("-", "_").lower()}/json/{name.replace("-", "_").lower()}.json',
                        *await self.__download_files(data, enum=profile)
                    ]
                }

                ConnectionS3.upload(result, result['path_data_raw'][0].replace('S3://ai-pipeline-raw-data/', ''), 'ai-pipeline-raw-data')
        
        return datas
    
    async def _get_by_profile(self, profile: ProfilEnum, **kwargs) -> list:
        (datas, i) = ([], 1) 
        while(True):
            data: list = await self._get_profiles(profile=profile, page=i, **kwargs) 
            if(not data): break
            datas.extend(data)
            i += 1
        return datas
    
    async def _get_all_profiles(self, **kwargs):
        return [await self._get_by_profile(profile=profile, **kwargs) for profile in ProfilEnum]

if(__name__ == '__main__'):

    baseKemenparekraf: BaseKemenparekraf = BaseKemenparekraf()
    # data = asyncio.run(baseKemenparekraf._get_all_statistics(write=True))
    data = asyncio.run(baseKemenparekraf._get_all_profiles(write=True))
    print([len(d) for d in data])