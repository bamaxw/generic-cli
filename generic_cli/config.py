'''GenericClient session configuration'''
from typing import Container, Dict, Union
from dataclasses import dataclass, field

from tenacity.stop import stop_base
from tenacity.wait import wait_base

from . import defaults

Policies = Union[stop_base, wait_base]


@dataclass
class SessionConfig:
    '''
    Contains session configuration for Client
    That includes retry specification, error throwing etc
    '''
    retry_codes: Container[Union[str, int]] = field(default_factory=lambda: defaults.RETRY_CODES)
    retry_policy: Dict[str, Policies] = field(default_factory=lambda: defaults.RETRY_POLICY)
    timeout: int = defaults.TIMEOUT
