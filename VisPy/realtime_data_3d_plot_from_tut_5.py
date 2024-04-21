# https://www.youtube.com/watch?v=k1Z-55lHNm8&list=PL2OQ8odJIDfPU67ML2k-ldvgtISoxJE8b&index=5
# https://vispy.org/gallery/scene/realtime_data/ex03c_data_sources_threaded_events.html


import time  # noqa
import numpy as np
from math import sin, pi

from PyQt5 import QtWidgets, QtCore

from vispy.scene import SceneCanvas, visuals
from vispy.app import use_app, Timer

IMAGE_SHAPE = (600, 800)  # (height, width)
CANVAS_SIZE = (800, 600)  # (width, height)
NUM_LINE_POINTS = 200

COLORMAP_CHOICES = ["viridis", "reds", "blues"]
LINE_COLOR_CHOICES = ["black", "red", "blue"]


class MyMainWindow(QtWidgets.QMainWindow):

    # a signal what wil later be used when closing the GUI
    closing = QtCore.pyqtSignal()

    def __init__(self, canvas_wrapper, *args, **kwargs):
        #QMainWindow is a subclass (aka child class) so we are going to call the init method on the base class
        #https://stackoverflow.com/questions/19205916/how-to-call-base-classs-init-method-from-the-child-class
        super().__init__(*args, **kwargs)

        #set up a central widget to hold all the other widgets.
        central_widget = QtWidgets.QWidget()
        #creating "main_layout" which is the the classic HBox Layout here.
        main_layout = QtWidgets.QHBoxLayout()
        #the qt controls, (which are a couple of drop down menus,define in the controls class elswher ein the code) will go on the left because they have been added first
        self._controls = Controls()
        main_layout.addWidget(self._controls)

        # an instance of the canvasWrapper(), passed in from __main__ will go on the right, as it was added 2nd
        self._canvas_wrapper = canvas_wrapper
        # when we want to incorporate the vispy canvas into a larger application we use this scenecanvas native property
        main_layout.addWidget(self._canvas_wrapper.canvas.native)

        # set this layout (main_layout) on the central widget
        central_widget.setLayout(main_layout)
        #  set the central widget on our main window.
        self.setCentralWidget(central_widget)

        self._connect_controls()

    # tell our controls to connect their signals (which get sent out when you e.g. use the dropdown box)
    # to our CanvasWrapper() methods (set_image_colormap and set_line_color)
    def _connect_controls(self):
        # _controls.colormap_chooser is the Qcombobox object we made in the controls class
        # built into that class is the currentTextChanged signal, and all signals have a "connect" method
        # we need to provide a method to this signal to be called when it gets emitted (e.g. when the value in the combo box changes)
        # that method is self._canvas_wrapper.set_image_colormap
        # not we don't use the brackets because we dont want to call it when we set it up.
        self._controls.colormap_chooser.currentTextChanged.connect(self._canvas_wrapper.set_image_colormap)
        #same goes
        self._controls.line_color_chooser.currentTextChanged.connect(self._canvas_wrapper.set_line_color)

    # this needed because there no signal built into Qt that tell sus the window is closing.
    # this causes the .closing signal to emit when the GUI is closed.
    def closeEvent(self, event):
        print("Closing main Window!")
        self.closing.emit()
        return super().closeEvent(event)


class Controls(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # we will subclass this from qtwidget's "qwidget"
        # https://stackoverflow.com/questions/19205916/how-to-call-base-classs-init-method-from-the-child-class
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout()
        #adding a label for the drop down box
        self.colormap_label = QtWidgets.QLabel("Image Colormap:")
        layout.addWidget(self.colormap_label)
        # adding a label for the drop down box
        self.colormap_chooser = QtWidgets.QComboBox()
        self.colormap_chooser.addItems(COLORMAP_CHOICES)
        layout.addWidget(self.colormap_chooser)

        self.line_color_label = QtWidgets.QLabel("Line color:")
        layout.addWidget(self.line_color_label)
        self.line_color_chooser = QtWidgets.QComboBox()
        self.line_color_chooser.addItems(LINE_COLOR_CHOICES)
        layout.addWidget(self.line_color_chooser)

        layout.addStretch(1)
        self.setLayout(layout)


class CanvasWrapper:
    def __init__(self):
        # create a canvas
        self.canvas = SceneCanvas(size=CANVAS_SIZE)
        # adding a grid widget to the canvas so you can split it up like you want.
        self.grid = self.canvas.central_widget.add_grid()

        # adding the 1st view, in the 1st row, 1st column, background cyan
        self.view_top = self.grid.add_view(0, 0, bgcolor='cyan')
        # use the function to create some random image data (600 x 800 pixels)
        image_data = _generate_random_image_data(IMAGE_SHAPE)
        # create an image visual
        self.image = visuals.Image(
            image_data,
            # the texture format is a customisation on this image on how I want it ti interact with the GPU on the back end.
            texture_format="auto",
            # apply the viridis colour map
            cmap=COLORMAP_CHOICES[0],
            # apply a parent child relationship to self.view_top (defined above) and the image itself.
            parent=self.view_top.scene,
        )
        #apply a build in vispy camera called panzoom, allows click drag and mouse wheel zoom.
        self.view_top.camera = "panzoom"
        # set up the starting view port. by default vispy adds a buffer but here it perfectly matches.
        self.view_top.camera.set_range(x=(0, IMAGE_SHAPE[1]), y=(0, IMAGE_SHAPE[0]), margin=0)

        # adding the 2nd view, in the 2nd row, 1st column, background #c0c0c0
        self.view_bot = self.grid.add_view(1, 0, bgcolor='#c0c0c0')
        # use the function to create some random line data
        line_data = _generate_random_line_positions(NUM_LINE_POINTS)
        # create an line visual

        # self.line = visuals.Line(
        #     line_data,
        #     # apply a parent child relationship to self.view_self.view_top (defined above) and the image itself.
        #     parent=self.view_bot.scene,
        #     color=LINE_COLOR_CHOICES[0])
        self.line = visuals.Markers(
            pos=line_data,
            parent=self.view_bot.scene,
            edge_width = 5,
            face_color=LINE_COLOR_CHOICES[2])
        self.view_bot.camera = "panzoom"
        # out the entire line in the view.
        self.view_bot.camera.set_range(x=(0, NUM_LINE_POINTS), y=(0, 1))

    #this method changes the image colourmap. based on the information we get form the qt controls
    def set_image_colormap(self, cmap_name: str):
        print(f"Changing image colormap to {cmap_name}")
        # remember self.image is an instance of vispy visuals module (vispy.scene.visuals)
        # the cmap property of visuals is being set to a string
        self.image.cmap = cmap_name

    def set_line_color(self, color):
        print(f"Changing line color to {color}")
        # remember that self.line is an instance of the vispy visuals module (vispy.scene.visuals)
        # not a property this time but call the set_data() method from the visuals module
        self.line.set_data(face_color=color)

    # this is the 'slot' or the method that the new_data signal (defined at the top of the DataSource class)
    # but they are not connected yet. that is done in __main__
    def update_data(self, new_data_dict):
        print("Updating data...")
        # using the .set_data method from the scene.visuals class, which was assigned to self.image and self.line above.
        self.image.set_data(new_data_dict["image"])
        self.line.set_data(new_data_dict["line"])

def _generate_random_image_data(shape, dtype=np.float32):
    rng = np.random.default_rng()
    data = rng.random(shape, dtype=dtype)
    return data


def _generate_random_line_positions(num_points, dtype=np.float32):
    rng = np.random.default_rng()
    pos = np.empty((num_points, 2), dtype=np.float32)
    pos[:, 0] = np.arange(num_points)
    pos[:, 1] = rng.random((num_points,), dtype=dtype)
    return pos

# generates the live data for the vispy scene
# any object that emits a signal needs to be subclass of QObject, hence why QtCore.QObject is being subclassed.
class DataSource(QtCore.QObject):
    """Object representing a complex data producer."""
    # here is a new signal, what is passed to the QtCore.pyqtSignal class is the types of things that will be emitted from that signal .
    #in this case a dictionary of new data
    new_data = QtCore.pyqtSignal(dict)

    # the finished signal, later connected t "data_thread.quit, QtCore.Qt.DirectConnection" and "data_source.deleteLater"
    finished = QtCore.pyqtSignal()

    # limits the number of iteratiosn the data will be generated, the parent thing is just something that Pyqt needs to know...?
    def __init__(self, num_iterations=1000, parent=None):
        super().__init__(parent)

        # this is will be used  when the GUI is closed, to break the loop that generates the data
        self._should_end = False
        self._count = 0
        self._num_iters = num_iterations

        # this is the last bunch of data to be sent.
        self._image_data = _generate_random_image_data(IMAGE_SHAPE)
        self._line_data = _generate_random_line_positions(NUM_LINE_POINTS)

    # this function kind of iterates the whole pyQt GUI update cycle.
    # passing in event timer,
    def run_data_creation(self):
        if self._should_end or self._count >= self._num_iters:
            print("Data source is finishing")
            self.finished.emit()
            return

        # Uncomment to mimic a long-running computation
        time.sleep(.1)
        image_data = self._update_image_data(self._count)
        line_data = self._update_line_data(self._count)
        self._count += 1

        # Create the dictionary to emit. with our new data
        data_dict = {
            "image": image_data,
            "line": line_data,
        }

        # emit the signal (a dictionary in this case), call the emit method from QtCore.pyqtSignal
        self.new_data.emit(data_dict)

        # this method means, "with no delay (0), add run_data_collection to the background thread event loop"
        # A special method ,
        QtCore.QTimer.singleShot(0, self.run_data_creation)

    # _update_image_data and _update_line_data emulate new data coming in from an external source
    def _update_image_data(self, count):
        img_count = count % IMAGE_SHAPE[1]
        self._image_data[:, img_count] = img_count / IMAGE_SHAPE[1]
        rdata_shape = (IMAGE_SHAPE[0], IMAGE_SHAPE[1] - img_count - 1)
        self._image_data[:, img_count + 1:] = _generate_random_image_data(rdata_shape)
        #using the .copy() method from numpy to send the data, any other methods that uses this signal, cannot corrupt the results.
        # important because in multi thread scripts you dont want things to become mixedup and out of sync.
        return self._image_data.copy()

    def _update_line_data(self, count):
        # the numpy roll method to shift over everything in the array
        self._line_data[:, 1] = np.roll(self._line_data[:, 1], -1)
        self._line_data[-1, 1] = abs(sin((count / self._num_iters) * 16 * pi))
        return self._line_data

    # this function is called when the .closing signal is called
    def stop_data(self):
        print("Data source is quitting...")
        self._should_end = True

# if __name__ makes sure that this code can only be run as a script.
# standard python practice. esp if this is part of a big package and you dont want
# it to imported into something else.
if __name__ == "__main__":
    #this vispy helper method puts a wrapper around pyqt5 and lets you do all the pyqt5 stuff
    app = use_app("pyqt5")
    # manually create the qt5 application.
    app.create()

    # create an instance of the data_source class
    data_source = DataSource()
    # it is celaner to create the canvas wrapper instance here and pass it into MyMainWindow
    # it prevents problems with property attribute access
    canvas_wrapper = CanvasWrapper()

    #showing the secenecanvas (it has been moved to its own class called MyMainWindow
    win = MyMainWindow(canvas_wrapper)

    #thread handler for the data creation.
    # parent=win means if a parent is destroyed (ie a window is closed, the children, the data_thread needs to be destroyed also.
    data_thread = QtCore.QThread(parent=win)

    # create an instance of the data_source class
    data_source = DataSource()

    # data_source is a Qobject (because QtCore.QObject was subclassed when DataSource was created)
    # so .moveToThread is a method you can call on all QObjects
    # this moves data_source (an instance of DataSource) to the data_thread
    data_source.moveToThread(data_thread)

    # access new_data by attribute access,
    # connecting the new_data signal (from the DataSource class)
    # with the update_data slot (from the canvas wrapper class, but it will have been passed into MyMainWindow by the time it is called)
    data_source.new_data.connect(canvas_wrapper.update_data)

    # .started is a signal that comes with the QtCore.QThread object,
    # this says the thread has started and is ready to compute!
    # we are going to connect this signal to the run_data_creation method
    # which will start data generation when the thread is started
    data_thread.started.connect(data_source.run_data_creation)

    # connect a new "finish" signal on our data_source, to our data thread
    # QtCore.Qt.DirectConnection still needs to be kept else I get the following error.
    # WARNING: QThread: Destroyed while thread is still running
    data_source.finished.connect(data_thread.quit, QtCore.Qt.DirectConnection)

    # if the window is closed, tell the data source to stop
    win.closing.connect(data_source.stop_data)

    # when the thread has ended, delete the data source from memory
    data_thread.finished.connect(data_source.deleteLater)

    # .show is actually a method from SceneCanvas but that was created in CanvasWrapper, which was passed into MyMainWindow, which was assigned to win
    win.show()

    # this will start a thread, and once it has set up, it emits a signal (remember we used the .started method)
    # this signal will start the run_data_creation
    data_thread.start()

    ##assign an instance of the canvas wrapper class to "canvas_wrapper", but just no qt5
    #canvas_wrapper = CanvasWrapper()
    ##self.canvas which is assigned to scene canvas, has the show() method inside which you are calling below
    #canvas_wrapper.canvas.show()

    # start the qt5 event loop and handle all the events
    app.run()

    # when you close your GUI window the script will return to here,
    # this .wait() method is from QtCore.QThread
    print("Waiting for data source to close gracefully...")
    data_thread.wait(5000)