from src.main import EngineCrawler

from src.services.dataICC import DataICC
from src.services.dataDivtik import DataDivtik
from src.services.dataReview import DataReview

def main():
    cli: EngineCrawler = EngineCrawler()

    cli.main.add_command(DataICC.main, name='data_icc')
    cli.main.add_command(DataDivtik.main, name='data_divtik')
    cli.main.add_command(DataReview.main, name='data_review')
    cli.main()

if(__name__ == '__main__'):
    main()