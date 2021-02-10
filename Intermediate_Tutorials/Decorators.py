"""
https://www.youtube.com/watch?v=FsAPt_9Bf3U
"""
"""
A decorator is a function that takes a second function as an argument,
then, via the definition of a third function (the wrapper)
would return the second function (not yet exectued)
adds some kind of functionality, like logging or timing how long a function ran
then finally the decorator returns the wrapper function all without altering the original function that was passed in
"""

"""
so we know with the example below, 
that the outer function (aka the decorator) returns the inner functiion (aka the wrapper)
waiting to be executed, and when it is executed (by assigning the outer function to a vairable and calling it.
it will print the msg
"""
def outer_function(msg):
    def inner_function():
        print(msg)
    return inner_function

hello = outer_function('Hey everyone')

hello()


"""
now what if instead of printing a message we pass in what if we execute a funciton we pass in...
decorating our functions allows us to easily add functionality to our existing functions
by adding that functionality inside of our wrapper.
you are "wrapping up" extra functionality with an existing function (like two presents in one wrapping paper)
"""

def decorator_function(original_function):

    def wrapper_function(*args, **kwargs):
        print('wrapper executed this before the {} function'.format(original_function.__name__))
        return original_function(*args, **kwargs)

    return wrapper_function

""""
By adding the @decorator function, it is the same
as:
- passing in the display function into the decorator function
- assigning the decorator function to an object
- executing the object
 
decorated_display = decorator_function(display)
decorated_display()

"""
@decorator_function
def display():
    print('the display function ran')

"""
except now we just have to execute display,
and the decorator function will also run. 
"""

display()

"""
so now we can add the decorator to any function right?
and the wrapper function will add functionality to whatever we decorate.
ALMOST.
We just have to make one modification to the the wrapper function and the original function it returns.
We added '*args' and '**kwards' which mean any number of arguments and keyword arguments respectively.
this means that when you decorate the function display_info(name, age), the wrapper is ready and waiting
to execture its fucntions along with display_info. BUT
the wrapper needs to pass arguments onto the original function after it is done adding its extra functionality.
so it uses '*args' and '**kwards' in both the wrapper and the orignal funciton.
because we don't know and dont care how many arguments there are, the wrapper just wants to pas them thru
so that they can just get on with adding their functionality
"""
@decorator_function
def display_info(name, age):
    print('display_info ran with arguments ({}, {})'.format(name, age))



display_info('john', 25)



"""
there is also the possibility of using a class as a decorator
"""

class Decorator_class(object):

    def __init__(self, original_function):
        print('instance created')
        self.original_function = original_function

    """
    the call method will run when an instance of the class has been called like a funciton
    """
    def __call__(self, *args, **kwargs):
        print('the call method executed this before the {} function'.format(self.original_function.__name__))
        return self.original_function(*args, **kwargs)

"""
decorating a class also calls an instance of it.
it is like writing: show = Decorator_class()?
"""


@Decorator_class
def show():
    print('the show function ran')

@Decorator_class
def show_info(name, age):
    print('show_info ran with arguments ({}, {})'.format(name, age))


"""now calling a class like a function invokes the __call__ method"""
show()
show_info('gianni', 30)



