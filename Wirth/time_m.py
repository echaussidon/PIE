"""

Creer une decoration python pour pouvoir mesurer le temps d'execution de fonction.
Il suffit de faire :
@time_measurement
def ma_function():
    return "blabal"

"""

import functools
import time
import constantes as c

def time_measurement(func):
    """Timestamp decorator for dedicated functions"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        mlsec = repr(elapsed).split('.')[1][:3]
        readable = time.strftime("%H:%M:%S.{}".format(mlsec), time.gmtime(elapsed))
        if c.print_time_measurement :
            print('Function "{}": {} sec'.format(func.__name__, readable))
        return result
    return wrapper
