import asyncio

from requests import Session, Response
from json import dumps
from aiohttp import ClientSession

from src.helpers import Parser

class BaseKamusLengkap:
    def __init__(self) -> None: 
        self.__headers: dict = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Cookie': '_ga_8T8L7MG7M3=GS1.1.1717070638.3.1.1717071469.60.0.0; _ga=GA1.2.1804044434.1716985220; _gid=GA1.2.202718563.1716985221; __gads=ID=2ef50b9b1c31086d:T=1716985222:RT=1717071318:S=ALNI_MYdqOU4YD-8YcDgtPxan_pZp_C2Dg; __gpi=UID=00000e33b9209fea:T=1716985222:RT=1717071318:S=ALNI_MarnK9CeN4Zyz5HTM-w4kWys4_BUA; __eoi=ID=d63376d28cd64b7e:T=1716985222:RT=1717071318:S=AA-AfjZgWf47nt1zAvEdvSXBreG9; MgidStorage=%7B%220%22%3A%7B%22svspr%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22svsds%22%3A2%7D%2C%22C136453%22%3A%7B%22page%22%3A1%2C%22time%22%3A%221717070674580%22%7D%7D; _gat_gtag_UA_62906508_1=1; FCNEC=%5B%5B%22AKsRol9l_4AvupogIEqSet_P-t4umHRM1Emo78hVzci8X8vurLStwoUAHbkbJKD7svl1oVyboxADyY7lzsf0xg1GsymjT2I_ja-N-vemZNFdcE6QXZZUnmCxa_Wx4jICEHbid9g7TAzJt35eieCtaes74EMN_v4Usg%3D%3D%22%5D%5D',
        }

    async def _get_all(self) -> list:
        all_data: list = []
        for i in range(ord('a'), ord('z') + 1):
            if(data := await self._get_by_char(chr(i))): all_data.extend(data.pop())
        
        print(dumps(all_data, indent=4))
        return all_data


    async def _get_by_char(self, char: str) -> list: 
        i: int = 0
        all_data: list = []
        for i in range(5):
            start: int = i * 10 + 1
            data: list = await asyncio.gather(*(self._get_by_char_page(char, page) for page in range(start, start + 10)))
            all_data.extend(data)
            if(False in data): break
            i += 1
            
        return [data for data in all_data if data]

    async def _get_by_char_page(self, char: str, page: int) -> dict: 
        async with ClientSession() as session:
            async with session.get(f'https://kamuslengkap.com/kamus/minang-indonesia/huruf/{char}/page/{page}',
                                   headers=self.__headers) as response:
                if(response.status != 200 or page < 1): return False
                soup: Parser = Parser(await response.text())
                return soup.select('.n29.b12.c67.b77.c23 a').map(lambda e: {'bahasa_minang': e.select_one('h3').get_text().strip(), 'bahasa_indonesia': e.select_one('p').get_text().strip()})


if(__name__ == '__main__'): 
    asyncio.run(BaseKamusLengkap()._get_all())
        