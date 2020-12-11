class Employee_auto:
    """this is a class attribute it can be used anywhere
    in the class"""
    num_of_emps = 0
    raise_amount = 1.04


    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'
        Employee_auto.num_of_emps += 1
        """so here we are using the init method to iterate thru the number
        of employees, this does not make it in instance attribute, so we refer to the class
         when calling and modifying this attribute"""

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)
        """self.raise_amount can also be written as below
        
        self.pay = int(self.pay * Employee_auto.raise_amount)
        
        and will still state 1.04. this is 
        because when you make an instance of a class
        in it there will be a copy of anything defined in the __init__ 
        (the instance attributes) AND a reference to the 
        class wide attributes see (*) below for proof"""


emp_1 = Employee_auto('Corey', 'Schafer', 50000)
emp_2 = Employee_auto('Joe', 'La D', 40000)

print(emp_1.pay)
emp_1.apply_raise()
print(emp_1.pay)

"""(*) the statement below prints the 'namespace' of emp_1 class instance as a dictionary
we can see that raise amount (a class attribute) is not sen there
"""
print(emp_1.__dict__)

"""now we will modify emp_2 raise amount to 1.05 and print it as a dict
you will see that an instance attribute 'raise_amount' has been 
created. """
emp_2.raise_amount = 1.05
print(emp_2.__dict__)


"""if we modify the class attribute 'raise_amount' to equal 1.07
 and re print the class instance emp_2 as a dictionary
 we see that the raise amount remains unchanged. 
 this is because it is now an instance attribute and takes preference over
 the class attribute. 
 """
Employee_auto.raise_amount = 1.07
print(emp_2.__dict__)