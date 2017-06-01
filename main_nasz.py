import sys, psutil, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QRectF, QTimer, Qt
from PyQt5.QtWidgets import *
from Klasy import *


from gui_nasze import Ui_Form

sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook

plansza_id=1

class MyForm(QMainWindow, Ui_Form):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)
        self.obrazki = {'player': QImage("graphics/player.jpg"), 'czolg': QImage("graphics/czolg.jpg"), 'sciana_zniszczalna': QImage("graphics/sciana_zniszczalna.jpg"), 'sciana_niezniszczalna': QImage("graphics/sciana_niezniszczalna.jpg"), }
        self.scene = QGraphicsScene()
        self.czolgi = []
        self.player = None
        self.pociski = {}
        self.kafelki = {}
        file = open('plansza'+str(plansza_id)+'.txt')

        for i, line in enumerate(file):
            for j in range(0,20):
                if line[j] == ' ':
                    self.kafelki[(j,i)] = kafelek(xy=(j,i),typ = 'chodnik',obrazki = self.obrazki)
                if line[j] == '#':
                    self.kafelki[(j,i)] = kafelek(xy=(j,i), typ='sciana_nzn',obrazki = self.obrazki)
                if line[j] == '*':
                    self.kafelki[(j,i)] = kafelek(xy=(j,i), typ='sciana_zn',obrazki = self.obrazki)
                if line[j] == 'P':
                    self.player = player(xy=(j, i), obrazki = self.obrazki)
                    self.kafelki[(j, i)] = kafelek(xy=(j, i), typ='chodnik', obrazki=self.obrazki)
                if line[j] == '<':
                    self.czolgi.append(czolg(xy=(j, i), dir = 180, obrazki = self.obrazki))
                    self.kafelki[(j, i)] = kafelek(xy=(j, i), typ='chodnik', obrazki=self.obrazki)
                if line[j] == '>':
                    self.czolgi.append(czolg(xy=(j, i), dir=0, obrazki=self.obrazki))
                    self.kafelki[(j, i)] = kafelek(xy=(j, i), typ='chodnik', obrazki=self.obrazki)
                if line[j] == '^':
                    self.czolgi.append(czolg(xy=(j, i), dir=90, obrazki=self.obrazki))
                    self.kafelki[(j, i)] = kafelek(xy=(j, i), typ='chodnik', obrazki=self.obrazki)
                if line[j] == 'v':
                    self.czolgi.append(czolg(xy=(j, i), dir=270, obrazki=self.obrazki))
                    self.kafelki[(j, i)] = kafelek(xy=(j, i), typ='chodnik', obrazki=self.obrazki)




        self.timer = QTimer(self)

        self.plansza.setScene(self.scene)

        for xy in self.kafelki.keys():
                self.scene.addItem(self.kafelki[xy])
        self.scene.addItem(self.player)
        for i in self.czolgi:
            self.scene.addItem(i)


        self.timer.timeout.connect(self.latanie)
        self.b_start.clicked.connect(self.start)
        self.b_reset.clicked.connect(self.reset)


    def start(self):
        self.timer.start(10)
        kod = self.textBox.toPlainText()
        for i in self.player.run(self.kafelki, self.scene, kod):
            print(i)
    def reset(self):
        self.reset()

    def latanie(self):
        for i in self.scene.items():
            if type(i) == pocisk:
                i.lot()

    # def closeEvent(self, event):
    #     pass




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyForm()
    window.show()
    sys.exit(app.exec_())



