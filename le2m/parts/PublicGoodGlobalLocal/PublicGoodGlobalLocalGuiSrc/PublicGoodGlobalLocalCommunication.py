# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'localGlobalGuiSrcCommunication.ui'
#
# Created: Mon Aug 24 13:21:46 2015
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
        Dialog.resize(518, 635)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_periode = QtGui.QLabel(Dialog)
        self.label_periode.setObjectName(_fromUtf8("label_periode"))
        self.horizontalLayout_2.addWidget(self.label_periode)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_historique = QtGui.QPushButton(Dialog)
        self.pushButton_historique.setObjectName(_fromUtf8("pushButton_historique"))
        self.horizontalLayout_2.addWidget(self.pushButton_historique)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.textEdit_explication = QtGui.QTextEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_explication.sizePolicy().hasHeightForWidth())
        self.textEdit_explication.setSizePolicy(sizePolicy)
        self.textEdit_explication.setMinimumSize(QtCore.QSize(500, 80))
        self.textEdit_explication.setMaximumSize(QtCore.QSize(500, 80))
        self.textEdit_explication.setObjectName(_fromUtf8("textEdit_explication"))
        self.verticalLayout.addWidget(self.textEdit_explication)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.listWidget = QtGui.QListWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMinimumSize(QtCore.QSize(500, 300))
        self.listWidget.setMaximumSize(QtCore.QSize(500, 300))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.textEdit_composition = QtGui.QTextEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_composition.sizePolicy().hasHeightForWidth())
        self.textEdit_composition.setSizePolicy(sizePolicy)
        self.textEdit_composition.setMinimumSize(QtCore.QSize(500, 100))
        self.textEdit_composition.setMaximumSize(QtCore.QSize(500, 100))
        self.textEdit_composition.setObjectName(_fromUtf8("textEdit_composition"))
        self.verticalLayout.addWidget(self.textEdit_composition)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_periode.setText(_translate("Dialog", "TextLabel", None))
        self.pushButton_historique.setText(_translate("Dialog", "PushButton", None))
        self.pushButton.setText(_translate("Dialog", "Envoyer", None))

