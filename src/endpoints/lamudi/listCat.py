location = []

type_property = [
    'apartment',    
    'apartment/apartments',    
    'apartment/studio',    
    'apartment/condominium',
    'house',
    'house/single-family-house',
    'house/townhouse',
    'house/boarding-house',
    'house/subsidized-house',
    'house/villa',
    'commercial-1',
    'commercial-1/shophouse',
    'commercial-1/offices',
    'commercial-1/retail',
    'commercial-1/industrialwarehouse',
    'commercial-1/hotelleisure',
    'land',
    'land/lotland',
    'kos',
    'kos/putra',
    'kos/putri',
    'kos/campur',
]

# query sewa

{
    "term":{
        "rentFrequency":"yearly"
    }
}
