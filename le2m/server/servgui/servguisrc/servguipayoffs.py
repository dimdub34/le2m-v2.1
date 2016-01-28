# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'le2mServGuiSrcGains2.ui'
#
# Created: Mon Aug 24 11:10:29 2015
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
        Dialog.resize(554, 608)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableView = QtGui.QTableView(Dialog)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_imprimer = QtGui.QPushButton(Dialog)
        self.pushButton_imprimer.setObjectName(_fromUtf8("pushButton_imprimer"))
        self.horizontalLayout.addWidget(self.pushButton_imprimer)
        self.pushButton_enregistrer = QtGui.QPushButton(Dialog)
        self.pushButton_enregistrer.setObjectName(_fromUtf8("pushButton_enregistrer"))
        self.horizontalLayout.addWidget(self.pushButton_enregistrer)
        self.pushButton_afficher = QtGui.QPushButton(Dialog)
        self.pushButton_afficher.setObjectName(_fromUtf8("pushButton_afficher"))
        self.horizontalLayout.addWidget(self.pushButton_afficher)
        self.pushButton_ajouter = QtGui.QPushButton(Dialog)
        self.pushButton_ajouter.setObjectName(_fromUtf8("pushButton_ajouter"))
        self.horizontalLayout.addWidget(self.pushButton_ajouter)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButton_imprimer.setText(_translate("Dialog", "Imprimer", None))
        self.pushButton_enregistrer.setText(_translate("Dialog", "Enregistrer sous", None))
        self.pushButton_afficher.setText(_translate("Dialog", "Afficher sur les postes clients", None))
        self.pushButton_ajouter.setText(_translate("Dialog", "Ajouter aux gains finaux", None))

