# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'questcompquest.ui'
#
# Created: Wed Jul 20 07:44:18 2016
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(600, 450)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_numeroQuestion = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_numeroQuestion.setFont(font)
        self.label_numeroQuestion.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_numeroQuestion.setObjectName(_fromUtf8("label_numeroQuestion"))
        self.horizontalLayout.addWidget(self.label_numeroQuestion)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.textEdit_ennonce = QtGui.QTextEdit(Dialog)
        self.textEdit_ennonce.setMinimumSize(QtCore.QSize(580, 100))
        self.textEdit_ennonce.setMaximumSize(QtCore.QSize(580, 100))
        self.textEdit_ennonce.setReadOnly(True)
        self.textEdit_ennonce.setObjectName(_fromUtf8("textEdit_ennonce"))
        self.horizontalLayout_3.addWidget(self.textEdit_ennonce)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.hl_propositions = QtGui.QHBoxLayout()
        self.hl_propositions.setObjectName(_fromUtf8("hl_propositions"))
        self.verticalLayout.addLayout(self.hl_propositions)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton_valider = QtGui.QPushButton(Dialog)
        self.pushButton_valider.setObjectName(_fromUtf8("pushButton_valider"))
        self.horizontalLayout_2.addWidget(self.pushButton_valider)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Question de compréhension", None))
        self.label_numeroQuestion.setText(_translate("Dialog", "Question ", None))
        self.pushButton_valider.setText(_translate("Dialog", "Valider", None))

