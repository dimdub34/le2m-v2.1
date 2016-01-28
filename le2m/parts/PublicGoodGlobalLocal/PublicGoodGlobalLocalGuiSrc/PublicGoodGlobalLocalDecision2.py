# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'localGlobalGuiSrcDecision2.ui'
#
# Created: Sun Aug 23 11:47:55 2015
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
        Dialog.resize(448, 262)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_periode = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_periode.setFont(font)
        self.label_periode.setObjectName(_fromUtf8("label_periode"))
        self.horizontalLayout.addWidget(self.label_periode)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_historique = QtGui.QPushButton(Dialog)
        self.pushButton_historique.setObjectName(_fromUtf8("pushButton_historique"))
        self.horizontalLayout.addWidget(self.pushButton_historique)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.textEdit_explication = QtGui.QTextEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_explication.sizePolicy().hasHeightForWidth())
        self.textEdit_explication.setSizePolicy(sizePolicy)
        self.textEdit_explication.setMaximumSize(QtCore.QSize(300, 80))
        self.textEdit_explication.setObjectName(_fromUtf8("textEdit_explication"))
        self.horizontalLayout_2.addWidget(self.textEdit_explication)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_decision_individuel = QtGui.QLabel(Dialog)
        self.label_decision_individuel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_decision_individuel.setObjectName(_fromUtf8("label_decision_individuel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_decision_individuel)
        self.spinBox_individuel = QtGui.QSpinBox(Dialog)
        self.spinBox_individuel.setObjectName(_fromUtf8("spinBox_individuel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.spinBox_individuel)
        self.label_decision_local = QtGui.QLabel(Dialog)
        self.label_decision_local.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_decision_local.setObjectName(_fromUtf8("label_decision_local"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_decision_local)
        self.spinBox_local = QtGui.QSpinBox(Dialog)
        self.spinBox_local.setObjectName(_fromUtf8("spinBox_local"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.spinBox_local)
        self.label_decision_global = QtGui.QLabel(Dialog)
        self.label_decision_global.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_decision_global.setObjectName(_fromUtf8("label_decision_global"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_decision_global)
        self.spinBox_global = QtGui.QSpinBox(Dialog)
        self.spinBox_global.setObjectName(_fromUtf8("spinBox_global"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.spinBox_global)
        self.horizontalLayout_3.addLayout(self.formLayout)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_periode.setText(_translate("Dialog", "Période", None))
        self.pushButton_historique.setText(_translate("Dialog", "Historique", None))
        self.label_decision_individuel.setText(_translate("Dialog", "Nombre de jetons que vous placez sur votre compte individuel", None))
        self.label_decision_local.setText(_translate("Dialog", "Nombre de jetons que vous placez sur le compte collectif local", None))
        self.label_decision_global.setText(_translate("Dialog", "Nombre de jetons que vous placez sur le compte collectif global", None))

