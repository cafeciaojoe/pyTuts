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

size = 5
color = (0.0, 1.0, 0.0, 0.5)

#pxMode True producing some funny points at the origin, especially if you immediateley move the camera after the window opens
sp1 = gl.GLScatterPlotItem(size=size, color = color, pxMode=False)
w.addItem(sp1)

axisitem = gl.GLAxisItem()
w.addItem(axisitem)

def updateData(pos_dict):
    pos=pos_dict.get("marker")
    print('1',pos)
    sp1.setData(pos=pos)

## Start a timer to rapidly update the plot in spw
# t = QtCore.QTimer()
# t.timeout.connect(updateData)
# t.start(50)

class DataSource(QtCore.QObject):
    """Object representing a complex data producer."""
    new_data = QtCore.pyqtSignal(dict)
    finished = QtCore.pyqtSignal()

    def __init__(self, num_iterations=100, parent=None):
        super().__init__(parent)
        self._should_end = False
        self._count = 0
        self._num_iters = num_iterations
        self._marker_data = [0,0,0]


    def run_data_creation(self):
        if self._should_end or self._count >= self._num_iters:
            print("Data source finishing")
            self.finished.emit()
            return

        time.sleep(.1)
        marker_data = self._update_marker_data(self._count)
        self._count += 1

        data_dict = {
            "marker": marker_data,
        }
        self.new_data.emit(data_dict)
        QtCore.QTimer.singleShot(0,self.run_data_creation)

    def _update_marker_data(self, count):
        self._marker_data[0] = np.random.random()
        self._marker_data[1] = np.random.random()
        self._marker_data[2] = np.random.random()
        print('0',self._marker_data)
        return self._marker_data.copy()

    def stop_data(self):
        print("Data source is quitting...")
        self._should_end = True


if __name__ == '__main__':

    data_thread = QtCore.QThread(parent=w)
    data_source = DataSource()
    data_source.moveToThread(data_thread)

    # update the visualization when there is new data
    data_source.new_data.connect(updateData)
    # start data generation when the thread is started
    data_thread.started.connect(data_source.run_data_creation)
    # if the data source finishes before the window is closed, kill the thread
    # to clean up resources
    data_source.finished.connect(data_thread.quit)

    # when the thread has ended, delete the data source from memory
    data_thread.finished.connect(data_source.deleteLater)

    data_thread.start()

    pg.exec()

    # if the window is closed, tell the data source to stop
    #w.closing.connect(data_source.stop_data)
    data_source.stop_data()

    print("Waiting for data source to close gracefully...")
    data_thread.quit()
    data_thread.wait(5000)
    print("see ya ")