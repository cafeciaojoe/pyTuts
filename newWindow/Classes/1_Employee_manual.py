class Employee_manual:
    "add pass to avoid having to define class attributes, methods and variables"
    pass

"creating instances of the employee class"
emp_1 = Employee.manual()
emp_2 = Employee.manual()

"you can see they take up different spots in the memory"
print(emp_1)
print(emp_1)

"now we will create some instance variables"

emp_1.first = 'corey'
emp_1.last = 'schafer'
emp_1.email = 'corey.chafer@company.com'
emp_1.pay = 50000

emp_2.first = 'joe'
emp_2.last = 'la d'
emp_2.email = 'joe.d@company.com'
emp_2.pay = 40000

print(emp_1.email)
print(emp_2.email)


