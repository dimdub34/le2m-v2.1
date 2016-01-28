# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'waiting_screen.ui'
#
# Created: Mon Jul 11 09:21:37 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_WaitingScreen(object):
    def setupUi(self, WaitingScreen):
        WaitingScreen.setObjectName(_fromUtf8("WaitingScreen"))
        WaitingScreen.resize(1024, 768)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WaitingScreen.sizePolicy().hasHeightForWidth())
        WaitingScreen.setSizePolicy(sizePolicy)
        WaitingScreen.setMinimumSize(QtCore.QSize(1024, 768))
        self.verticalLayout = QtGui.QVBoxLayout(WaitingScreen)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lbl_waiting = QtGui.QLabel(WaitingScreen)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(75)
        font.setBold(True)
        self.lbl_waiting.setFont(font)
        self.lbl_waiting.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_waiting.setObjectName(_fromUtf8("lbl_waiting"))
        self.horizontalLayout.addWidget(self.lbl_waiting)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(WaitingScreen)
        QtCore.QMetaObject.connectSlotsByName(WaitingScreen)

    def retranslateUi(self, WaitingScreen):
        WaitingScreen.setWindowTitle(QtGui.QApplication.translate("WaitingScreen", "Waiting", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_waiting.setText(QtGui.QApplication.translate("WaitingScreen", "Veuillez patienter ...", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    WaitingScreen = QtGui.QWidget()
    ui = Ui_WaitingScreen()
    ui.setupUi(WaitingScreen)
    WaitingScreen.show()
    sys.exit(app.exec_())

