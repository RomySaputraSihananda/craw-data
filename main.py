import click

from typing import final

from services import Lemon8, Quora, Glassdoor, MicrosoftStore 

@final
class Main:
    @click.group()
    def main(**kwargs) -> None:
        """ Main Engine """
        pass

    @staticmethod
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_user_id', 'by_username', 'by_url', 'by_post_id']))
    @click.option('--user_id', default=None, help='User ID')
    @click.option('--post_id', default=None, help='Post ID')
    @click.option('--username', default=None, help='Username')
    @click.option('--url', default=None, help='Url')
    @click.option('--s3', default=False, help='Send to S3 ?')
    @click.option('--clean', default=False, help='Send to clean path')
    def lemon8(**kwargs):
        """ Lemon8 Engine """
        return Lemon8(**kwargs)

    @staticmethod
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_question_str']))
    @click.option('--s3', default=False, help='Send to S3 ?')
    @click.option('--clean', default=False, help='Send to clean path')
    @click.option('--question', default=None, help='Question')
    def quora(**kwargs):
        """ Quora Engine """
        return Quora(**kwargs)


    @staticmethod
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_employer_id', 'by_page', 'all_detail']))
    @click.option('--s3', default=False, help='Send to S3 ?')
    @click.option('--clean', default=False, help='Send to clean path')
    @click.option('--employer_id', default=None, help='Employer id')
    @click.option('--page', default=None, help='Number page')
    def glassdoor(**kwargs):
        """ Glassdoor Engine """
        return Glassdoor(**kwargs)
    
    @staticmethod
    @main.command()
    @click.argument('method', metavar='METHOD', type=click.Choice(['by_product_id', 'by_media_type', 'all_media']))
    @click.option('--s3', default=False, help='Send to S3 ?')
    @click.option('--clean', default=False, help='Send to clean path')
    @click.option('--product_id', default=None, help='Product id')
    @click.option('--media', default=None, help='Media type')
    def microsoftStore(**kwargs):
        """ Glassdoor Engine """
        return MicrosoftStore(**kwargs)

if(__name__ == "__main__"):
    Main.main()
