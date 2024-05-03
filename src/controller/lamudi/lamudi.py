import re

from http import HTTPStatus
from fastapi import APIRouter, Response, Query, Depends, Path
from fastapi.responses import JSONResponse
from typing import List, Annotated

from src.library.api.lamudi import BaseLamudi
from src.library.api.lamudi.categoryEnum import PenawaranEnum, FrekuensiSewaEnum, PropertyEnum
from src.helpers import BodyResponse

class LamudiController(BaseLamudi):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.router: APIRouter = APIRouter() 
        self.router.get('/location')(self.get_location)
        self.router.get('/property')(self.get_property)
    
    async def get_location(
            self, 
            keyword: str = Query(default='Malang', description='keyword of location'), 
            level: int = Query(default=2, description='level of result location slug'),
            page: int = Query(default=1, description='nomor page'),
            size: int = Query(default=10, description='size of page'),
    ) -> JSONResponse:
        """
            Get list of location slug:

            - **keyword**: keywords from the location to be searched
            - **level**: level of result location slug
                - **level 1**: "/east-java" 
                - **level 2**: "/east-java/malang" 
                - **level 3**: "/east-java/malang/kepanjen"
            - **page**: number of page
            - **size**: size of page
        """
            
        if(not keyword): return JSONResponse(content=BodyResponse(HTTPStatus.BAD_REQUEST, None, message='keyword cannot be empty').__dict__, status_code=HTTPStatus.BAD_REQUEST)
        
        return JSONResponse(content=BodyResponse(HTTPStatus.OK, await super()._get_location(keyword, level=level, page=page, size=size), message=f'list location with keyword {keyword}', page=page, size=size).__dict__, status_code=HTTPStatus.OK)
    
    async def get_property(
        self, 
        location_keyword: str = Query(example='Malang', default=None, description='search product by location keyword'),
        location_slug: str = Query(default=None, description='search product by location slug'),
        penawaran_type: str = Query(default='DI_JUAL', enum=[penawaran.name for penawaran in PenawaranEnum], description='type dari penawaran'),
        frekuensi_sewa: str = Query(default=None, enum=[frekuensi.name for frekuensi in FrekuensiSewaEnum], description='type waktu sewa'),
        property_type: str = Query(default=None, enum=[property.name for property in PropertyEnum], description='type property'),
        rentang_harga: str = Query(default=None, description='rentang harga dalam rupiah (Rp) | example: 1000000-5000000 | patern: ^\d+-\d+$'),
        rentang_area: str = Query(default=None, description='rentang area dalam meter persegi (m²) | example: 100-500 | patern: ^\d+-\d+$'),
        kamar_tidur: int = Query(default=None, description='jumlah kamar tidur di setiap property', gt=0, le=5),
        kamar_mandi: int = Query(default=None, description='jumlah kamar mandi di setiap property', gt=0, le=5),
        extra_keyword: str = Query(default=None, description='kata kunci yang relevan'),
        page: int = Query(default=1, description='number of page'),
        size: int = Query(default=10, description='size of page'),
    ) -> JSONResponse:

        valid: function = lambda string: True if re.match(r'^\d+-\d+$', string) else False

        if(penawaran_type not in PenawaranEnum.__members__): 
            return JSONResponse(
                content=BodyResponse(
                    HTTPStatus.BAD_REQUEST, 
                    None, 
                    message=f'invalid value of penawaran_type'
                ).__dict__, 
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        if(PenawaranEnum[penawaran_type] == PenawaranEnum.DI_JUAL and frekuensi_sewa): 
            return JSONResponse(
                content=BodyResponse(
                    HTTPStatus.BAD_REQUEST, 
                    None, 
                    message=f'invalid value of frekuensi_sewa, cannot use frekuensi_sewa if using penawaran.DI_JUAL'
                ).__dict__, 
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        if(frekuensi_sewa and frekuensi_sewa not in FrekuensiSewaEnum.__members__): 
            return JSONResponse(
                content=BodyResponse(
                    HTTPStatus.BAD_REQUEST, 
                    None, 
                    message=f'invalid value of frekuensi_sewa'
                ).__dict__, 
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        if(property_type and property_type not in PropertyEnum.__members__): 
            return JSONResponse(
                content=BodyResponse(
                    HTTPStatus.BAD_REQUEST, 
                    None, 
                    message=f'invalid value of property_type'
                ).__dict__, 
                status_code=HTTPStatus.BAD_REQUEST
        )


        if(rentang_harga and not valid(rentang_harga)): 
            return JSONResponse(
                content=BodyResponse(
                    HTTPStatus.BAD_REQUEST, 
                    None, 
                    message=f'invalid format of kisaran_harga'
                ).__dict__, 
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        if(rentang_area and not valid(rentang_area)): 
            return JSONResponse(
                content=BodyResponse(
                    HTTPStatus.BAD_REQUEST, 
                    None, 
                    message=f'invalid format of rentang_area'
                ).__dict__, 
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        if(property_type and
            (PropertyEnum[property_type].name.lower().startswith('komersial') or PropertyEnum[property_type].name.lower().startswith('tanah'))
            and
            (kamar_mandi or kamar_tidur)):
            return JSONResponse(
                content=BodyResponse(
                    HTTPStatus.BAD_REQUEST, 
                    None, 
                    message=f'invalid kamar_mandi or kamar_tidur on property komersial or tanah'
                ).__dict__, 
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        return JSONResponse(
            content=BodyResponse(
                HTTPStatus.OK, 
                await super()._get_property(
                    location_keyword=location_keyword,
                    location_slug=location_slug,
                    penawaran=PenawaranEnum[penawaran_type],
                    frekuensi=FrekuensiSewaEnum[frekuensi_sewa] if frekuensi_sewa else None,
                    property=PropertyEnum[property_type] if property_type else None,
                    rentang_harga=rentang_harga,
                    rentang_area=rentang_area,
                    kamar_mandi=kamar_mandi,
                    kamar_tidur=kamar_tidur,
                    extra_keyword=extra_keyword,
                    page=page, 
                    size=size
                ),
                message=f'result data'
            ).__dict__, 
            status_code=HTTPStatus.OK
        )
