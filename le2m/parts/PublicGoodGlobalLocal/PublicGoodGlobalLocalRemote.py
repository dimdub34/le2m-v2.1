# -*- coding: utf-8 -*-

from twisted.internet import defer, reactor
from twisted.spread import pb
import logging
import random
import datetime
from client.cltgui.cltguidialogs import GuiRecapitulatif

import PublicGoodGlobalLocalParams as pms
from PublicGoodGlobalLocalGui import GuiDecision, GuiInformation, \
    GuiCommunication

logger = logging.getLogger("le2m")


class RemotePGGL(pb.Referenceable):
    def __init__(self, le2mclt):
        self.le2mclt = le2mclt
        self._pgglservplay = None
        self._currentsequence = None
        self._currentperiod = None
        self._historique = []
        self._ecran_communication = None

    def remote_configure(self, pgglservplay, sequence, traitement,
                         communication, communication_temps):
        """
        Appelée lorsque le jeu est lancé
        Permet de configure le jeu (traitement ou autre ...)
        :param pgglservplay: pour pouvoir envoyer les messages
        :param sequence:
        :param traitement:
        :param communication: si oui ou non c'est avec communication
        :param communication_temps: le temps de communication, en secondes
        :return: rien
        """
        self._pgglservplay = pgglservplay
        self._currentsequence = sequence
        pms.TRAITEMENT = traitement
        pms.COMMUNICATION = communication
        pms.COMMUNICATION_TEMPS = communication_temps

        # on vide l'historique puisque nouvelle séquence
        del self._historique[:]
        logger.info(u"Ok configuration de la partie")

    def remote_newperiod(self, periode):
        """
        Set la période. Faire ici actions en début de période, si besoin
        :param periode:
        :return: rien
        """
        self._currentperiod = periode

    def remote_display_communication(self):
        """
        Affichage de l'écran pour le chat
        :return:
        """
        logger.info(u"Affichage de communication")
        if self.le2mclt.simulation:
            defered = defer.Deferred()
            heure_debut = datetime.datetime.now()
            reactor.callLater(
                random.randint(0, 10),
                self.send_message_simulation,
                defered, heure_debut, u"message simulation"
            )
            return defered
        else:
            defered = defer.Deferred()
            self._ecran_communication = GuiCommunication(
                defered=defered,
                automatique=self.le2mclt.automatique,
                parent=self.le2mclt.gestionnaire_graphique.ecran_attente,
                periode=self._currentperiod,
                historique=self._historique,
                remote=self
            )
            self._ecran_communication.show()
            return defered

    @defer.inlineCallbacks
    def send_message_simulation(self, defered, heure_debut, message):
        logger.info(u"{} send_message_simulation {}".format(
            self.le2mclt.uid, message))
        yield (self._pgglservplay.callRemote("sendmessage", message))
        if (datetime.datetime.now() - heure_debut).seconds < \
                pms.COMMUNICATION_TEMPS:
            reactor.callLater(
                random.randint(0, 5),
                self.send_message_simulation,
                defered, heure_debut, message)
        else:
            if self.le2mclt.automatique:
                self._ecran_communication.terminer_session()
            else:
                defered.callback(1)

    @defer.inlineCallbacks
    def send_message(self, message):
        """
        Envoi du message au serveur. Appelé depuis le gui
        :param message:
        :return:
        """
        logger.debug(u"Envoi du message: {}".format(message))
        yield (self._pgglservplay.callRemote("sendmessage", message))

    def remote_display_message(self, message):
        """
        Ajoute le message à la liste des messages reçus
        :param message:
        :return:
        """
        if self.le2mclt.simulation:
            logger.info(u"Simulation - display_message: {}".format(message))
        else:
            self._ecran_communication.ui.listWidget.addItem(message)

    def remote_display_decision(self):
        """
        Affiche l'écran de décision: répartition dotation entre 3 cptes:
        individuel, local et global
        :return: un dictionnaire avec les contributions dans chaque compte
        """
        logger.info(u"Affichage de l'écran de décision")
        if self.le2mclt.simulation:
            indiv, loc, glob = 0, 0, 0
            while indiv + loc + glob != pms.DOTATION:
                indiv = random.randint(0, pms.DOTATION)
                loc = random.randint(0, pms.DOTATION - indiv)
                glob = random.randint(0, pms.DOTATION - indiv - loc)
            decisions = {"individuel": indiv, "local": loc, "global": glob}
            logger.info(u"Renvoi: {}".format(decisions))
            return decisions
        else: 
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered,
                self.le2mclt.automatique,
                self.le2mclt.gestionnaire_graphique.ecran_attente,
                self._currentperiod, self._historique
            )
            ecran_decision.show()
            return defered

    def remote_display_information(self, texte_info, histo_info):
        """
        Affiche l'écran d'information
        Si traitement avec désapprobation permet la saisie des points de
        désapprobation
        :param texte_info:
        :param histo_info:
        :return: True si pas de désapprobation, sinon le nombre de points
        attribués
        """
        if self.le2mclt.simulation:
            if pms.TRAITEMENT == pms.CARTONS_LOCAL or \
            pms.TRAITEMENT == pms.CARTONS_LOCAL_AUTRE or \
            pms.TRAITEMENT == pms.CARTONS_GLOBAL or \
            pms.TRAITEMENT == pms.CARTONS_LOCAL_GLOBAL:
                desapprobation = random.randint(0, pms.DOTATION_CARTONS)
            else:
                desapprobation = u"Ok"
            logger.info(u"Renvoi: {}".format(desapprobation))
            return desapprobation
        else:
            defered = defer.Deferred()
            ecran_info = GuiInformation(
                defered,
                self.le2mclt.automatique,
                self.le2mclt.gestionnaire_graphique.ecran_attente,
                self._currentperiod,
                self._historique,
                texte_info,
                histo_info
            )
            ecran_info.show()
            return defered

    def remote_display_summary(self, texte_recap, historique):
        """
        Affiche le récap de la période
        :param texte_recap: le texte du récap
        :param historique: l'historique
        :return: True
        """
        self._historique = historique
        if self.le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = GuiRecapitulatif(
                defered,
                self.le2mclt.automatique,
                self.le2mclt.gestionnaire_graphique.ecran_attente,
                self._currentperiod, self._historique, texte_recap
            )
            ecran_recap.ui.tableView.setFixedSize(500, 110)
            ecran_recap.show()
            return defered

