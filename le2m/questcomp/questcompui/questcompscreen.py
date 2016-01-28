# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'questcompscreen.ui'
#
# Created: Thu Sep 10 10:43:27 2015
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(274, 562)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeWidget_questionnaire = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget_questionnaire.setMinimumSize(QtCore.QSize(0, 500))
        self.treeWidget_questionnaire.setObjectName(_fromUtf8("treeWidget_questionnaire"))
        self.treeWidget_questionnaire.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout.addWidget(self.treeWidget_questionnaire)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 274, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_nouveau = QtGui.QAction(MainWindow)
        self.action_nouveau.setObjectName(_fromUtf8("action_nouveau"))
        self.action_ouvrir = QtGui.QAction(MainWindow)
        self.action_ouvrir.setObjectName(_fromUtf8("action_ouvrir"))
        self.action_enregistrer = QtGui.QAction(MainWindow)
        self.action_enregistrer.setObjectName(_fromUtf8("action_enregistrer"))
        self.action_enregistrer_sous = QtGui.QAction(MainWindow)
        self.action_enregistrer_sous.setObjectName(_fromUtf8("action_enregistrer_sous"))
        self.action_imprimer = QtGui.QAction(MainWindow)
        self.action_imprimer.setObjectName(_fromUtf8("action_imprimer"))
        self.action_fermer = QtGui.QAction(MainWindow)
        self.action_fermer.setObjectName(_fromUtf8("action_fermer"))
        self.action_quitter = QtGui.QAction(MainWindow)
        self.action_quitter.setObjectName(_fromUtf8("action_quitter"))
        self.action_nouvelle_question = QtGui.QAction(MainWindow)
        self.action_nouvelle_question.setObjectName(_fromUtf8("action_nouvelle_question"))
        self.action_a_propos = QtGui.QAction(MainWindow)
        self.action_a_propos.setObjectName(_fromUtf8("action_a_propos"))
        self.action_aide = QtGui.QAction(MainWindow)
        self.action_aide.setObjectName(_fromUtf8("action_aide"))
        self.action_tester = QtGui.QAction(MainWindow)
        self.action_tester.setObjectName(_fromUtf8("action_tester"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "LE2M_comprehension", None))
        self.action_nouveau.setText(_translate("MainWindow", "Nouveau", None))
        self.action_ouvrir.setText(_translate("MainWindow", "Ouvrir", None))
        self.action_enregistrer.setText(_translate("MainWindow", "Enregistrer", None))
        self.action_enregistrer_sous.setText(_translate("MainWindow", "Enregistrer sous", None))
        self.action_imprimer.setText(_translate("MainWindow", "Imprimer", None))
        self.action_fermer.setText(_translate("MainWindow", "Fermer", None))
        self.action_quitter.setText(_translate("MainWindow", "Quitter", None))
        self.action_nouvelle_question.setText(_translate("MainWindow", "Nouvelle question", None))
        self.action_a_propos.setText(_translate("MainWindow", "A propos", None))
        self.action_aide.setText(_translate("MainWindow", "Aide", None))
        self.action_tester.setText(_translate("MainWindow", "Tester le questionnaire", None))

