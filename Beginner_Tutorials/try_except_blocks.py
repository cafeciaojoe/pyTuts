"""
https://www.youtube.com/watch?v=NIWwJbo-9_8
try and except is supposed to catch expected errors. so we can handle them properly
"""


try:
    f = open('test.txt')
    # var = bad_var
        # you can just manually raise exceptions.
        # raise Exception

    
    """we can set exceptions to a specific time of error. so that we catch the errors we want/ expect"""
except FileNotFoundError:
    print('sorry this file does not exist')

    """make sure you put the more general 'exception' at the bottoms"""
    """ by using as, you can print the exception name on its own without a traceback"""
except Exception as e:
    print(e)

    """this will run if the try clause did NOT raise an exception"""
else:
    print(f.read())
    f.close()

    """this runs no matter what happens, this is good for releasing resources, no matter what. 
    like closing down a database"""
finally:
    print('executing finally')