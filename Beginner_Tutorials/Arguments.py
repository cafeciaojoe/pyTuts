"""
ARGUMENTS
if you assign a value to an argument int he definition of a function or a calss, you wont need to do so when you call or
make an instance of it respectively. but you can still
"""
class Position:
    def __init__(self, x, y, z, roll=0.0, pitch=0.0, yaw=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

home = Position(0,0,0,100,200,300)

print(home.roll)

home.roll = 900

print(home.roll)
