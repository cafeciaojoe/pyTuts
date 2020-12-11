# Suppose this is foo.py.
# https://stackoverflow.com/questions/419163/what-does-if-name-main-do#:~:text=__name__%20%3A%20Every%20module,which%20top%2Dlevel%20code%20executes.

print("before import")
import math

print("before functionA")
def functionA():
    print("Function A")

print("before functionB")
def functionB():
    print("Function B {}".format(math.sqrt(100)))

print("before __name__ guard")
if __name__ == '__main__':
    functionA()
    functionB()
print("after __name__ guard")

"""
# What gets printed if foo is the main program
before import
before functionA
before functionB
before __name__ guard
Function A
Function B 10.0
after __name__ guard
"""

"""
# What gets printed if foo is imported as a regular module
before import
before functionA
before functionB
before __name__ guard
after __name__ guard
"""

