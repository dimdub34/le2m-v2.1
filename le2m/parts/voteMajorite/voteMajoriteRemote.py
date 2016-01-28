# -*- coding: utf-8 -*-

import logging
import random

from twisted.internet import defer
from twisted.spread import pb

from client.cltgui.cltguidialogs import GuiRecapitulatif
import voteMajoriteParams as pms
from voteMajoriteGui import GuiDecision, DSummary


logger = logging.getLogger("le2m")


class RemoteVM(pb.Referenceable):
    """
    Class remote, remote_ methods can be called by the server
    """
    def __init__(self, le2mclt):
        self._le2mclt = le2mclt
        self._currentperiod = 0

    def remote_configure(self, params):
        logger.info(u"{} configure".format(self._le2mclt.uid))
        for k, v in params.iteritems():
            setattr(pms, k, v)

    def remote_newperiod(self, periode):
        logger.info(u"{} Period {}".format(self._le2mclt.uid, periode))
        self._currentperiod = periode

    def remote_display_decision(self, profil):
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            decision = random.randint(0, 1)
            logger.info(u"{} Send back {}".format(self._le2mclt.uid, decision))
            return decision
        else: 
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered, self._le2mclt.automatique,
                self._le2mclt.screen, self._currentperiod, pms.PROFILS[profil])
            ecran_decision.show()
            return defered

    def remote_display_summary(self, texte_recap, historique, profil):
        logger.info(u"{} Summary".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = DSummary(
                defered, self._le2mclt.automatique, self._le2mclt.screen,
                texte_recap, historique, pms.PROFILS[profil])
            ecran_recap.show()
            return defered
