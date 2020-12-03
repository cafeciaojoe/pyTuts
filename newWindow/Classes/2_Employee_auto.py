class Employee_auto:
    'self.first = first is the same as emp_1 = corey'

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

emp_1 = Employee_auto('Corey', 'Schafer', 50000)
emp_2 = Employee_auto('Joe', 'La D', 40000)

print(emp_1.email)
print(emp_2.email)