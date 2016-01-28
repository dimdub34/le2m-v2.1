# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PublicGoodGameGenderConfigure.ui'
#
# Created: Thu Dec  3 17:27:09 2015
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
        Dialog.resize(281, 269)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_treatment = QtGui.QLabel(Dialog)
        self.label_treatment.setObjectName(_fromUtf8("label_treatment"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_treatment)
        self.comboBox_treatment = QtGui.QComboBox(Dialog)
        self.comboBox_treatment.setObjectName(_fromUtf8("comboBox_treatment"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox_treatment)
        self.label_hommes = QtGui.QLabel(Dialog)
        self.label_hommes.setObjectName(_fromUtf8("label_hommes"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_hommes)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.spinBox_hommes = QtGui.QSpinBox(Dialog)
        self.spinBox_hommes.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_hommes.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.spinBox_hommes.setObjectName(_fromUtf8("spinBox_hommes"))
        self.horizontalLayout.addWidget(self.spinBox_hommes)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_0 = QtGui.QLabel(Dialog)
        self.label_0.setObjectName(_fromUtf8("label_0"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_0)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.spinBox_0 = QtGui.QSpinBox(Dialog)
        self.spinBox_0.setObjectName(_fromUtf8("spinBox_0"))
        self.horizontalLayout_2.addWidget(self.spinBox_0)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_1 = QtGui.QLabel(Dialog)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.spinBox_1 = QtGui.QSpinBox(Dialog)
        self.spinBox_1.setObjectName(_fromUtf8("spinBox_1"))
        self.horizontalLayout_3.addWidget(self.spinBox_1)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.spinBox_2 = QtGui.QSpinBox(Dialog)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.horizontalLayout_4.addWidget(self.spinBox_2)
        self.formLayout.setLayout(4, QtGui.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.spinBox_3 = QtGui.QSpinBox(Dialog)
        self.spinBox_3.setObjectName(_fromUtf8("spinBox_3"))
        self.horizontalLayout_5.addWidget(self.spinBox_3)
        self.formLayout.setLayout(5, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.spinBox_4 = QtGui.QSpinBox(Dialog)
        self.spinBox_4.setObjectName(_fromUtf8("spinBox_4"))
        self.horizontalLayout_6.addWidget(self.spinBox_4)
        self.formLayout.setLayout(6, QtGui.QFormLayout.FieldRole, self.horizontalLayout_6)
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
        self.label_treatment.setText(_translate("Dialog", "Traitement", None))
        self.label_hommes.setText(_translate("Dialog", "Nombre d\'hommes", None))
        self.label_0.setText(_translate("Dialog", "Nombre de groupes avec 0 homme", None))
        self.label_1.setText(_translate("Dialog", "Nombre de groupes avec 1 homme", None))
        self.label_2.setText(_translate("Dialog", "Nombre de groupes avec 2 hommes", None))
        self.label_3.setText(_translate("Dialog", "Nombre de groupes avec 3 hommes", None))
        self.label_4.setText(_translate("Dialog", "Nombre de groupes avec 4 hommes", None))

