"""Attribute is data associated with a class
 Method is a function that is associated with a class"""

class Employee_manual:

    def banana(self):
        print('banana')
    "add pass to avoid having to define class attributes and methods"
    pass

"creating instances of the employee class"
emp_1 = Employee_manual()
emp_2 = Employee_manual()

"you can see they take up different spots in the memory"
print(emp_1)
print(emp_1)

"""instance variable are unique to the instance of a class. when you create an instance 
variable, it is formatted as so 'class.variableName = whatever' 
"""

#Qhow can you tell the difference between an instance variable and a method?

"""Well the method is a function to it will have a pair of parenthesis following it"""

""""""

emp_1.first = 'corey'
emp_1.last = 'schafer'
emp_1.email = 'corey.chafer@company.com'
emp_1.banana()
emp_1.pay = 50000

emp_2.first = 'joe'
emp_2.last = 'la d'
emp_2.email = 'joe.d@company.com'
emp_2.pay = 40000

print(emp_1.email)
print(emp_2.email)

"""what about a variable that is defined inside a class? aka instance variable? 
see next py file. """