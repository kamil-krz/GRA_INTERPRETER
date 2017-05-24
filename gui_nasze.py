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
        self.textBox = QtWidgets.QPlainTextEdit(Form)
        self.textBox.setGeometry(QtCore.QRect(560, 90, 521, 651))
        self.textBox.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.textBox.setObjectName("textBox")
        self.b_reset = QtWidgets.QPushButton(Form)
        self.b_reset.setGeometry(QtCore.QRect(90, 20, 381, 51))
        self.b_reset.setObjectName("b_reset")
        self.b_start = QtWidgets.QPushButton(Form)
        self.b_start.setGeometry(QtCore.QRect(650, 20, 381, 51))
        self.b_start.setObjectName("b_start")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.b_reset.setText(_translate("Form", "RESET"))
        self.b_start.setText(_translate("Form", "START"))

