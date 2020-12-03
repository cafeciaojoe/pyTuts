import sys
from PyQt5 import QtWidgets


"passing the Qwidget class into another class because it is imported?"

class Window(QtWidgets.QWidget):

    def __init__(self):
        "call the constructor (the__init__) of the parent class, in this cse it is QWidget"
        super().__init__()

        self.init_ui()

    def init_ui(self):
        "can also use setText later on to define the name of the button or label"
        self.b = QtWidgets.QPushButton('push me')
        self.l = QtWidgets.QLabel('not been clicked')

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.l)
        h_box.addStretch()

        "v_box is an instance of the class QVBoxLayout()"
        v_box = QtWidgets.QVBoxLayout()
        "which is hy you can perform all of these QWidget methods to it"
        v_box.addWidget(self.b)
        v_box.addLayout(h_box)

        "class is a QWidget, defined in v_box"
        self.setLayout(v_box)
        self.setWindowTitle('PyQt5 Lesson 5')

        "ceating a connection between the signal (clicked) and the slot (self)"
        self.b.clicked.connect(self.btn_click)

        self.show()

    def btn_click(self):
        self.l.setText('i have been clicked')


app = QtWidgets.QApplication(sys.argv)
"why does creating an instance of this class make it run in a loop"
a_window = Window()
sys.exit(app.exec())