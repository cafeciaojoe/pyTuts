import time

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

size = 20
color = (0.0, 1.0, 0.0, 0.5)
pos = np.array([10,10,10])

#pxMode True and t.start below (400) producing some funny point at the origin
sp1 = gl.GLScatterPlotItem(pos=pos, size=size, color = color, pxMode = True)
w.addItem(sp1)


axisitem = gl.GLAxisItem()
w.addItem(axisitem)

def updateData():
    xd =1*np.random.random()
    yd =1*np.random.random()
    zd =1*np.random.random()
    new_pos = np.array([xd,yd,zd])
    print(new_pos)
    sp1.setData(pos=new_pos)

## Start a timer to rapidly update the plot in spw
t = QtCore.QTimer()
t.timeout.connect(updateData)
t.start(400)


if __name__ == '__main__':
    pg.exec()
    print("see ya")