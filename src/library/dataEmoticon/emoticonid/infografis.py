
import requests
class BaseSatuDataPertanianInfografis(Spider):
    start_urls = ['https://satudata.pertanian.go.id/datasets/infografis']

    def __init__(self, **kwargs: Any):
        super().__init__('pertanian-infografis', **kwargs)

    def start(self, *args, **kwargs) -> None:
        process = CrawlerProcess(get_project_settings())
        process.crawl(BaseSatuDataPertanianInfografis)

        return process.start()
    
    def __download_image(self, urls: str):
        for url in urls:
            _, format = (file := url.split('/')[-1]).split('.') 

            if((response := requests.get(url)).status_code == 200):
                ConnectionS3.upload_content(response.content, (path := f'S3://ai-pipeline-statistics/data/data_raw/data statistic/satu data kementrian pertanian/infografis/{format}/{file}').replace('S3://ai-pipeline-statistics/', ''))
                yield path

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for card in response.css('.text-center'):
            data: dict = {
                'link': (link := 'https://satudata.pertanian.go.id/datasets'),
                'domain': (link_split := link.split('/')[:-1])[2],
                'tag': link_split[2:],
                'crawling_time': Datetime.now(),
                'crawling_time_epoch': int(time()),
                'title': (title := card.css('::text').getall()[-1].strip()),
                'img_urls': (img_urls := [
                    card.css('img::attr(src)').get(),
                    *['https://satudata.pertanian.go.id/assets/docs/infografis/' + img['photo'] for img in requests.get('https://satudata.pertanian.go.id/galeri/photo/' + card.css('.text-center .link-box.rounded:last-child a::attr(data-id)').get()).json()]
                ]),
                'path_data_raw': [
                    f'S3://ai-pipeline-statistics/data/data_raw/data statistic/satu data kementrian pertanian/infografis/json/{title}.json',
                    *list(self.__download_image(img_urls))
                ]
            }

            ConnectionS3.upload(data, data['path_data_raw'][0].replace('S3://ai-pipeline-statistics/', ''))
            
