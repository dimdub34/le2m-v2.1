# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OL_widDe.ui'
#
# Created: Tue Jan 26 07:40:52 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(368, 45)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_de = QtGui.QPushButton(Form)
        self.pushButton_de.setEnabled(True)
        self.pushButton_de.setCheckable(False)
        self.pushButton_de.setObjectName(_fromUtf8("pushButton_de"))
        self.horizontalLayout.addWidget(self.pushButton_de)
        self.label_de_text = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_de_text.setFont(font)
        self.label_de_text.setObjectName(_fromUtf8("label_de_text"))
        self.horizontalLayout.addWidget(self.label_de_text)
        self.label_de = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_de.setFont(font)
        self.label_de.setObjectName(_fromUtf8("label_de"))
        self.horizontalLayout.addWidget(self.label_de)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton_de.setText(_translate("Form", "Cliquez pour lancer le dé", None))
        self.label_de_text.setText(_translate("Form", "Résultat du lancé de dé: ", None))
        self.label_de.setText(_translate("Form", "?", None))

