import sys
"no longer do we use the import line below"
#from PyQt5 import QtWidgets
"we use this one below instead as it means we no longer have to write QtWidgets before every subclass"
from PyQt5.QtWidgets import (QLineEdit, QSlider, QPushButton, QVBoxLayout, QApplication, QWidget)
from PyQt5.QtCore import Qt

"passing the Qwidget class into another class because it is imported?"

class Window(QWidget):

    def __init__(self):
        "call the constructor (the__init__) of the parent class, in this cse it is QWidget"
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.le = QLineEdit()
        self.b1 = QPushButton('Clear')
        self.b2 = QPushButton('Print')
        self.s1 = QSlider(Qt.Horizontal)
        self.s1.setMinimum(1)
        self.s1.setMaximum(99)
        self.s1.setValue(25)
        self.s1.setTickInterval(10)
        self.s1.setTickPosition(QSlider.TicksBelow)

        v_box = QVBoxLayout()
        v_box.addWidget(self.le)
        v_box.addWidget(self.b1)
        v_box.addWidget(self.b2)
        v_box.addWidget(self.s1)

        self.setLayout(v_box)
        self.setWindowTitle('PyQt5 Lesson 8')

        self.show()

    def btn


app = QApplication(sys.argv)
"why does creating an instance of this class make it run in a loop"
a_window = Window()
sys.exit(app.exec())