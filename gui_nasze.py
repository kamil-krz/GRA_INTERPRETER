# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_nasze.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1094, 754)
        self.plansza = QtWidgets.QGraphicsView(Form)
        self.plansza.setGeometry(QtCore.QRect(10, 90, 500, 500))
        self.plansza.setMinimumSize(QtCore.QSize(500, 500))
        self.plansza.setMaximumSize(QtCore.QSize(500, 500))
        self.plansza.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.plansza.setObjectName("plansza")
        self.textBox = CodeEditor(Form)
        self.textBox.setGeometry(QtCore.QRect(560, 90, 521, 501))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.textBox.setPalette(palette)
        self.textBox.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.textBox.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.textBox.setTabStopWidth(40)
        self.textBox.setObjectName("textBox")
        self.b_reset = QtWidgets.QPushButton(Form)
        self.b_reset.setGeometry(QtCore.QRect(10, 20, 381, 51))
        self.b_reset.setObjectName("b_reset")
        self.b_start = QtWidgets.QPushButton(Form)
        self.b_start.setGeometry(QtCore.QRect(840, 20, 221, 51))
        self.b_start.setObjectName("b_start")
        self.combo_plansze = QtWidgets.QComboBox(Form)
        self.combo_plansze.setGeometry(QtCore.QRect(30, 610, 101, 21))
        self.combo_plansze.setObjectName("combo_plansze")
        self.b_pause = QtWidgets.QPushButton(Form)
        self.b_pause.setEnabled(False)
        self.b_pause.setGeometry(QtCore.QRect(580, 20, 221, 51))
        self.b_pause.setObjectName("b_pause")
        self.konsola = QtWidgets.QTextBrowser(Form)
        self.konsola.setGeometry(QtCore.QRect(560, 600, 521, 141))
        self.konsola.setObjectName("konsola")
        self.horizontalSlider = QtWidgets.QSlider(Form)
        self.horizontalSlider.setGeometry(QtCore.QRect(190, 610, 321, 22))
        self.horizontalSlider.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.horizontalSlider.setMinimum(20)
        self.horizontalSlider.setMaximum(180)
        self.horizontalSlider.setSingleStep(10)
        self.horizontalSlider.setProperty("value", 120)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.b_help = QtWidgets.QPushButton(Form)
        self.b_help.setGeometry(QtCore.QRect(350, 700, 161, 41))
        self.b_help.setObjectName("b_help")
        self.l_nick = QtWidgets.QLabel(Form)
        self.l_nick.setGeometry(QtCore.QRect(440, 20, 61, 21))
        self.l_nick.setText("")
        self.l_nick.setObjectName("l_nick")
        self.l_hp = QtWidgets.QLabel(Form)
        self.l_hp.setGeometry(QtCore.QRect(440, 50, 61, 21))
        self.l_hp.setObjectName("l_hp")
        self.l_mpm = QtWidgets.QLabel(Form)
        self.l_mpm.setGeometry(QtCore.QRect(200, 640, 61, 21))
        self.l_mpm.setObjectName("l_mpm")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.b_reset.setText(_translate("Form", "Reset"))
        self.b_start.setText(_translate("Form", "Start"))
        self.b_pause.setText(_translate("Form", "Pause"))
        self.b_help.setText(_translate("Form", "HELP"))
        self.l_hp.setText(_translate("Form", "HP: 3"))
        self.l_mpm.setText(_translate("Form", "10"))

from Klasy_uzytkowe import CodeEditor

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

