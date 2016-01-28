# -*- coding: utf-8 -*-

from twisted.internet import defer
from twisted.spread import pb
import logging
import random
from client.cltgui.cltguidialogs import GuiRecapitulatif
import PublicGoodGameSolidarityParams as pms
from PublicGoodGameSolidarityGui import GuiDecision, DVote
from util.utiltools import get_module_info

logger = logging.getLogger("le2m")


class RemotePGGS(pb.Referenceable):
    """
    Class remote, remote_ methods can be called by the server
    """
    def __init__(self, le2mclt):
        self._le2mclt = le2mclt
        self._periode_courante = 0
        self._historique = []

    def remote_configure(self, params):
        logger.info(u"{} Configure".format(self._le2mclt.uid))
        for k, v in params.viewitems():
            setattr(pms, k, v)
        logger.debug(get_module_info(pms))

    def remote_newperiod(self, periode):
        logger.info(u"{} Period {}".format(self._le2mclt.uid, periode))
        self._periode_courante = periode
        if self._periode_courante == 1:
            del self._historique[:]

    def remote_display_decision(self):
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            decision = random.randrange(
                    pms.DECISION_MIN, pms.DECISION_MAX + pms.DECISION_STEP,
                    pms.DECISION_STEP)
            logger.info(u"{} Send back {}".format(self._le2mclt.uid, decision))
            return decision
        else: 
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered, self._le2mclt.automatique,
                self._le2mclt.screen, self._periode_courante, self._historique)
            ecran_decision.show()
            return defered

    def remote_display_summary(self, texte_recap, historique):
        logger.info(u"{} Summary".format(self._le2mclt.uid))
        self._historique = historique
        if self._le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = GuiRecapitulatif(
                defered, self._le2mclt.automatique, self._le2mclt.screen,
                self._periode_courante, self._historique, texte_recap)
            ecran_recap.show()
            return defered

    def remote_display_vote(self):
        logger.info(u"{} vote".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            vote = random.choice(list(pms.VOTE_CODE.viewkeys()))
            logger.info(u"{} send back {}".format(
                self._le2mclt.uid, pms.get_vote(vote)))
            return vote
        else:
            defered = defer.Deferred()
            screenvote = DVote(
                defered, self._le2mclt.automatique, self._le2mclt.screen)
            screenvote.show()
            return defered
