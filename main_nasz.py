from PyQt5.QtGui import QImage, QTextBlockFormat, QTextCursor, QTextFormat, QPainter
from PyQt5.QtCore import QRectF, QTimer, Qt, QRect
from PyQt5.QtWidgets import *
from Klasy import *
from ThreadWithExc import *
from gui_nasze import Ui_Form
import os




# sys._excepthook = sys.excepthook
# def exception_hook(exctype, value, traceback):
#     sys._excepthook(exctype, value, traceback)
#     sys.exit(1)
# sys.excepthook = exception_hook


class MyForm(QMainWindow, Ui_Form):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)

        for root, dirs, files in os.walk('maps'):
            for i in files:
                if ".map" in i:
                    i = i.replace(".map","")
                    self.combo_plansze.addItem(i)

        self.MPM=10        #moves per minute

        self.threads_list = []
        self.player_thread=None
        self.kod_result = ''
        self.aktualna_linia=0;

        self.timer = QTimer(self)
        self.timer_action = QTimer(self)

        self.ActionEvent = threading.Event()
        self.krokowaEvent = threading.Event()
        self.exitEvent = threading.Event()
        self.exitEvent.clear()

        self.timer.timeout.connect(self.latanie)
        self.timer_action.timeout.connect(self.action)
        self.b_start.clicked.connect(self.start)
        self.b_reset.clicked.connect(self.reset)
        self.horizontalSlider.valueChanged.connect(self.suwak)
        self.combo_plansze.currentIndexChanged.connect(self.reset)
        self.b_help.clicked.connect(self.help)
        self.b_pause.clicked.connect(self.pauza)

        self.suwak()
        self.map_init('plansza_0')




    def map_init(self,nazwa):
        self.map = map(nazwa=nazwa)
        self.scene=self.map.getScene()
        self.player=self.map.player
        self.plansza.setScene(self.scene)



    def action(self):
        self.ActionEvent.set()
        if  not self.player_thread==None and not self.player_thread.isAlive() :
            self.pauza()
            self.b_pause.setEnabled(False)
            self.b_start.setEnabled(False)
        self.l_hp.setText("HP:" + str(self.player.hp))

        if self.player.hp <= 0:
                    if self.player_thread.isAlive():
                        self.player_thread.raiseExc(Exception)

        self.konsola.setText(self.player.result)



    def start(self):
        self.suwak()
        self.timer.start(int(60*1000/self.MPM/50))
        self.timer_action.start(int(60*1000/self.MPM))
        self.krokowaEvent.set()
        self.exitEvent.set()


        kod = self.textBox.toPlainText()

        for idx,item in enumerate(self.scene.items()):
            if type(item)==player and (self.player_thread == None or not self.player_thread.isAlive()):
                self.player_thread = ThreadWithExc(name='player_thread',
                     target=item.run,
                     args=(kod, self.ActionEvent, self.krokowaEvent,self.exitEvent,))

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
        # self.konsola.clear()
        self.textBox.setEnabled(True)

        for j in range(0, len(self.textBox.toPlainText().splitlines())):
            format = QTextBlockFormat()
            format.setBackground(Qt.white)
            self.setLineFormat(j, format)



       # DZIALAJACY RESET
        for t in self.threads_list:
            if t.is_alive():
                t.raiseExc(SystemExit)
                time.sleep(0.1)
                pass
        self.threads_list=[]
        self.player_thread=None
        self.timer.stop()
        self.timer_action.stop()
        self.map_init(str(self.combo_plansze.currentText()))

    def pauza(self):
        for t in self.threads_list:
            if t.isAlive() and t != self.player_thread:
                t.raiseExc(Exception)
        self.threads_list=[]
        self.timer_action.stop()
        self.krokowaEvent.clear()
        self.timer.stop()
        self.b_start.setEnabled(True)
        self.b_pause.setEnabled(False)



    def latanie(self):
        self.krokowaEvent.set()
        self.malujLinie()
        for i in self.scene.items():
            if type(i) == pocisk:
                i.lot()

        self.scene.update()

    def malujLinie(self):
        format = QTextBlockFormat()
        format.setBackground(Qt.white)
        self.setLineFormat(self.aktualna_linia, format)
        self.aktualna_linia = self.player.licznik
        format = QTextBlockFormat()
        format.setBackground(Qt.cyan)
        self.setLineFormat(self.aktualna_linia, format)


    def setLineFormat(self, lineNumber, format):
        cursor = QTextCursor(self.textBox.document().findBlockByNumber(lineNumber))
        cursor.setBlockFormat(format)


    def suwak(self):
        self.exitEvent.clear()
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
                               "czolg - przeciwnik \n"
                               "pocisk \n")
        msg.setWindowTitle("HELP")
        msg.setStandardButtons(QMessageBox.Close)

        retval = msg.exec_()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyForm()
    window.show()
    sys.exit(app.exec_())



