import pytz
import re

from datetime import datetime
from typing import final

@final
class Datetime:
    def execute(text: str | int) -> str:
        try:
            return datetime.strptime(text, "%Y%m%d%H%M%S%f").strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            try:
                return datetime.fromtimestamp(text).strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                raise e
    def excel_serial_date(text: str, format: str = "%Y-%m-%d") -> str:
        delta: datetime = datetime.strptime(text, format) - datetime(1899, 12, 30)
        excel_serial_date = delta.days + delta.seconds / (24 * 60 * 60)  
        return str(int(excel_serial_date))
        
    def excel_serial_date_now(format: str = "%Y-%m-%d") -> tuple:
        tz = pytz.timezone("Asia/Jakarta")
        return (Datetime.excel_serial_date(date := datetime.now(tz).strftime(format)), date)

    def utc(text: str) -> str:
        if(re.search('\.\d+Z$', text)):
            return datetime.strptime(text[:-2], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
    
    def utc_epoch(text: str) -> int:
        if(match := re.search('\.\d+Z$', text)):
            return int(datetime.strptime(text.replace(match.group(0), ''), "%Y-%m-%dT%H:%M:%S").timestamp())
        return int(datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").timestamp())

    def now() -> str:
        tz = pytz.timezone("Asia/Jakarta")
        date = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return date
    
if(__name__ == '__main__'):
    print(Datetime.utc('2012-08-16T00:03:43.2882034Z'))