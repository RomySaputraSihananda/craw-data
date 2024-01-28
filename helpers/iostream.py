import os
import json

from json import dumps
from functools import wraps

from config.logging import logging

class Iostream:
    
    @staticmethod
    def check_path(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(args[-1])
            directory: str = os.path.dirname(args[0])

            if not os.path.isdir(directory) and bool(directory):
                os.makedirs(directory)
            
            return func(*args, **kwargs)
        
        return wrapper

    @staticmethod
    @check_path
    def write_json(data: dict, file_path: str) -> None:
        with open(file_path, 'w') as file:
            file.write(dumps(data, indent=4, ensure_ascii=False))

        logging.info(file_path)
    
    @staticmethod
    def update_log(data, file_name="Monitoring_data.json"):
        try:
            with open(file_name, "r") as file:
                logs = json.load(file)
        except FileNotFoundError:
            logs = []

        updated_logs = [
            {**e, **data} if e["id_sub_source"] == data["id_sub_source"] and not e.get("id_data") else e for e in logs
        ]

        with open(file_name, "w") as file:
            json.dump(updated_logs, file, indent=2)

    @staticmethod
    @check_path
    def write_log(data, file_name="Monitoring_data.json"):
        try:
            with open(file_name, "r") as file:
                logs = json.load(file)
        except Exception:
            logs = []

        logs.append(data)

        with open(file_name, "w") as file:
            json.dump(logs, file, indent=2)
    
    @staticmethod
    def info_log(log, id_data, status, process_name='Crawling', error=None, file_name="Monitoring_log_error.json", **kwargs):
        data = {
            "Crawlling_time": log.get("Crawlling_time"),
            "id_project": log.get("id_project"),
            "project": log.get("project"),
            "sub_project": log.get("sub_project"),
            "source_name": log.get("source_name"),
            "sub_source_name": log.get("sub_source_name"),
            "id_sub_source": log.get("id_sub_source"),
            "id_data": id_data,
            "process_name": process_name if process_name else "Crawling",
            "status": status,
            "type_error": error.__class__.__name__ if error else "",
            "message": str(error) if error else "",
            "assign": log.get("assign"),
        }

        Iostream.write_log(data, f'logging/{kwargs.get("name").split(".")[-1]}/{file_name}')

from time import sleep
# testing
if(__name__ == '__main__'):
    # Iostream.write_file('o.json', {"memek":"dshfh"})
    log = {
        "Crawlling_time": "2024-01-30",
        "id_sub_source": 123,
        "project": "Project A",
        "sub_project": "Sub Project A",
        "source_name": "Source 1",
        "sub_source_name": "Sub Source 1",
        "assign": "User A",
        'total': 0
    }
    Iostream.write_log(log)
    for i in range(100):
        Iostream.update_log({
            "Crawlling_time": "2024-01-30",
            "id_sub_source": 123,
            "project": "Project A",
            "sub_project": "Sub Project A",
            "source_name": "Source 1",
            "sub_source_name": "Sub Source 1",
            "assign": "User A",
            'total': i * 100
        })
        sleep(1)