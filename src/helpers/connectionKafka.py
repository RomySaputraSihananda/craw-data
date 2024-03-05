from kafka import KafkaProducer
from json import dumps
from time import sleep
from click import style

from src.helpers import Decorator 
from src.config import logging

class ConnectionKafka:
    def __init__(self, bootstrap_servers: str | list = None) -> None:
        self.__bootstrap_servers: str | list = bootstrap_servers.split(',')
        self.__producer: KafkaProducer = KafkaProducer(bootstrap_servers=self.__bootstrap_servers, value_serializer=lambda x: dumps(x).encode('utf-8'))
    
    @Decorator.logging_path(style('SEND KAFKA', fg='bright_cyan'))
    def send(self, topic: str, data: dict, **kwargs) -> None:
        if(not data): return
        try:
            return self.__producer.send(topic=topic, value=data)
        except Exception as e:
            return logging.error(f'failed send to kafka {self.__bootstrap_servers}')
        
if(__name__ == '__main__'):
    ConnectionKafka('kafka01.production02.bt:9092')