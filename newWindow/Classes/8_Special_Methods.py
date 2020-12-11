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

    def __add__(self,other):
        return self.pay + other.pay

    """
    special methods, are what actutally gets called by python's built in arithmatic functions.
    such as + - len() str() 
    now when you define a special method in a class you are adding to that functionality of 
    the corresponding build in method. see below where the the def __add__ method is now 
    capable of adding the pay of 
    """


    # def __repr__(self):
    #     pass
    #
    # def __str__(self):
    #     pass

emp_1 = Employee('Corey', 'Schafer', 50000)
emp_2 = Employee('Joe', 'Blogs', 40000)

print(emp_1+emp_2)
print(2+2)


