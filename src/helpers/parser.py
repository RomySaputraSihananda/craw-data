from bs4 import BeautifulSoup, SoupStrainer
from bs4.builder import TreeBuilder
from bs4.element import PageElement as PageElement, ResultSet, Tag
import requests

from typing import Callable, Any, final

class Array:
    def __init__(self, list: list) -> None:
        self.__list: list = list

    def map(self, function: Callable[..., Any]) -> list:
        return list(map(function, self.__list))
    def to_list(self):
        return self.__list


# def getSoup(url, method = 'get', **kwargs):
#     res = requests.request(method, url, **kwargs)
#     if res.status_code != 200:
#         print('response not success')
#         return None
#     return BeautifulSoup(res.content, 'html.parser')

class Parser(BeautifulSoup):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, 'html.parser', **kwargs)
    
    def select(self, *args) -> Array:
        return Array(super().select(*args))
    
    def select_one(self, *args, index: int = 0) -> PageElement:
        return self.select(*args).map(lambda e: e)[index]
    
if(__name__ == '__main__'):
    # soup = getSoup(
    #     'https://cekbpom.pom.go.id/get_detail_produk_obat',
    #     'post',
    #     headers = {
    #         'Cookie': 'webreg=f3rs64qmrr4k7lln0cud4virv480jdca',
    #         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    #         'X-Requested-With': 'XMLHttpRequest',
    #     },
    #     data={
    #         'product_id': 'ERBA324762202400002',
    #         'aplication_id': '02'
    #     }, verify=False)
    
    # print(soup.select('#id_produk').map())
    with open('test.html', 'r') as file:
            data = file.read()

        
    soup: Parser = Parser(data)

    soup.select()