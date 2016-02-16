# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
from collections import OrderedDict
from server.servbase import Base
from server.servparties import Partie
from util.utiltools import get_module_attributes
from util.utili18n import le2mtrans
import prisonnersDilemmaParams as pms
import prisonnersDilemmaTexts as texts_DP
from prisonnersDilemmaTexts import trans_DP

logger = logging.getLogger("le2m")


class PartieDP(Partie):
    __tablename__ = "partie_prisonnersDilemma"
    __mapper_args__ = {'polymorphic_identity': 'prisonnersDilemma'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsDP')

    def __init__(self, le2mserv, joueur):
        super(PartieDP, self).__init__("prisonnersDilemma", "DP")
        self._le2mserv = le2mserv
        self.joueur = joueur
        self.DP_gain_ecus = 0
        self.DP_gain_euros = 0

    @defer.inlineCallbacks
    def configure(self, *args):
        logger.debug(u"{} Configure".format(self.joueur))
        yield (self.remote.callRemote("configure", get_module_attributes(pms)))

    @defer.inlineCallbacks
    def newperiod(self, period):
        logger.debug(u"{} New Period".format(self.joueur))
        self.currentperiod = RepetitionsDP(period)
        self.currentperiod.DP_group = self.joueur.groupe
        self._le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (self.remote.callRemote("newperiod", period))
        logger.info(u"{} Ready for period {}".format(self.joueur, period))

    @defer.inlineCallbacks
    def display_decision(self):
        """
        Display the decision screen on the remote
        Get back the decision
        :return:
        """
        logger.debug(u"{} Decision".format(self.joueur))
        debut = datetime.now()
        self.currentperiod.DP_decision = \
            yield(self.remote.callRemote("display_decision"))
        self.currentperiod.DP_decisiontime = \
            (datetime.now() - debut).seconds
        self.joueur.info(u"{}".format(
            pms.get_option(self.currentperiod.DP_decision)))
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        """
        Compute the payoff for the period
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))
        self.currentperiod.DP_periodpayoff = 0

        if self.currentperiod.DP_decision == pms.get_option("X"):
            if self.currentperiod.DP_decisionother == pms.get_option("X"):
                self.currentperiod.DP_periodpayoff = pms.XX
            else:
                self.currentperiod.DP_periodpayoff = pms.XY
        else:
            if self.currentperiod.DP_decisionother == pms.get_option("Y"):
                self.currentperiod.DP_periodpayoff = pms.YX
            else:
                self.currentperiod.DP_periodpayoff = pms.YY

        # cumulative payoff since the first period
        if self.currentperiod.DP_period < 2:
            self.currentperiod.DP_cumulativepayoff = \
                self.currentperiod.DP_periodpayoff
        else: 
            previousperiod = self.periods[
                self.currentperiod.DP_period - 1]
            self.currentperiod.DP_cumulativepayoff = \
                previousperiod.DP_cumulativepayoff + \
                self.currentperiod.DP_periodpayoff

        # we store the period in the self.periodes dictionnary
        self.periods[self.currentperiod.DP_period] = self.currentperiod

        logger.debug(u"{} Period Payoff {}".format(
            self.joueur, self.currentperiod.DP_periodpayoff))

    @defer.inlineCallbacks
    def display_summary(self):
        logger.debug(u"{} Summary".format(self.joueur))
        yield(self.remote.callRemote(
            "display_summary", self.currentperiod.todict()))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def compute_partpayoff(self):
        logger.debug(u"{} Part Payoff".format(self.joueur))

        self.DP_gain_ecus = self.currentperiod.DP_cumulativepayoff
        self.DP_gain_euros = float(self.DP_gain_ecus) * \
            float(pms.TAUX_CONVERSION)
        yield (self.remote.callRemote(
            "set_payoffs", self.DP_gain_euros, self.DP_gain_ecus))

        logger.info(u'{} Payoff ecus {} Payoff euros {:.2f}'.format(
            self.joueur, self.DP_gain_ecus, self.DP_gain_euros))


class RepetitionsDP(Base):
    __tablename__ = 'partie_prisonnersDilemma_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_prisonnersDilemma.partie_id"))

    DP_period = Column(Integer)
    DP_treatment = Column(Integer)
    DP_group = Column(Integer)
    DP_decision = Column(Integer)
    DP_decisiontime = Column(Integer)
    DP_decisionother = Column(Integer)
    DP_periodpayoff = Column(Float)
    DP_cumulativepayoff = Column(Float)

    def __init__(self, period):
        self.DP_treatment = pms.TREATMENT
        self.DP_period = period
        self.DP_decisiontime = 0
        self.DP_periodpayoff = 0
        self.DP_cumulativepayoff = 0

    def todict(self, joueur=None):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if joueur:
            temp["joueur"] = joueur
        return temp

