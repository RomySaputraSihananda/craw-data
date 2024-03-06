import click

from click import Context

from src.interfaces import BaseGroupClick
from .kafkaConsumer import KafkaConsumer

class Other(BaseGroupClick):
    @click.group()
    def main() -> None:
        """ Other Function """
        ...

    @main.command()
    @click.option('--broker', required=True, help='broker name of kafka', type=str)
    @click.option('--topic', required=True, help='topic name of kafka', type=str)
    def kafkaconsumer(**kwargs) -> None:
        """ Kafka Consumer """
        return KafkaConsumer(**kwargs)