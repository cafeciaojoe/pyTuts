"""
PASS BY REFERENCE
https://realpython.com/python-pass-by-reference/#replicating-pass-by-reference-with-python

Python's functions does not operate on the exact variable (as stored in the computers memory) like other
languages. You need to use a bunch of other methods to work around it.

"""

def main_a():
    n = 9001
    print(f"Initial address of n: {id(n)}")
    increment(n)
    print(f"  Final address of n: {id(n)}")

def increment(x):
    print(f"Initial address of x: {id(x)}")
    x += 1
    print(f"  Final address of x: {id(x)}")
#     the final address of x shows that the incremented value has a different place in the memory even though it is still x.
# and it is only assigned back to the original place in the memory after the increment function is completed.

def main_b():
    counter = 0
    print(f"Address of counter before Alice: {id(counter)}")
    greeting, counter = greet("Alice", counter)
    print(f"Address of counter after Alice: {id(counter)}")
    print(f"{greeting}\nCounter is {counter}")
    print(f"Address of counter before Bob: {id(counter)}")
    greeting, counter = greet("Bob", counter)
    print(f"Address of counter After Bob: {id(counter)}")
    print(f"{greeting}\nCounter is {counter}")

def greet(name, passed_in_counter):
    print(f"Initial address of passed in counter: {id(passed_in_counter)}")
    return f"Hi, {name}!", passed_in_counter + 1

if __name__ == '__main__':
    main_a()
    main_b()