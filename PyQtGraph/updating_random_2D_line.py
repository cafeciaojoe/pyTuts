import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets

app = pg.mkQApp()
mw = QtWidgets.QMainWindow()
mw.setWindowTitle('pyqtgraph example: PlotWidget')
mw.resize(800, 800)
cw = QtWidgets.QWidget()
mw.setCentralWidget(cw)
l = QtWidgets.QVBoxLayout()
cw.setLayout(l)

pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
l.addWidget(pw)

mw.show()

## Create an empty plot curve to be filled later, set its pen (color)
p1 = pw.plot()
p1.setPen((200, 200, 100))

pw.setXRange(0, 10)
pw.setYRange(0, 10)

def rand(n):
    x_data = 10*np.random.random(n)
    y_data = 10*np.random.random(n)
    return x_data, y_data

def updateData():
    yd, xd = rand(5)
    p1.setData(y=yd, x=xd)

## Start a timer to rapidly update the plot in pw
t = QtCore.QTimer()
t.timeout.connect(updateData)
t.start(5)
#updateData()


if __name__ == '__main__':
    pg.exec()