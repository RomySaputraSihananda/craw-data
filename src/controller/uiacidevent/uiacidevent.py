from http import HTTPStatus
from datetime import datetime
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from src.helpers import BodyResponse
from src.library.dataDivtik import AbstractUiacidEvent

class UiacidEventController(AbstractUiacidEvent): 
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.router: APIRouter = APIRouter() 
        self.router.get('/getEvent')(self.get_event_by_date)

    async def get_event_by_date(
            self, 
            month: int = Query(default=(datetime_now := datetime.now()).month, description='month of event', ge=1, le=12), 
            year: int = Query(default=datetime_now.year, description='year of event'),
    ) -> JSONResponse:
        events= await super()._get_event_by_date(year, month)
        if(not events): return JSONResponse(
            content=BodyResponse(
                HTTPStatus.NOT_FOUND, 
                None, 
                message=f'there are no events in {year}-{month}',
            ).__dict__, 
            status_code=HTTPStatus.NOT_FOUND
        )

        return JSONResponse(
            content=BodyResponse(
                HTTPStatus.OK, 
                events, 
                message=f'list of events in {year}-{month}', 
            ).__dict__, 
            status_code=HTTPStatus.OK
        )