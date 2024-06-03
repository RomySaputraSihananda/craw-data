from src.helpers import Parser
import requests
from json import dumps
def filter(e):
    try:
        [bahasa_konjo, bahasa_indonesia] = e.get_text().split('\xa0', 1)
        return {
            'bahasa_konjo': bahasa_konjo.strip(),
            'bahasa_indonesia': bahasa_indonesia.replace('\xa0', '').replace('See main entry:', '').strip()
        }
    except: ...

def start():
    all_data = []
    for i in range(2, 30):
        res = requests.get(url := f'https://media.ipsapps.org/kjc/oda/lexicon/{"" if i > 9 else "0"}{i}.htm')
        if(res.status_code != 200): break
        soup: Parser = Parser(res.text)
        all_data.extend([data for data in soup.select('p').map(filter) if data])
    return all_data

start()