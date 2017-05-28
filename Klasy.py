from PyQt5.QtCore import (QRectF, Qt)
from PyQt5.QtGui import (QBrush, QColor, QImage)
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5 import QtTest


class czolg(QGraphicsItem):
    def __init__(self, xy=(-1, -1), dir=180, colour='green', icon='graphics/player.png'):
        QGraphicsItem.__init__(self)
        self.colour = colour
        self.icon = icon
        self.xy = xy
        self.dir = dir

    def boundingRect(self):
        return QRectF(0, 0, 500, 500)


    def paint(self, painter,option, widget):
        x, y = self.xy
        colour = QBrush(QColor(self.colour))
        painter.setBrush(colour)
        painter.drawRect(x*25+2, y*25+2, 21, 21)
        colour = QBrush(QColor('black'))
        painter.setBrush(colour)
        if self.dir == 0:
            painter.drawRect(x * 25+10, y * 25 + 10, 15, 5)
        if self.dir == 90:
            painter.drawRect(x * 25 + 10, y * 25, 5, 15)
        if self.dir == 180:
            painter.drawRect(x * 25 , y * 25 + 10, 15, 5)
        if self.dir == 270:
            painter.drawRect(x * 25 + 10, y * 25 + 10, 5, 15)

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
    def __init__(self, xy=(-1, -1), typ = 'chodnik'):
        QGraphicsItem.__init__(self)
        self.typ = typ
        self.xy = xy

    def boundingRect(self):
        return QRectF(0, 0, 500, 500)

    def paint(self, painter, option, widget):
        x, y = self.xy
        if self.typ == 'chodnik':
            self.colour = 'white'
        elif self.typ == 'sciana_zn':
            self.colour = 'gray'
        elif self.typ == 'sciana_nzn':
            self.colour = 'black'
        colour = QBrush(QColor(self.colour))
        painter.setBrush(colour)
        painter.drawRect(x * 25 , y * 25 , 25, 25)


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

    def run(self, kafelki, scene):
        self.kafelki = kafelki
        self.scene = scene
        ##########################################################################
        ##########################################################################
        self.obrot_prawo()
        self.jedz_prosto(6)
        self.strzal()
        self.jedz_prosto(2)








