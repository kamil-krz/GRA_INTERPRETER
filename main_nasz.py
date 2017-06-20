import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QRectF, QTimer, Qt
from PyQt5.QtWidgets import *
from Klasy import *
from ThreadWithExc import *
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
        self.obrazki = {'player': QImage("graphics/player.jpg"), 'czolg': QImage("graphics/czolg.jpg"), 'sciana_zniszczalna': QImage("graphics/sciana_zniszczalna.jpg"), 'sciana_niezniszczalna': QImage("graphics/sciana_niezniszczalna.jpg"), }
        self.scene = QGraphicsScene()
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)


        self.MPM=120        #moves per minute
        self.threads_list = []
        self.player=None
        self.player_thread=None

        self.timer = QTimer(self)
        self.timer_action = QTimer(self)
        self.plansza.setScene(self.scene)
        self.ActionEvent = threading.Event()
        self.krokowaEvent = threading.Event()

        self.timer.timeout.connect(self.latanie)
        self.timer_action.timeout.connect(self.action)
        self.b_start.clicked.connect(self.start)
        self.b_reset.clicked.connect(self.reset)

        self.laduj_plansze('plansza1.txt')

    def laduj_plansze(self,nazwa):
        file = open(nazwa)
        for i, line in enumerate(file):
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
                    self.scene.addItem(czolg(xy=(j, i), dir=180, obrazki=self.obrazki, type='prosto', scene=self.scene))
                    self.scene.addItem(kafelek(xy=(j, i), typ='chodnik', obrazki=self.obrazki))
                if line[j] == '>':
                    self.scene.addItem(czolg(xy=(j, i), dir=0, obrazki=self.obrazki, type='prosto', scene=self.scene))
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


    def start(self):
        self.timer.start(int(60*1000/self.MPM/20))
        self.timer_action.start(int(60*1000/self.MPM))

        kod = self.textBox.toPlainText()
        for idx,item in enumerate(self.scene.items()):
            if type(item)==player:
                self.player_thread = ThreadWithExc(name='player_thread',
                     target=item.run,
                     args=(kod,self.ActionEvent,self.krokowaEvent,))


                self.threads_list.append(self.player_thread)
                # for i in self.player.run( kod):
                #     print(i)
            elif type(item)==czolg:
                t = ThreadWithExc(name='czolg_'+str(idx),
                                     target=item.go_AI,
                                     args=(self.ActionEvent,))
                self.threads_list.append(t)



        for t in self.threads_list:
            t.daemon = True
            t.start()


    def reset(self):

        self.krokowaEvent.set()



        # DZIALAJACY RESET
        # for t in self.threads_list:
        #     if t.isAlive():
        #         t.raiseExc(Exception)
        #         time.sleep(0.1)
        # self.threads_list=[]
        # self.timer.stop()
        # self.timer_action.stop()
        # self.scene.clear()
        # self.laduj_plansze('plansza1.txt')




        # for t in self.threads_list:
        #     if t.isAlive():
        #         t.raiseExc(Exception)
        #         time.sleep(0.1)
        # self.threads_list=[]
        # self.timer.stop()
        # self.timer_action.stop()



        # self.scene.addItem(kafelek())
        pass

    def latanie(self):
        for i in self.scene.items():
            if type(i) == pocisk:
                i.lot()
            elif type(i)==player:
                print(i.licznik)
                if i.hp<=0:
                    for t in self.threads_list:
                        if t.getName()=='player_thread':
                            if t.isAlive():
                                t.raiseExc(Exception)
                                time.sleep(0.1)

        # self.scene.addItem(pocisk())
        self.scene.update()






    # def closeEvent(self, event):
    #     pass




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyForm()
    window.show()
    sys.exit(app.exec_())



