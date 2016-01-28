# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PublicGoodGameGenderDecision.ui'
#
# Created: Fri Dec  4 10:36:17 2015
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
        Dialog.resize(376, 449)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
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
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.textEdit_explication = QtGui.QTextEdit(Dialog)
        self.textEdit_explication.setMaximumSize(QtCore.QSize(300, 80))
        self.textEdit_explication.setObjectName(_fromUtf8("textEdit_explication"))
        self.horizontalLayout_2.addWidget(self.textEdit_explication)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem4 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.widget_icones = QtGui.QWidget(Dialog)
        self.widget_icones.setObjectName(_fromUtf8("widget_icones"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget_icones)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_grouptype = QtGui.QLabel(self.widget_icones)
        self.label_grouptype.setObjectName(_fromUtf8("label_grouptype"))
        self.verticalLayout.addWidget(self.label_grouptype)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_icon_1 = QtGui.QLabel(self.widget_icones)
        self.label_icon_1.setText(_fromUtf8(""))
        self.label_icon_1.setPixmap(QtGui.QPixmap(_fromUtf8("../PublicGoodGameGenderImg/femme.jpg")))
        self.label_icon_1.setObjectName(_fromUtf8("label_icon_1"))
        self.horizontalLayout_4.addWidget(self.label_icon_1)
        self.label_icon_2 = QtGui.QLabel(self.widget_icones)
        self.label_icon_2.setText(_fromUtf8(""))
        self.label_icon_2.setPixmap(QtGui.QPixmap(_fromUtf8("../PublicGoodGameGenderImg/femme.jpg")))
        self.label_icon_2.setObjectName(_fromUtf8("label_icon_2"))
        self.horizontalLayout_4.addWidget(self.label_icon_2)
        self.label_icon_3 = QtGui.QLabel(self.widget_icones)
        self.label_icon_3.setText(_fromUtf8(""))
        self.label_icon_3.setPixmap(QtGui.QPixmap(_fromUtf8("../PublicGoodGameGenderImg/homme.jpg")))
        self.label_icon_3.setObjectName(_fromUtf8("label_icon_3"))
        self.horizontalLayout_4.addWidget(self.label_icon_3)
        self.label_icon_4 = QtGui.QLabel(self.widget_icones)
        self.label_icon_4.setText(_fromUtf8(""))
        self.label_icon_4.setPixmap(QtGui.QPixmap(_fromUtf8("../PublicGoodGameGenderImg/homme.jpg")))
        self.label_icon_4.setObjectName(_fromUtf8("label_icon_4"))
        self.horizontalLayout_4.addWidget(self.label_icon_4)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5.addWidget(self.widget_icones)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        spacerItem8 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem8)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem9)
        self.label_decision = QtGui.QLabel(Dialog)
        self.label_decision.setObjectName(_fromUtf8("label_decision"))
        self.horizontalLayout_3.addWidget(self.label_decision)
        self.spinBox_decision = QtGui.QSpinBox(Dialog)
        self.spinBox_decision.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_decision.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.spinBox_decision.setObjectName(_fromUtf8("spinBox_decision"))
        self.horizontalLayout_3.addWidget(self.spinBox_decision)
        spacerItem10 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem10)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem11 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem11)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_periode.setText(_translate("Dialog", "Période 0", None))
        self.pushButton_historique.setText(_translate("Dialog", "Historique", None))
        self.textEdit_explication.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Texte explication</p></body></html>", None))
        self.label_grouptype.setText(_translate("Dialog", "Composition de votre groupe", None))
        self.label_decision.setText(_translate("Dialog", "Texte décision", None))

