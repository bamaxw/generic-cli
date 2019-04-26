from typing import Any, AsyncIterator, Container, Dict, Optional, Type, Union
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from types import TracebackType
import logging

from aiohttp import ClientResponse as Response, ClientSession as Session

from crossroads import CrossRoads

from .utils import cache_for, minutes
from .config import SessionConfig

log = logging.getLogger(__name__)


class Client:
    '''
    Generic-Client Client
    implements generic connections management
    host management and anything that any specific clients might use
    commonly
    Arguments:
        host   -- url of the host to connect to
        prefix -- a base path present in each url
        config -- ClientSession management config
    '''
    def __init__(self, host: str, prefix: str = '', config: Union[None, Dict[str, Any], SessionConfig] = None) -> None:
        self._host = host
        self._prefix = prefix

    async def __aenter__(self) -> 'Client':
        return self



class Client:
    host: Optional[str] = None
    service_name: Optional[str] = None
    prefix: str = ''
    def __init__(self,
                 env: Optional[str] = None,
                 *,
                 service_name: Optional[str] = None,
                 prefix: str = '',
                 host: Optional[str] = None,
                 config: Union[None, Dict[str, Any], SessionConfig] = None) -> None:
        # Validate arguments
        if self.service_name and service_name:
            raise TypeError("'service_name' specified at both class and instance level")
        if self.prefix and prefix:
            raise TypeError("'prefix' specified at both class and instance level")
        # Validate config type
        if isinstance(config, (dict, type(None))):
            session_config = SessionConfig(**config or {})
        elif isinstance(config, SessionConfig):
            session_config = config
        else:
            raise TypeError(f"config type {type(config)} could not be recognized,"
                            " please use a dictionary or generic_cli.config.SessionConfig")
        service_name = service_name or self.service_name
        host = host or self.host
        prefix = (prefix
                  if prefix is None
                  else self.prefix)
        if not host:
            if not service_name and not env:
                raise TypeError("In auto-resolve mode both 'service_name' and 'env' must be provided")
            log.info('Running in auto-resolve mode')
        else:
            log.info('Running in static mode with host: %r', host)
        self._host = host  # If host is None - auto-resolve mode is enabled
                           # Settings host to any value will disable auto-resolve
        self._service_name = service_name
        self._prefix = prefix
        self.env = env
        self.config = session_config
        self._session = Session()

    async def __aenter__(self) -> 'AutoResolveClient':
        try:
            await self.get_host()
        except:
            await self.close()
            raise
        return self

    async def __aexit__(self, exc_type: Type[Exception], exc: Exception, tb: TracebackType) -> None:
        await self.close()

    async def close(self) -> None:
        '''Close underlying async connections'''
        await self._session.close()

    @cache_for(minutes(60))
    async def get_host(self) -> str:
        '''
        Returns host url
        In the case host was passed as an argument to constructor it's going to be returned
        In the case it wasn't - it's going to be auto-resolved based on 'service_name' and 'env'
        '''
        if self._host is not None:
            return self._host
        async with CrossRoads(self.env) as crossroads:
            host = await crossroads.get(self._service_name)
            log.info("Resolved %s's host to %r [name=%r env=%r]",
                     self.__class__.__name__,
                     host,
                     self._service_name,
                     self.env)
            return host

    async def get_base_url(self) -> str:
        '''Returns client's base url'''
        host = await self.get_host()
        return f'{host}{self._prefix}'

    @asynccontextmanager
    async def issue(self, method: str, path: str, **kw) -> AsyncIterator[Response]:
        '''Manages all request dispatches'''
        base_url = await self.get_base_url()
        url = f'{base_url}{path}'
        log.info('Getting url %r', url)
        async with self._session.request(method, url, **kw) as res:
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
