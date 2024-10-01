import json

from typing import List, Any, Optional, Union, Dict
from dataclasses import dataclass, asdict
from time import time
from pytz import timezone
from datetime import datetime

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
    path_data_raw: Optional[Union[str, List[str]]] = None
    crawling_time: Optional[str] = datetime\
        .now(
            timezone("Asia/Jakarta")
        )\
        .strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    crawling_time_epoch: Optional[int] = int(time())
    table_name: Optional[str] = None
    country_name: Optional[str] = 'Indonesia'
    level: Optional[str] = "nasional"
    stage: Optional[str] = "Crawling data"
    update_schedule: Optional[str] = None

    @property
    def dict(
        self: 'Metadata'
    ) -> Dict[str, Any]:
        return asdict(
            self
        )
    
    @property
    def json(
        self: 'Metadata'
    ) -> Dict[str, Any]:    
        return json\
            .dumps(
                self.dict
            )