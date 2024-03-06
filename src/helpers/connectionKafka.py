from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
from click import style

from src.helpers import Decorator 
from src.config import logging

class ConnectionKafka:
    def __init__(self, topic: str, bootstrap_servers: str | list = None, type: str = 'producer') -> None:
        self.__bootstrap_servers: str | list = bootstrap_servers.split(',')
        self.__topic = topic

        if(type == 'producer'):
            self.__producer: KafkaProducer = KafkaProducer(bootstrap_servers=self.__bootstrap_servers, value_serializer=lambda x: dumps(x).encode('utf-8'))
        else:
            self.__consumer: KafkaConsumer = KafkaConsumer(self.__topic, bootstrap_servers=self.__bootstrap_servers)

    @Decorator.logging_path(style('PRODUCE KAFKA', fg='bright_cyan'))
    def send(self, data: dict, **kwargs) -> None:
        if(not data): return
        try:
            return self.__producer.send(topic=self.__topic, value=data)
        except Exception as e:
            return logging.error(f'failed send to kafka {self.__bootstrap_servers}')
    
    def consume(self, **kwargs):
        for message in self.__consumer:
            data: list = loads(message.value.decode('utf-8'))
            logging.info(f'{style("[ CONSUME KAFKA ]", fg="bright_cyan")} [ {style(data["domain"], fg="bright_green")} ] {style(list(data.keys()), fg="bright_magenta")}')

if(__name__ == '__main__'):
    # ConnectionKafka('kafka01.production02.bt:9092')
    ConnectionKafka('sc-raw-gosip-daily-006', 'kafka01.production02.bt:9092', 'consumer').consume()