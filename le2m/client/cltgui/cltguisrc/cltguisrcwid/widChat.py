# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widChat.ui'
#
# Created: Tue Feb 23 09:31:19 2016
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
        Form.resize(368, 479)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_read = QtGui.QLabel(Form)
        self.label_read.setObjectName(_fromUtf8("label_read"))
        self.verticalLayout.addWidget(self.label_read)
        self.textEdit_read = QtGui.QTextEdit(Form)
        self.textEdit_read.setObjectName(_fromUtf8("textEdit_read"))
        self.verticalLayout.addWidget(self.textEdit_read)
        self.label_write = QtGui.QLabel(Form)
        self.label_write.setObjectName(_fromUtf8("label_write"))
        self.verticalLayout.addWidget(self.label_write)
        self.textEdit_write = QtGui.QTextEdit(Form)
        self.textEdit_write.setObjectName(_fromUtf8("textEdit_write"))
        self.verticalLayout.addWidget(self.textEdit_write)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_read.setText(_translate("Form", "TextLabel", None))
        self.label_write.setText(_translate("Form", "TextLabel", None))
        self.pushButton.setText(_translate("Form", "Envoyer", None))

