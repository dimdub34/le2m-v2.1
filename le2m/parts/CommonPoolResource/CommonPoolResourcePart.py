# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
from util.utiltools import get_module_attributes
from server.servbase import Base
from server.servparties import Partie
import CommonPoolResourceParams as pms


logger = logging.getLogger("le2m")


class PartieCPR(Partie):
    __tablename__ = "partie_CommonPoolResource"
    __mapper_args__ = {'polymorphic_identity': 'CommonPoolResource'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsCPR')

    def __init__(self, le2mserv, joueur):
        super(PartieCPR, self).__init__("CommonPoolResource", "CPR")
        self._le2mserv = le2mserv
        self.joueur = joueur
        self.CPR_gain_ecus = 0
        self.CPR_gain_euros = 0

    @defer.inlineCallbacks
    def configure(self, *args):
        logger.debug(u"{} Configure".format(self.joueur))
        yield (self.remote.callRemote("configure", get_module_attributes(pms)))
        self.joueur.info(u"Ok")

    @defer.inlineCallbacks
    def newperiod(self, period):
        """
        Create a new period and inform the remote
        If this is the first period then empty the historic
        :param period:
        :return:
        """
        logger.debug(u"{} New Period".format(self.joueur))
        self.currentperiod = RepetitionsCPR(period)
        self.currentperiod.CPR_group = self.joueur.groupe
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
        self.currentperiod.CPR_decision = \
            yield(self.remote.callRemote("display_decision"))
        self.currentperiod.CPR_decisiontime = \
            (datetime.now() - debut).seconds
        self.joueur.info(u"{}".format(self.currentperiod.CPR_decision))
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        """
        Compute the payoff for the period
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))
        self.currentperiod.CPR_periodpayoff = pms.get_gain(
            self.currentperiod.CPR_decision,
            self.currentperiod.CPR_decisiongroup)

        # cumulative payoff since the first period
        if self.currentperiod.CPR_period < 2:
            self.currentperiod.CPR_cumulativepayoff = \
                self.currentperiod.CPR_periodpayoff
        else: 
            previousperiod = self.periods[
                self.currentperiod.CPR_period - 1]
            self.currentperiod.CPR_cumulativepayoff = \
                previousperiod.CPR_cumulativepayoff + \
                self.currentperiod.CPR_periodpayoff

        # we store the period in the self.periodes dictionnary
        self.periods[self.currentperiod.CPR_period] = \
            self.currentperiod

        logger.debug(u"{} Period Payoff {}".format(
            self.joueur, self.currentperiod.CPR_periodpayoff))

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

        self.CPR_gain_ecus = self.currentperiod.CPR_cumulativepayoff
        self.CPR_gain_euros = float(self.CPR_gain_ecus) * float(pms.TAUX_CONVERSION)
        yield (self.remote.callRemote(
            "set_payoffs", self.CPR_gain_euros, self.CPR_gain_ecus))

        logger.info(u'{} Payoff ecus {} Payoff euros {:.2f}'.format(
            self.joueur, self.CPR_gain_ecus, self.CPR_gain_euros))


class RepetitionsCPR(Base):
    __tablename__ = 'partie_CommonPoolResource_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_CommonPoolResource.partie_id"))

    CPR_period = Column(Integer)
    CPR_treatment = Column(Integer)
    CPR_group = Column(Integer)
    CPR_decision = Column(Integer)
    CPR_decisiongroup = Column(Integer)
    CPR_decisiontime = Column(Integer)
    CPR_periodpayoff = Column(Float)
    CPR_cumulativepayoff = Column(Float)

    def __init__(self, period):
        self.CPR_treatment = pms.TREATMENT
        self.CPR_period = period
        self.CPR_decisiontime = 0
        self.CPR_periodpayoff = 0
        self.CPR_cumulativepayoff = 0

    def todict(self, joueur=None):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if joueur:
            temp["joueur"] = joueur
        return temp

