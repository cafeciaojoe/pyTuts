class Employee_auto:
    """this is a class variable it can be used anywhere
    in the class"""
    num_of_emps = 0
    raise_amount = 1.04


    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'
        """so here we are using the init method to iterate thru the number
        of employees, now this instances of this variable should not exist 
        for each instance of the employee class so we refer to the class
         when calling and modifying this variable"""
        Employee_auto.num_of_emps += 1

    "each method within in a class automaticall takes the instance as the first argument"
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)
        """self.raise_amount can also be written as below
        and will still state 1.04. this is 
        because when you make an instance of a class
        there will be a copy of anything defined in the __init__ 
        (the instance variables) and a reference to the 
        class wide instance variables see (*) below for proof"""
        # self.pay = int(self.pay * Employee_auto.raise_amount)

emp_1 = Employee_auto('Corey', 'Schafer', 50000)
emp_2 = Employee_auto('Joe', 'La D', 40000)

""" OS here we are accessing an instance variable from emp_1,
  and using a method on emp_1
  both using the same syntax of .something"""
print(emp_1.pay)
emp_1.apply_raise()
print(emp_1.pay)

"""(*) the statement below prints emp_1 class instance as a dictionary
we can see that raise amount (a class variable) is not sen there"""
print(emp_1.__dict__)

"""now we will modify emp_2 raise amount to 1.05 and print it as a dict
you will see that an instance variable 'raise_amount' has been 
created. """
emp_2.raise_amount = 1.05
print(emp_2.__dict__)

"""if we modify the rais """
