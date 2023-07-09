import logging
import time
from functools import wraps


def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.debug(
            "Time taken: {0:.2f} seconds".format(end_time - start_time)
        )
        return result

    return wrapper
