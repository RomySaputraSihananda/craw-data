import requests

from requests import Response

class CheckProxy:
    def __init__(self) -> None:
        self.request_ip()
        self.request_ip({
            'http':  'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        })
    
    @staticmethod
    def request_ip(proxies: dict = None) -> None:
        try:
            response: Response = requests.get('http://httpbin.org/ip', proxies=proxies)
            print(f'{"with proxies" if proxies else "without proxies"}\t:: {response} :: {response.json()}')
        except Exception as error:
            print(f'with proxies"\t:: <Error    [999]> :: {error.__class__.__name__}')
            