from typing import AsyncIterator, Optional, Type
from contextlib import asynccontextmanager
from types import TracebackType
import logging

from aiohttp import ClientResponse as Response, ClientSession as Session

from crossroads import CrossRoads

from .utils import cache_for, minutes

log = logging.getLogger(__name__)


class Client:
    def __init__(self, host: str, prefix: str = '') -> None:
        self.host = host
        self.prefix = prefix
        self.session = Session()

    def __aenter__(self) -> 'Client':
        return self

    async def __aexit__(self, exc_type: Type[Exception], exc: Exception, tb: TracebackType) -> None:
        await self.close()

    async def close(self) -> None:
        await self.session.close()

    async def get_host(self) -> str:
        return self.host

    async def get_base_url(self) -> str:
        host = await self.get_host()
        return f'{host}{self.prefix}'

    @asynccontextmanager
    async def issue(self, method: str, path: str, *a, **kw) -> AsyncIterator[Response]:
        base_url = await self.get_base_url()
        url = f'{base_url}{path}'
        async with self.session.request(method, url, *a, **kw) as res:
            yield res

    @asynccontextmanager
    async def post(self, *a, **kw) -> AsyncIterator[Response]:
        async with self.issue('POST', *a, **kw) as res:
            yield res

    @asynccontextmanager
    async def get(self, *a, **kw) -> AsyncIterator[Response]:
        async with self.issue('GET', *a, **kw) as res:
            yield res

    @asynccontextmanager
    async def put(self, *a, **kw) -> AsyncIterator[Response]:
        async with self.issue('PUT', *a, **kw) as res:
            yield res

    @asynccontextmanager
    async def delete(self, *a, **kw) -> AsyncIterator[Response]:
        async with self.issue('DELETE', *a, **kw) as res:
            yield res

    @asynccontextmanager
    async def head(self, *a, **kw) -> AsyncIterator[Response]:
        async with self.issue('HEAD', *a, **kw) as res:
            yield res


class AutoResolveClient(Client):
    def __init__(self, name: str, env: str) -> None:
        self.name = name
        self.env = env

    @classmethod
    async def resolve(cls, *a, **kw) -> 'AutoResolveClient':
        '''Instantiate AutoResolveClient and immediatelly resolve its host'''
        instance = cls(*a, **kw)
        await instance.get_host()
        return instance

    @cache_for(minutes(60))
    async def get_host(self) -> str:
        host = await CrossRoads(self.env).get(self.name)
        log.info("Resolved %s's host to %r [name=%r env=%r]",
                 self.__class__.__name__,
                 host,
                 self.name,
                 self.env)
        return host
