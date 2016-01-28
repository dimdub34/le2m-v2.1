# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'le2mServGuiSrcListeExperiences.ui'
#
# Created: Mon Sep 14 09:58:12 2015
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
        Dialog.resize(318, 386)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_explication = QtGui.QLabel(Dialog)
        self.label_explication.setObjectName(_fromUtf8("label_explication"))
        self.verticalLayout.addWidget(self.label_explication)
        self.listView = QtGui.QListView(Dialog)
        self.listView.setMinimumSize(QtCore.QSize(300, 0))
        self.listView.setObjectName(_fromUtf8("listView"))
        self.verticalLayout.addWidget(self.listView)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_basepath = QtGui.QLabel(Dialog)
        self.label_basepath.setObjectName(_fromUtf8("label_basepath"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_basepath)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButton_base = QtGui.QPushButton(Dialog)
        self.pushButton_base.setObjectName(_fromUtf8("pushButton_base"))
        self.horizontalLayout_3.addWidget(self.pushButton_base)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.label_basepath1 = QtGui.QLabel(Dialog)
        self.label_basepath1.setObjectName(_fromUtf8("label_basepath1"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_basepath1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_basepath2 = QtGui.QLabel(Dialog)
        self.label_basepath2.setObjectName(_fromUtf8("label_basepath2"))
        self.horizontalLayout_2.addWidget(self.label_basepath2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_basename = QtGui.QLabel(Dialog)
        self.label_basename.setObjectName(_fromUtf8("label_basename"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_basename)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit_nom_base = QtGui.QLineEdit(Dialog)
        self.lineEdit_nom_base.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_nom_base.setObjectName(_fromUtf8("lineEdit_nom_base"))
        self.horizontalLayout.addWidget(self.lineEdit_nom_base)
        self.label_nom_base_extension = QtGui.QLabel(Dialog)
        self.label_nom_base_extension.setObjectName(_fromUtf8("label_nom_base_extension"))
        self.horizontalLayout.addWidget(self.label_nom_base_extension)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_test = QtGui.QLabel(Dialog)
        self.label_test.setObjectName(_fromUtf8("label_test"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_test)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.checkBox_test = QtGui.QCheckBox(Dialog)
        self.checkBox_test.setText(_fromUtf8(""))
        self.checkBox_test.setObjectName(_fromUtf8("checkBox_test"))
        self.horizontalLayout_5.addWidget(self.checkBox_test)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_explication.setText(_translate("Dialog", "TextLabel", None))
        self.label_basepath.setText(_translate("Dialog", "TextLabel", None))
        self.pushButton_base.setText(_translate("Dialog", "Modifier", None))
        self.label_basepath1.setText(_translate("Dialog", "TextLabel", None))
        self.label_basepath2.setText(_translate("Dialog", "TextLabel", None))
        self.label_basename.setText(_translate("Dialog", "TextLabel", None))
        self.label_nom_base_extension.setText(_translate("Dialog", "TextLabel", None))
        self.label_test.setText(_translate("Dialog", "Session de test", None))

