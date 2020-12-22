"""https://www.youtube.com/watch?v=swU3c34d2NQ"""
"""
Closures

Wikipedia says:
"A closure is a record storing a function together with
an environment: a mapping associating each free variable of the function
with the value or storage location to which the name was bound then the
closure was created. A closure, unlike a plain function, allows the
function to access those captured variables throughout the closure's
reference to them, even when the function is invoked outside their scope
"""

def outer_func(msg):
    message = msg

    def inner_func():
        """
        when our inner function accesses the message variable
        this is called a free variable, because it was not defines within the funciton
        """
        print(message)

    """
    including the parenthesis executes the function. 
    not including the parentheses will just return the function without executing it. 
    """
    return inner_func
"""reminder you cannot call 'inner_func() outside of outer_func UNLESS you assign it to a vaiable as we do below. """
hi_func = outer_func('hi')
hello_func = outer_func('hello')

"""
if we run these now, each of these functions remembers the value of their own message variable. 

"""
hi_func()
hello_func()

"""
here is a more practical example and one slightly more complex
"""
import logging
logging.basicConfig(filename='example.log', level = logging.INFO)


def logger(func):
    """*args means this functill nake any number of arguments"""
    def log_func(*args):
        logging.info('running "{}" with arguments {}'.format(func.__name__, args))
        """note that not only are we printing, but we are also executing the func in the one line"""
        print(func(*args))
    return log_func

def add(x, y):
    return x+y

def sub(x, y):
    return x-y

"""these lines Prime the logger function witht he function to use for the mathematical operation
you now 
"""
add_logger = logger(add)
sub_logger = logger(sub)

add_logger(3, 3)

"""
a good way to remember this is that closures, 'close over' the free variables from their environment. 
in this case 'func' is the free variable
"""

"""
it should be noted here however that the use of closures for loggers is not as elegant as decorators. 
see decorators.py
"""