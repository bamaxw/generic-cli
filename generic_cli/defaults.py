'''Default values for Generic Client configuration'''
from tenacity import wait_exponential, stop_after_delay

RETRY_CODES = {'5xx'}
TIMEOUT = 30
RETRY_POLICY = {
    'wait': wait_exponential(),
    'stop': stop_after_delay(30)
}
