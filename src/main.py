import click

from click.core import Context
from typing import Any, MutableMapping, Sequence, final

from src.services.dataReview import Lemon8, Quora, Glassdoor, MicrosoftStore, Taptap
from src.services.dataDivtik import Cekbpom
from src.services.dataICC import TravelokaEvent

from src.services.dataDivtik import DataDivtik
from src.interfaces import BaseGroupClick

@final
class EngineCrawler(BaseGroupClick):
    @click.group()
    @click.version_option(version='3.1.6', prog_name='Engine Crawler Data', message=f'{click.style("%(prog)s", fg="bright_magenta")} version {click.style("%(version)s", fg="bright_magenta")}')
    @click.option('--s3', is_flag=True, default=False, help='send s3')
    @click.option('--kafka', is_flag=True, default=False, help='send kafka')
    @click.option('--bootstrap', default=None, help='bootstrap kafka')
    @click.option('--topic', default=None, help='topic kafka')
    @click.option('--clean', is_flag=True, default=False, help='data clean')
    @click.pass_context
    def main(ctx: Context, **kwargs) -> None:
        """ Engine Crawler Data """
        if(kwargs.get('kafka') and (not kwargs.get('bootstrap') or not kwargs.get('topic'))):
            raise click.BadParameter('--bootstrap and --topic is required')
        ctx.obj = kwargs 

from src.services.dataICC import DataICC
if(__name__ == "__main__"):
    cli: EngineCrawler = EngineCrawler()

    cli.main.add_command(DataICC.main, name='data_icc')
    cli.main()