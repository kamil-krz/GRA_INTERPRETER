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
                    elif type(i)==kafelek and i.typ!='chodnik':
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
                move=random.randint(1, 4)
                if move==1:
                    self.jedz()
                elif move==2:
                    self.obrot_lewo()
                elif move==3:
                    self.obrot_prawo()
                elif move==4:
                    self.strzal()
        elif self.type=='prosto':
            while(True):
                if (self.hp <= 0):
                    return 0
                self.jedz()
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
                if type(i)==kafelek and i.typ=='chodnik':
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
    def __init__(self, xy=(-1, -1), dir=180, obrazki = None,delay=700,scene=None):
        QGraphicsItem.__init__(self)
        self.xy = xy
        self.dir = dir
        self.obrazek = obrazki['player']
        self.delay=delay
        self.hp=3
        self.scene = scene


    def run(self, kod,e,e_krokowa):
        self.e=e
        self.e_krokowa=e_krokowa
        kod2=''
        self.licznik=0;

        for idx,l in enumerate(kod.splitlines()):
            wciecia=''
            for a in l:
                if a==' ' or a=='\t':
                    wciecia+=a
                else:
                    if a.isalnum() or a=='_' or  a in '()-._,<>[]{};':
                        kod2 += wciecia + 'self.licznik=' + str(idx) + '\n'
                        kod2 += wciecia + 'self.e_krokowa.wait()\n' + wciecia + 'self.e_krokowa.clear()' + '\n'
                        kod2 += l + '\n'
                    break
            if wciecia==l:
                kod2 += ' \n \n \n \n'


        print(kod2)

        # czolg.strzal = self.strzal
        #
        # czolg.jedz = self.jedz
        # czolg.obrot_prawo = self.obrot_prawo
        # czolg.obrot_lewo = self.obrot_lewo
        ##########################################################################
        ##########################################################################
        if 'class' in kod2:
            return ['Nie wolno definować nowych klas']
        elif 'import' in kod2:
            return ['Nie wolno importować']
        try:
            exec(kod2)
            return ['Wykonano kod']
        except:
            formatted_lines = traceback.format_exc().splitlines()
            formatted_lines[3]=  formatted_lines[3].split(',')[1].lstrip() + ":"
            print (formatted_lines[3:])
            return formatted_lines[3:]
            # except Exception as err:
            #     print(type(err))
            #     print(err)






