import zipfile
import io
import asyncio

from time import time
from aiohttp import ClientSession

from src.helpers import Parser, requests, Datetime, Iostream, ConnectionS3
from .enums import CategoryEnum, ProvinceEnum


class BaseBISekda:
   def __init__(self) -> None: ...

   def __get_ticket_provinsi(self, provinsi: ProvinceEnum) -> tuple:
      response = requests.get('https://www.bi.go.id/id/statistik/ekonomi-keuangan/sekda/StatistikRegionalDetail.aspx',
                              params={
                                 'idprov': str(provinsi.value)
                              },
                              headers={
                                 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                              })
      soup: Parser = Parser(response.text)
      
      return (soup.select_one('#__EVENTVALIDATION')['value'], soup.select_one('#__VIEWSTATE')['value'])

   @staticmethod
   async def download(**kwargs):
      async with ClientSession() as session:
         async with session.get(kwargs.get('url'),
                              headers={
                                 'Content-Type': 'application/x-www-form-urlencoded'
                              }) as response:
            results = []
            with zipfile.ZipFile(io.BytesIO(await response.read())) as zip_ref:
               for file_name in zip_ref.namelist():
                  _, format =  file_name.split('.')
                  with zip_ref.open(file_name) as file_in_zip:
                     # import os
                     ConnectionS3.upload_content(file_in_zip.read(), (result_path := f'S3://ai-pipeline-statistics/data/data_raw/bank_indonesia/BI/sekda/{(kwargs.get("provinsi").name)}/{format}/{file_name}').replace('S3://ai-pipeline-statistics/', ''))
                     # output_dir = (result_path := f'S3://ai-pipeline-statistics/data/data_raw/bank_indonesia/BI/sekda/{(kwargs.get("provinsi").name)}/{format}/{file_name}').replace('S3://ai-pipeline-statistics/', '')
   
                     # if not os.path.isdir(output_dir2 := os.path.dirname(output_dir)): 
                     #    os.makedirs(output_dir2, exist_ok=True) 
                     
                     # from aiofiles import open

                     # async with open(output_dir, 'wb') as f:
                     #    await f.write(file_in_zip.read())
                        
                  results.append(result_path)
            
            return results

   async def _get_by_provinsi_category(self, provinsi: ProvinceEnum, category: CategoryEnum):
      (__EVENTVALIDATION, __VIEWSTATE) = self.__get_ticket_provinsi(provinsi)
      response = requests.post('https://www.bi.go.id/id/statistik/ekonomi-keuangan/sekda/StatistikRegionalDetail.aspx',
                              params={
                                 'idprov': str(provinsi.value)
                              },
                              headers={
                                 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                 'Content-Type': 'application/x-www-form-urlencoded'
                              }, 
                              data={
                                 "MSOGallery_FilterString": "",
                                 "MSOGallery_SelectedLibrary": "",
                                 "MSOLayout_InDesignMode": "",
                                 "MSOLayout_LayoutChanges": "",
                                 "MSOSPWebPartManager_DisplayModeName": "Browse",
                                 "MSOSPWebPartManager_EndWebPartEditing": "false",
                                 "MSOSPWebPartManager_ExitingDesignMode": "false",
                                 "MSOSPWebPartManager_OldDisplayModeName": "Browse",
                                 "MSOSPWebPartManager_StartWebPartEditingName": "false",
                                 "MSOTlPn_Button": "none",
                                 "MSOTlPn_SelectedWpId": "",
                                 "MSOTlPn_ShowSettings": "False",
                                 "MSOTlPn_View": "0",
                                 "MSOWebPartPage_PostbackSource": "",
                                 "MSOWebPartPage_Shared": "",
                                 "__EVENTARGUMENT": "",
                                 "__EVENTTARGET": "ctl00$ctl54$g_077c3f62_96a4_43aa_b013_8e274cf2ce9d$ctl00$DropDownListCategorySekda",
                                 "__EVENTVALIDATION": __EVENTVALIDATION,
                                 "__LASTFOCUS": "",
                                 "__REQUESTDIGEST": "",
                                 "__SCROLLPOSITIONX": "0",
                                 "__SCROLLPOSITIONY": "0",
                                 "__VIEWSTATE": __VIEWSTATE,
                                 "__VIEWSTATEGENERATOR": "30A8BD62",
                                 "_maintainWorkspaceScrollPosition": "0",
                                 "_wpSelected": "",
                                 "_wpcmWpid": "",
                                 "_wzSelected": "",
                                 'ctl00$ctl54$g_077c3f62_96a4_43aa_b013_8e274cf2ce9d$ctl00$DropDownListProvinsiSekda': str(provinsi.value),
                                 'ctl00$ctl54$g_077c3f62_96a4_43aa_b013_8e274cf2ce9d$ctl00$DropDownListCategorySekda': str(category.value),
                                 "ctl00$ctl74": "",
                                 "wpcmVal": "",
                              })

      soup: Parser = Parser(response.text)

      data: dict = {
         'link': (link := response.url),
         'domain': (link_split := link.split('/'))[2],
         'tag': link_split[2:],
         'domain': link_split[2],
         'crawling_time': Datetime.now(),
         'crawling_time_epoch': int(time()),
         'title': 'Statistik Ekonomi dan Keuangan Daerah (SEKDA)',
         'Indikator Ekonomi Regional Terpilih Provinsi': provinsi.name.title().replace('_', ' '),
         'Kategori': category.name.title().replace('_', ' '),
         'Kategori Statistik': dict(soup.select('table > tr td a').map(lambda e: (e.get_text().strip(), e['href']))),
         'path_data_raw': [
            f'S3://ai-pipeline-statistics/data/data_raw/bank_indonesia/BI/sekda/{(provinsi.name)}/json/{category.name}.json'
         ]
      }

      for path in await asyncio.gather(*(self.download(url=link, provinsi=provinsi) for link in data['Kategori Statistik'].values())):
         data['path_data_raw'].extend(path)

      # Iostream.write_json(data, data['path_data_raw'][0].replace('S3://ai-pipeline-statistics/', ''), indent=4)
      ConnectionS3.upload(data, data['path_data_raw'][0].replace('S3://ai-pipeline-statistics/', ''))

   async def _get_by_provinsi(self, provinsi: ProvinceEnum):
      await asyncio.gather(*(self._get_by_provinsi_category(provinsi, category) for category in CategoryEnum))

   async def _get_by_category(self, category: CategoryEnum):
      await asyncio.gather(*(self._get_by_provinsi_category(provinsi, category) for provinsi in ProvinceEnum))
   
   async def _get_all(self):
      for provinsi in ProvinceEnum:
         await self._get_by_provinsi(provinsi)

if(__name__ == '__main__'): 
   asyncio.run(BaseBISekda()._get_by_provinsi(ProvinceEnum.PAPUA_BARAT))