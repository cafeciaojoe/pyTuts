def addition(a,b):
    return a + b

print(addition(10,10))

class Arithmatic():
    """
    the init function automatically sets up the variables a and b
    but it is not needed here. we can just set them up in def minus
    """
    def __init__(self,a,b):
        self.a = a
        self.b = b

    def minus(self,a,b):
        self.a = a
        self.b = b
        return a - b

"""
Just calling the class Arithmatic(a,b)  by itself will not do anything
you need to make an instance of it. 
"""
equation = Arithmatic(10,10)
""

print(equation.minus(10,9))


