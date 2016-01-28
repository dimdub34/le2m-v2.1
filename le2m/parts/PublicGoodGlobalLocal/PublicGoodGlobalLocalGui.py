# -*- coding: utf-8 -*-

"""
Module contenant les interfaces graphiques.
Les objects sont des boites de dialogues qui permettent des saisies
Les valeurs saisies sont vérifiées puis, après confirmation, envoyées au serveur
"""

from PyQt4 import QtGui, QtCore
import logging
import random
from twisted.internet import defer, reactor
from collections import namedtuple
import datetime
from client.cltgui.cltguitablemodels import TableModelHistorique
from client.cltgui.cltguidialogs import GuiHistorique

import PublicGoodGlobalLocalParams as pms
import PublicGoodGlobalLocalTextes as texts
from PublicGoodGlobalLocalGuiSrc import PublicGoodGlobalLocalDecision2, \
    PublicGoodGlobalLocalInformation2, PublicGoodGlobalLocalConfiguration, \
    PublicGoodGlobalLocalCommunication
    

logger = logging.getLogger('le2m.{}'.format(__name__))
    

class GuiDecision(QtGui.QDialog):
    """
    Ecran pour la saisie des contributions dans chaque compte
    3 comptes: individuel, local et global
    """
    def __init__(self, defered, automatique, ecran_attente,
                 periode, historique):
        super(GuiDecision, self).__init__(ecran_attente)

        # variables
        self._defered = defered
        self._automatique = automatique
        self._historique = historique

        # création fenetre
        self.ui = PublicGoodGlobalLocalDecision2.Ui_Dialog()
        self.ui.setupUi(self)

        # période et historique
        self.ui.label_periode.setText(texts.PERIODE_label(periode))
        self.ui.pushButton_historique.setText(texts.HISTORIQUE_button)
        self.ui.pushButton_historique.clicked.connect(self._afficher_historique)

        # explication
        self.ui.textEdit_explication.setText(texts.DECISION_explication)
        self.ui.textEdit_explication.setReadOnly(True)
        self.ui.textEdit_explication.setFixedSize(350, 70)

        # cpte indiv
        self.ui.label_decision_individuel.setText(
            texts.DECISION_label_individuel)
        self.ui.spinBox_individuel.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.ui.spinBox_individuel.setMinimum(pms.INDIVIDUEL_MIN)
        self.ui.spinBox_individuel.setMaximum(pms.INDIVIDUEL_MAX)
        self.ui.spinBox_individuel.setSingleStep(pms.INDIVIDUEL_STEP)

        # cpte loc
        self.ui.label_decision_local.setText(texts.DECISION_label_local)
        self.ui.spinBox_local.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.ui.spinBox_local.setMinimum(pms.LOCAL_MIN)
        self.ui.spinBox_local.setMaximum(pms.LOCAL_MAX)
        self.ui.spinBox_local.setSingleStep(pms.LOCAL_STEP)

        # cpte glob
        self.ui.label_decision_global.setText(texts.DECISION_label_global)
        self.ui.spinBox_global.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.ui.spinBox_global.setMinimum(pms.GLOBAL_MIN)
        self.ui.spinBox_global.setMaximum(pms.GLOBAL_MAX)
        self.ui.spinBox_global.setSingleStep(pms.GLOBAL_STEP)

        # boutons ok et cancel
        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Cancel). \
            setVisible(False)

        # automatique
        if self._automatique:
            cind, cloc, cglob = 0, 0, 0
            while cind + cloc + cglob != pms.DOTATION:
                cind = random.randrange(
                    self.ui.spinBox_individuel.minimum(),
                    self.ui.spinBox_individuel.maximum(),
                    self.ui.spinBox_individuel.singleStep())
                cloc = random.randrange(
                    self.ui.spinBox_local.minimum(),
                    self.ui.spinBox_local.maximum(),
                    self.ui.spinBox_local.singleStep())
                cglob = random.randrange(
                    self.ui.spinBox_global.minimum(),
                    self.ui.spinBox_global.maximum(),
                    self.ui.spinBox_global.singleStep())
            self.ui.spinBox_individuel.setValue(cind)
            self.ui.spinBox_local.setValue(cloc)
            self.ui.spinBox_global.setValue(cglob)
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(self._accept)
            self._timer.start(7000)

        # taille et titre fenetre
        self.setFixedSize(450, 265)
        self.setWindowTitle(texts.DECISION_title)

    def _afficher_historique(self):
        ecran_historique = GuiHistorique(self, self._historique)
        ecran_historique.show()

    def _accept(self):
        """
        Appelée lorsque le sujet clique sur le bouton OK
        Vérifie les saisies. Si pas d'erreur demande confirmation. Si confirmé
        envoie les données au serveur
        :return:
        """
        try:
            self._timer.stop()
        except AttributeError:
            pass

        # vérification saisies
        indiv = self.ui.spinBox_individuel.value()
        loc = self.ui.spinBox_local.value()
        glob = self.ui.spinBox_global.value()
        if indiv + loc + glob != pms.DOTATION:
            QtGui.QMessageBox.warning(
                self, texts.DECISION_error.titre, texts.DECISION_error.texte)
            return

        # confirmation
        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, texts.DECISION_confirmation.titre,
                texts.DECISION_confirmation.texte,
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if confirmation != QtGui.QMessageBox.Yes:
                return

        # envoi des décisions au serveur
        decisions = dict()
        decisions['individuel'] = indiv
        decisions['local'] = loc
        decisions['global'] = glob
        logger.info(u"Renvoi: {}".format(decisions))
        self._defered.callback(decisions)
        self.accept()
        

class GuiInformation(QtGui.QDialog):
    """
    Boite de dialogue qui affiche les informations concernant les contributions
    des groupes dans le compte local et dans le compte global.
    Dans le traitement avec cartons/désapprobation, possibilité de mettre des
    points de désapprobation à l'autre sous-groupe
    """
    def __init__(self, defered, automatique, ecran_attente, periode, historique,
                 texte_info, historique_info):
        super(GuiInformation, self).__init__(ecran_attente)

        # variables
        self._defered = defered
        self._automatique = automatique
        self._historique = historique

        # création fenetre
        self.ui = PublicGoodGlobalLocalInformation2.Ui_Dialog()
        self.ui.setupUi(self)

        # période et historique
        self.ui.label_periode.setText(texts.PERIODE_label(periode))
        self.ui.pushButton_historique.setText(texts.HISTORIQUE_button)
        self.ui.pushButton_historique.clicked.connect(self._afficher_historique)

        # explication (information)
        self.ui.textEdit_explication.setText(texte_info)
        self.ui.textEdit_explication.setFixedSize(450, 80)

        # historique information
        self._table_model = TableModelHistorique(historique_info)
        self.ui.tableView_information.setFixedSize(450, 110)
        self.ui.tableView_information.setModel(self._table_model)
        self.ui.tableView_information.horizontalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch
        )
        self.ui.tableView_information.verticalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch
        )

        # si traitement avec désapprobation
        if pms.TRAITEMENT == pms.CARTONS_LOCAL or \
            pms.TRAITEMENT == pms.CARTONS_LOCAL_AUTRE or \
            pms.TRAITEMENT == pms.CARTONS_GLOBAL or \
            pms.TRAITEMENT == pms.CARTONS_LOCAL_GLOBAL:
            self.ui.widget_cartons.setVisible(True)
            self.ui.spinBox_cartons.setButtonSymbols(
                QtGui.QAbstractSpinBox.NoButtons)
            self.ui.spinBox_cartons.setMinimum(pms.CARTONS_MIN)
            self.ui.spinBox_cartons.setMaximum(pms.CARTONS_MAX)
            self.ui.spinBox_cartons.setSingleStep(pms.CARTONS_STEP)
            self.ui.spinBox_cartons.setValue(self.ui.spinBox_cartons.minimum())
        else:
            self.ui.widget_cartons.setVisible(False)

        # boutons ok et cancel
        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Cancel).setVisible(
            False)

        # automatique
        if self._automatique:
            if self.ui.widget_cartons.isVisible():
                self.ui.spinBox_cartons.setValue(
                    random.randrange(
                        self.ui.spinBox_cartons.minimum(),
                        self.ui.spinBox_cartons.maximum(),
                        self.ui.spinBox_cartons.singleStep()
                    )
                )
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(self._accept)
            self._timer.start(7000)

        # taille et titre fenetre
        self.setFixedSize(595, 340)
        self.setWindowTitle(texts.INFORMATION_title)

    def _afficher_historique(self):
        ecran_historique = GuiHistorique(self, self._historique)
        ecran_historique.show()

    def _accept(self):
        """
        Arret du timer si actif
        Vérification des saisies si besoin
        Demande de confirmation si besoin
        Envoi des données au serveur
        :return: un dictionnaire avec soit le nombre de points de désapprobation
        soit ok
        """
        try:
            self._timer.stop()
        except AttributeError:
            pass

        renvoi = {}
        # si traitement avec désapprobation
        if self.ui.widget_cartons.isVisible():
            renvoi = self.ui.spinBox_cartons.value()
            if not self._automatique:
                confirmation = QtGui.QMessageBox.question(
                    self, texts.INFORMATION_confirmation.titre,
                    texts.INFORMATION_confirmation.texte,
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                if confirmation != QtGui.QMessageBox.Yes:
                    return
        else:
            renvoi = u"Ok"
        logger.info(u"Renvoi: {}".format(renvoi))
        self._defered.callback(renvoi)
        self.accept()


class GuiCommunication(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, periode, historique,
                 remote):
        super(GuiCommunication, self).__init__(parent)

        # variables
        self._defered = defered
        self._automatique = automatique
        self._historique = historique
        self._remote = remote

        # création gui
        self.ui = PublicGoodGlobalLocalCommunication.Ui_Dialog()
        self.ui.setupUi(self)

        # periode et historique
        self.ui.label_periode.setText(texts.PERIODE_label(periode))
        self.ui.pushButton_historique.setText(texts.HISTORIQUE_button)
        self.ui.pushButton_historique.clicked.connect(self._afficher_historique)

        # liste qui affiche les messages: self.ui.listWidget
        # textedit pour écrire message: self.ui.textEdit
        # bouton envoyer
        self.ui.pushButton.clicked.connect(lambda _: self._send_message())

        # lancement de la session
        self._timer_session = QtCore.QTimer()
        self._timer_session.timeout.connect(self.terminer_session)
        self._timer_session.start(pms.COMMUNICATION_TEMPS * 1000)

        if self._automatique:
            heure_debut = datetime.datetime.now()
            reactor.callLater(
                random.randint(0, 10),
                self._remote.send_message_simulation,
                self._defered, heure_debut,
                u"message automatique")

        self.setWindowTitle(texts.COMMUNICATION_title)
        self.setFixedSize(520, 635)
        logger.debug(u"arrivé ici")

    def _afficher_historique(self):
        ecran_historique = GuiHistorique(self, self._historique)
        ecran_historique.show()

    def reject(self):
        pass

    def terminer_session(self):
        try:
            self._timer_session.stop()
        except AttributeError:
            pass
        self._defered.callback(1)
        self.accept()

    @defer.inlineCallbacks
    def _send_message(self):
        self.ui.pushButton.setEnabled(False)
        self.ui.textEdit_composition.setReadOnly(True)
        message = unicode(self.ui.textEdit_composition.toPlainText().toUtf8(),
                          "utf8")
        yield (self._remote.send_message(message))
        self.ui.textEdit_composition.clear()
        self.ui.textEdit_composition.setReadOnly(False)
        self.ui.pushButton.setEnabled(True)


class GuiConfiguration(QtGui.QDialog):
    """
    Boite de dialogue pour la configuration de la partie
    Choix du traitement et si communication ou non
    """
    Configuration = namedtuple(
        "Configuration",
        ["nombreperiodes", "traitement", "communication", "communication_temps",
         "communication_periodes"])

    def __init__(self, nombreperiodes, liste_traitements, liste_communication,
                 communication_temps, communication_periodes):
        super(GuiConfiguration, self).__init__()
        self.ui = PublicGoodGlobalLocalConfiguration.Ui_Dialog()
        self.ui.setupUi(self)

        # valeurs des widgets de choix
        self.ui.spinBox_nombreperiodes.setValue(nombreperiodes)
        self.ui.comboBox_traitement.addItems(liste_traitements)
        self.ui.comboBox_communication.addItems(liste_communication)
        self.ui.spinBox_temps.setValue(communication_temps)
        self.ui.lineEdit_periodes.setText(communication_periodes)

        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def _accept(self):
        comm_per = unicode(self.ui.lineEdit_periodes.text().toUtf8(), "utf8")
        self._configuration = self.Configuration(
            self.ui.spinBox_nombreperiodes.value(),
            self.ui.comboBox_traitement.currentIndex(),
            self.ui.comboBox_communication.currentIndex(),
            self.ui.spinBox_temps.value(),
            [int(p) for p in comm_per.split()])
        confirm = QtGui.QMessageBox.question(
            self,
            u"Confirmation",
            u"Appliquer la configuration suivante: \n"
            u"Nombre de périodes: {}\n"
            u"Traitement: {}\n"
            u"Communication: {}\n"
            u"Temps de communication: {} secondes\n"
            u"Périodes de communication: {}".format(
                self._configuration.nombreperiodes,
                texts.get_traitement(self._configuration.traitement),
                texts.get_communication(self._configuration.communication),
                self._configuration.communication_temps,
                self._configuration.communication_periodes
            ),
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if confirm != QtGui.QMessageBox.Yes:
            return
        self.accept()

    def get_configuration(self):
        return self._configuration


