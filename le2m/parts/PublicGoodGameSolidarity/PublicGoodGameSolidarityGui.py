# -*- coding: utf-8 -*-
"""
Ce module contient les boites de dialogue du programme.
"""

from PyQt4 import QtGui, QtCore
import logging
from client.cltgui.cltguidialogs import GuiHistorique
import PublicGoodGameSolidarityParams as pms
import PublicGoodGameSolidarityTexts as textes
from server.servgui.servguidialogs import GuiPayoffs
from twisted.internet import defer
from client.cltgui.cltguiwidgets import WPeriod, WExplication, WSpinbox, \
    WCombo, WRadio


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
            text=textes.DECISION_explication, parent=self, size=(450, 60))
        layout.addWidget(self._widexplication)

        self._widdecision = WSpinbox(
            label=textes.DECISION_label, minimum=pms.DECISION_MIN,
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
        self.setWindowTitle(textes.DECISION_titre)
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
                self, textes.DECISION_confirmation.titre,
                textes.DECISION_confirmation.message,
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes: 
                return
        logger.info(u"Decision callback {}".format(decision))
        self._defered.callback(decision)
        self.accept()


class DConfigure(QtGui.QDialog):
    def __init__(self, parent):
        super(DConfigure, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)

        treats = pms.get_treatments()
        self._widtreat = WCombo(
            label=u"Traitement",
            items=[treats[k] for k in sorted(treats.viewkeys())],
            parent=self)
        self._widtreat.ui.comboBox.setCurrentIndex(pms.TRAITEMENT)
        layout.addWidget(self._widtreat)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setWindowTitle("Configuration")
        self.adjustSize()
        self.setFixedSize(self.size())

    def get_infos(self):
        return self._widtreat.get_currentindex()


class DGains(GuiPayoffs):
    def __init__(self, le2mserver, gains_txt, textes_finaux, gains):
        GuiPayoffs.__init__(self, le2mserver, "PublicGoodGameSolidarity",
                            gains_txt)

        self._textes_finaux = textes_finaux
        self._gains = gains
        self._le2mserv = le2mserver
        self.ui.pushButton_afficher.clicked.disconnect(self._display_onremotes)
        self.ui.pushButton_afficher.clicked.connect(
            lambda _: self._display_onremotes2())

    @defer.inlineCallbacks
    def _display_onremotes2(self):
        if not self._textes_finaux:
            return
        confirm = self._le2mserv.gestionnaire_graphique.question(
            u"Afficher les gains sur les postes?")
        if not confirm:
            return
        for j in self._le2mserv.gestionnaire_joueurs.get_players("base"):
            yield (j.display_information(self._textes_finaux[j.joueur]))

    def _add_tofinalpayoffs(self):
        if not self._gains:
            return
        for k, v in self._gains.iteritems():
            k.get_part("base").paiementFinal += float(v)
        self._le2mserv.gestionnaire_base.enregistrer()
        self._le2mserv.gestionnaire_graphique.infoserv(
            u"Gains de TeamCommunication ajoutés aux gains finaux", fg="red")


class DVote(QtGui.QDialog):
    def __init__(self, defered, automatique, parent):
        super(DVote, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        self._widexplication = WExplication(
            text=textes.VOTE_explication, parent=self)
        layout.addWidget(self._widexplication)

        self._widvote = WRadio(
            label=u"Votre vote",
            texts=[pms.VOTE_CODE.get(k) for k in
                   sorted(pms.VOTE_CODE.viewkeys())],
            automatique=self._automatique, parent=self)
        layout.addWidget(self._widvote)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer.start(7000)

        self.setWindowTitle(u"Vote")
        self.adjustSize()
        self.setFixedSize(self.size())

    def reject(self):
        pass

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass
        try:
            dec = self._widvote.get_checkedbutton()
        except ValueError:
            QtGui.QMessageBox.warning(
                self, u"Attention", u"Il faut prendre une décision")
            return
        logger.info(u"Send back {}".format(pms.get_vote(dec)))
        self.accept()
        self._defered.callback(dec)
