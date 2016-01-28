# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TeamCommunicationAddictionnalquestions.ui'
#
# Created: Wed Nov  4 08:50:09 2015
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
        Dialog.resize(675, 211)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_reponses = QtGui.QWidget(Dialog)
        self.widget_reponses.setObjectName(_fromUtf8("widget_reponses"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_reponses)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_reponses = QtGui.QLabel(self.widget_reponses)
        self.label_reponses.setObjectName(_fromUtf8("label_reponses"))
        self.horizontalLayout_3.addWidget(self.label_reponses)
        self.spinBox_reponses = QtGui.QSpinBox(self.widget_reponses)
        self.spinBox_reponses.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBox_reponses.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.spinBox_reponses.setObjectName(_fromUtf8("spinBox_reponses"))
        self.horizontalLayout_3.addWidget(self.spinBox_reponses)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addWidget(self.widget_reponses)
        self.widget_infosatisfaction = QtGui.QWidget(Dialog)
        self.widget_infosatisfaction.setObjectName(_fromUtf8("widget_infosatisfaction"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_infosatisfaction)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_infosatisfaction = QtGui.QLabel(self.widget_infosatisfaction)
        self.label_infosatisfaction.setObjectName(_fromUtf8("label_infosatisfaction"))
        self.horizontalLayout_2.addWidget(self.label_infosatisfaction)
        self.horizontalSlider_infosatisfaction = QtGui.QSlider(self.widget_infosatisfaction)
        self.horizontalSlider_infosatisfaction.setMinimum(1)
        self.horizontalSlider_infosatisfaction.setMaximum(7)
        self.horizontalSlider_infosatisfaction.setSliderPosition(4)
        self.horizontalSlider_infosatisfaction.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_infosatisfaction.setTickPosition(QtGui.QSlider.TicksBelow)
        self.horizontalSlider_infosatisfaction.setTickInterval(1)
        self.horizontalSlider_infosatisfaction.setObjectName(_fromUtf8("horizontalSlider_infosatisfaction"))
        self.horizontalLayout_2.addWidget(self.horizontalSlider_infosatisfaction)
        self.lcdNumber_infosatisfaction = QtGui.QLCDNumber(self.widget_infosatisfaction)
        self.lcdNumber_infosatisfaction.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lcdNumber_infosatisfaction.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lcdNumber_infosatisfaction.setFrameShadow(QtGui.QFrame.Sunken)
        self.lcdNumber_infosatisfaction.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumber_infosatisfaction.setProperty("intValue", 4)
        self.lcdNumber_infosatisfaction.setObjectName(_fromUtf8("lcdNumber_infosatisfaction"))
        self.horizontalLayout_2.addWidget(self.lcdNumber_infosatisfaction)
        spacerItem1 = QtGui.QSpacerItem(13, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.widget_infosatisfaction)
        self.widget_jobsatisfaction = QtGui.QWidget(Dialog)
        self.widget_jobsatisfaction.setObjectName(_fromUtf8("widget_jobsatisfaction"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget_jobsatisfaction)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_jobsatisfaction = QtGui.QLabel(self.widget_jobsatisfaction)
        self.label_jobsatisfaction.setObjectName(_fromUtf8("label_jobsatisfaction"))
        self.horizontalLayout.addWidget(self.label_jobsatisfaction)
        self.horizontalSlider_jobsatisfaction = QtGui.QSlider(self.widget_jobsatisfaction)
        self.horizontalSlider_jobsatisfaction.setMinimum(1)
        self.horizontalSlider_jobsatisfaction.setMaximum(7)
        self.horizontalSlider_jobsatisfaction.setSliderPosition(4)
        self.horizontalSlider_jobsatisfaction.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_jobsatisfaction.setTickPosition(QtGui.QSlider.TicksBelow)
        self.horizontalSlider_jobsatisfaction.setTickInterval(1)
        self.horizontalSlider_jobsatisfaction.setObjectName(_fromUtf8("horizontalSlider_jobsatisfaction"))
        self.horizontalLayout.addWidget(self.horizontalSlider_jobsatisfaction)
        self.lcdNumber_jobsatisfaction = QtGui.QLCDNumber(self.widget_jobsatisfaction)
        self.lcdNumber_jobsatisfaction.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lcdNumber_jobsatisfaction.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lcdNumber_jobsatisfaction.setFrameShadow(QtGui.QFrame.Sunken)
        self.lcdNumber_jobsatisfaction.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumber_jobsatisfaction.setProperty("intValue", 4)
        self.lcdNumber_jobsatisfaction.setObjectName(_fromUtf8("lcdNumber_jobsatisfaction"))
        self.horizontalLayout.addWidget(self.lcdNumber_jobsatisfaction)
        spacerItem2 = QtGui.QSpacerItem(128, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.widget_jobsatisfaction)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.horizontalSlider_infosatisfaction, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.lcdNumber_infosatisfaction.display)
        QtCore.QObject.connect(self.horizontalSlider_jobsatisfaction, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.lcdNumber_jobsatisfaction.display)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_reponses.setText(_translate("Dialog", "Parmi vos XX réponses, combien de réponses justes êtes-vous sûr(e) d\'avoir?", None))
        self.label_infosatisfaction.setText(_translate("Dialog", "Sur une échelle de 1 (tout à fait insatisfait) à 7 (tout à fait satisfait), <br />où situez-vous votre niveau de satisfaction par rapport aux informations échangées dans votre groupe?", None))
        self.label_jobsatisfaction.setText(_translate("Dialog", "Sur une échelle de 1 (tout à fait insatisfait) à 7 (tout à fait satisfait),<br />où situez-vous votre niveau de satisfaction par rapport à la tâche", None))

