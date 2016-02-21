# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widRadio.ui'
#
# Created: Sun Feb 21 14:47:14 2016
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
        Form.resize(340, 41)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout_radios = QtGui.QHBoxLayout()
        self.horizontalLayout_radios.setObjectName(_fromUtf8("horizontalLayout_radios"))
        self.radioButton_0 = QtGui.QRadioButton(Form)
        self.radioButton_0.setObjectName(_fromUtf8("radioButton_0"))
        self.buttonGroup = QtGui.QButtonGroup(Form)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.radioButton_0)
        self.horizontalLayout_radios.addWidget(self.radioButton_0)
        self.radioButton_1 = QtGui.QRadioButton(Form)
        self.radioButton_1.setObjectName(_fromUtf8("radioButton_1"))
        self.buttonGroup.addButton(self.radioButton_1)
        self.horizontalLayout_radios.addWidget(self.radioButton_1)
        self.horizontalLayout.addLayout(self.horizontalLayout_radios)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "TextLabel", None))
        self.radioButton_0.setText(_translate("Form", "RadioButton", None))
        self.radioButton_1.setText(_translate("Form", "RadioButton", None))

