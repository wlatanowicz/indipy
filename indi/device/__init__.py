import logging
import threading
from functools import wraps

from .driver import Driver
from .proxy import Proxy

NON_BLOCKING_ENABLED = True


def non_blocking(fun):
    @wraps(fun)
    def wrapped(*args, **kwargs):
        def inner_fun():
            try:
                fun(*args, **kwargs)
            except Exception as e:
                logger = logging.getLogger(fun.__module__)
                logger.exception(e)

        if NON_BLOCKING_ENABLED:
            th = threading.Thread(target=inner_fun)
            th.start()
        else:
            inner_fun()

    return wrapped
