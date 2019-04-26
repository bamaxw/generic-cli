'''Utility functions and classes for core generic-cli'''
from typing import Any, Awaitable, Callable, Dict, TypeVar, Union
from functools import wraps
import inspect
import time

T = TypeVar('T')
AsyncMethod = Callable[[Any], Awaitable[T]]
AsyncFunc = Callable[[], Awaitable[T]]
AsyncCallable = Union[AsyncMethod, AsyncFunc]


def minutes(mins: float) -> float:
    '''Returns amount of seconds in that many minutes'''
    return mins * 60


def cache_for(seconds: float) -> 'CacheFor':
    '''Same as CacheFor()'''
    return CacheFor(seconds)


class CacheFor:
    '''
    Caches function response for the amount of seconds
    specified in timeout argument passed to the class constructor
    '''
    _func_cache: Dict[AsyncCallable, Any] = {}
    _func_timestamps: Dict[AsyncCallable, float] = {}
    def __init__(self, timeout: float) -> None:
        self.timeout = timeout

    def __call__(self, func: AsyncCallable) -> AsyncCallable:
        sig = inspect.signature(func)
        params = sig.parameters
        if len(params) > 1 or (len(params) == 1 and 'self' not in params):
            raise TypeError('CacheFor can be called on a method or function with no arguments only!'
                            f' Detected signature: {str(sig)}')
        self._func_timestamps[func] = 0
        @wraps(func)
        async def _method_wrapper(*a):
            if self._func_timestamps[func] + self.timeout <= time.time():
                self._func_cache[func] = await func(*a)
            return self._func_cache[func]
        return _method_wrapper
