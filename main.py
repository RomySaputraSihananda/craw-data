import click

from click.core import Context
from typing import final

from services import Lemon8, Quora, Glassdoor, MicrosoftStore, Taptap
from services.dataDivtik import Cekbpom

@final
class Main:
    @staticmethod
    def merge(ctx: Context, **kwargs) -> dict:
        return {**ctx.obj, **kwargs}
    
    @click.group()
    @click.version_option(version='2.0.0', prog_name='Engine Crawler Data', message=f'{click.style("%(prog)s", fg="bright_magenta")} version {click.style("%(version)s", fg="bright_magenta")}')
    @click.pass_context
    @click.pass_context
    def main(ctx: Context, **kwargs) -> None:
        """ Engine Crawler Data """
        ctx.obj = kwargs

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
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_product_id', 'by_media_type', 'all_media']))
    @click.option('--product_id', default=None, help='Product id')
    @click.option('--media', default=None, help='Media type')
    @click.pass_context
    def taptap(ctx: Context, **kwargs):
        """ TapTap Engine """
        return Taptap(**Main.merge(ctx, **kwargs))
    
    @staticmethod
    @data_divtik.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_product_id', 'by_media_type', 'all_media']))
    @click.option('--product_id', default=None, help='Product id')
    @click.option('--media', default=None, help='Media type')
    @click.pass_context
    def Cekbpom(ctx: Context, **kwargs):
        return Cekbpom(**Main.merge(ctx, **kwargs))
    

if(__name__ == "__main__"):
    Main.main()
