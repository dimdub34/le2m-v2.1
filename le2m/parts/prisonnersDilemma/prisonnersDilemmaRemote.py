# -*- coding: utf-8 -*-

import logging
import random
from twisted.internet import defer
from client.cltremote import IRemote
from client.cltgui.cltguidialogs import GuiRecapitulatif
import prisonnersDilemmaParams as pms
from prisonnersDilemmaGui import GuiDecision
import prisonnersDilemmaTexts as texts_DP


logger = logging.getLogger("le2m")


class RemoteDP(IRemote):
    """
    Class remote, remote_ methods can be called by the server
    """
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)
        self._histo_vars = ["DP_period", "DP_decision", "DP_decisionother",
                            "DP_periodpayoff", "DP_cumulativepayoff"]
        self.histo.append(texts_DP.get_histo_head())

    def remote_configure(self, params):
        logger.info(u"{} configure".format(self._le2mclt.uid))
        for k, v in params.viewitems():
            setattr(pms, k, v)

    def remote_newperiod(self, period):
        logger.info(u"{} Period {}".format(self._le2mclt.uid, period))
        self._currentperiod = period
        if self._currentperiod == 1:
            del self._histo[1:]

    def remote_display_decision(self):
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            decision = random.randint(0, 1)
            logger.info(u"{} Send back {}".format(self._le2mclt.uid, decision))
            return decision
        else: 
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered, self._le2mclt.automatique,
                self._le2mclt.screen, self.currentperiod, self.histo)
            ecran_decision.show()
            return defered

    def remote_display_summary(self, period_content):
        logger.info(u"{} Summary".format(self._le2mclt.uid))
        self.histo.append([period_content.get(k) for k in self._histo_vars])
        if self._le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = GuiRecapitulatif(
                defered, self._le2mclt.automatique, self._le2mclt.screen,
                self.currentperiod, self.histo,
                texts_DP.get_text_summary(period_content))
            ecran_recap.show()
            return defered
