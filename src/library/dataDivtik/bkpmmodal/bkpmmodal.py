import asyncio

from urllib.parse import parse_qs
from httpx import AsyncClient
from bs4 import BeautifulSoup
from metadata import Metadata
from datetime import datetime
from playwright.async_api import async_playwright
from src.helpers import ConnectionS3
class BkpmModal:
    def __init__(self) -> None:
        self.__assesion = AsyncClient()

    async def _process_document(self, obj, page):
        await page.goto(obj["link"])

        data = {
            k: v[0] for k, v in parse_qs(obj["link"].split('?')[-1]).items()
        }

        for selector, value in [
            ('#name', 'test '),
            ('#email', 'test@test.test'),
            ('#phone', '19')
        ]:
            await page.type(selector, value)

        async with page.expect_download(timeout=360000) as download_info:
            await (await page.wait_for_selector('#btn-btn')).click()
            download = await download_info.value
            _, format = (filename := data["filename"].lower().replace(' ', '_').replace('-', '_')).rsplit('.', 1)
            
            await download.save_as(filename_tmp := '/tmp/%s/%s' % (format, filename))
        
        metadata = Metadata(
            link='https://www.bkpm.go.id/id/info/realisasi-investasi/',  
            source='www.bkpm.go.id',
            tags=[
                'www.bkpm.go.id',
                'info',
                'realisasi-investasi',
                'Realisasi Penanaman Modal'
            ],
            title='Investment Realizations',
            desc='Browse Investment Realization reports from Ministry of Investment/BKPM, Layanan data terbuka dari Kementerian Investasi/BKPM, Pintu utama untuk mengakses informasi dan aplikasi perizinan dan nonperizinan',
            category='Realisasi Penanaman Modal',
            data={**obj, **data},
            sub_title=obj["title"],
            path_data_raw=[
                f'  /json/{obj["title"].lower().replace(" ", "_").replace("-", "_")}.json',
                f's3://ai-pipeline-raw-data/data/data_descriptive/bkpm/realisasi_penanaman_modal/{format}/{filename}',
            ],
            create_date=obj["create_date"],
            update_schedule='monthly'
        )
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = []
            futures.append(
                executor.submit(
                    ConnectionS3.upload_content, 
                    filename_tmp, 
                    metadata.path_data_raw[1].replace('s3://ai-pipeline-raw-data/', ''), 
                    'ai-pipeline-raw-data'
                )
            )
            futures.append(
                executor.submit(
                    ConnectionS3.upload,
                    metadata.json, 
                    metadata.path_data_raw[0].replace('s3://ai-pipeline-raw-data/', ''), 
                    'ai-pipeline-raw-data'
                )
            )

            for future in futures:
                future.result()

    async def worker(self):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=False)
            page = await browser.new_page()
            page_int = 1
            while(True):
                datas = [data async for data in self._get_documents(page_int)]
                if(not datas): break
                for data in datas:
                    await self._process_document(
                        data,
                        page    
                    )       
                page_int += 1

    async def _get_documents(self, page):
        response = await self.__assesion.get(   
            'https://www.bkpm.go.id/id/info/realisasi-investasi',
            params={
                'page': page
            }
        )

        soup = BeautifulSoup(response.text, 'html.parser')
        clean = lambda x: x.replace("Jan", "Jan").replace("Feb", "Feb").replace("Mar", "Mar").replace("Apr", "Apr").replace("Mei", "May").replace("Jun", "Jun").replace("Jul", "Jul").replace("Agt", "Aug").replace("Sep", "Sep").replace("Okt", "Oct").replace("Nov", "Nov").replace("Des", "Dec")
        for div in soup.select('#ul > div')[1:]:
            yield {
                    'link': div.select_one('button[data-bs-target="#staticBackdrop"]')['data-remote'],
                    'title': div.select_one('h2').get_text(strip=True),
                    'create_date': datetime.strptime(clean(div.select_one('p').get_text(strip=True)), "%d %b %Y").strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )   
                }

if(__name__ == '__main__'):
    b = BkpmModal()
    asyncio.run(b.worker()) 