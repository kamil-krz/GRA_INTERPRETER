import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QTextBlockFormat, QTextCursor, QTextFormat, QPainter
from PyQt5.QtCore import QRectF, QTimer, Qt, QRect
from PyQt5.QtWidgets import *
from Klasy import *
from ThreadWithExc import *
from gui_nasze import Ui_Form
import os
import Klasy_uzytkowe



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
        self.obrazki = {'player': QImage("graphics/player.jpg"), 'czolg': QImage("graphics/czolg.jpg"), 'sciana_zniszczalna': QImage("graphics/sciana_zniszczalna.jpg"), 'sciana_niezniszczalna': QImage("graphics/sciana_niezniszczalna.jpg"), }

        for root, dirs, files in os.walk('maps'):
            for i in files:
                if ".dat" in i:
                    i = i.replace(".dat","")
                    self.combo_plansze.addItem(i)
        self.scene = QGraphicsScene()
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)


        self.MPM=10        #moves per minute

        self.threads_list = []
        self.player = None
        self.player_thread=None
        self.kod_result = ''

        self.timer = QTimer(self)
        self.timer_action = QTimer(self)
        self.plansza.setScene(self.scene)
        self.ActionEvent = threading.Event()
        self.krokowaEvent = threading.Event()

        self.timer.timeout.connect(self.latanie)
        self.timer_action.timeout.connect(self.action)
        self.b_start.clicked.connect(self.start)
        self.b_reset.clicked.connect(self.reset)
        self.horizontalSlider.valueChanged.connect(self.suwak)
        self.combo_plansze.currentIndexChanged.connect(self.reset)
        self.b_help.clicked.connect(self.help)
        self.b_pause.clicked.connect(self.pauza)

        self.suwak()
        self.laduj_plansze("maps/"+str(self.combo_plansze.currentText()) + ".dat")



    def laduj_plansze(self,nazwa):
        file = open(nazwa)
        for i, line in enumerate(file):
            if i>=20:
                break
            for j in range(0, 20):
                if line[j] == ' ':
                    self.scene.addItem(kafelek(xy=(j, i), typ='chodnik', obrazki=self.obrazki))
                if line[j] == '#':
                    self.scene.addItem(kafelek(xy=(j, i), typ='sciana_nzn', obrazki=self.obrazki))
                if line[j] == '*':
                    self.scene.addItem(kafelek(xy=(j, i), typ='sciana_zn', obrazki=self.obrazki))
                if line[j] == 'P':
                    self.player=player(xy=(j, i), obrazki=self.obrazki, scene=self.scene)
                    self.scene.addItem(self.player)
                    self.scene.addItem(kafelek(xy=(j, i), typ='chodnik', obrazki=self.obrazki))
                if line[j] == '<':
                    self.scene.addItem(czolg(xy=(j, i), dir=180, obrazki=self.obrazki, type='random', scene=self.scene))
                    self.scene.addItem(kafelek(xy=(j, i), typ='chodnik', obrazki=self.obrazki))
                if line[j] == '>':
                    self.scene.addItem(czolg(xy=(j, i), dir=0, obrazki=self.obrazki, type='random', scene=self.scene))
                    self.scene.addItem(kafelek(xy=(j, i), typ='chodnik', obrazki=self.obrazki))
                if line[j] == '^':
                    self.scene.addItem(czolg(xy=(j, i), dir=90, obrazki=self.obrazki, type='random', scene=self.scene))
                    self.scene.addItem(kafelek(xy=(j, i), typ='chodnik', obrazki=self.obrazki))
                if line[j] == 'v':
                    self.scene.addItem(czolg(xy=(j, i), dir=270, obrazki=self.obrazki, type='prosto', scene=self.scene))
                    self.scene.addItem(kafelek(xy=(j, i), typ='chodnik', obrazki=self.obrazki))

        for i in self.scene.items():
            if type(i) != kafelek:
                i.setZValue(0.5)



    def action(self):
        self.ActionEvent.set()
        if not self.player_thread.isAlive():
            self.pauza()
            self.b_pause.setEnabled(False)
        self.l_hp.setText("HP:" + str(self.player.hp))
        for j in range(0, len(self.textBox.toPlainText().splitlines())):
            if j == self.player.licznik:
                format = QTextBlockFormat()
                format.setBackground(Qt.cyan)
            else:
                format = QTextBlockFormat()
                format.setBackground(Qt.white)
            self.setLineFormat(j, format)
        if self.player.hp <= 0:
            for t in self.threads_list:
                if t.getName() == 'player_thread':
                    if t.isAlive():
                        t.raiseExc(Exception)
                        time.sleep(0.1)
        self.konsola.setText(self.player.result)


    def start(self):
        self.suwak()
        self.timer.start(int(60*1000/self.MPM/50))
        self.timer_action.start(int(60*1000/self.MPM))
        self.krokowaEvent.set()

        kod = self.textBox.toPlainText()
        for idx,item in enumerate(self.scene.items()):
            if type(item)==player and (self.player_thread == None or not self.player_thread.isAlive()):
                self.player_thread = ThreadWithExc(name='player_thread',
                     target=item.run,
                     args=(kod, self.ActionEvent, self.krokowaEvent,))

                self.threads_list.append(self.player_thread)
            elif type(item)==czolg:
                t = ThreadWithExc(name='czolg_'+str(idx),
                                     target=item.go_AI,
                                     args=(self.ActionEvent,))
                self.threads_list.append(t)
        self.b_pause.setEnabled(True)
        self.combo_plansze.setEnabled(False)
        self.b_start.setEnabled(False)
        self.textBox.setEnabled(False)

        for t in self.threads_list:
            t.daemon = True
            t.start()


    def reset(self):
        self.b_pause.setEnabled(False)
        self.b_start.setEnabled(True)
        self.combo_plansze.setEnabled(True)
        self.konsola.clear()
        self.textBox.setEnabled(True)

        for j in range(0, len(self.textBox.toPlainText().splitlines())):
            format = QTextBlockFormat()
            format.setBackground(Qt.white)
            self.setLineFormat(j, format)

       # self.krokowaEvent.set()



       # DZIALAJACY RESET
        for t in self.threads_list:
            if t.isAlive():
                t.raiseExc(Exception)
                time.sleep(0.1)
        self.threads_list=[]
        self.timer.stop()
        self.timer_action.stop()
        self.scene.clear()
        self.laduj_plansze("maps/"+str(self.combo_plansze.currentText()) + ".dat")

    def pauza(self):
        for t in self.threads_list:
            if t.isAlive() and t != self.player_thread:
                t.raiseExc(Exception)
                time.sleep(0.1)
        self.threads_list=[]
        self.timer_action.stop()
        self.krokowaEvent.clear()
        time.sleep(int(60*1000/self.MPM/20)/100)
        self.timer.stop()
        self.b_start.setEnabled(True)
        self.b_pause.setEnabled(False)



    def latanie(self):
        for i in self.scene.items():
            if type(i) == pocisk:
                i.lot()

        # self.scene.addItem(pocisk())
        self.scene.update()

    def setLineFormat(self, lineNumber, format):
        cursor = QTextCursor(self.textBox.document().findBlockByNumber(lineNumber))
        cursor.setBlockFormat(format)


    def suwak(self):
        self.MPM = self.horizontalSlider.value()
        self.l_mpm.setText(str(self.horizontalSlider.value()))
        self.timer.setInterval(int(60*1000/self.MPM/50))
        self.timer_action.setInterval(int(60*1000/self.MPM))


    def help(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Dostępne polecenia klasy gracz: ")
        msg.setInformativeText("gracz.jedz(liczba_pol) - jazda o liczbę pol - domyślnie +1 \n \n"
                               "gracz.obrot_prawo() - obrot zgodnie z ruchem wskazowek zegara \n \n"
                               "gracz.obrot_lewo() - obrot przeciwnie do ruchu wskazowek zegara \n \n"
                               "gracz.strzal() - wystrzelenie pocisku \n \n"
                               "gracz.radar(kierunek) - skanowanie w okreslonym kierunku - domyślnie przód \n \n"
                               "Radar zwraca (odleglosc, typ_przeszkody) \n"
                               "Dostępne typy przeszkód: \n"
                               "sciana_nzn - ściana nieziszczalna \n"
                               "sciana_zn - ściana zniszczalna \n"
                               "czolg - przeciwnik \n")
        msg.setWindowTitle("HELP")
        msg.setStandardButtons(QMessageBox.Close)

        retval = msg.exec_()



    # def closeEvent(self, event):
    #     pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyForm()
    window.show()
    sys.exit(app.exec_())



