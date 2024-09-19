from typing import List, Any, Optional
from dataclasses import dataclass
from time import time
from src.helpers import Datetime

@dataclass
class Metadata:
    link: Optional[str] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    title: Optional[str] = None
    sub_title: Optional[str] = None
    range_data: Optional[str] = None
    create_date: Optional[str] = None
    update_date: Optional[str] = None
    data: Optional[Any] = None
    desc: Optional[str] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    path_data_raw: Optional[List[str]] = None
    crawling_time: Optional[str] = Datetime.now()
    crawling_time_epoch: Optional[int] = int(time())
    table_name: Optional[str] = None
    country_name: Optional[str] = 'Indonesia'
    level: Optional[str] = "nasional"
    stage: Optional[str] = "Crawling data"
    update_schedule: Optional[str] = None

if(__name__ == '__main__'):
    print(Metadata().__dict__)