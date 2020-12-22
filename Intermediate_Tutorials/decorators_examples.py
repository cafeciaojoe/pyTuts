"""
decorators can be used to log things and time things.
they can also be stacked or chained, but this requires the import
of a library called functools
"""
from functools import wraps

def my_logger(orig_func):
    import logging
    logging.basicConfig(filename='{}.log'.format(orig_func.__name__), level = logging.INFO)

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        logging.info('{} ran with args: {}, and kwargs {}'.format(orig_func.__name__, *args, **kwargs))
        """return the original function with all the arguments and kew word arguments just passed thru"""
        return orig_func(*args, **kwargs)

    """return the wrapper function unexecuted"""
    return wrapper

def my_timer(orig_func):
    import time

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        print('{} ran in: {} sec'.format(orig_func.__name__, t2))
        return result

    """return the wrapper function unexecuted"""
    return wrapper


@my_logger
def display_info(name, age):
    print('display_info ran with arguments ({}, {})'.format(name, age))

display_info('john', 30)

"""
now remember if you put @my_logger as a decorator it is the same as passing display_info (original funciton)
into my_logger (the decorator)

display_info = my_logger(display_info)

now if you put:
@my_logger
@my_timer
it is the same as:

display_info = my_timer(my_logger(display_info))

Which WOULD pass display_info into my_logger
BUT WOULD NOT pass display_info into my_timer
it would instead pass the wrapper from my_logger into my_timer
because that is what my_logger returns.

So we need to:
from functools import wraps

and place the decorator @wraps on top of every wrapper funcitons. 

"""
