"""Angela Sodemann https://youtu.be/tSy8QbcOSxc"""

import numpy as np

# sin in radians
# np.sin(3.14)

# Theta angle in degrees
T1 = 90
T2 = 0

# Theta in radians
T1 = (T1/180.0)*np.pi
T2 = (T2/180.0)*np.pi

R0_1 = [[np.cos(T1),-np.sin(T1),0],[np.sin(T1),np.cos(T1),0],[0,0,1]]
R1_2 = [[np.cos(T2),-np.sin(T2),0],[np.sin(T2),np.cos(T2),0],[0,0,1]]

R0_2 = np.dot(R0_1,R1_2)

print(R0_2)

