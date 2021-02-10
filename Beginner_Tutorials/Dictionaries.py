"""
Dictionaries
https://www.youtube.com/watch?v=daefaLgNkw0
"""

student = {'name': 'John', 'age': 25, 'courses': ['math','CompSci']}

print(student['name'])
"""KerError is the error type you get if you get the key of the dictionary wrong"""

"""if you use .get() method, it returns None, unless you specify what you want returned as the second argument"""
print(student.get('name'))
print(student.get('phone','Not Found'))

"""we can add values to a dictionary:"""
student['phone'] = '555-555'
print(student)

"""you can update the values of existing keys:"""
student['name'] = 'Jane'
print(student)


"""you can update multiple keys at the same time"""
student.update({'name': 'Suresh', 'age': 22, 'phone': '888-888'})
print(student)

print()
"""you can delete values"""
del student['age']
print(student)

print()
"""you can retrieve the length, keys or values"""
print(student.keys())
print(student.values())
print(student.items())
x = student.items()
# Items return a dict_items type, which is essentially a list of tuples

print()
"""you can loop through these key values like so"""
for key, value in student.items():
    print(key, value)



class HTTYD():

    def __init__(self):
        self.hi = {'_cf': Position(0,0,0)}

    def main(self):
        _cf = self.hi['_cf']
        print(_cf.x)

class Position:
    def __init__(self, x, y, z, roll=0.0, pitch=0.0, yaw=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw


s = HTTYD()
s.main()

