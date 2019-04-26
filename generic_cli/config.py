'''GenericClient session configuration'''
from typing import Collection, Dict, Union
from dataclasses import dataclass, field

from tenacity.stop import stop_base
from tenacity.wait import wait_base

from . import defaults

PolicyType = Union[stop_base, wait_base]


@dataclass
class SessionConfig:
    '''
    Contains session configuration for Client
    That includes retry specification, error throwing etc
    '''
    retry_codes: Collection[str] = field(default_factory=lambda: defaults.RETRY_CODES)
    retry_policy: Dict[str, PolicyType] = field(default_factory=lambda: defaults.RETRY_POLICY)
    timeout: int = defaults.TIMEOUT
    def __post_init__(self) -> None:
        self.retry_codes = {str(retry_code) for retry_code in self.retry_codes}
