import click
import uvicorn
import socket

from json import dumps
from click.core import Context
from typing import Any, final

from src.interfaces import BaseGroupClick
from src.helpers import ConnectionS3, ConnectionKafka
from src.controller import app
from .__version__ import __version__, __title__  

@final
class EngineCrawler(BaseGroupClick):
    @click.group()
    @click.version_option(version=__version__, prog_name=__title__, message=f'{click.style("%(prog)s", fg="bright_magenta")} version {click.style("%(version)s", fg="bright_magenta")}')
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
    
    @main.command()
    @click.option('--prefix', required=True, help='prefix of s3', type=str)
    @click.option('--broker', required=True, help='broker name of kafka', type=str)
    @click.option('--topic', required=True, help='topic name of kafka', type=str)
    def s32k(**kwargs):
        """ S3 To Kafka """
        try:
            conn = ConnectionKafka(kwargs.get('topic'), kwargs.get('broker').split(','))
            for prefix in ConnectionS3.get_all_prefix(kwargs.get('prefix')):
                conn.send(dumps(ConnectionS3.get_content(prefix)))
        except Exception as e:
            raise click.BadParameter('--broker is bad value')
    
    @main.command()
    @click.option('--port', help='port of service', default=4444)
    @click.option('--local', is_flag=True, help='serve to local network')
    def serve(**kwargs):
        return uvicorn.run(app, port=kwargs.get('port'), host=socket.gethostbyname(socket.gethostname()))

from src.services.dataICC import DataICC
if(__name__ == "__main__"):
    cli: EngineCrawler = EngineCrawler()

    cli.main.add_command(DataICC.main, name='data_icc')
    cli.main()