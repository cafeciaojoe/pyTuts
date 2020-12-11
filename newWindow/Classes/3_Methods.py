class Employee:

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

    """
    each method within in a class automatically takes the instance as the first argument
    because outside the class in the big bad world, when you call a method, python still
    needs to know where that method came from and will automatically pass in the class
    INSTANCE for you.
    
    because you have to perform that method on an instance right?
    
    emp_1.fullname()
    

    """

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

emp_1 = Employee('Corey', 'Schafer', 50000)
emp_2 = Employee('Joe', 'La D', 40000)

print(emp_1.email)
print(emp_2.email)

print(emp_1.fullname())
print(emp_2.fullname())

"leave out the () and you will get the methods location on memory not the return of that method"
print(emp_1.fullname)
"""
if you do not add self to the method then python things that the method takes "0 positional
arguments" meaning the methods needs nothing to run. but methods need at least 1 positional
argument because they need to know which instance they are working on. so when you run
something like emp_1.fullname() and the method full name is not deifne with self as a 
positional argument, then you will get an error because 'emp_1' is the positional 
argument and the ill defines method fullname was not expecting it
"""
"""also notice that youc an call the class two ways. the first way 
automatially puts the instance in as the first argument
the second way you must specify the instance"""

print(emp_1.fullname())
print(Employee.fullname(emp_1))

"""
    can you perform a method on a instance from a diferent class?
"""

class Employee_animal:
    def __init__(self, first, last):
        self.first = first
        self.last = last

emp_3 = Employee_animal('Dino', 'dongo')

emp_3.fullname()

"""
the answer is NO! despite the animal employee having a first and last name, 
the fullname method does not exist in it's class, you get this error

Traceback (most recent call last):
  File "/Users/cafeciaojoe/PycharmProjects/pyTuts/newWindow/Classes/3_Methods.py", line 58, in <module>
    emp_3.fullname()
AttributeError: 'Employee_Animal' object has no attribute 'fullname'

"""