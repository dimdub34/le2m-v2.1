# -*- coding: utf-8 -*-

import logging
from PyQt4 import QtGui, QtCore
from util.utili18n import le2mtrans
from client.cltgui.cltguiwidgets import WPeriod, WExplication, WRadio
from client.cltgui.cltguidialogs import GuiHistorique
import prisonnersDilemmaTexts as texts_DP
from prisonnersDilemmaTexts import trans_DP
import prisonnersDilemmaParams as pms


logger = logging.getLogger("le2m")


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, periode, historique):
        super(GuiDecision, self).__init__(parent)

        # variables
        self._defered = defered
        self._automatique = automatique
        self._historique = GuiHistorique(self, historique)

        layout = QtGui.QVBoxLayout(self)

        wperiod = WPeriod(period=periode, ecran_historique=self._historique,
                          parent=self)
        layout.addWidget(wperiod)

        wexplanation = WExplication(
            text=texts_DP.get_text_explanation(), parent=self, size=(450, 80))
        layout.addWidget(wexplanation)

        options = tuple([v for k, v in sorted(pms.OPTIONS.viewitems())])
        self._wdecision = WRadio(
            texts=options, label=trans_DP(u"Choose an option"),
            parent=self, automatique=self._automatique)
        layout.addWidget(self._wdecision)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Decision"))
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
        try:
            decision = self._wdecision.get_checkedbutton()
        except ValueError:
            QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"),
                trans_DP(u"You have to choose an option"))
            return

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
