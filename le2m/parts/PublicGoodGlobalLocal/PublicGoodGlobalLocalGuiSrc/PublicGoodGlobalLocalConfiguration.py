# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'localGlobalGuiSrcConfiguration.ui'
#
# Created: Mon Aug 24 21:58:02 2015
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
        Dialog.resize(353, 197)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_traitement = QtGui.QLabel(Dialog)
        self.label_traitement.setObjectName(_fromUtf8("label_traitement"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_traitement)
        self.comboBox_traitement = QtGui.QComboBox(Dialog)
        self.comboBox_traitement.setObjectName(_fromUtf8("comboBox_traitement"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBox_traitement)
        self.label_communication = QtGui.QLabel(Dialog)
        self.label_communication.setObjectName(_fromUtf8("label_communication"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_communication)
        self.comboBox_communication = QtGui.QComboBox(Dialog)
        self.comboBox_communication.setObjectName(_fromUtf8("comboBox_communication"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBox_communication)
        self.label_temps = QtGui.QLabel(Dialog)
        self.label_temps.setObjectName(_fromUtf8("label_temps"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_temps)
        self.spinBox_temps = QtGui.QSpinBox(Dialog)
        self.spinBox_temps.setEnabled(True)
        self.spinBox_temps.setMaximum(9999)
        self.spinBox_temps.setObjectName(_fromUtf8("spinBox_temps"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.spinBox_temps)
        self.label_periodes = QtGui.QLabel(Dialog)
        self.label_periodes.setObjectName(_fromUtf8("label_periodes"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_periodes)
        self.lineEdit_periodes = QtGui.QLineEdit(Dialog)
        self.lineEdit_periodes.setEnabled(True)
        self.lineEdit_periodes.setObjectName(_fromUtf8("lineEdit_periodes"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit_periodes)
        self.label_nombreperiodes = QtGui.QLabel(Dialog)
        self.label_nombreperiodes.setObjectName(_fromUtf8("label_nombreperiodes"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_nombreperiodes)
        self.spinBox_nombreperiodes = QtGui.QSpinBox(Dialog)
        self.spinBox_nombreperiodes.setObjectName(_fromUtf8("spinBox_nombreperiodes"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.spinBox_nombreperiodes)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_traitement.setText(_translate("Dialog", "Traitement", None))
        self.label_communication.setText(_translate("Dialog", "Communication", None))
        self.label_temps.setText(_translate("Dialog", "Temps de communication (en secondes)", None))
        self.label_periodes.setText(_translate("Dialog", "Périodes de communication (séparées par un espace)", None))
        self.label_nombreperiodes.setText(_translate("Dialog", "Nombre de périodes", None))

