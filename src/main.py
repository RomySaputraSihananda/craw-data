import click

from click.core import Context
from typing import final

from src.services.dataReview import Lemon8, Quora, Glassdoor, MicrosoftStore, Taptap
from src.services.dataDivtik import Cekbpom
from src.services.dataICC import TravelokaEvent

@final
class Main:
    @staticmethod
    def merge(ctx: Context, **kwargs) -> dict:
        return {**ctx.obj, **kwargs}
    
    @click.group()
    @click.version_option(version='2.0.0', prog_name='Engine Crawler Data', message=f'{click.style("%(prog)s", fg="bright_magenta")} version {click.style("%(version)s", fg="bright_magenta")}')
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

    @main.group()
    @click.pass_context
    def data(ctx: Context):
        """ Data T4 """
        ... 

    @main.group()
    @click.pass_context
    def data_review(ctx: Context):
        """ Data Review """
        ... 

    @main.group()
    @click.pass_context
    def data_divtik(ctx: Context):
        """ Data Divtik """
        ... 

    @main.group()
    @click.pass_context
    def data_icc(ctx: Context):
        """ Data ICC """
        ... 

    @staticmethod
    @data_review.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_user_id', 'by_username', 'by_url', 'by_post_id']))
    @click.option('--user_id', default=None, help='User ID')
    @click.option('--post_id', default=None, help='Post ID')
    @click.option('--username', default=None, help='Username')
    @click.option('--url', default=None, help='Url')
    @click.pass_context
    def lemon8(ctx: Context, **kwargs):
        """ Lemon8 Engine """
        return Lemon8(**Main.merge(ctx, **kwargs))

    @staticmethod
    @data_review.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_question_str']))
    @click.option('--question', default=None, help='Question')
    @click.pass_context
    def quora(ctx: Context, **kwargs):
        """ Quora Engine """
        return Quora(**Main.merge(ctx, **kwargs))


    @staticmethod
    @data_review.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_employer_id', 'by_page', 'all_detail']))
    @click.option('--employer_id', default=None, help='Employer id')
    @click.option('--page', default=None, help='Number page')
    @click.pass_context
    def glassdoor(ctx: Context, **kwargs):
        """ Glassdoor Engine """
        return Glassdoor(**Main.merge(ctx, **kwargs))
    
    @staticmethod
    @data_review.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_product_id', 'by_media_type', 'all_media']))
    @click.option('--product_id', default=None, help='Product id')
    @click.option('--media', default=None, help='Media type')
    @click.pass_context
    def microsoftStore(ctx: Context, **kwargs):
        """ MicrosoftStore Engine """
        return MicrosoftStore(**Main.merge(ctx, **kwargs))
    
    @staticmethod
    @data_review.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_app_id', 'by_platform', 'all_platform']))
    @click.option('--app_id', default=None, help='App id')
    @click.option('--platform', default=None, help='platform type')
    @click.pass_context
    def taptap(ctx: Context, **kwargs):
        """ TapTap Engine """
        return Taptap(**Main.merge(ctx, **kwargs))
    
    @staticmethod
    @data_divtik.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_product_id', 'by_page', 'all_detail']))
    @click.option('--product_id', default=None, help='Product id')
    @click.option('--page', default=None, help='Number page')
    @click.option('--start', default=1, help='start page')
    @click.pass_context
    def cekbpom(ctx: Context, **kwargs):
        return Cekbpom(**Main.merge(ctx, **kwargs))
    
    @staticmethod
    @data_icc.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_location', 'all_location']))
    @click.option('--location', default=None, help='Location name')
    @click.option('--start', default=None, help='strtstart location')
    @click.pass_context
    def travelokaEvent(ctx: Context, **kwargs):
        return TravelokaEvent(**Main.merge(ctx, **kwargs))
    

if(__name__ == "__main__"):
    Main.main()