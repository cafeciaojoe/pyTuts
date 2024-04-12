#https://www.youtube.com/watch?v=k1Z-55lHNm8&list=PL2OQ8odJIDfPU67ML2k-ldvgtISoxJE8b&index=1

import numpy as np
#import QtWidgets module
from PyQt5 import QtWidgets

from vispy.scene import SceneCanvas, visuals
from vispy.app import use_app

IMAGE_SHAPE = (600, 800)  # (height, width)
CANVAS_SIZE = (800, 600)  # (width, height)
NUM_LINE_POINTS = 200

COLORMAP_CHOICES = ["viridis", "reds", "blues"]
LINE_COLOR_CHOICES = ["black", "red", "blue"]


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
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

        # an instance of the canvasWrapper() will go on the right, as it was added 2nd
        self._canvas_wrapper = CanvasWrapper()
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
        self.line = visuals.Line(
            line_data,
            # apply a parent child relationship to self.view_self.view_top (defined above) and the image itself.
            parent=self.view_bot.scene,
            color=LINE_COLOR_CHOICES[0])
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
        self.line.set_data(color=color)


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

# if __name__ makes sure that this code can only be run as a script.
# standard python practice. esp if this is part of a big package and you dont want
# it to imported into something else.
if __name__ == "__main__":
    #this vispy helper method puts a wrapper around pyqt5 and lets you do all the pyqt5 stuff
    app = use_app("pyqt5")
    # manually create the qt5 application.
    app.create()

    #showing the secenecanvas (it has been moved to its own class called MyMainWindow
    win = MyMainWindow()
    win.show()

    #assign an instance of the canvas wrapper class to "canvas_wrapper", but just no qt5
    canvas_wrapper = CanvasWrapper()
    #self.canvas which is assigned to scene canvas, has the show() method inside which you are calling below
    canvas_wrapper.canvas.show()

    # start the qt5 event loop and handle all the events
    app.run()