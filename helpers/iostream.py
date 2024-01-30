import re
import json

from json import dumps, loads
from typing import final

from helpers.decorators import Decorator

@final 
class Iostream:
    @staticmethod
    @Decorator.logging_path()
    @Decorator.check_path
    def write_json(data: dict, file_path: str) -> None:
        with open(file_path, 'w') as file:
            file.write(dumps(data, indent=4, ensure_ascii=False))
    
    @staticmethod
    def update_log(data: dict, file_name="Monitoring_data.json", **kwargs):
        try:
            with open(f'logging/{kwargs.get("name").split(".")[-1] if kwargs.get("name") else "test"}/{file_name}', "r") as file:
                logs = json.load(file)
        except Exception:
            logs = []

        updated_logs = [
            {**e, **data} if e["id_sub_source"] == data["id_sub_source"] and not e.get("id_data") else e for e in logs
        ]

        Iostream.write_json(updated_logs, f'logging/{kwargs.get("name").split(".")[-1] if kwargs.get("name") else "test"}/{file_name}')

    @staticmethod
    def write_log(data: dict, file_name="Monitoring_data.json", **kwargs):
        try:
            with open(f'logging/{kwargs.get("name").split(".")[-1] if kwargs.get("name") else "test"}/{file_name}', "r") as file:
                logs = json.load(file)
        except Exception:
            logs = []

        logs.append(data)

        Iostream.write_json(logs, f'logging/{kwargs.get("name").split(".")[-1] if kwargs.get("name") else "test"}/{file_name}')

    @staticmethod
    def info_log(log: dict, id_data: str, status: str, process_name: str ='Crawling', error: Exception =None, file_name="Monitoring_log_error.json", **kwargs):
        data: dict = {
            "Crawlling_time": log.get("Crawlling_time"),
            "id_project": log.get("id_project"),
            "project": log.get("project"),
            "sub_project": log.get("sub_project"),
            "source_name": log.get("source_name"),
            "sub_source_name": log.get("sub_source_name"),
            "id_sub_source": log.get("id_sub_source"),
            "id_data": str(id_data),
            "process_name": process_name if process_name else "Crawling",
            "status": status,
            "type_error": error.__class__.__name__ if error else "",
            "message": str(error) if error else "",
            "assign": log.get("assign"),
        }

        Iostream.write_log(data, file_name, **kwargs)
    
    @staticmethod
    def dict_to_deep(data: dict) -> dict:
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    data[key] = Iostream.dict_to_deep(value)
                elif isinstance(value, list):
                    data[key] = [Iostream.dict_to_deep(item) for item in value]
                elif isinstance(value, str):
                    try:
                        data[key] = loads(value)
                    except Exception:
                        data[key] = re.sub('<.*?>', '', value)
        return data

from time import sleep
# testing
if(__name__ == '__main__'):
    # Iostream.write_file('o.json', {"memek":"dshfh"})
    log = {
            "Crawlling_time": 'kdjs',
            "id_project": None,
            "project": "Data Intelligence",
            "sub_project": "data review",
            "source_name": 'domain',
            "sub_source_name": "user_unique_name",
            "id_sub_source": "item_id",
            "total_data": 'comments',
            "total_success": 0,
            "total_failed": 0,
            "status": "Process",
            "assign": "romy",
        }
    Iostream.write_log(log)
    for i in range(10):
        Iostream.update_log({
            "Crawlling_time": 'kdjs',
            "id_project": None,
            "project": "Data Intelligence",
            "sub_project": "data review",
            "source_name": 'domain',
            "sub_source_name": "user_unique_name",
            "id_sub_source": "item_id",
            "total_data": 'comments',
            "total_success": i if bool(i % 2) else 0, 
            "total_failed": 0,
            "status": "Process",
            "assign": "romy",
        })
        sleep(0.5)
    Iostream.update_log({
            "Crawlling_time": 'kdjs',
            "id_project": None,
            "project": "Data Intelligence",
            "sub_project": "data review",
            "source_name": 'domain',
            "sub_source_name": "user_unique_name",
            "id_sub_source": "item_id",
            "total_data": 'comments',
            "total_success": i if bool(i % 2) else 0, 
            "total_failed": 0,
            "status": "Done",
            "assign": "romy",
        })