import sys
from PyQt5 import QtWidgets, QtGui

def window():
    " sys.argv is the path to the python file "
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    "PASS W AS AN ARGUMENT TO TELL THE WIDGET TO PUT LABEL IN THE WINDOW"
    l1 = QtWidgets.QLabel(w)
    l2 = QtWidgets.QLabel(w)
    l2.setPixmap(QtGui.QPixmap('globe.png'))
    l1.setText("hellow world")
    w.setWindowTitle('lesson 2')
    w.setGeometry(100,100,300,400)
    l1.move(130,20)
    w.show()
    "this will exit the python script but call execute the 'app' upon exit, creating a loop"
    sys.exit(app.exec_())

print(sys.argv[0])
window()