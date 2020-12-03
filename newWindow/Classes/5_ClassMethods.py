class Employee:

    num_of_emps = 0
    """(*) is changed by the class method function set_raise_amount"""
    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

        Employee.num_of_emps += 1

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    """this alters the functionality of our function such that it recieves the 
    class as the first argument instead of the instance 
    This is the same as saying Employee.raise_amount = 1.05
    it changes the raise amount for all instances of employees
    """
    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amount = amount
        pass

    # @classmethod
    # def from_string(cls, string):
    #     first, last, pay = string.split('-')
    #     return cls(first,last,pay)

    """
    Class methods can manipulate the class itself, so in this case this function
    manipulates some data so that it can be used to create an instance of a new class.
    to do that you need to call the class. A regular instanc emethod does
    not have the power to initiate the class or manipulate its variables
    
    it really is a kind of extension of the line "emp_3 = Employee.from_string(emp_3_str)"
    which is calling or initiating the Employee class to make an instance. 
    """
    @classmethod
    def from_string(cls, string):
        first, last, pay = string.split('-')
        return cls(first,last,pay)

    # def from_string(self, string):
    #     first, last, pay = string.split('-')
    #     return self(first,last,pay)


emp_1 = Employee('Corey', 'Schafer', 50000)
emp_2 = Employee('Joe', 'La D', 40000)

Employee.set_raise_amt(1.05)
"""now you can also run a class method from an instance but it wont do anything 
different, it is still aimed at the class variable. plus it is just bad practice.
]"""
# emp_1.set_raise_amt(1.05)

print(Employee.raise_amount)
print(emp_1.raise_amount)
print(emp_2.raise_amount)

"""
PROBLEM
If the new employee data comes in as a string seperated by hyphens, 
then you are going to want to parse it put into discrete objects.
rather than writing a line of code every time you want to do that, 
then calling an instance of employee (emp_3 = Employee('name', 'name', salary)
we an write a @class method that will will do all of this at once.
this is known as a alternative constructor."
"""

emp_3_str = 'John-Doe-70000'
emp_4_str = 'Steve-Smith-30000'
emp_5_str = 'Jane-Doe-90000'

emp_3 = Employee.from_string(emp_3_str)
print(emp_3.fullname())