# -*- coding: utf-8 -*-
"""
Ce module contient les boites de dialogue du programme.
"""

import logging
from PyQt4 import QtGui, QtCore
from client.cltgui.cltguidialogs import GuiHistorique
import CommonPoolResourceParams as pms
import CommonPoolResourceTexts as texts_CPR
from client.cltgui.cltguiwidgets import WPeriod, WExplication, WSpinbox


logger = logging.getLogger("le2m")


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, periode, historique):
        super(GuiDecision, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique
        self._historique = GuiHistorique(self, historique)

        layout = QtGui.QVBoxLayout(self)

        self._widperiod = WPeriod(
            period=periode, ecran_historique=self._historique, parent=self)
        layout.addWidget(self._widperiod)

        self._widexplication = WExplication(
            text=texts_CPR.DECISION_explication, parent=self)
        layout.addWidget(self._widexplication)

        self._widdecision = WSpinbox(
            label=texts_CPR.DECISION_label, minimum=pms.DECISION_MIN,
            maximum=pms.DECISION_MAX, interval=pms.DECISION_STEP,
            automatique=self._automatique, parent=self)
        layout.addWidget(self._widdecision)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)

        # title and size
        self.setWindowTitle(texts_CPR.DECISION_titre)
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
                self, texts_CPR.DECISION_confirmation.titre,
                texts_CPR.DECISION_confirmation.message,
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes: 
                return
        self.accept()
        self._defered.callback(decision)

