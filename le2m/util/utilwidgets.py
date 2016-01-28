#! /usr/bin/env python2.7
# coding: utf-8

import sys
import os
from PyQt4 import QtGui, QtCore
import random
from utiltools import get_parent_folder
from utilgui import widDice, widRandint, widHeadTail
from configuration.configconst import PILE, FACE


class WDice(QtGui.QWidget):
    def __init__(self, speed=10, tries=1, automatique=False, parent=None,
                 autotime=2000):
        """

        :param speed:
        :param tries: 0=infinity
        :return:
        """
        super(WDice, self).__init__(parent)
        self._automatique = automatique

        self.ui = widDice.Ui_Form()
        self.ui.setupUi(self)

        self._speed = speed
        self._tries = tries
        self._currenttry = 0
        des = [QtGui.QPixmap(os.path.join(
            get_parent_folder(__file__), "utilgui", "img", "de_{}.png".format(i)))
               for i in range(1, 7)]
        self._des = dict(zip(range(1, 7), des))

        self._currentpix = self._des[1]
        self.ui.label_de.setPixmap(self._currentpix)

        stylesheet = \
            "QPushButton {width: 60; height: 20; border: 1px ridge gray;}"
        self.ui.pushButton_start.setStyleSheet(stylesheet)
        self.ui.pushButton_start.clicked.connect(self._start)
        self.ui.pushButton_stop.setStyleSheet(stylesheet)
        self.ui.pushButton_stop.clicked.connect(self._stop)
        self.ui.pushButton_stop.setEnabled(False)

        if self._automatique:
            self._start()
            self._timerAuto = QtCore.QTimer()
            self._timerAuto.timeout.connect(self.ui.pushButton_stop.click)
            self._timerAuto.start(autotime)
        self.adjustSize()

    def _start(self):
        self.ui.pushButton_stop.setEnabled(True)
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._changepix)
        self._timer.start(self._speed)

    def _changepix(self):
        self._currentpix = self._des[random.randint(1, 6)]
        self.ui.label_de.setPixmap(self._currentpix)

    def _stop(self):
        try:
            self._timerAuto.stop()
        except AttributeError:
            pass
        self._timer.stop()
        self._currenttry += 1
        if self._currenttry == self._tries:
            self.ui.pushButton_start.setEnabled(False)
            self.ui.pushButton_stop.setEnabled(False)

    def get_dicevalue(self):
        for k, v in self._des.iteritems():
            if v == self._currentpix:
                return k


class WRandint(QtGui.QWidget):
    def __init__(self, parent=None, minimum=0, maximum=100, speed=10, tries=1,
                 automatique=False, autotime=2000):
        super(WRandint, self).__init__(parent)

        self._minimum = minimum
        self._maximum = maximum
        self._speed = speed
        self._tries = tries
        self._currenttry = 0
        self._automatique = automatique

        self.ui = widRandint.Ui_Form()
        self.ui.setupUi(self)
        self.ui.spinBox_min.setValue(self._minimum)
        self.ui.spinBox_max.setValue(self._maximum)

        stylesheet = \
            "QPushButton {width: 60; height: 20; border: 1px ridge gray;}"
        self.ui.pushButton_start.setStyleSheet(stylesheet)
        self.ui.pushButton_start.clicked.connect(self._start)
        self.ui.pushButton_stop.setStyleSheet(stylesheet)
        self.ui.pushButton_stop.clicked.connect(self._stop)
        self.ui.pushButton_stop.setEnabled(False)

        self.adjustSize()

        if self._automatique:
            self._start()
            self._timerAuto = QtCore.QTimer()
            self._timerAuto.timeout.connect(self.ui.pushButton_stop.click)
            self._timerAuto.start(autotime)

    def _start(self):
        self.ui.pushButton_stop.setEnabled(True)
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._changevalue)
        self._timer.start(self._speed)

    def _changevalue(self):
        self.ui.lcdNumber.display(
            random.randint(self.ui.spinBox_min.value(),
                           self.ui.spinBox_max.value()))

    def _stop(self):
        try:
            self._timerAuto.stop()
        except AttributeError:
            pass
        self._timer.stop()
        self._currenttry += 1
        if self._currenttry == self._tries:
            self.ui.pushButton_start.setEnabled(False)
            self.ui.pushButton_stop.setEnabled(False)

    def get_value(self):
        return self.ui.lcdNumber.value()


class WHeadtail(QtGui.QWidget):
    def __init__(self, parent=None, speed=10, tries=1,
                 automatique=False, autotime=2000):
        super(WHeadtail, self).__init__(parent)

        self._speed = speed
        self._tries = tries
        self._currenttry = 0
        self._automatique = automatique

        self.ui = widHeadTail.Ui_Form()
        self.ui.setupUi(self)
        self._pile = QtGui.QPixmap(
            os.path.join(get_parent_folder(__file__),
                         "utilgui", "img", "pile.png"))
        self._face = QtGui.QPixmap(
            os.path.join(get_parent_folder(__file__),
                         "utilgui", "img", "face.png"))
        self.ui.label.setPixmap(self._pile)
        self._current = self._pile

        self.ui.pushButton_start.clicked.connect(self._start)
        self.ui.pushButton_stop.clicked.connect(self._stop)
        self.ui.pushButton_stop.setEnabled(False)

        self.adjustSize()

        if self._automatique:
            self._start()
            self._timerAuto = QtCore.QTimer()
            self._timerAuto.timeout.connect(self.ui.pushButton_stop.click)
            self._timerAuto.start(autotime)

    def _start(self):
        self.ui.pushButton_stop.setEnabled(True)
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._changevalue)
        self._timer.start(self._speed)

    def _changevalue(self):
        self._current = self._pile if self._current is self._face else self._face
        self.ui.label.setPixmap(self._current)

    def _stop(self):
        try:
            self._timerAuto.stop()
        except AttributeError:
            pass
        self._timer.stop()
        self._currenttry += 1
        if self._currenttry == self._tries:
            self.ui.pushButton_start.setEnabled(False)
            self.ui.pushButton_stop.setEnabled(False)

    def get_value(self):
        return PILE if self._current is self._pile else FACE


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    wde = WHeadtail(tries=0)
    wde.show()
    sys.exit(app.exec_())
