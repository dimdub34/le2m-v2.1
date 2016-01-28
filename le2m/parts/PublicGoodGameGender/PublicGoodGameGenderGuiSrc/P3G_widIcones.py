# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'P3G_widIcones.ui'
#
# Created: Sun Jan  3 15:20:52 2016
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
        Form.resize(410, 139)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(86, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_grouptype = QtGui.QLabel(Form)
        self.label_grouptype.setObjectName(_fromUtf8("label_grouptype"))
        self.verticalLayout.addWidget(self.label_grouptype)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_icon_1 = QtGui.QLabel(Form)
        self.label_icon_1.setText(_fromUtf8(""))
        self.label_icon_1.setPixmap(QtGui.QPixmap(_fromUtf8("../PublicGoodGameGenderImg/femme.jpg")))
        self.label_icon_1.setObjectName(_fromUtf8("label_icon_1"))
        self.horizontalLayout.addWidget(self.label_icon_1)
        self.label_icon_2 = QtGui.QLabel(Form)
        self.label_icon_2.setText(_fromUtf8(""))
        self.label_icon_2.setPixmap(QtGui.QPixmap(_fromUtf8("../PublicGoodGameGenderImg/femme.jpg")))
        self.label_icon_2.setObjectName(_fromUtf8("label_icon_2"))
        self.horizontalLayout.addWidget(self.label_icon_2)
        self.label_icon_3 = QtGui.QLabel(Form)
        self.label_icon_3.setText(_fromUtf8(""))
        self.label_icon_3.setPixmap(QtGui.QPixmap(_fromUtf8("../PublicGoodGameGenderImg/homme.jpg")))
        self.label_icon_3.setObjectName(_fromUtf8("label_icon_3"))
        self.horizontalLayout.addWidget(self.label_icon_3)
        self.label_icon_4 = QtGui.QLabel(Form)
        self.label_icon_4.setText(_fromUtf8(""))
        self.label_icon_4.setPixmap(QtGui.QPixmap(_fromUtf8("../PublicGoodGameGenderImg/homme.jpg")))
        self.label_icon_4.setObjectName(_fromUtf8("label_icon_4"))
        self.horizontalLayout.addWidget(self.label_icon_4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem1 = QtGui.QSpacerItem(86, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_grouptype.setText(_translate("Form", "Composition de votre groupe", None))

