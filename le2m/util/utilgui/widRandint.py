# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widRandint.ui'
#
# Created: Wed Jan 13 14:37:34 2016
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
        Form.resize(280, 110)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_min = QtGui.QLabel(Form)
        self.label_min.setObjectName(_fromUtf8("label_min"))
        self.horizontalLayout.addWidget(self.label_min)
        self.spinBox_min = QtGui.QSpinBox(Form)
        self.spinBox_min.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.spinBox_min.setMaximum(999)
        self.spinBox_min.setObjectName(_fromUtf8("spinBox_min"))
        self.horizontalLayout.addWidget(self.spinBox_min)
        self.label_max = QtGui.QLabel(Form)
        self.label_max.setObjectName(_fromUtf8("label_max"))
        self.horizontalLayout.addWidget(self.label_max)
        self.spinBox_max = QtGui.QSpinBox(Form)
        self.spinBox_max.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.spinBox_max.setMaximum(999)
        self.spinBox_max.setObjectName(_fromUtf8("spinBox_max"))
        self.horizontalLayout.addWidget(self.spinBox_max)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.lcdNumber = QtGui.QLCDNumber(Form)
        self.lcdNumber.setFrameShape(QtGui.QFrame.NoFrame)
        self.lcdNumber.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.horizontalLayout_2.addWidget(self.lcdNumber)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.pushButton_start = QtGui.QPushButton(Form)
        self.pushButton_start.setObjectName(_fromUtf8("pushButton_start"))
        self.horizontalLayout_3.addWidget(self.pushButton_start)
        self.pushButton_stop = QtGui.QPushButton(Form)
        self.pushButton_stop.setObjectName(_fromUtf8("pushButton_stop"))
        self.horizontalLayout_3.addWidget(self.pushButton_stop)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.spinBox_min, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.lcdNumber.display)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_min.setText(_translate("Form", "Minimum", None))
        self.label_max.setText(_translate("Form", "Maximum", None))
        self.pushButton_start.setText(_translate("Form", "Start", None))
        self.pushButton_stop.setText(_translate("Form", "Stop", None))

