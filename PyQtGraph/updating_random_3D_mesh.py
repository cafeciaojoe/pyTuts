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
#sp1 = gl.GLScatterPlotItem(pos=pos, size=size, color = color, pxMode = True)
#w.addItem(sp1)


md = gl.MeshData.sphere(rows=10, cols=20, radius=.1)
# colors = np.random.random(size=(md.faceCount(), 4))
# colors[:,3] = 0.3
# colors[100:] = 0.0
colors = np.ones((md.faceCount(), 4), dtype=float)
colors[::2, 0] = 0
colors[:, 1] = np.linspace(0, 1, colors.shape[0])
md.setFaceColors(colors)
m4 = gl.GLMeshItem(meshdata=md, smooth=False)  # , shader='balloon')

w.addItem(m4)

# md = gl.MeshData.sphere(rows=4, cols=8, radius=.1)
# m4 = gl.GLMeshItem(meshdata=md, smooth=False, drawFaces=False, drawEdges=True, edgeColor=(1, 1, 1, 1))
# w.addItem(m4)

axisitem = gl.GLAxisItem()
w.addItem(axisitem)

def updateData():
    xp = 1
    yp = 0
    zp = 0
    new_pos = np.array([xp,yp,zp])
    print(new_pos)

    #print(new_pos)
    #sp1.setData(pos=new_pos)

    current_pos_4x4 = pg.transformToArray(m4.transform())
    #print(current_pos_4x4)
    #print(current_pos_4x4[(1,3)])
    xc = current_pos_4x4[(0,3)]
    yc = current_pos_4x4[(1,3)]
    zc = current_pos_4x4[(2,3)]
    current_pos = np.array([xc,yc,zc])
    print(current_pos)

    pos_d = np.subtract(new_pos,current_pos)

    m4.translate(pos_d[0],pos_d[1],pos_d[2])
    #not exatly sure how local works here.
    m4.rotate(10,1,1,1)

## Start a timer to rapidly update the plot in spw
t = QtCore.QTimer()
t.timeout.connect(updateData)
t.start(100)


if __name__ == '__main__':
    pg.exec()
    print("see ya")