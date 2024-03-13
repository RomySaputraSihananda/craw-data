import os
import asyncio

from dotenv import load_dotenv
from requests import Response, Session
from aiohttp import ClientSession

load_dotenv()

class BaseKlook:
    def __init__(self) -> None:
        self.__requests: Session = Session()
        self.__requests.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; arm_64; Android 12; CPH2205) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.3.86.00 SA/3 Mobile Safari/537.36",
            "currency": "IDR",
            "Cookie": os.getenv('COOKIE_KLOOK')
        })

    def _get_id_countries(self) -> list: 
        response : Response = self.__requests.get('https://www.klook.com/v1/usrcsrv/destination/guide')
        return [country['klook_id'] for country in response.json()['result']['app_destination_guide_list'][0]['sub_menu_list']]
    
    def _get_activities(self, country_id: int, page: int, **kwargs) -> list | None:
        response : Response = self.__requests.get(f'https://www.klook.com//v2/usrcsrv/search/country/{country_id}/activities?start={page}&size={kwargs.get("size", 25)}')
        
        return response.json()['result']['activities']

    def _get_info_activity(self, url: str) -> dict:
        response: Response = self.__requests.get(url)
        print(response.text)

    async def _process_activity(self, activity: dict) -> None: ...

if(__name__ == '__main__'):
    print(
            BaseKlook()._get_info_activity('https://www.klook.com/id/activity/2082-go-karting-experience-akihabara-tokyo/')
    )