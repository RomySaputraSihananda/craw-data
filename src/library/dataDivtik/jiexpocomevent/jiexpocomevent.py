import re
import asyncio
import requests

from functools import reduce
from aiohttp import ClientSession
from json import loads, dumps
from time import time
from calendar import month_name

from src.helpers import torrequests, Parser, Datetime, Iostream

from .filterEnum import FilterEnum

class BaseJiexpocomEvent:
    def __init__(self) -> None:
        ...
    
    async def __get_detail(self, link: str, data: dict):
        async with ClientSession() as session:
            async with session.get(link) as response:
                soup: Parser = Parser(await response.text())
                del data['@type']
                del data['@context']
                def parse(e):
                    key: str = e.pop('@type')
                    return data | { key: e }
                
                return {'link': str(response.url)} | reduce(lambda a, b: dict(a, **b), [
                    parse(e) for e in loads(soup.select_one('script[type="application/ld+json"]').string)['@graph']
                ])

    async def __get_all_detail(self, content: str) -> list:
        def get_other_detail(e, f):
            return {
                e[0].select_one('h3').get_text(): e[0].select_one('p').get_text(),
                e[1].select_one('h3').get_text() + '_format': e[1].select_one('p').get_text(),
                e[2].select_one('h3').get_text(): e[2].select_one('p span').get_text(),
                'link_calendar': {a.get_text(): a['href'] if ('https:' in a['href']) else 'https:' + a['href'] for a in e[3].select('p a')},
            } | {
                    'time': {em['class'][0]: em.get_text() for em in f.select('.desc_trig_outter .evo_start em')} | {'evcal_time': f.select_one('.desc_trig_outter .evcal_time').get_text()},
                    'event_type': f.select_one('em[data-filter="event_type"]').get_text()
                }
        
        soup: Parser = Parser(content)
        links = soup.select('div > a').map(lambda e: e['href'])
        data: list = soup.select('script[type="application/ld+json"]').map(lambda e: loads(re.sub(r',\s*}', '}', e.string)))

        other_details: list = soup.select('.eventon_list_event.evo_eventtop').map(lambda e: get_other_detail(e.select('.evcal_evdata_cell'), e))
        
        return await asyncio.gather(*(self.__get_detail(link, data[i] | other_details[i]) for i, link in enumerate(links)))

    async def _get_event_by_date(self, month: int, year: int, filter: FilterEnum) -> list:
        data = {
            'action': 'the_ajax_hook',
            'direction': 'none',
            'sort_by': 'sort_date',
            'filters[0][filter_type]': 'tax',
            'filters[0][filter_name]': 'event_type',
            'filters[0][filter_val]': '94,71,69,84,70,87,114,',
            'shortcode[hide_past]': 'no',
            'shortcode[show_et_ft_img]': 'no',
            'shortcode[event_order]': 'ASC',
            'shortcode[ft_event_priority]': 'no',
            'shortcode[lang]': 'L1',
            'shortcode[month_incre]': '0',
            'shortcode[only_ft]': 'no',
            'shortcode[hide_ft]': 'no',
            'shortcode[evc_open]': 'no',
            'shortcode[show_limit]': 'no',
            'shortcode[etc_override]': 'no',
            'shortcode[show_limit_redir]': '0',
            'shortcode[tiles]': 'yes',
            'shortcode[tile_height]': '0',
            'shortcode[tile_bg]': '1',
            'shortcode[tile_count]': '3',
            'shortcode[tile_style]': '1',
            'shortcode[members_only]': 'no',
            'shortcode[ux_val]': '0',
            'shortcode[show_limit_ajax]': 'no',
            'shortcode[show_limit_paged]': '1',
            'shortcode[hide_mult_occur]': 'no',
            'shortcode[show_repeats]': 'no',
            'shortcode[hide_end_time]': 'no',
            'evodata[cyear]': str(year),
            'evodata[cmonth]': str(month),
            'evodata[runajax]': '1',
            'evodata[evc_open]': '0',
            'evodata[cal_ver]': '2.6.13',
            'evodata[mapscroll]': 'true',
            'evodata[mapformat]': 'roadmap',
            'evodata[mapzoom]': '18',
            'evodata[mapiconurl]': '',
            'evodata[ev_cnt]': '0',
            'evodata[show_limit]': 'no',
            'evodata[tiles]': 'yes',
            'evodata[sort_by]': 'sort_date',
            'evodata[filters_on]': 'true',
            'evodata[range_start]': '0',
            'evodata[range_end]': '0',
            'evodata[send_unix]': '0',
            'evodata[ux_val]': '0',
            'evodata[accord]': '1',
            'evodata[rtl]': 'no',
            'ajaxtype': 'jumper',
        }
        
        response: dict = requests.post('https://exhibition.jiexpo.com/wp-admin/admin-ajax.php', data=data).json()
        del response['status']
        
        event_list: list = response.pop('eventList')
        events: list = await self.__get_all_detail(response.pop('content'))

        return [event_list[i] | event for i, event in enumerate(events)], response
    
    async def _get_event_by_date_write(self, month, year) -> None:
        events, response = await self._get_event_by_date(month, year)

        for i, event in enumerate(events):
            data: dict = {
                "link": (link := event['link']),
                "domain": (link_split := link.split('/')[:-1])[2],
                "tag": link_split[2:],
                "crawling_time": Datetime.now(),
                "crawling_time_epoch": int(time()),
                **response,
                'data': event,
                "path_data_raw": f'S3://ai-pipeline-raw-data/data/data_descriptive/jiexpocom/data_event/{response["year"]}/{month_name[response["month"]].lower()}/json/{event["event_id"]}.json',
            }
            
            Iostream.write_json(data, data['path_data_raw'].replace('S3://ai-pipeline-raw-data/', ''), indent=4)

if(__name__ == '__main__'): 
    data = asyncio.run(BaseJiexpocomEvent()._get_event_by_date_write(6, 2024))
    print(
        dumps(
            data,
            indent=4
        )
    )