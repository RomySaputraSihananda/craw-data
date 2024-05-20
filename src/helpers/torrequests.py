from typing import Any, MutableMapping
from requests.models import Response
from requests.sessions import PreparedRequest
from stem import CircStatus, Signal
from stem.control import Controller
from requests import Session, Response, Request
from time import sleep
from halo import Halo
from random import choice
from requests.utils import resolve_proxies
import sys 
import time
from datetime import timedelta
from requests.hooks import dispatch_hook
from requests.cookies import extract_cookies_to_jar

if sys.platform == "win32":
    preferred_clock = time.perf_counter
else:
    preferred_clock = time.time

class TorSession(Session):
    def __init__(
            self, 
            proxies: dict = {
                'http':  'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050',
            },
            port: int = 9051,
            password: str = 'romys') -> None:
        self.__proxies: dict = proxies
        self.__controller: Controller = Controller.from_port(port=port) 
        self.__controller.authenticate(password=password)

        super().__init__()
 
    def send(self, request: PreparedRequest, *, stream: bool | None = ..., verify: bool | str | None = ..., proxies: MutableMapping[str, str] | None = ..., cert: str | tuple[str, str] | None = ..., timeout: float | tuple[float, float] | tuple[float, None] | None = ..., allow_redirects: bool = ..., **kwargs: Any) -> Response:
        kwargs.setdefault("stream", self.stream)
        kwargs.setdefault("verify", self.verify)
        kwargs.setdefault("cert", self.cert)
        kwargs.setdefault("proxies", self.__proxies)

        if isinstance(request, Request):
            raise ValueError("You can only send PreparedRequests.")

        allow_redirects = kwargs.pop("allow_redirects", True)
        stream = kwargs.get("stream")
        hooks = request.hooks

        start = preferred_clock()

        with Halo(f'request to <{request.method} [{request.url}]>', spinner=choice(['dots', 'dots8', 'dots9', 'line'])) as halo:
            with Session() as session:
                r = session.get_adapter(url=request.url).send(request, **kwargs)
            
            halo.succeed(f'request success {r}')
            
        elapsed = preferred_clock() - start
        r.elapsed = timedelta(seconds=elapsed)

        r = dispatch_hook("response", hooks, r, **kwargs)

        if r.history:

            for resp in r.history:
                extract_cookies_to_jar(self.cookies, resp.request, resp.raw)

        extract_cookies_to_jar(self.cookies, request, r.raw)

        if allow_redirects:
            gen = self.resolve_redirects(r, request, **kwargs)
            history = [resp for resp in gen]
        else:
            history = []

        if history:
            history.insert(0, r)
            r = history.pop()
            r.history = history

        if not allow_redirects:
            try:
                r._next = next(
                    self.resolve_redirects(r, request, yield_requests=True, **kwargs)
                )
            except StopIteration:
                pass

        if not stream:
            r.content
        
        self.__change_ip()

        return r
    
    def __change_ip(self):
        self.__controller.signal(Signal.NEWNYM)
        with Halo(spinner=choice(['dots', 'dots8', 'dots9', 'line'])) as halo:
            for i in range(round(self.__controller.get_newnym_wait()), 0, -1):
                halo.text = f'waiting change ip {i:>2d} s'
                sleep(1)
            halo.succeed('ip change complete!')

    def close(self) -> None:
        self.__controller.close()
        return super().close()

def request(method, url, **kwargs):
    with TorSession(
            proxies=kwargs.pop('proxies', {
                'http':  'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050',
            }), 
            port=kwargs.pop('port', 9051), 
            password=kwargs.pop('password', 'romys')
        ) as session:
        return session.request(method=method, url=url, **kwargs)

def get(url, params=None, **kwargs):
    return request("get", url, params=params, **kwargs)

def options(url, **kwargs):
    return request("options", url, **kwargs)

def head(url, **kwargs):
    kwargs.setdefault("allow_redirects", False)
    return request("head", url, **kwargs)

def post(url, data=None, json=None, **kwargs):
    return request("post", url, data=data, json=json, **kwargs)

def put(url, data=None, **kwargs):
    return request("put", url, data=data, **kwargs)

def patch(url, data=None, **kwargs):
    return request("patch", url, data=data, **kwargs)

def delete(url, **kwargs):
    return request("delete", url, **kwargs)

if(__name__ == '__main__'):
    session = TorSession(password='romys')
    # session = Session()
    for _ in range(5):
    # from requests import get
        print(session.get('http://httpbin.org/ip').json())
    # print(get('https://httpbin.org/cookies/set/ok/2').headers)