# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Ui_Form):
        Ui_Form.setObjectName("Ui_Form")
        Ui_Form.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Ui_Form)
        self.pushButton.setGeometry(QtCore.QRect(110, 80, 181, 111))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Ui_Form)
        self.pushButton.clicked.connect(Ui_Form.close)
        QtCore.QMetaObject.connectSlotsByName(Ui_Form)

    def retranslateUi(self, Ui_Form):
        _translate = QtCore.QCoreApplication.translate
        Ui_Form.setWindowTitle(_translate("Ui_Form", "Form"))
        self.pushButton.setText(_translate("Ui_Form", "Zamknij Mnie"))

