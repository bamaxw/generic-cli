class Signal(Exception):
    '''
    Signals are class of exceptions that serve as 'signals'
    for the Client to do something
    '''

class ShouldRetry(Signal):
    '''
    Notifies the tenacity.retry that it should retry
    '''
