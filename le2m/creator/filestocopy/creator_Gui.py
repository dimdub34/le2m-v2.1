# -*- coding: utf-8 -*-
"""
This module contains the GUI
"""

import logging
from PyQt4 import QtGui, QtCore
from util.utili18n import le2mtrans
import EXPERIENCE_NOMParams as pms
from EXPERIENCE_NOMTexts import trans_EXPERIENCE_NOM_COURT
import EXPERIENCE_NOMTexts as texts_EXPERIENCE_NOM_COURT
from client.cltgui.cltguidialogs import GuiHistorique
from client.cltgui.cltguiwidgets import WPeriod, WExplication, WSpinbox


logger = logging.getLogger("le2m")


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, period, historique):
        super(GuiDecision, self).__init__(parent)

        # variables
        self._defered = defered
        self._automatique = automatique
        self._historique = GuiHistorique(self, historique)

        layout = QtGui.QVBoxLayout(self)

        # should be removed if one-shot game
        wperiod = WPeriod(
            period=period, ecran_historique=self._historique)
        layout.addWidget(wperiod)

        wexplanation = WExplication(
            text=texts_EXPERIENCE_NOM_COURT.get_text_explanation(),
            size=(450, 80), parent=self)
        layout.addWidget(wexplanation)

        self._wdecision = WSpinbox(
            label=trans_EXPERIENCE_NOM_COURT(u"label decision"),
            minimum=pms.DECISION_MIN, maximum=pms.DECISION_MAX,
            interval=pms.DECISION_STEP, automatique=self._automatique,
            parent=self)
        layout.addWidget(self._wdecision)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(trans_EXPERIENCE_NOM_COURT(u"Title"))
        self.adjustSize()
        self.setFixedSize(self.size())

        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)
                
    def reject(self):
        pass
    
    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        decision = self._wdecision.get_value()
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
