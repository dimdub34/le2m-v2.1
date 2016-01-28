# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey

from server.servbase import Base
from server.servparties import Partie
from util.utili18n import le2mtrans
import CommonPoolResourceParams as pms
import CommonPoolResourceTexts as texts


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
        self._texte_recapitulatif = u""
        self._texte_final = u""
        self.CPR_gain_ecus = 0
        self.CPR_gain_euros = 0
        self._histo_vars = [
            "CPR_period", "CPR_decision",
            "CPR_periodpayoff",
            "CPR_cumulativepayoff"]
        self._histo = [
            [le2mtrans(u"Period"), le2mtrans(u"Decision"),
             le2mtrans(u"Period\npayoff"), le2mtrans(u"Cumulative\npayoff")]]
        self.periods = {}
        self.currentperiod = None

    @defer.inlineCallbacks
    def configure(self, *args):
        """
        Allow to make changes in the part parameters
        :param args:
        :return:
        """
        logger.debug(u"{} Configure".format(self.joueur))
        # ici mettre en place la configuration
        yield (self.remote.callRemote("configure", *args))

    @defer.inlineCallbacks
    def newperiod(self, period):
        """
        Create a new period and inform the remote
        If this is the first period then empty the historic
        :param periode:
        :return:
        """
        logger.debug(u"{} New Period".format(self.joueur))
        if period == 1:
            del self._histo[1:]
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
        """
        Create the summary (txt and historic) and then display it on the
        remote
        :param args:
        :return:
        """
        logger.debug(u"{} Summary".format(self.joueur))
        self._texte_recapitulatif = texts.get_recapitulatif(self.currentperiod)
        self._histo.append(
            [getattr(self.currentperiod, e) for e in self._histo_vars])
        yield(self.remote.callRemote(
            "display_summary", self._texte_recapitulatif, self._histo))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()
    
    def compute_partpayoff(self):
        """
        Compute the payoff of the part
        :return:
        """
        logger.debug(u"{} Part Payoff".format(self.joueur))
        # gain partie
        self.CPR_gain_ecus = \
            self.currentperiod.CPR_cumulativepayoff
        self.CPR_gain_euros = \
            float(self.CPR_gain_ecus) * \
            float(pms.TAUX_CONVERSION)

        # texte final
        self._texte_final = texts.get_texte_final(
            self.CPR_gain_ecus,
            self.CPR_gain_euros)

        logger.debug(u"{} Final text {}".format(self.joueur, self._texte_final))
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

    def todict(self, joueur):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        temp["joueur"] = joueur
        return temp

