"""https://www.youtube.com/watch?v=kr0mpwqttM0"""

"""
First-Class functions:
"A  programming language is said to have first-class functions if it treats functions as first-class citizens."

First-Class Citizen (Programming):
"A first class citizen (sometimes called first-class objects) in a programming language is an entity which supports all
the operations generally available to other entities. These operations typically include being passed as an argument,
retuned from a function, and assigned to a variable.
"""

def square(x):
    return x * x

def cube(x):
    return x * x * x

"""when we use the parenthesis we EXECUTE the function"""
#f = square(5)

"""when we do not use the parethesis we assign it to a variable"""

# f = square
#
# print(square)
# print(f(5))

"""
square is a fist class function because you can assign it to f and now f is the function
we can also:
- pass functions as arguments
- return functions as the result from other functions

if a functions does these things, they are called "higher order functions"
"""


"""notice how when we pass the function as an argument into another function we are not using the parenthesis
we are not trying to execute the argument
"""
def my_map(func, arg_list):
    result = []
    for i in arg_list:
        result.append(func(i))
    return result

squares = my_map(square, [1,2,3,4,5])

print(squares)

# a function is defined with one argument
def logger(msg):

    """
    # the function above defines the funciton below,
    # which takes no arguments
    # but it does recognise 'msg' the argument from the funciton above
    """
    def log_message():
        print('log', msg)
    """
    # it returns the inner function BUT WITHOUT PARETHESIS
    # if you use the parenthesis you cannot assign logger() to anything
    # BECAUSE YOU ARE EXECUTING the return object (it will turn into None)
    """
    return log_message

"""
this works with the return 'log_message' or 'log_message()'
"""
logger('hi')

"""
this only works when the return 'log_message' has no parenthesis
this is because this line is only assigning logger('hi') to log_hi
not executing anything. 
"""
log_hi = logger('hi')
"""
only now are you executing the function
"""
log_hi()

"""
here is a semi real world example
"""

def html_tag(tag):

    def wrap_text(msg):
        """
        when using the format method, The placeholders can be identified using named indexes {price},
        numbered indexes {0}, or even empty placeholders {}.
        https://www.w3schools.com/python/ref_string_format.asp
        """
        print('<{0}>{1}</{0}>'.format(tag, msg))

    return wrap_text

"""
h1 is passed into html_tag
as we see from above, this line does no executing. 
all it does is bring 'print_h1' up to the 'wrap_text()' function
inside the html_tag function. just waiting to be executed
and waiting to recieve a 'msg' argument
"""
print_h1 = html_tag('h1')

"""
proof of this can be seen when you print it you get
<function html_tag.<locals>.wrap_text at 0x10e2cfdd0>
"""
print(print_h1)
"""
now you can see that the arguments in the lines below get passed into the 'wrap_text()' funciton, the second function. 
and it remembers the h1 argument because print_h1 is a copy of the html_tag funciton with h1 passed in. 
"""
print_h1('Test Headline!')
print_h1('Test Headline!')






