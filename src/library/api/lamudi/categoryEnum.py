from enum import Enum
from fastapi.encoders import jsonable_encoder

class PropertyEnum(Enum):
    APARTEMEN='apartment'    
    APARTEMEN_APARTEMEN='apartment/apartments'
    APARTEMEN_STUDIO='apartment/studio'    
    APARTEMEN_KONDOMINIUM='apartment/condominium'
    RUMAH='house'
    RUMAH_SINGLE='house/single-family-house'
    RUMAH_TOWNHOUSE='house/townhouse'
    RUMAH_KOSAN='house/boarding-house'
    RUMAH_SUBSIDI='house/subsidized-house'
    RUMAH_VILLA='house/villa'
    KOMERSIAL='commercial-1'
    KOMERSIAL_RUKO='commercial-1/shophouse'
    KOMERSIAL_KANTOR='commercial-1/offices'
    KOMERSIAL_USAHA='commercial-1/retail'
    KOMERSIAL_GUDANG='commercial-1/industrialwarehouse'
    KOMERSIAL_HOTEL='commercial-1/hotelleisure'
    TANAH='land'
    TANAH_TANAH='land/lotland'
    KOS='kos'
    KOS_PUTRA='kos/putra'
    KOS_PUTRI='kos/putri'
    KOS_CAMPUR='kos/campur'

class FrekuensiSewaEnum(Enum):
    PER_TAHUN='yearly'
    PER_BULAN='mountly'
    PER_MINGGU='weekly'
    PER_HARI='daily'

class PenawaranEnum(str, Enum):
    DI_JUAL='for-sale'
    DI_SEWAKAN='for-rent'

