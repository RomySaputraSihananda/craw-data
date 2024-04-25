import pandas
import asyncio
import requests

from json import dumps, loads
from requests import Session, Response
from aiohttp import ClientSession

from .subsector import Subsector

from src.helpers import Parser

class BaseBdsp():
    def __init__(self) -> None:
        self.__requests: Session = Session() 
        self.__requests.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        })

    def __get_provinces(self) -> list:
        return self.__requests.get('https://bdsp2.pertanian.go.id/bdsp/id/lokasi/getProv').json()
    
    def __get_kabupaten(self, fkode_prop: str) -> list:
        return self.__requests.post('https://bdsp2.pertanian.go.id/bdsp/id/lokasi/getKab',
                                    data={
                                        'fkode_prop': fkode_prop
                                    }).json()
        
    async def __get_komoditas(self, subsector: Subsector) -> list:
        try:
            async with ClientSession() as session:
                async with session.post('https://bdsp2.pertanian.go.id/bdsp/id/komoditas/getKomBySubsektor',
                                data={
                                    'subsektorcd': subsector.value
                                }) as response:
            
                    return await asyncio.gather(*(self.__get_indikator(subsector, komoditas) for komoditas in loads(await response.text())))
        except:
            await asyncio.sleep(1)
            return await self.__get_komoditas(subsector)
    
    
    async def __get_indikator(self, subsector: Subsector, komoditas: dict) -> list:
        try:
            async with ClientSession() as session:
                async with session.post('https://bdsp2.pertanian.go.id/bdsp/id/indikator/getIndiByKomSubsek',
                                        headers=self.__requests.headers,
                                        data={
                                            'subsektorcd': subsector.value,
                                            'komcd': komoditas["fkomcd"]
                                        }) as response:
            
                    return await asyncio.gather(*(self.__get_satuan(subsector, komoditas, indikator) for indikator in loads(await response.text())))
        except:
            await asyncio.sleep(1)
            return await self.__get_indikator(subsector, komoditas)
    
    async def __get_satuan(self, subsector: Subsector, komoditas: dict, indikator: dict) -> list:
        try:
            async with ClientSession() as session:
                async with session.post('https://bdsp2.pertanian.go.id/bdsp/id/satuan/getSatuan',
                                        headers=self.__requests.headers,
                                        data={
                                            'subsektorcd': subsector.value,
                                            'komcd': komoditas["fkomcd"],
                                            'indikatorcd': indikator["findicd"]
                                        }) as response:
            
                    return await asyncio.gather(*(self.__get_result(subsector, komoditas, indikator, {
                                    "fkode_prop": "35",
                                    "nama_prop": "Jawa Timur"
                        },satuan) for satuan in loads(await response.text())))
        except:
            await asyncio.sleep(1)
            return await self.__get_satuan(subsector, komoditas, indikator)

    async def __get_result(self, subsector: Subsector, komoditas: dict, indikator: dict, provinsi: dict, satuan: dict) -> str:
        try:
            async with ClientSession() as session:
                async with session.post('https://bdsp2.pertanian.go.id/bdsp/id/lokasi/result',
                                        headers=self.__requests.headers,
                                        data={
                                            'subsektorcd': subsector.value,
                                            'subsektornm': subsector.name.replace('_', ' ').title(),
                                            'komoditas': komoditas["fkomcd"],
                                            'komoditasnm': komoditas["fkomnm"],
                                            'indikator': indikator["findicd"],
                                            'indikatornm': indikator["findinm"],
                                            'level': '03',
                                            'levelnm': 'Kabupaten',
                                            'prov': provinsi['fkode_prop'],
                                            'provnm': provinsi["nama_prop"],
                                            'sts_angka': '6',
                                            'sts_angkanm': 'Angka Tetap',
                                            'sumb_data': '00',
                                            'sumb_datanm': '-- Pilih Sumber Data --',
                                            'tahunAwal': '1970',
                                            'tahunAkhir': '2024',
                                            'satuan': satuan["fkeyid"],
                                            'satuannm': satuan["fsatuan"],
                                            'judul': 'lokasi',
                                        }
                                    ) as response:
            
                    soup: Parser = Parser(data := await response.text())
                    print(data)
                    header: list = soup.select('table thead tr td').map(lambda e: e.get_text())
                    values: list = soup.select('table tbody tr').map(lambda e: [f.get_text() for f in e.select('td')])
                    footer: list = soup.select('table tfoot tr td').map(lambda e: e.get_text())

                    df = pandas.DataFrame(columns=header, data=[*values, [len(values) + 1, *footer]], index=False)
                    print(nama := '{}_{}_{}_{}_ {}'.format(
                        subsector.name.replace('_', ' ').title(),
                        komoditas["fkomnm"],
                        indikator["findinm"],
                        provinsi["nama_prop"],
                        satuan["fsatuan"])
                    )

                    async def write_excel_async(df, filename):
                        print(filename)
                        loop = asyncio.get_event_loop()
                        await loop.run_in_executor(None, pandas.DataFrame.to_excel, df, filename)

                    await write_excel_async(df, f'test/xlsx/{nama.replace("/", "_")}.xlsx')

        except Exception as e:
            print(e)
            await asyncio.sleep(1)
            await self.__get_result(subsector, komoditas, indikator, provinsi, satuan)

    
    async def start(self, subsector):
        provinsi = {
            "fkode_prop": "35",
            "nama_prop": "Jawa Timur"
        }

        await self.__get_komoditas(subsector)

        # for komoditas in self.__get_komoditas(subsector := Subsector.HORTIKULTURA):
        #     for indikator in self.__get_indikator(subsector, komoditas):
        #         await asyncio.gather(*(self.__get_result(subsector, komoditas, indikator, provinsi, satuan) for satuan in self.__get_satuan(subsector, komoditas, indikator)))
                    

if(__name__ == '__main__'):
    asyncio.run(BaseBdsp().start(Subsector.HORTIKULTURA))
    

    # import requests

    # headers = 

    # data = 

    # response = requests.post(
    #     'https://bdsp2.pertanian.go.id/bdsp/id/site/writeexcel/resultToExcel',
    #     headers=headers,
    #     data=data,
    # )

    # with open('test.xls', 'wb') as file:
    #         file.write(response.content)

