from contextlib import asynccontextmanager
from functools import wraps


class Signal(Exception):
    '''
    Signals are class of exceptions that serve as 'signals'
    for the Client to do something
    '''
    def __init__(self, return_) -> None:
        super().__init__()
        self._return = return_


class ShouldRetry(Signal):
    '''
    Notifies the tenacity.retry that it should retry
    '''


def return_from_signal(func):
    @wraps(func)
    def _wrapper(*a, **kw):
        try:
            return func(*a, **kw)
        except Signal as sig:
            return sig._return
    return _wrapper
