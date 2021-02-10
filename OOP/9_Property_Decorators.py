class Worker:

    def __init__(self,first,last):
        self.first = first
        self.last = last
        self.email = first + '.' + last + '@email.com'

    def wholeName(self):
        return '{} {}'.format(self.first,self.last)

worker_1 = Worker('John', 'Smith')

"""
PROBLEM
in any given instance,
when you change the attribute 'self.first' the 'self.email' attribute does not change
because it is created in the init method using the first values for those attributes.
for example if a worker changed their name to jim, the email would remain the same 
just run these three lines and you will see the email did not change"""

worker_1.first = 'jim'

print(worker_1.first)
print(worker_1.email)
print(worker_1.wholeName())

"""we could create an email method 'def email()' but the problem with this is that it could break
the code for everyone who is sing the employee class and have hundress of employee emails
generated from the __init__ method called for each instance of Employee.

"""

class Employee:

    def __init__(self,first,last):
        self.first = first
        self.last = last

    """ so the property decorator reclassifies the method as a property of the class
    that way you HAVE TO access it like a an attribute. ie you cannot use () when calling it.
    If we did not have the @property decorator you would need to call the email as a mehtod
    print(emp_1.email())
    """
    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)

    """
    so now we are going to change the full name method to a property so we can 
    also treat it like an attribute.
    """
    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    """
    now that we are treating the fullname method as attribute we can also write code that lets
    you set it like an attribute using whats called a setter. right now, if you try to define this
    property above without a setter, you will get an error. 
    so we use the @methodName.setter decorator to do this.
    
    in the past, to change (set) an attribute of a class you would write
    emp_1.first = 'jim' 
    and 'jim'; is literally assigned to the object emp_1.first
    
    but now even though we are treating these methods as attributes, they are still methods
    and can perform some additional functionality for us when we set them 
    NOTE - the function must be the same name as it's @property counterpart
    """
    @fullname.setter
    def fullname(self, name):
        print('the setter has been called')
        first, last = name.split(' ')
        self.first = first
        self.last = last

    """
    again, now that we are treating the fullname method as attribute we can also write code that
    lets you delete it like an attribute. but with additional functionality when you do it. 
    """
    @fullname.deleter
    def fullname(self):
        print('the deleter has been called')
        self.first = None
        self.last = None

emp_1 = Employee('john','smith')
emp_2 = Employee('joe','blogs')

print('name before changing is', emp_1.email)

"""
so now when you try to ASSIGN something 'emp_1.fullname' (which is essentially a method that is called on an instance, 
somehting that you would not be allow to assign anything to otherwise),python will use the setter version of that method. 
"""
emp_1.fullname = 'corey schafer'


print('employeees first name is now',emp_1.first)
print('employeees first name is now',emp_1.email)
"""
remember fullname used to be a method you would call on an instance, emp_1.fullname()
"""
print('employeees full name is now',emp_1.fullname)

"""
so now the inbuilt funciton del (which usually comepletely removes whatever is after 'del'
ie it is no longer defined) will call the deleter version of the fullname method.
but the code we have written does something a little softer than that and just sets the
first and last names to none.   
"""
del emp_1.fullname

"""
you can see that the instance of the class still exisis
"""
print(emp_1)
print(emp_1.first)

"""
'del emp_1' will un assign it the class instance... your're fired!
 
 """






