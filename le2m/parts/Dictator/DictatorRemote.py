# -*- coding: utf-8 -*-

from twisted.internet import defer
import logging
import random
from client.cltremote import IRemote
from client.cltgui.cltguidialogs import GuiRecapitulatif
import DictatorParams as pms
from DictatorGui import GuiDecision
from util.utiltools import get_module_info
import DictatorTexts as texts

logger = logging.getLogger("le2m")


class RemoteDIC(IRemote):
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)

    def remote_configure(self, params):
        logger.info(u"{} Configure".format(self._le2mclt.uid))
        for k, v in params.iteritems():
            setattr(pms, k, v)
        logger.debug("Params")
        logger.debug(get_module_info(pms))

    def remote_display_role(self, role):
        self._role = role
        if not self.histo:
            self.histo.append(list(texts.get_histo_build(self._role).viewvalues()))
        txt = texts.trans_DIC(u"You are player") + u" {}".format(
            u"A" if role == pms.PLAYER_A else u"B")
        return self._le2mclt.get_remote("base").remote_display_information(txt)

    def remote_newperiod(self, period):
        logger.info(u"{} Period {}".format(self._le2mclt.uid, period))
        self.currentperiod = period
        if self.currentperiod == 1:
            del self.histo[1:]

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
                self._le2mclt.automatique,
                self._le2mclt.screen,
                self.currentperiod, self.histo)
            ecran_decision.show()
            return defered

    def remote_display_summary(self, period_content):
        logger.info(u"{} Summary".format(self._le2mclt.uid))
        texte_recap = texts.get_recapitulatif(period_content)
        self.histo.append(
            [period_content.get(k) for k in
             list(texts.get_histo_build(self._role).viewkeys())])
        if self._le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = GuiRecapitulatif(
                defered,
                self._le2mclt.automatique,
                self._le2mclt.screen,
                self.currentperiod, self.histo, texte_recap)
            ecran_recap.show()
            return defered
