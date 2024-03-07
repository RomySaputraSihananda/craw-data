from src.main import EngineCrawler

from src.services.dataICC import DataICC
from src.services.dataDivtik import DataDivtik
from src.services.dataReview import DataReview
from src.services.dataTeritorial import DataTeritorial
from src.services.other import Other

from __version__ import __title__, __author_email__, __autor__, __description__, __license__, __url__, __version__

def main():
    cli: EngineCrawler = EngineCrawler()

    cli.main.add_command(DataICC.main, name='data_icc')
    cli.main.add_command(DataDivtik.main, name='data_divtik')
    cli.main.add_command(DataReview.main, name='data_review')
    cli.main.add_command(DataTeritorial.main, name='data_teritorial')
    cli.main.add_command(Other.main, name='other')
    
    cli.main()

if(__name__ == '__main__'):
    main()