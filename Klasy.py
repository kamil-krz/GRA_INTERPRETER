import math
from PyQt5.QtCore import (QRectF, Qt)
from PyQt5.QtGui import QBrush, QColor, QImage, QBrush, QPixmap, QTransform
#from PyQt5.QtGui.__init__ import QTransform
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5 import QtTest
import sys
from sys import exc_info
import traceback
import time
import random
import sys

from PyQt5.QtWidgets import QGraphicsScene


class czolg(QGraphicsItem):
    def __init__(self, xy=(-1, -1), dir=180, obrazki = None,type='stojacy',delay=500,scene=None,hp=1):
        QGraphicsItem.__init__(self)
        self.scene = scene
        self.delay=delay
        self.xy = xy
        self.dir = dir
        self.obrazek = obrazki['czolg']
        self.type=type
        self.hp = hp



    def boundingRect(self):
        return QRectF(0, 0, 500, 500)

    def paint(self, painter, option, widget):
        x, y = self.xy
        rect = QRectF(x * 25, y * 25, 25, 25)

        if self.dir == 0:
            obrot = QTransform().rotate(90)
            painter.drawImage(rect, self.obrazek.transformed(obrot))
        if self.dir == 90:
            painter.drawImage(rect, self.obrazek)
        if self.dir == 180:
            obrot = QTransform().rotate(-90)
            painter.drawImage(rect, self.obrazek.transformed(obrot))
        if self.dir == 270:
            obrot = QTransform().rotate(180)
            painter.drawImage(rect, self.obrazek.transformed(obrot))

    def obrot_prawo(self):
        self.e.wait()
        self.dir = self.dir - 90
        if self.dir <0:
            self.dir = self.dir +360
        self.e.clear()

    def obrot_lewo(self):
        self.e.wait()
        self.dir = self.dir + 90
        if self.dir >=360:
            self.dir = self.dir - 360
        self.e.clear()

    def radar(self,dir2='przod'):
        if(dir2=='lewo'):
            dir2=self.dir+90
            if dir2==360:
                dir2=0
        elif (dir2 == 'prawo'):
            dir2 = self.dir - 90
            if dir2 == -90:
                dir2 = 270
        elif (dir2 == 'tyl'):
            dir2 = self.dir - 180
            if dir2 == -180:
                dir2 = 180
            elif dir2==-90:
                dir2=270
        else:
            dir2=self.dir

        for i in range(1, 20):
            if dir2 == 0:
                xy = (self.xy[0] + i, self.xy[1])
            elif dir2 == 180:
                xy = (self.xy[0] - i, self.xy[1])
            elif dir2 == 90:
                xy = (self.xy[0], self.xy[1] - i)
            elif dir2 == 270:
                xy = (self.xy[0], self.xy[1] + i)
            for k in self.scene.items():
                if k.xy == xy:
                    if type(k) == kafelek:
                        if k.typ != 'chodnik':
                            return (i, k.typ)
                    elif type(k) == czolg or type(k) == player:
                        return (i, 'czolg')
                elif int(k.xy[0]/25)==xy[0] and int(k.xy[1]/25)==xy[1]:
                    return (i,'pocisk')

    def jedz(self, dist=1):
        for i in range(abs(dist)):
            self.e.wait()
            if dist>0:

                if self.dir == 0:
                    xy = (self.xy[0] + 1, self.xy[1])
                if self.dir == 180:
                    xy = (self.xy[0] - 1, self.xy[1])
                if self.dir == 90:
                    xy = (self.xy[0],self.xy[1] - 1)
                if self.dir == 270:
                    xy = (self.xy[0],self.xy[1] + 1)


            elif dist<0:

                if self.dir == 0:
                    xy = (self.xy[0] - 1, self.xy[1])
                if self.dir == 180:
                    xy = (self.xy[0] + 1, self.xy[1])
                if self.dir == 90:
                    xy = (self.xy[0], self.xy[1] + 1)
                if self.dir == 270:
                    xy = (self.xy[0], self.xy[1] - 1)


            for i in self.scene.items():
                if  i.xy == xy:
                    if (type(i) == czolg or type(i) == player)and i!=self:
                        xy = self.xy
                        break
                    elif type(i)==kafelek and (i.typ!='chodnik' and i.typ!='target'):
                        xy = self.xy
                        break

            self.xy = xy
            self.e.clear()




    def strzal(self):
        self.e.wait()
        if self.dir == 0:
            xy = (self.xy[0]*25+25, self.xy[1]*25+12)
        if self.dir == 180:
            xy = (self.xy[0]*25, self.xy[1]*25+12)
        if self.dir == 90:
            xy = (self.xy[0]*25+12, self.xy[1]*25)
        if self.dir == 270:
            xy = (self.xy[0]*25+12, self.xy[1]*25+25)

        p=pocisk(xy=xy,dir = self.dir, scena = self.scene)
        self.scene.addItem(p)

        self.e.clear()


    def go_AI(self, e):
        self.e=e
        if self.type=='stojacy':
            return
        elif self.type=='random':
            while(True):
                if(self.hp<=0):
                    return 0
                if self.radar('lewo')[1]=='pocisk':
                    self.jedz()
                    continue
                elif self.radar('prawo')[1]=='pocisk':
                    self.jedz()
                    continue
                elif self.radar('tyl')[1]=='pocisk':
                    self.obrot_lewo()
                    continue

                move=random.randint(1, 15)
                if move<5 and self.radar()[0]>1:
                    self.jedz()
                elif move==6 and self.radar('lewo')[0]>1:
                    self.obrot_lewo()
                elif move==7 and self.radar('prawo')[0]>1:
                    self.obrot_prawo()
                elif move==8 :
                    self.strzal()
                elif move>=9 and self.radar()[1]=='czolg':
                    self.strzal()
        elif self.type=='prosto':
            while(True):
                if (self.hp <= 0):
                    return 0
                if self.radar()[0]>1:
                    self.jedz()
                else:
                    self.obrot_lewo()
                    self.obrot_lewo()
                if self.radar()[1] =='czolg' and random.random()<0.8:
                    self.strzal()




    def hit(self):
        self.hp-=1
        if self.hp<=0:
            self.scene.removeItem(self)



class kafelek(QGraphicsItem):
    def __init__(self, xy=(-1, -1), typ = 'chodnik', obrazki = None):
        QGraphicsItem.__init__(self)
        self.typ = typ
        self.xy = xy
        self.obrazki = obrazki

    def boundingRect(self):
        return QRectF(0, 0, 500, 500)

    def paint(self, painter, option, widget):
        x, y = self.xy
        rect = QRectF(x * 25, y * 25, 25, 25)

        if self.typ == 'chodnik':
            colour = QBrush(QColor('black'))
            painter.setBrush(colour)
            painter.drawRect(x * 25, y * 25, 25, 25)
        elif self.typ == 'sciana_zn':
            painter.drawImage(rect, self.obrazki['sciana_zniszczalna'])
        elif self.typ == 'sciana_nzn':
            painter.drawImage(rect, self.obrazki['sciana_niezniszczalna'])
        elif self.typ == 'target':
            colour = QBrush(QColor('red'))
            painter.setBrush(colour)
            painter.drawRect(x * 25, y * 25, 25, 25)



class pocisk(QGraphicsItem):
    def __init__(self, xy=(-1, -1), dir = 0, scena = {} ):
        QGraphicsItem.__init__(self)
        self.xy = xy
        self.dir = dir
        self.scene = scena

    def boundingRect(self):
        return QRectF(0, 0, 500, 500)

    def paint(self, painter, option, widget):
        x, y = self.xy

        colour = QBrush(QColor('yellow'))
        painter.setBrush(colour)
        painter.drawRect(x-1, y-1, 3, 3)

    def lot(self):
        if self.dir == 0:
            xy = (self.xy[0] + 2, self.xy[1])
        elif self.dir == 180:
            xy = (self.xy[0] - 2, self.xy[1])
        elif self.dir == 90:
            xy = (self.xy[0], self.xy[1] - 2)
        elif self.dir == 270:
            xy = (self.xy[0], self.xy[1] + 2)
        else:
            xy=self.xy
        for i in self.scene.items():
            if i.xy==((int(xy[0]/25)),int(xy[1]/25)):
                if type(i)==kafelek and (i.typ=='chodnik' or i.typ=='target'):
                    self.xy = xy

                elif type(i)==kafelek and i.typ=='sciana_zn':
                    self.scene.removeItem(self)
                    i.typ = 'chodnik'
                    break
                elif type(i)==kafelek and i.typ=='sciana_nzn':
                    self.scene.removeItem(self)
                    break

                elif type(i) == czolg:
                    i.hit();
                    self.scene.removeItem(self)
                    break
                elif type(i)==player:
                    self.scene.removeItem(self)
                    i.hit();
                    break


class player(czolg):
    def __init__(self, xy=(-1, -1), dir=180, obrazki = None,scene=None):
        QGraphicsItem.__init__(self)
        self.licznik = 0
        self.xy = xy
        self.dir = dir
        self.obrazek = obrazki['player']
        self.hp=3
        self.scene = scene
        self.result=''

    def add_result(self,*string):
        self.result += '\n'
        for s in string:
            self.result+=str(s)
            self.result+=' '


    def run(self, kod,e,e_krokowa,e_exit):
        self.add_result('Uruchomiono kod\n')
        self.e=e
        self.e_krokowa=e_krokowa
        self.e_exit=e_exit
        self.kod2=''
        self.licznik=0;



        gracz.jedz=self.jedz
        gracz.obrot_prawo=self.obrot_prawo
        gracz.obrot_lewo=self.obrot_lewo
        gracz.strzal=self.strzal
        gracz.radar=self.radar


        import pygame
        pygame.init()
        pygame.joystick.init()
        js = pygame.joystick.Joystick(0)
        js.init()



        for idx,l in enumerate(kod.splitlines()):
            wciecia=''
            for a in l:
                if a==' ' or a=='\t':
                    wciecia+=a
                else:
                    if 'else ' in l:
                        self.kod2 += ' \n \n \n '+l+'\n'
                    elif 'elif ' in l:
                        self.kod2 += ' \n \n \n'+l+'\n'

                    elif a.isalnum() or a=='_' or  a in '()-._,<>[]{};':
                        self.kod2 += wciecia + 'self.licznik=' + str(idx) + '\n'
                        self.kod2 +=  wciecia + 'if not self.e_exit.is_set(): sys.exit(0)' + '\n'+wciecia + 'self.e_krokowa.wait()\n' + wciecia + 'self.e_krokowa.clear()' + '\n'
                        self.kod2 += l + '\n'
                    break
            if wciecia==l:
                self.kod2 += ' \n \n \n \n'


        # self.add_result(self.kod2)


        if 'class ' in kod:
            self.add_result('\nNie wolno definować nowych klas')
            return
        elif 'import ' in kod:
            self.add_result('\nNie wolno importować')
            return
        elif 'self.' in kod:
            self.add_result('\nUżyj klasy gracz zamiast self')
            return
        try:
            print=self.add_result
            exec(self.kod2)
            self.add_result('\nWykonano kod')


            return
        except SyntaxError as err:
            error_class = err.__class__.__name__
            detail = err.args[0]
            line_number = err.lineno
            self.add_result("%s at line %d of %s: %s" % (error_class, math.ceil(line_number / 4), 'user code', detail))
            return
        except Exception as err:
            error_class = err.__class__.__name__
            detail = err.args[0]
            cl, exc, tb = sys.exc_info()
            line_number = traceback.extract_tb(tb)[-1][1]
            self.add_result("%s at line %d of %s: %s" % (error_class, math.ceil(line_number/4), 'user code', detail))

        except SystemExit as e:
            self.add_result("Przerwano dzialanie kodu")

        return



class gracz:
    def jedz(self):
        pass
    def obrot_prawo(self):
        pass
    def obrot_lewo(self):
        pass
    def strzal(self):
        pass
    def radar(self):
        pass


class map:
    def __init__(self, nazwa='plansza_0'):
        self.scene = QGraphicsScene()
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)

        self.czolgi = []
        self.player=None
        self.cele=[]
        self.help=''
        self.target=(-1,-1)

        self.obrazki = {'player': QImage("graphics/player.jpg"), 'czolg': QImage("graphics/czolg.jpg"),
                        'sciana_zniszczalna': QImage("graphics/sciana_zniszczalna.jpg"),
                        'sciana_niezniszczalna': QImage("graphics/sciana_niezniszczalna.jpg"), }

        self.laduj_plansze('maps/' + nazwa + '.map')
        self.laduj_czolgi('maps/' + nazwa + '.tanks')
        # for i in self.scene.items():
        #     if type(i) != kafelek:
        #         i.setZValue(0.5)


    def laduj_plansze(self, nazwa):
        file = open(nazwa)
        for i, line in enumerate(file):
            if i < 20:

                for j in range(0, 20):
                    if line[j] == ' ':
                        self.scene.addItem(kafelek(xy=(j, i), typ='chodnik', obrazki=self.obrazki))
                    elif line[j] == '#':
                        self.scene.addItem(kafelek(xy=(j, i), typ='sciana_nzn', obrazki=self.obrazki))
                    elif line[j] == '*':
                        self.scene.addItem(kafelek(xy=(j, i), typ='sciana_zn', obrazki=self.obrazki))
                    elif line[j] == 'x':
                        self.target=(j,i)
                        self.scene.addItem(kafelek(xy=(j, i), typ='target', obrazki=self.obrazki))
            elif i==20 and 'cele' in line:
                line=line.replace('\n','')
                self.cele=line.split(' ')[1:]
            elif i>21:
                self.help+=line+'\n'


    def laduj_czolgi(self, nazwa):
        file = open(nazwa)
        for i, line in enumerate(file):
            line=line.replace('\n','')
            line = line.split(' ')
            if line[0] == 'player':
                self.player = player(xy=(int(line[2]), int(line[1])),dir=int(line[3]), obrazki=self.obrazki, scene=self.scene)
                self.scene.addItem(self.player)
            elif line[0] == 'czolg':
                cz = czolg(xy=(int(line[2]), int(line[1])), dir=int(line[3]), obrazki=self.obrazki, type=line[4], scene=self.scene)
                self.czolgi.append(cz)
                self.scene.addItem(cz)
    def getScene(self):
        return self.scene
    def getHelp(self):
        return self.help


