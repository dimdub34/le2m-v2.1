# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widTable.ui'
#
# Created: Fri Jan  1 20:05:08 2016
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
        Form.resize(312, 48)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_pol_0 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_pol_0.setFont(font)
        self.label_pol_0.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_pol_0.setFrameShadow(QtGui.QFrame.Plain)
        self.label_pol_0.setObjectName(_fromUtf8("label_pol_0"))
        self.gridLayout.addWidget(self.label_pol_0, 0, 0, 1, 1)
        self.label_pol_1 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_pol_1.setFont(font)
        self.label_pol_1.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_pol_1.setFrameShadow(QtGui.QFrame.Plain)
        self.label_pol_1.setObjectName(_fromUtf8("label_pol_1"))
        self.gridLayout.addWidget(self.label_pol_1, 0, 1, 1, 1)
        self.label_pol_2 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_pol_2.setFont(font)
        self.label_pol_2.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_pol_2.setFrameShadow(QtGui.QFrame.Plain)
        self.label_pol_2.setObjectName(_fromUtf8("label_pol_2"))
        self.gridLayout.addWidget(self.label_pol_2, 0, 2, 1, 1)
        self.label_pol_3 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_pol_3.setFont(font)
        self.label_pol_3.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_pol_3.setFrameShadow(QtGui.QFrame.Plain)
        self.label_pol_3.setObjectName(_fromUtf8("label_pol_3"))
        self.gridLayout.addWidget(self.label_pol_3, 0, 3, 1, 1)
        self.label_val_0 = QtGui.QLabel(Form)
        self.label_val_0.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_val_0.setFrameShadow(QtGui.QFrame.Plain)
        self.label_val_0.setAlignment(QtCore.Qt.AlignCenter)
        self.label_val_0.setObjectName(_fromUtf8("label_val_0"))
        self.gridLayout.addWidget(self.label_val_0, 1, 0, 1, 1)
        self.label_val_1 = QtGui.QLabel(Form)
        self.label_val_1.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_val_1.setFrameShadow(QtGui.QFrame.Plain)
        self.label_val_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_val_1.setObjectName(_fromUtf8("label_val_1"))
        self.gridLayout.addWidget(self.label_val_1, 1, 1, 1, 1)
        self.label_val_2 = QtGui.QLabel(Form)
        self.label_val_2.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_val_2.setFrameShadow(QtGui.QFrame.Plain)
        self.label_val_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_val_2.setObjectName(_fromUtf8("label_val_2"))
        self.gridLayout.addWidget(self.label_val_2, 1, 2, 1, 1)
        self.label_val_3 = QtGui.QLabel(Form)
        self.label_val_3.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_val_3.setFrameShadow(QtGui.QFrame.Plain)
        self.label_val_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_val_3.setObjectName(_fromUtf8("label_val_3"))
        self.gridLayout.addWidget(self.label_val_3, 1, 3, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_pol_0.setText(_translate("Form", "Politique 1", None))
        self.label_pol_1.setText(_translate("Form", "Politique 2", None))
        self.label_pol_2.setText(_translate("Form", "Politique 3", None))
        self.label_pol_3.setText(_translate("Form", "Politique 4", None))
        self.label_val_0.setText(_translate("Form", "8", None))
        self.label_val_1.setText(_translate("Form", "8", None))
        self.label_val_2.setText(_translate("Form", "2", None))
        self.label_val_3.setText(_translate("Form", "8", None))

