from http import HTTPStatus
from datetime import datetime
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from time import time

from src.helpers import BodyResponse, Datetime
from src.library.dataDivtik import AbstractJiexpocomEvent, FilterEnum

class JiexpocomEventController(AbstractJiexpocomEvent): 
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.router: APIRouter = APIRouter() 
        self.router.get('/getEvent')(self.get_event_by_date)

    async def get_event_by_date(
            self, 
            month: int = Query(default=(datetime_now := datetime.now()).month, description='month of event', ge=1, le=12), 
            year: int = Query(default=datetime_now.year, description='year of event'),
            filter: str = Query(default=None, enum=[filter.name for filter in FilterEnum], description='filter event'),
    ) -> JSONResponse:
        (events, response) = await super()._get_event_by_date(month, year, filter)
        if(not events): return JSONResponse(
            content=BodyResponse(
                HTTPStatus.NOT_FOUND, 
                None, 
                message=f'there are no events in {response["cal_month_title"]}',
                **response
            ).__dict__, 
            status_code=HTTPStatus.NOT_FOUND
        )
        
        headers: dict = {
            "source": (link := "https://exhibition.jiexpo.com/event-directory"),
            "domain": (link_split := link.split('/'))[2],
            "data_name": "data_event",
            "tag": [*link_split[2:], 'data_event'],
            "crawling_time": Datetime.now(),
            "crawling_time_epoch": int(time())
        } 

        return JSONResponse(
            content=BodyResponse(
                HTTPStatus.OK, 
                [
                    {
                        "link_source": (url := event["link"]),
                        "event_name": event["name"],
                        "event_organizer": event["Organizer"],
                        "category": 'event',
                        "start_date": (start_date_split := event["startDate"].split('T'))[0],
                        "end_date": (end_date_split := event["endDate"].split('T'))[0],
                        "start_time": '.'.join(start_date_split[1].split('-')[1:][:2]),
                        "end_time": '.'.join(end_date_split[1].split('-')[1:][:2]),
                        "event_tag": [*headers['tag'], *url.split('/')[:-1][2:]],
                        "event_description": event["description"],
                        "social_media": None,
                        "link_image": event["ImageObject"]["url"]
                    }  for event in events
                ], 
                message=f'list of events in {response["cal_month_title"]}', 
                **response,
                **headers
            ).__dict__, 
            status_code=HTTPStatus.OK
        )