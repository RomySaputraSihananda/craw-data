__author__ = 'Gumilar Ganjar Permana'

import re
import requests
import asyncio

from requests import Response
from bs4 import BeautifulSoup
from aiohttp import ClientSession

from src.helpers import Iostream
from .kabupaten import KabupatenEnum

class WikipediaCrawler:
    def __init__(self) -> None:
        ...
    
    @staticmethod
    def __clean_text(text: str) -> str:
        clean_text: str = re.sub(r'(\n)?\[.*\](\n)?', ' ', text).replace(' • ', ' ').replace(' ', ' ').strip(' ')
        if(match := re.findall(r'Rp\.?\s*([+-]?\s*\d{1,3}(?:\.\d{3})*)(?:,\d+)?', clean_text)):
            return int("".join(match).replace('.', ''))
        elif '\n' in clean_text:
            return [clean for clean in clean_text.split('\n') if clean]
        elif '), ' in clean_text:
            clean_texts: list = [clean for clean in clean_text.split('), ') if clean]
            return [f'{clean})' if "(" in clean else clean for clean in clean_texts]
        
        return clean_text

    async def _get_wikipedia_detail_by_location(self, location: KabupatenEnum) -> dict:
        async with ClientSession() as session:
            async with session.get(location.value) as response:
                soup: BeautifulSoup = BeautifulSoup(await response.text(), 'html.parser')
                rows: list  = soup.select('.infobox.ib-settlement.vcard tbody tr')
                
                headers = {}
                for row in rows:
                    try:
                        data.update({
                            self.__clean_text(row.find('th').get_text()): self.__clean_text(row.find('td').get_text()) if not row.select('li') else [self.__clean_text(li.get_text()) for li in row.select('li')]
                        })
                    except:
                        if(images := row.select('img')):
                            for image in images:
                                value: str = 'https:' + image.attrs['src'] if not 'https:' in image.attrs['src'] else image.attrs['src']
                                key: str = value if not 'alt' in image.attrs else image.attrs['alt']
                                key: str = re.sub(r'\d+px-', '', value.split('/')[-1].split('.')[0]) if not key or 'https' in key else key
                                data: dict = {
                                    **headers,
                                    'images': headers['images'] | {key: value} if 'images' in headers else {key: value}
                                }
                Iostream.write_json(data, f'test/{data["Provinsi"].replace(" ", "_")}/{location.name.title()}.json')
    

    async def _get_all_location(self) -> None:
        await asyncio.gather(*(self._get_wikipedia_detail_by_location(kabupaten) for kabupaten in KabupatenEnum))

if(__name__ == '__main__'):
    asyncio.run(WikipediaCrawler()._get_all_location())
    # WikipediaCrawler()._get_wikipedia_detail_by_location(KabupatenEnum.KABUPATEN_BANTAENG)