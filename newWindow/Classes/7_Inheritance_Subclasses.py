class Employee:

    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)


"""
just by passing in an existing class into a new class, the new class will inherit the 
attributes and methods of the class that is passed in.

raise_amount overwrites the parent class attribute. 
"""
class Developer(Employee):
    raise_amount = 1.1

    """
    a developer in the company will more specific data like prgramming language. 
    but we still want the employee class to create the instances for their name, email 
    and pay (that way self.first etc are only typed once)
    
    So we call super().__init__(arg1,arg2...)
    so that lets the parent class handle these arguments. it passes them up the chain
    it is the same as Employee.__init__(first, last, pay) but more modular. 
    """

    def __init__(self, first, last, pay,prog_lang):
        super().__init__(first, last, pay)
        self.prog_lang = prog_lang
    pass

class Manager(Employee):

    #Pro tip never use mutable (changable) data types as default arguments
    def __init__(self, first, last, pay,employees=None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employee = []
        else:
            self.employees = employees

    def add_emp(self, employee):
        if employee not in self.employees:
            self.employees.append(employee)

    def remove_emp(self, employee):
        if employee in self.employees:
            self.employees.remove(employee)

    def print_employees(self):
        for emp in self.employees:
            print('-->', emp.fullname())


dev_1 = Developer('Joe','Blogs',50000, 'Python')
dev_2 = Developer('Test','Employee',60000, 'Java')

mgr_1 = Manager('sue','smith', 90000, [dev_1])

mgr_1.add_emp(dev_2)

"""
Python has in built methods called isinstance() and is subclass()
you can use them on objects to see where they came from. 
So. if you see an object (lower case word) and want to know where it cam from you can 
say...
"""

print(isinstance(mgr_1,Manager))

"""
or if you see a class (capitalised) and want to see where it came from you can say
"""

print(issubclass(Developer, Employee))

"""
further to this, if you want to look at information about a class you just need to
use the built in help() method on a class or and instance to find out information
about there it came fromm, what gets passed into it and what instance variables it holds. 
"""
help(mgr_1)

#print(help(Developer))

"""
class Developer(Employee)
 |  Developer(first, last, pay)
 |  
 |  Method resolution order:
 |      Developer
 |      Employee
 |      builtins.object 
        #this is the stuff that all classes inherit from python like 'type()' or 'print'
 |  
 |  Methods inherited from Employee:
 |  
 |  __init__(self, first, last, pay)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  apply_raise(self)
 |  
 |  fullname(self)
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors inherited from Employee:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes inherited from Employee:
 |  
 |  raise_amt = 1.04
"""