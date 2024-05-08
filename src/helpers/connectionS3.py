import boto3
import os
import requests
import asyncio

from click import style
from json import dumps
from dotenv import load_dotenv
from typing import Any, final
from requests import Response
from json import loads
from src.helpers.decorators import Decorator

load_dotenv()
s3: Any = boto3.client('s3', aws_access_key_id= os.getenv('S3_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'), endpoint_url=os.getenv('S3_ENDPOINT_URL'))

@final
class ConnectionS3:
    @staticmethod
    @Decorator.logging_path(style('SEND S3', fg='bright_red'))
    def upload(body: dict, key: str, bucket: str = 'ai-pipeline-statistics') -> None:
        response:  Any = s3.put_object(Bucket=bucket, Key=key, Body=dumps(body, indent=4, ensure_ascii=False))
        if(response['ResponseMetadata']['HTTPStatusCode'] != 200): raise Exception('failed send s3')

    @staticmethod
    @Decorator.logging_path(style('SEND S3 FILE', fg='bright_red'))
    def upload_content(file_path: str|bytes, key: str, bucket: str = 'ai-pipeline-statistics') -> None:
        if isinstance(file_path, bytes):
            content = file_path
            response:  Any = s3.put_object(Bucket=bucket, Key=key, Body=content)
            if(response['ResponseMetadata']['HTTPStatusCode'] != 200): raise Exception('failed send s3')
        else:
            with open(file_path, 'rb') as file:
                s3.upload_fileobj(file, bucket, key)

    @staticmethod
    def get_all_prefix(prefix: str, bucket: str = 'ai-pipeline-statistics') -> list:
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        all_prefix: list = response.get('Contents', [])
        return [prefix['Key'] for prefix in all_prefix]

        while(response.get('NextContinuationToken')):
            response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, ContinuationToken=response['NextContinuationToken'])
            all_prefix.extend(response.get('Contents', []))
        
        return [prefix['Key'] for prefix in all_prefix]
    
    @staticmethod
    @Decorator.logging_path(style('GET S3 FILE', fg='bright_red'))
    def get_content(key: str, bucket: str = 'ai-pipeline-statistics') -> str:
        return loads(s3.get_object(Bucket=bucket, Key = key)['Body'].read())

    @staticmethod
    @Decorator.logging_path(style('SEND S3 CONTENT', fg='bright_red'))
    def upload_content(content: bytes, key: str, bucket: str = 'ai-pipeline-statistics') -> None:
        response:  Any = s3.put_object(Bucket=bucket, Key=key, Body=content)
        if(response['ResponseMetadata']['HTTPStatusCode'] != 200): raise Exception('failed send s3')

if(__name__ == '__main__'):
    # data = ConnectionS3.get_all_prefix('data/data_raw/wikipedia/data teritorial/json/')
    # print(len(data))
    # ConnectionS3.upload({"apakah_berhasil": True, "update": 3}, 'test/initesting.json')
    # response: Response = requests.get('https://avatars.githubusercontent.com/u/1242887?v=4')
    # ConnectionS3.upload_content(response.content, 'test/test.jpg')
    ConnectionS3.upload_content('data/test/2011/hasil_lit_bnn_2011-3.pdf', 'test/test2.jpg')

