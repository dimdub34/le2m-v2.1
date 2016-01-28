#! /usr/bin/env python2.7
# coding: utf-8

import sys
from PyQt4 import QtGui
from client.cltgui.cltguisrc.cltguisrcwid import widCompterebours
# from client.cltgui.cltguiwidgets import WCompterebours
from datetime import time, timedelta
from util.utiltools import CompteARebours


class WCompterebours(QtGui.QWidget):
    """

    """
    def __init__(self, parent, temps, actionfin):
        """
        :param parent:
        :param temps: datetime.time(0, 2, 0)  # heures, minutes, secondes
        :param actionfin:
        :return:
        """
        super(WCompterebours, self).__init__(parent)
        self.ui = widCompterebours.Ui_Form()
        self.ui.setupUi(self)

        self.ui.label.setText(u"Temps restant")
        tps = timedelta(hours=temps.hour, minutes=temps.minute,
                        seconds=temps.second).seconds
        self.compterebours = CompteARebours(tps)
        self.compterebours.changetime[str].connect(self.ui.label_timer.setText)
        self.compterebours.endoftime.connect(actionfin)
        self.compterebours.start()


class TestCompteRebours(QtGui.QDialog):
    def __init__(self):
        super(TestCompteRebours, self).__init__()
        layout = QtGui.QVBoxLayout(self)

        self._widcompterebours = WCompterebours(
            self, time(0, 0, 30), self._displayfin)
        layout.addWidget(self._widcompterebours)

    def _displayfin(self):
        QtGui.QMessageBox.information(self, u"Fin", u"Ok")
        self.accept()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    screen = TestCompteRebours()
    screen.show()
    sys.exit(app.exec_())