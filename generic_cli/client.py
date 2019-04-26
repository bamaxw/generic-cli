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
        self._host = host
        self._prefix = prefix
        self.session = Session()

    async def __aenter__(self) -> 'Client':
        return self

    async def __aexit__(self, exc_type: Type[Exception], exc: Exception, tb: TracebackType) -> None:
        await self.close()

    async def close(self) -> None:
        '''Close underlying async connections'''
        await self.session.close()

    async def get_host(self) -> str:
        '''Returns clients host url'''
        return self._host

    async def get_base_url(self) -> str:
        '''Returns clients base url'''
        host = await self.get_host()
        return f'{host}{self._prefix}'

    @asynccontextmanager
    async def issue(self, method: str, path: str, *a, **kw) -> AsyncIterator[Response]:
        '''Manages all request dispatches'''
        base_url = await self.get_base_url()
        url = f'{base_url}{path}'
        log.info('Getting url %r', url)
        async with self.session.request(method, url, *a, **kw) as res:
            yield res

    @asynccontextmanager
    async def post(self, *a, **kw) -> AsyncIterator[Response]:
        '''Issues a post request'''
        async with self.issue('POST', *a, **kw) as res:
            yield res

    @asynccontextmanager
    async def get(self, *a, **kw) -> AsyncIterator[Response]:
        '''Issues a get request'''
        async with self.issue('GET', *a, **kw) as res:
            yield res

    @asynccontextmanager
    async def put(self, *a, **kw) -> AsyncIterator[Response]:
        '''Issues a put request'''
        async with self.issue('PUT', *a, **kw) as res:
            yield res

    @asynccontextmanager
    async def delete(self, *a, **kw) -> AsyncIterator[Response]:
        '''Issues a delete request'''
        async with self.issue('DELETE', *a, **kw) as res:
            yield res

    @asynccontextmanager
    async def head(self, *a, **kw) -> AsyncIterator[Response]:
        '''Issues a head request'''
        async with self.issue('HEAD', *a, **kw) as res:
            yield res


class AutoResolveClient(Client):
    def __init__(self, name: str, env: str, host: Optional[str] = None, prefix: str = '') -> None:
        super().__init__(host, prefix)
        self.name = name
        self.env = env

    async def __aenter__(self) -> 'AutoResolveClient':
        await self.get_host()
        return self

    @cache_for(minutes(60))
    async def get_host(self) -> str:
        if self._host is not None:
            return await super().get_host()
        crossroads = CrossRoads(self.env)
        host = await crossroads.get(self.name)
        await crossroads.close()
        log.info("Resolved %s's host to %r [name=%r env=%r]",
                 self.__class__.__name__,
                 host,
                 self.name,
                 self.env)
        return host
