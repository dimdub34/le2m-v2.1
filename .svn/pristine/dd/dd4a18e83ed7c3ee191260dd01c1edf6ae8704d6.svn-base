# -*- coding: utf-8 -*-

import logging
import random

from twisted.internet import defer
from twisted.spread import pb
from util.utiltools import get_module_info
from client.cltgui.cltguidialogs import GuiRecapitulatif
import oathAndLiesParams as pms
from oathAndLiesGui import DDecisionA, DDecisionB


logger = logging.getLogger("le2m")


class RemoteOL(pb.Referenceable):
    """
    Class remote, remote_ methods can be called by the server
    """
    def __init__(self, le2mclt):
        self._le2mclt = le2mclt
        self._currentperiod = 0
        self._histo = []

    def remote_configure(self, params):
        """
        Appelé au démarrage de la partie, permet de configure le remote
        par exemple: traitement, séquence ...
        :param args:
        :return:
        """
        logger.info(u"{} configure".format(self._le2mclt.uid))
        for k, v in params.iteritems():
            setattr(pms, k, v)
        logger.debug(u"Params")
        logger.debug(get_module_info(pms))

    def remote_newperiod(self, periode):
        """
        Appelé au début de chaque période.
        L'historique est "vidé" s'il s'agit de la première période de la partie
        Si c'est un jeu one-shot appeler cette méthode en mettant 0
        :param periode: le numéro de la période courante
        :return:
        """
        logger.info(u"{} Period {}".format(self._le2mclt.uid, periode))
        self._currentperiod = periode
        if self._currentperiod == 1:
            del self._histo[:]

    def remote_display_decision_A(self):
        """
        Display the decision screen
        :return: deferred
        """
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            tirage = random.randint(1, 6)
            mensonge = True if random.random() >= 0.75 else False
            message = tirage if not mensonge else random.randint(1, 6)
            renvoi = {"dice": tirage, "message": message}
            logger.info(u"{} Send back {}".format(self._le2mclt.uid, renvoi))
            return renvoi
        else: 
            defered = defer.Deferred()
            ecran_decision = DDecisionA(
                defered, self._le2mclt.automatique, self._le2mclt.screen)
            ecran_decision.show()
            return defered

    def remote_display_decision_B(self, message):
        """
        Display the decision screen
        :return: deferred
        """
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            decision = random.randint(1, 6)
            logger.info(u"{} Send back {}".format(self._le2mclt.uid, decision))
            return decision
        else:
            defered = defer.Deferred()
            ecran_decision = DDecisionB(
                defered, self._le2mclt.automatique, self._le2mclt.screen,
                message)
            ecran_decision.show()
            return defered

    def remote_display_summary(self, texte_recap, historique):
        """
        Display the summary screen
        :param texte_recap:
        :param historique:
        :return: deferred
        """
        logger.info(u"{} Summary".format(self._le2mclt.uid))
        self._histo = historique
        if self._le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = GuiRecapitulatif(
                defered, self._le2mclt.automatique, self._le2mclt.screen,
                self._currentperiod, self._histo, texte_recap)
            ecran_recap.widexplication.ui.textEdit.setFixedSize(450, 90)
            ecran_recap.show()
            return defered
