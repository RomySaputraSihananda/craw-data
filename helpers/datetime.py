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
            if(re.search('\.(\d{7})Z$', text)):
                return datetime.strptime(text[:-2], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
            return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")

    def now() -> str:
        tz = pytz.timezone("Asia/Jakarta")
        date = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return date
    
if(__name__ == '__main__'):
    print(Datetime.execute('2021-11-02T16:00:00Z'))