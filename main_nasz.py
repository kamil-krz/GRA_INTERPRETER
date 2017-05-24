import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from Klasy import *

from gui_nasze import Ui_Form

sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook


class MyForm(QMainWindow, Ui_Form):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)

        self.scene = QGraphicsScene()
        self.czolgi = czolg(xy=(10, 10))

        self.plansza.setScene(self.scene)
        self.scene.addItem(self.czolgi)

        self.b_start.clicked.connect(self.start)


    def start(self):
        self.czolgi.goto((12,12))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyForm()
    window.show()
    sys.exit(app.exec_())
    sys.exit(app.exec_())