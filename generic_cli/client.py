from typing import Optional
import logging

from crossroads import CrossRoads

from .utils import cache_for, minutes

log = logging.getLogger(__name__)


class Client:
    def __init__(self, host: str, prefix: str = '') -> None:
        self.host = host
        self.prefix = prefix

    async def get_host(self) -> str:
        return self.host

    async def get_base_url(self) -> str:
        host = await self.get_host()
        return f'{host}{self.prefix}'


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
