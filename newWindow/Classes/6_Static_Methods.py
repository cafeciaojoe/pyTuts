class Employee:

    num_of_emps = 0
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
    the instance into the function. ir you do not need to use any variables or 
    functions in the class. BUT the function is related to the class so we want
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

emp_1 = Employee('Corey', 'Schafer', 50000)
emp_2 = Employee('Joe', 'La D', 40000)



import datetime
start_date = datetime.date(2016,7,11)

"""now you still have to use Employee. because the static method is still
part of the Employee class, but the Employee __init__ is not run and you 
do not have a new instance of this class proof below as it is just
a simple ol bool"""
print(Employee.is_workday(start_date))

proof = Employee.is_workday(start_date)
print(type(proof))