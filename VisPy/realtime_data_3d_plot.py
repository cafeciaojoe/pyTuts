import time
from math import sin, pi

import numpy as np
from PyQt5 import QtWidgets, QtCore

import vispy
from vispy.scene import SceneCanvas, visuals
from vispy.app import use_app

IMAGE_SHAPE = (600, 800)  # (height, width)
CANVAS_SIZE = (800, 600)  # (width, height)


COLORMAP_CHOICES = ["viridis", "reds", "blues"]
MARKER_COLOR_CHOICES = ["black", "red", "blue"]


class Controls(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout()
        self.colormap_label = QtWidgets.QLabel("Image Colormap:")
        layout.addWidget(self.colormap_label)
        self.colormap_chooser = QtWidgets.QComboBox()
        self.colormap_chooser.addItems(COLORMAP_CHOICES)
        layout.addWidget(self.colormap_chooser)

        self.marker_color_label = QtWidgets.QLabel("Marker color:")
        layout.addWidget(self.marker_color_label)
        self.marker_color_chooser = QtWidgets.QComboBox()
        self.marker_color_chooser.addItems(MARKER_COLOR_CHOICES)
        layout.addWidget(self.marker_color_chooser)

        layout.addStretch(1)
        self.setLayout(layout)


class CanvasWrapper:
    def __init__(self):
        self.canvas = SceneCanvas(size=CANVAS_SIZE)
        self.grid = self.canvas.central_widget.add_grid()

        self.view_top = self.grid.add_view(0, 0, bgcolor='cyan')
        image_data = _generate_random_image_data(IMAGE_SHAPE)
        self.image = visuals.Image(
            image_data,
            texture_format="auto",
            cmap=COLORMAP_CHOICES[0],
            parent=self.view_top.scene,
        )
        self.view_top.camera = "panzoom"
        self.view_top.camera.set_range(x=(0, IMAGE_SHAPE[1]), y=(0, IMAGE_SHAPE[0]), margin=0)

        self.view_bot = self.grid.add_view(1, 0, bgcolor='#c0c0c0')
        marker_data = _generate_random_marker_positions()
        self.marker = visuals.Markers(
            pos=marker_data,
            parent=self.view_bot.scene,
            face_color=MARKER_COLOR_CHOICES[0])
        self.view_bot.camera = vispy.scene.TurntableCamera(distance=10.0, center=(0.0, 0.0, 0.0))
        #self.view_bot.camera.set_range(x=(0, 0), y=(0, 0), z =(10, 10))

        plane_size = 10
        visuals.Plane(
            width=plane_size,
            height=plane_size,
            width_segments=plane_size,
            height_segments=plane_size,
            color=(0.5, 0.5, 0.5, 0.5),
            edge_color="gray",
            parent=self.view_bot.scene)

        self._addArrows(1, 0.02, 0.1, 0.1, self.view_bot.scene)

    def _addArrows(self, length, width, head_length, head_width, parent):
        # The Arrow visual in vispy does not seem to work very good,
        # draw arrows using lines instead.
        w = width / 2
        hw = head_width / 2
        base_len = length - head_length

        # X-axis
        visuals.LinePlot([
            [0, w, 0],
            [base_len, w, 0],
            [base_len, hw, 0],
            [length, 0, 0],
            [base_len, -hw, 0],
            [base_len, -w, 0],
            [0, -w, 0]],
            width=1.0, color='red', parent=parent, marker_size=0.0)

        # Y-axis
        visuals.LinePlot([
            [w, 0, 0],
            [w, base_len, 0],
            [hw, base_len, 0],
            [0, length, 0],
            [-hw, base_len, 0],
            [-w, base_len, 0],
            [-w, 0, 0]],
            width=1.0, color='green', parent=parent, marker_size=0.0)

        # Z-axis
        visuals.LinePlot([
            [0, w, 0],
            [0, w, base_len],
            [0, hw, base_len],
            [0, 0, length],
            [0, -hw, base_len],
            [0, -w, base_len],
            [0, -w, 0]],
            width=1.0, color='blue', parent=parent, marker_size=0.0)

    def set_image_colormap(self, cmap_name: str):
        print(f"Changing image colormap to {cmap_name}")
        self.image.cmap = cmap_name

    def set_marker_color(self, color: str):
        print(f"Changing marker color to {color}")
        self.marker.set_data(face_color=color)
        print(type(self.marker.set_data))

    def update_data(self, new_data_dict):
        print("Updating data...")
        self.image.set_data(new_data_dict["image"])
        self.marker.set_data(new_data_dict["marker"])


def _generate_random_image_data(shape, dtype=np.float32):
    rng = np.random.default_rng()
    data = rng.random(shape, dtype=dtype)
    return data

def _generate_random_marker_positions(dtype=np.float32):
    rng = np.random.default_rng()
    pos = np.empty((1, 3), dtype=np.float32)
    return pos


class MyMainWindow(QtWidgets.QMainWindow):
    closing = QtCore.pyqtSignal()

    def __init__(self, canvas_wrapper: CanvasWrapper, *args, **kwargs):
        super().__init__(*args, **kwargs)

        central_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QHBoxLayout()

        self._controls = Controls()
        main_layout.addWidget(self._controls)
        self._canvas_wrapper = canvas_wrapper
        main_layout.addWidget(self._canvas_wrapper.canvas.native)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self._connect_controls()

    def _connect_controls(self):
        self._controls.colormap_chooser.currentTextChanged.connect(self._canvas_wrapper.set_image_colormap)
        self._controls.marker_color_chooser.currentTextChanged.connect(self._canvas_wrapper.set_marker_color)

    def closeEvent(self, event):
        print("Closing main window!")
        self.closing.emit()
        return super().closeEvent(event)


class DataSource(QtCore.QObject):
    """Object representing a complex data producer."""
    new_data = QtCore.pyqtSignal(dict)
    finished = QtCore.pyqtSignal()

    def __init__(self, num_iterations=1000, parent=None):
        super().__init__(parent)
        self._should_end = False
        self._count = 0
        self._num_iters = num_iterations
        self._image_data = _generate_random_image_data(IMAGE_SHAPE)
        self._marker_data = _generate_random_marker_positions()

    def run_data_creation(self):
        if self._should_end or self._count >= self._num_iters:
            print("Data source finishing")
            self.finished.emit()
            return

        time.sleep(1)
        image_data = self._update_image_data(self._count)
        marker_data = self._update_marker_data(self._count)
        self._count += 1

        data_dict = {
            "image": image_data,
            "marker": marker_data,
        }
        self.new_data.emit(data_dict)
        QtCore.QTimer.singleShot(0, self.run_data_creation)

    def _update_image_data(self, count):
        img_count = count % IMAGE_SHAPE[1]
        self._image_data[:, img_count] = img_count / IMAGE_SHAPE[1]
        rdata_shape = (IMAGE_SHAPE[0], IMAGE_SHAPE[1] - img_count - 1)
        self._image_data[:, img_count + 1:] = _generate_random_image_data(rdata_shape)
        return self._image_data.copy()

    def _update_marker_data(self, count):
        # [:, 1] means slice the 2nd column out of self._marker_data
        #self._marker_data[:, 1] = np.roll(self._marker_data[:, 1], -1)
        #self._marker_data[-1, 1] = abs(sin((count / self._num_iters) * 16 * pi))
        rng = np.random.default_rng()
        self._marker_data[0,0] = rng.random(dtype=np.float32)
        self._marker_data[0,1] = rng.random(dtype=np.float32)
        self._marker_data[0,2] = rng.random(dtype=np.float32)
        return self._marker_data.copy()

    def stop_data(self):
        print("Data source is quitting...")
        self._should_end = True


if __name__ == "__main__":
    app = use_app("pyqt5")
    app.create()

    canvas_wrapper = CanvasWrapper()
    win = MyMainWindow(canvas_wrapper)
    data_thread = QtCore.QThread(parent=win)
    data_source = DataSource()
    data_source.moveToThread(data_thread)

    # update the visualization when there is new data
    data_source.new_data.connect(canvas_wrapper.update_data)
    # start data generation when the thread is started
    data_thread.started.connect(data_source.run_data_creation)
    # if the data source finishes before the window is closed, kill the thread
    # to clean up resources
    data_source.finished.connect(data_thread.quit)
    # if the window is closed, tell the data source to stop
    win.closing.connect(data_source.stop_data)
    # when the thread has ended, delete the data source from memory
    data_thread.finished.connect(data_source.deleteLater)

    win.show()
    data_thread.start()
    app.run()

    print("Waiting for data source to close gracefully...")
    data_thread.quit()
    data_thread.wait(5000)
