from PyQt5.QtCore import (QRectF, Qt)
from PyQt5.QtGui import (QBrush, QColor, QImage)
from PyQt5.QtWidgets import QGraphicsItem


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



    def goto(self, target):
        self.xy = target
        self.update()