import datetime

class Employee:

    num_of_emps = 0
    raise_amount = 1.04

    def __init__(self, first, last, pay,startDate):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'
        self.startDate = startDate

        Employee.num_of_emps += 1

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amount = amount
        pass

    @classmethod
    def from_string(cls, string):
        first, last, pay = string.split('-')
        return cls(first,last,pay)

    # def from_string(self, string):
    #     first, last, pay = string.split('-')
    #     return self(first,last,pay)

    """
    @staticmethod
    when you need to make a function that does need to pass the class or 
    the instance into the function. you do not need to pass in anything from the
    class. BUT the function is related to the class so we want
    to keep it all together. (for when you import a class into another file
    and you need this function 
    """

    "it is just like a function that sits outside a class! easy!"
    @staticmethod
    def is_workday(day):
        """
        in python there is a weekday() method from the datetime module
        that returns a number 0-6 corresponding to the day of the week
        """
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True

emp_1 = Employee('Corey', 'Schafer', 50000,datetime.date(2016,7,11))
emp_2 = Employee('Joe', 'La D', 40000, datetime.date(2016,7,11))


"""now you still have to use Employee. to access this method because the 
static method is still part of the Employee class, but the Employee __init__ 
is not run and you do not have a new instance of this class proof below as it is just
a simple ol bool"""

some_random_date = datetime.date(2016,7,11)
print(some_random_date)
print(Employee.is_workday(some_random_date))
print(type(Employee.is_workday(some_random_date)))

"""
now both 'emp_2.is_workday(startDate)' and 'Employee.is_workday(startDate)' return the 
following error

Traceback (most recent call last):
  File "/Users/cafeciaojoe/PycharmProjects/pyTuts/PyQt/OOP/6_Static_Methods.py", line 75, in <module>
    emp_2.is_workday(startDate)
NameError: name 'startDate' is not defined

this is because 'is_workday' is a static method and nothing gets passed in automatically.
you instead need to pass in the instance and the attribute. 
also note that the static method can be accessed by calling the class or the class instance

"""
print(emp_2.startDate)
#emp_2.is_workday(startDate)
#Employee.is_workday(startDate)
print(emp_2.is_workday(emp_2.startDate))
print(Employee.is_workday(emp_2.startDate))