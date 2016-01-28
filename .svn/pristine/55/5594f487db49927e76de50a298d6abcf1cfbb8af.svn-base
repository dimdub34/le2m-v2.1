# -*- coding: utf-8 -*-
"""
Ce module contient les boites de dialogue du programme.
"""

from PyQt4 import QtGui, QtCore
import logging
from client.cltgui.cltguiwidgets import WExplication, WCombo, WSpinbox
from util.dice import dice
import oathAndLiesParams as pms
import oathAndLiesTexts as texts
from oathAndLiesGuiSrc import OL_widgains


logger = logging.getLogger("le2m")


class DConfiguration(QtGui.QDialog):
    def __init__(self, parent):
        super(DConfiguration, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)
        self._widtreat = WCombo(
            label=u"Traitement", items=["SANS_SERMENT", "AVEC_SERMENT"],
            parent=self)
        layout.addWidget(self._widtreat)

        self._widgame = WCombo(
            label=u"Sélectionner le jeu",
            items=map(str, sorted(pms.CODES_PERIODES.viewkeys())), parent=self)
        self._widgame.ui.comboBox.setCurrentIndex(pms.GAME - 1)
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
        self._infos = {
            "treatment": self._widtreat.get_currentindex(),
            "game": self._widgame.get_currentindex() + 1}
        self.accept()

    def get_infos(self):
        return self._infos


class WGains(QtGui.QWidget):
    def __init__(self, automatique=False, parent=None, autotime=1000):
        super(WGains, self).__init__(parent)
        self.ui = OL_widgains.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_x.setText(u"Option X:")
        self.ui.label_y.setText(u"Option Y:")
        if automatique:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(self.ui.pushButton_ok.click)
            self._timer.start(autotime)


class DDecisionA(QtGui.QDialog):
    def __init__(self, defered, automatique, parent):
        super(DDecisionA, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        self._widexplication = WExplication(
            parent=self, text=texts.get_explication(pms.JOUEUR_A),
            size=(450, 80))
        layout.addWidget(self._widexplication)

        self._widgains = WGains(automatique=self._automatique, parent=self)
        self._widgains.ui.pushButton_ok.clicked.connect(
            lambda _: self._widdice.setEnabled(True))
        layout.addWidget(self._widgains)

        self._widdice = dice.WDice(automatique=self._automatique, parent=self,
                                   tries=1, speed=10, autotime=2000)
        self._widdice.ui.pushButton_stop.clicked.connect(
            lambda _: self._widmessage.setEnabled(True))
        layout.addWidget(self._widdice)
        self._widdice.setEnabled(False)

        messages = [u"Choisir"]
        messages.extend([u"Le résultat du lancé de dé est {}".format(i) for
                         i in range(1, 7)])
        self._widmessage = WCombo(
            label=u"Sélectionnez le message que vous transmettez au joueur B",
            items=messages, automatique=self._automatique, parent=self,
            autotime=4000)
        self._widmessage.ui.comboBox.currentIndexChanged.connect(
            lambda x: buttons.setEnabled(x))
        layout.addWidget(self._widmessage)
        self._widmessage.setEnabled(False)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)
        buttons.setEnabled(False)

        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer.start(8000)

        self.setWindowTitle(u"Décision")
        self.adjustSize()
        self.setFixedSize(self.size())

    def reject(self):
        pass

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass
        if not self._automatique:
            conf = QtGui.QMessageBox.question(
                self, u"Confirmation", u"Vous confirmez votre choix?",
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if conf != QtGui.QMessageBox.Yes:
                return
        dec = {"dice": self._widdice.get_dicevalue(),
               "message": self._widmessage.get_currentindex()}
        logger.info(u"Send back {}".format(dec))
        self.accept()
        self._defered.callback(dec)


class DDecisionB(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, message):
        super(DDecisionB, self).__init__(parent)
        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        self._widExplication = WExplication(
            text=texts.get_explication(pms.JOUEUR_B), parent=self,
            size=(450, 80))
        layout.addWidget(self._widExplication)

        layout_message = QtGui.QHBoxLayout()
        layout_message.addSpacerItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        self._labelMessage = QtGui.QLabel(
            u"Message de A: le résultat du lancé de dé est {}".format(message))
        layout_message.addWidget(self._labelMessage)
        layout_message.addSpacerItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        layout.addLayout(layout_message)

        self._widDecision = WSpinbox(
            label=u"Choisissez un nombre", minimum=1, maximum=6,
            automatique=self._automatique, parent=self)
        layout.addWidget(self._widDecision)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer.start(7000)

        self.setWindowTitle(u"Décision")
        self.adjustSize()
        self.setFixedSize(self.size())

    def reject(self):
        pass

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass
        if not self._automatique:
            conf = QtGui.QMessageBox.question(
                self, u"Confirmation", u"Vous confirmez votre choix?",
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if conf != QtGui.QMessageBox.Yes:
                return
        dec = self._widDecision.get_value()
        logger.info(u"Send back {}".format(dec))
        self.accept()
        self._defered.callback(dec)

