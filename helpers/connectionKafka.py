from kafka import KafkaProducer
from json import dumps
from time import sleep

from config import logging

producer = KafkaProducer(bootstrap_servers=[...], value_serializer=lambda x: dumps(x).encode('utf-8'))

class ConnectionKafka:
    @staticmethod
    def send(topic: str, datas: dict) -> None:
        if(not datas): return
        
        if(isinstance(datas, dict)):
            print(len(datas['data']))
            for data in datas['data']:
                logging.info(f'Send to Kafka {data["kabupaten"]["id_ID"]}')
                producer.send(topic=topic, value=data)
                sleep(2) 
            return

        producer.send(topic=topic, value=datas)
        sleep(2)

if(__name__ == '__main__'):
    ConnectionKafka.send()