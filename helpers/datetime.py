import pytz
from datetime import datetime
class Datetime:
    def execute(text: str) -> str:
        try:
            return datetime.strptime(text, "%Y%m%d%H%M%S%f").strftime("%Y-%m-%d %H:%M:%S");
        except Exception as e:
            return e;

    def now() -> str:
        tz = pytz.timezone("Asia/Jakarta")
        date = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return date