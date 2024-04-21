import numpy as np

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph import functions as fn
from pyqtgraph.Qt import QtCore

app = pg.mkQApp("GLScatterPlotItem Example")
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
w.setCameraPosition(distance=20)

g = gl.GLGridItem()
w.addItem(g)

pos = [0,0,0]
size = 5
color = (0.0, 1.0, 0.0, 0.5)

print(pos)
sp1 = gl.GLScatterPlotItem(pos=pos, size=size, color = color, pxMode=False)

w.addItem(sp1)

def rand():
    x_data = 10*np.random.random(n)
    y_data = 10*np.random.random(n)
    z_data = 10*np.random.random(n)
    return x_data, y_data, z_data

def updateData():
    xd =10*np.random.random()
    yd =10*np.random.random()
    zd =10*np.random.random()
    sp1.setData(pos=[xd, yd, zd])

## Start a timer to rapidly update the plot in spw
t = QtCore.QTimer()
t.timeout.connect(updateData)
t.start(50)


if __name__ == '__main__':
    pg.exec()