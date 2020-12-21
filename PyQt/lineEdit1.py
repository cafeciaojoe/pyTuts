import sys
from PyQt5 import QtWidgets


"passing the Qwidget class into another class because it is imported?"

class Window(QtWidgets.QWidget):

    def __init__(self):
        "call the constructor (the__init__) of the parent class, in this cse it is QWidget"
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.le = QtWidgets.QLineEdit()
        self.b1 = QtWidgets.QPushButton('Clear')
        self.b2 = QtWidgets.QPushButton('Print')

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.le)
        v_box.addWidget(self.b1)
        v_box.addWidget(self.b2)

        self.setLayout(v_box)
        self.setWindowTitle('PyQt5 Lesson 6-7')

        "calling a functioin that will determine what as been clicked"
        self.b1.clicked.connect(self.btn_clk)
        self.b2.clicked.connect(self.btn_clk)

        self.show()

    def btn_clk(self):
        "Sometimes it is convenient to know which widget is the sender of a signal. For this, PyQt5 has the sender method. "
        sender = self.sender()
        print(sender.text())
        if sender.text() == 'Print':
            print(self.le.text())
        else:
            self.le.clear()

app = QtWidgets.QApplication(sys.argv)
"why does creating an instance of this class make it run in a loop"
a_window = Window()
sys.exit(app.exec())