from json import loads

with open('/home/romy/Destop/data-sensor/data-review/endpoints/traveloka/geoid.json') as file:
    datas = loads(file.read())['geoFilters']



datas = [
            {
                'id': data['geoId'],
                'name': data['geoName'],
                'child': [
                    {
                        'id': i['geoId'],
                        'name': i['geoName'],
                        'child': [
                            {
                                'id': j['geoId'],
                                'name': j['geoName'],
                                'child': []
                            } for j in i['childGeoFilters']
                        ]
                    } for i in data['childGeoFilters']
                ]
            } for data in datas 
        ]

for data in datas:
    print(f'{data["name"].upper().replace(" ", "_")} = \"{data["id"]}\"')
    for i in data['child']:
        print(f'{i["name"].upper().replace(" ", "_")} = \"{i["id"]}\"')
        for j in i['child']:
            print(f'{j["name"].upper().replace(" ", "_")} = \"{j["id"]}\"')
