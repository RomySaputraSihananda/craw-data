from http import HTTPStatus
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from src.library.api.dephubgoid import BaseDephubgoid
from src.helpers import BodyResponse

class DephubgoidController(BaseDephubgoid):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.router: APIRouter = APIRouter() 
        self.router.get('/search')(self.search)
    
    async def search(
            self, 
            ship_name: str = Query(default='BAJI MINASA', description='ship name'), 
            tpk: str = Query(default='', description='tpk'), 
            page: int = Query(default=1, description='page number'),
            size: int = Query(default=10, description='size of page'),
    ) -> JSONResponse:
        (data, info) = await super()._search(ship_name=ship_name, tpk=tpk, page=page, size=size)

        if(not data): return JSONResponse(
            content=BodyResponse(
                HTTPStatus.NOT_FOUND, 
                None, 
                message=f'ships with name {ship_name} NOT FOUND'
            ).__dict__, 
            status_code=HTTPStatus.NOT_FOUND
        )
        return JSONResponse(content=BodyResponse(HTTPStatus.OK, data, message=f'list ships with name {ship_name}', page=page, size=size, info=info).__dict__, status_code=HTTPStatus.OK)
