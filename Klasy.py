from PyQt5.QtCore import (QRectF, Qt)
from PyQt5.QtGui import QBrush, QColor, QImage, QBrush, QPixmap, QTransform
#from PyQt5.QtGui.__init__ import QTransform
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5 import QtTest
import sys
from sys import exc_info
import traceback
import time



class czolg(QGraphicsItem):
    def __init__(self, xy=(-1, -1), dir=180, obrazki = None):
        QGraphicsItem.__init__(self)
        self.xy = xy
        self.dir = dir
        self.obrazek = obrazki['czolg']


    def boundingRect(self):
        return QRectF(0, 0, 500, 500)


    def paint(self, painter,option, widget):
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
        self.dir = self.dir - 90
        if self.dir <0:
            self.dir = self.dir +360
        self.update()
        QtTest.QTest.qWait(500)

    def obrot_lewo(self):
        self.dir = self.dir + 90
        if self.dir >=360:
            self.dir = self.dir - 360
        self.update()
        QtTest.QTest.qWait(500)

    def jedz_prosto(self, dist=1):
        for i in range(dist):
            if self.dir == 0:
                xy = (self.xy[0] + 1, self.xy[1])
            if self.dir == 180:
                xy = (self.xy[0] - 1, self.xy[1])
            if self.dir == 90:
                xy = (self.xy[0],self.xy[1] - 1)
            if self.dir == 270:
                xy = (self.xy[0],self.xy[1] + 1)

            for i in self.scene.items():
                if type(i) == czolg and i.xy == xy:
                    xy = self.xy

            if self.kafelki[xy].typ == 'chodnik':
                self.xy = xy
            self.update()
            QtTest.QTest.qWait(500)

    def jedz_tyl(self, dist=1):
        for i in range(dist):
            if self.dir == 0:
                xy = (self.xy[0] - 1, self.xy[1])
            if self.dir == 180:
                xy = (self.xy[0] + 1, self.xy[1])
            if self.dir == 90:
                xy = (self.xy[0],self.xy[1] + 1)
            if self.dir == 270:
                xy = (self.xy[0],self.xy[1] - 1)

            for i in self.scene.items():
                if type(i) == czolg and i.xy == xy:
                    xy = self.xy

            if self.kafelki[xy].typ == 'chodnik':
                self.xy = xy
            self.update()
            QtTest.QTest.qWait(500)

    def strzal(self):
        if self.dir == 0:
            xy = (self.xy[0]*25+12, self.xy[1]*25+12)
        if self.dir == 180:
            xy = (self.xy[0]*25+12, self.xy[1]*25+12)
        if self.dir == 90:
            xy = (self.xy[0]*25+12, self.xy[1]*25+12)
        if self.dir == 270:
            xy = (self.xy[0]*25+12, self.xy[1]*25+12)

        p = pocisk(xy=xy,dir = self.dir, scena = self.scene, kafelki = self.kafelki)
        self.scene.addItem(p)
        QtTest.QTest.qWait(500)


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
    def __init__(self, xy=(-1, -1), dir = 0, scena = {} , kafelki = {}):
        QGraphicsItem.__init__(self)
        self.xy = xy
        self.dir = dir
        self.scene = scena
        self.kafelki = kafelki


    def boundingRect(self):
        return QRectF(0, 0, 500, 500)

    def paint(self, painter, option, widget):
        x, y = self.xy
        colour = QBrush(QColor('yellow'))
        painter.setBrush(colour)
        painter.drawRect(x-1, y-1, 3, 3)

    def lot(self):

        if self.dir == 0:
            xy = (self.xy[0] + 1, self.xy[1])
        elif self.dir == 180:
            xy = (self.xy[0] - 1, self.xy[1])
        elif self.dir == 90:
            xy = (self.xy[0], self.xy[1] - 1)
        elif self.dir == 270:
            xy = (self.xy[0], self.xy[1] + 1)

        if self.kafelki[((int(xy[0]/25)),int(xy[1]/25))].typ == 'chodnik':
            self.xy = xy
        elif self.kafelki[((int(xy[0]/25)),int(xy[1]/25))].typ == 'sciana_zn':
            self.scene.removeItem(self)
            self.kafelki[((int(xy[0] / 25)), int(xy[1] / 25))].typ = 'chodnik'
        elif self.kafelki[((int(xy[0]/25)),int(xy[1]/25))].typ == 'sciana_nzn':
            self.scene.removeItem(self)

        for i in self.scene.items():
            if type(i) == czolg and i.xy == (((int(xy[0]/25)),int(xy[1]/25))):
                self.scene.removeItem(i)
                self.scene.removeItem(self)
        self.update()

class player(czolg):
    def __init__(self, xy=(-1, -1), dir=180, obrazki = None):
        QGraphicsItem.__init__(self)
        self.xy = xy
        self.dir = dir
        self.obrazek = obrazki['player']


    def run(self, kafelki, scene, kod):
        self.kafelki = kafelki
        self.scene = scene
        strzal = self.strzal
        jedz_tyl = self.jedz_tyl
        jedz_prosto = self.jedz_prosto
        obrot_prawo = self.obrot_prawo
        obrot_lewo = self.obrot_lewo
        ##########################################################################
        ##########################################################################
        if 'class' in kod:
            return ['Nie wolno definować nowych klas']
        elif 'import' in kod:
            return ['Nie wolno importować']
        try:
            exec(kod)
            return ['Wykonano kod']
        except:
            formatted_lines = traceback.format_exc().splitlines()
            formatted_lines[3]=  formatted_lines[3].split(',')[1].lstrip() + ":"
            return formatted_lines[3:]
            # except Exception as err:
            #     print(type(err))
            #     print(err)






