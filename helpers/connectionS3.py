import boto3
import os

from json import dumps
from dotenv import load_dotenv
from typing import Any, final

from helpers.decorators import Decorator

load_dotenv()
s3: Any = boto3.client('s3', aws_access_key_id= os.getenv('S3_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'), endpoint_url=os.getenv('S3_ENDPOINT_URL'))

@final
class ConnectionS3:
    @staticmethod
    @Decorator.logging_path('SEND S3')
    def upload(body: dict, key: str, bucket: str = 'ai-pipeline-statistics') -> None:
        response:  Any = s3.put_object(Bucket=bucket, Key=key, Body=dumps(body, indent=4, ensure_ascii=False))
        if(response['ResponseMetadata']['HTTPStatusCode'] != 200): raise Exception('failed send s3')

if(__name__ == '__main__'):
    ConnectionS3.upload({"apakah_berhasil": True, "update": 3}, 'test/initesting.json')
