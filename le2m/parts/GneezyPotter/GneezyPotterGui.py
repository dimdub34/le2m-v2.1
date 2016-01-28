# -*- coding: utf-8 -*-
"""
Ce module contient les boites de dialogue du programme.
"""

from PyQt4 import QtGui, QtCore
import logging
from client.cltgui.cltguiwidgets import WExplication, WSpinbox, WCombo
import GneezyPotterParams as pms
import GneezyPotterTexts as texts
from GneezyPotterTexts import _GP


logger = logging.getLogger("le2m")


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, periode, historique):
        super(GuiDecision, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        self._widexplication = WExplication(
            text=texts.DECISION_explication, size=(500, 70), parent=self)
        layout.addWidget(self._widexplication)

        self._widdecision = WSpinbox(
            label=texts.DECISION_label, minimum=pms.DECISION_MIN,
            maximum=pms.DECISION_MAX, interval=pms.DECISION_STEP,
            parent=self, automatique=self._automatique)
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
        self.setWindowTitle(texts.DECISION_titre)
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
                self, texts.DECISION_confirmation.titre,
                texts.DECISION_confirmation.message,
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes
            )
            if confirmation != QtGui.QMessageBox.Yes: 
                return
        logger.info(u"Send back {}".format(decision))
        self._defered.callback(decision)
        self.accept()


class GuiConfigure(QtGui.QDialog):
    def __init__(self, parent=None):
        super(GuiConfigure, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)

        self._widpayoffs = WCombo(
            label=_GP(u"Display summary (with payoffs)?"),
            items=(_GP(u"No"), _GP(u"Yes")), parent=self)
        layout.addWidget(self._widpayoffs)

        button = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        button.accepted.connect(self.accept)
        layout.addWidget(button)

        self.setWindowTitle(_GP(u"Configure"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def get_responses(self):
        return self._widpayoffs.get_currentindex()