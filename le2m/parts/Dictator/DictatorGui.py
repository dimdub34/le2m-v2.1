# -*- coding: utf-8 -*-
"""
Ce module contient les boites de dialogue du programme.
"""

from PyQt4 import QtGui, QtCore
import logging
from client.cltgui.cltguiwidgets import WExplication, WSpinbox, WCombo
import DictatorParams as pms
import DictatorTexts as textes


logger = logging.getLogger("le2m")


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, periode, historique):
        super(GuiDecision, self).__init__(parent)

        # variables
        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        self._widexplication = WExplication(
            text=textes.DECISION_explication, parent=self, size=(520, 60))
        layout.addWidget(self._widexplication)

        self._widdecision = WSpinbox(
            label=textes.DECISION_label, minimum=pms.DECISION_MIN,
            maximum=pms.DECISION_MAX, parent=self,
            automatique=self._automatique)
        layout.addWidget(self._widdecision)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        # title and size
        self.setWindowTitle(textes.DECISION_titre)
        self.adjustSize()
        self.setFixedSize(self.size())

        # automatic
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
        decision = self._widdecision.get_value()
        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, textes.DECISION_confirmation.titre,
                textes.DECISION_confirmation.message,
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes: 
                return
        logger.info(u"Send back {}".format(decision))
        self.accept()
        self._defered.callback(decision)


class DConfigure(QtGui.QDialog):
    def __init__(self, parent=None):
        super(DConfigure, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)

        game = pms.get_game()
        gamekeys = game.keys()
        gamekeys.sort()
        self._widgame = WCombo(label=u"Jeu", items=[game[k] for k in gamekeys],
                               parent=self)
        self._game = pms.GAME
        self._widgame.ui.comboBox.setCurrentIndex(self._game)
        layout.addWidget(self._widgame)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self._accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setWindowTitle(u"Configuration")
        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        self._game = self._widgame.get_currentindex()
        self.accept()

    def get_game(self):
        return self._game
