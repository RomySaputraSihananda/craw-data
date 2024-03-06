from typing import final

from src.helpers import ConnectionKafka

@final
class KafkaConsumer:
    def __init__(self, **kwargs) -> None:
        self.__connection: ConnectionKafka = ConnectionKafka(kwargs.get('topic'), kwargs.get('broker'), 'consumer')

        self.consume()

    @final
    def consume(self) -> None:
        self.__connection.consume()

if(__name__ == '__main__'):
    KafkaConsumer(**{
        'topic': 'data-knowledge-repo-general_10',
        'broker': 'kafka01.research.ai,kafka02.research.ai,kafka03.research.ai'  
    })
