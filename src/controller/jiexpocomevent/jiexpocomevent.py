from http import HTTPStatus
from datetime import datetime
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from src.helpers import BodyResponse
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

        return JSONResponse(
            content=BodyResponse(
                HTTPStatus.OK, 
                events, 
                message=f'list of events in {response["cal_month_title"]}', 
                **response
            ).__dict__, 
            status_code=HTTPStatus.OK
        )