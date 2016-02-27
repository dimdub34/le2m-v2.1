# -*- coding: utf-8 -*-

from twisted.internet import defer
import logging
import random
from client.cltremote import IRemote
from client.cltgui.cltguidialogs import GuiRecapitulatif
import GneezyPotterParams as pms
import GneezyPotterTexts as texts_GP
from GneezyPotterGui import GuiDecision
from configuration.configconst import PILE
from util.utili18n import le2mtrans


logger = logging.getLogger("le2m")


class RemoteGP(IRemote):
    """
    Class remote, celle qui est contactée par le client (sur le serveur)
    """
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)
        self._histo_vars = ["GP_decision", "GP_randomdraw", "GP_periodpayoff"]
        self.histo.append(texts_GP.get_histo_header())

    def remote_configure(self, params):
        logger.info(u"{} Configure".format(self._le2mclt.uid))
        for k, v in params.viewitems():
            setattr(pms, k, v)
        logger.debug(u"Display summary: {}".format(
            u"Yes" if pms.DISPLAY_SUMMARY else u"No"))
        del self.histo[1:]

    def remote_newperiod(self, period):
        logger.info(u"{} Period {}".format(self._le2mclt.uid, period))
        self.currentperiod = period

    def remote_display_decision(self):
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            decision = \
                random.randrange(
                    pms.DECISION_MIN,
                    pms.DECISION_MAX + pms.DECISION_STEP,
                    pms.DECISION_STEP)
            logger.info(u"{} Send back: {}".format(self._le2mclt.uid, decision))
            return decision
        else: 
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered,
                self._le2mclt.automatique, self._le2mclt.screen,
                self.currentperiod, self.histo)
            ecran_decision.show()
            return defered

    def remote_display_summary(self, period_content):
        logger.info(u"{} Summary".format(self._le2mclt.uid))
        line = []
        for k in self._histo_vars:
            if k == "GP_randomdraw":
                if period_content.get(k) == PILE:
                    line.append(le2mtrans(u"Tail"))
                else:
                    line.append(le2mtrans(u"Head"))
            else:
                line.append(period_content.get(k))
        self.histo.append(line)
        if self._le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = GuiRecapitulatif(
                defered,
                self._le2mclt.automatique, self._le2mclt.screen,
                self.currentperiod, self.histo,
                texts_GP.get_text_summary(period_content))
            ecran_recap.show()
            return defered
