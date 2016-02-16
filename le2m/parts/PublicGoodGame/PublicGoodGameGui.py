# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import logging
from client.cltgui.cltguidialogs import GuiHistorique
from client.cltgui.cltguiwidgets import WExplication, WPeriod, WSpinbox
from util.utili18n import le2mtrans
import PublicGoodGameParams as pms
import PublicGoodGameTexts as textes_PGG
from PublicGoodGameTexts import trans_PGG


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
            text=textes_PGG.get_text_explanation(),
            parent=self, size=(450, 80))
        layout.addWidget(wexplanation)

        self._wdecision = WSpinbox(
            label=trans_PGG(u"How much token(s) do you want to put in the "
                            u"public account?"),
            minimum=pms.DECISION_MIN, maximum=pms.DECISION_MAX,
            interval=pms.DECISION_STEP, automatique=self._automatique,
            parent=self)
        layout.addWidget(self._wdecision)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(trans_PGG(u"Decision"))
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
        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, le2mtrans(u"Confirmation"),
                le2mtrans(u"Do you confirm your choice?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes: 
                return
        decision = self._wdecision.get_value()
        logger.info(u"Decision callback {}".format(decision))
        self.accept()
        self._defered.callback(decision)
