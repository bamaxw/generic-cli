from typing import Any, Awaitable, Callable, Dict
from functools import wraps
import inspect
import time


def minutes(mins: float) -> float:
    return mins * 60


def cache_for(seconds: float) -> 'CacheFor':
    return CacheFor(seconds)


class CacheFor:
    _func_cache: Dict[Callable[[object], Awaitable[Any]], Any] = {}
    _func_timestamps: Dict[Callable[[object], Awaitable[Any]], float] = {}
    def __init__(self, timeout: float) -> None:
        self.timeout = timeout

    def __call__(self, func: Callable[[object], Awaitable[Any]]) -> Callable[[object], Awaitable[Any]]:
        if inspect.signature(func) not in ('(self)', '()'):
            raise TypeError('CacheFor can be called on a method or function with no arguments only!')
        @wraps(func)
        async def _method_wrapper(*a):
            if self._func_timestamps[func] + self.timeout >= time.time():
                self._func_cache[func] = await func(*a)
            return self._func_cache[func]
        return _method_wrapper
