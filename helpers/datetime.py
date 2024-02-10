import pytz
import re

from datetime import datetime
from typing import final

@final
class Datetime:
    def execute(text: str) -> str:
        try:
            return datetime.strptime(text, "%Y%m%d%H%M%S%f").strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            raise e
        
    def utc(text: str) -> str:
        if(re.search('\.(\d{7})Z$', text)):
            return datetime.strptime(text[:-2], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
    
    def utc_epoch(text: str) -> int:
        if(match := re.search('\.\d{7}Z$', text)):
            return int(datetime.strptime(text.replace(match.group(0), ''), "%Y-%m-%dT%H:%M:%S").timestamp())
        return int(datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").timestamp())

    def now() -> str:
        tz = pytz.timezone("Asia/Jakarta")
        date = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return date
    
if(__name__ == '__main__'):
    print(Datetime.utc_epoch('2016-01-21T22:09:15.1484054Z'))