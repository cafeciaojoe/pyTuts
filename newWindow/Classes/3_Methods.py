class Employee_auto:
    'self.first = first is the same as emp_1 = corey'

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

    "each method within in a class automaticall takes the instance as the first argument"
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

emp_1 = Employee_auto('Corey', 'Schafer', 50000)
emp_2 = Employee_auto('Joe', 'La D', 40000)

print(emp_1.email)
print(emp_2.email)

print(emp_1.fullname())
print(emp_2.fullname())

"leave out the () and you will get the methods location on memory not the return of that method"
print(emp_1.fullname)
"""
if you do not add self to the method then you will get and error. python passes in the instance name into the method 
automatically, so you need to use self to tell python that the instance name is coming, that it will be passed in"
"""
"""also notice that youc an call the class two ways. the first way 
automatially puts the instance in as the first argument
the second way you must specify the instance"""

print(emp_1.fullname())
print(Employee_auto.fullname(emp_1))

