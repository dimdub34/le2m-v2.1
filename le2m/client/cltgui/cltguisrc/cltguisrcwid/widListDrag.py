# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widListDrag.ui'
#
# Created: Thu Dec 31 13:00:14 2015
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
        Form.resize(628, 210)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.listWidget_left = QtGui.QListWidget(Form)
        self.listWidget_left.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.listWidget_left.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.listWidget_left.setObjectName(_fromUtf8("listWidget_left"))
        self.horizontalLayout.addWidget(self.listWidget_left)
        self.listWidget_right = QtGui.QListWidget(Form)
        self.listWidget_right.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.listWidget_right.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.listWidget_right.setObjectName(_fromUtf8("listWidget_right"))
        self.horizontalLayout.addWidget(self.listWidget_right)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))

