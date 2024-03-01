from src.main import EngineCrawler

from src.services.dataICC import DataICC
from src.services.dataDivtik import DataDivtik
from src.services.dataReview import DataReview
from src.services.dataTeritorial import DataTeritorial

import click
from src.helpers import ConnectionS3, ConnectionKafka
@click.command()
def s32k():
    for prefix in ConnectionS3.get_all_prefix('data/data_raw/bpom/product/'):
        conn = ConnectionKafka(['kafka01.research.ai', 'kafka02.research.ai', 'kafka02.research.ai'])
        conn.send('data-knowledge-repo-general_10', ConnectionS3.get_content(prefix))

def main():
    cli: EngineCrawler = EngineCrawler()

    cli.main.add_command(DataICC.main, name='data_icc')
    cli.main.add_command(DataDivtik.main, name='data_divtik')
    cli.main.add_command(DataReview.main, name='data_review')
    cli.main.add_command(DataTeritorial.main, name='data_teritorial')
    cli.main.add_command(s32k, name='s32k')
    cli.main()

if(__name__ == '__main__'):
    main()