# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import logging
from util.utili18n import le2mtrans
from client.cltgui.cltguiwidgets import WExplication, WSpinbox, WCombo
import GneezyPotterParams as pms
import GneezyPotterTexts as texts_GP
from GneezyPotterTexts import trans_GP


logger = logging.getLogger("le2m")


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, periode, historique):
        super(GuiDecision, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        self._widexplication = WExplication(
            text=texts_GP.get_text_explanation(), size=(500, 70), parent=self)
        layout.addWidget(self._widexplication)

        self._widdecision = WSpinbox(
            label=trans_GP(u"Choose the amount you want to invest in the "
                           u"risky option"),
            minimum=pms.DECISION_MIN, maximum=pms.DECISION_MAX,
            interval=pms.DECISION_STEP, parent=self,
            automatique=self._automatique)
        layout.addWidget(self._widdecision)

        # bouton box
        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)

        # title and size
        self.setWindowTitle(le2mtrans(u"Decision"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def reject(self):
        pass
    
    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        decision = self._widdecision.get_value()
        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, le2mtrans(u"Confirmation"),
                le2mtrans(u"Do you confirm your choice?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes: 
                return
        logger.info(u"Send back {}".format(decision))
        self.accept()
        self._defered.callback(decision)


class GuiConfigure(QtGui.QDialog):
    def __init__(self, parent=None):
        super(GuiConfigure, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)

        self._widpayoffs = WCombo(
            label=trans_GP(u"Display summary (with payoffs)?"),
            items=(trans_GP(u"No"), trans_GP(u"Yes")), parent=self)
        layout.addWidget(self._widpayoffs)

        button = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        button.accepted.connect(self.accept)
        layout.addWidget(button)

        self.setWindowTitle(trans_GP(u"Configure"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def get_responses(self):
        return self._widpayoffs.get_currentindex()