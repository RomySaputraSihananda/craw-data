import boto3
import os
import requests

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

    @staticmethod
    @Decorator.logging_path('SEND S3 FILE')
    def upload_content_local(file_path: str, key: str, bucket: str = 'ai-pipeline-statistics') -> None:
        with open(file_path, 'rb') as file:
            print(file)
            # s3.upload_fileobj(file, bucket, key)

    @staticmethod
    @Decorator.logging_path('SEND S3 CONTENT')
    def upload_content(content: bytes, key: str, bucket: str = 'ai-pipeline-statistics') -> None:
        response:  Any = s3.put_object(Bucket=bucket, Key=key, Body=content)
        if(response['ResponseMetadata']['HTTPStatusCode'] != 200): raise Exception('failed send s3')


if(__name__ == '__main__'):
    # ConnectionS3.upload({"apakah_berhasil": True, "update": 3}, 'test/initesting.json')
    # response: Response = requests.get('https://avatars.githubusercontent.com/u/1242887?v=4')
    # ConnectionS3.upload_content(response.content, 'test/test.jpg')
    ConnectionS3.upload_content('./test.jpg', 'test/test2.jpg')

