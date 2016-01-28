# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from collections import OrderedDict
from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey

from server.servbase import Base
from server.servparties import Partie
from util.utili18n import le2mtrans
from util.utiltools import get_module_attributes
import testParams as pms
import testTexts as texts


logger = logging.getLogger("le2m")


class PartieTT(Partie):
    __tablename__ = "partie_test"
    __mapper_args__ = {'polymorphic_identity': 'test'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsTT')

    def __init__(self, le2mserv, joueur):
        super(PartieTT, self).__init__("test", "TT")
        self._le2mserv = le2mserv
        self.joueur = joueur
        self._texte_recapitulatif = u""
        self._texte_final = u""
        self.TT_gain_ecus = 0
        self.TT_gain_euros = 0
        self._histo_build = OrderedDict()
        self._histo_build[le2mtrans(u"Period")] = "TT_period"
        self._histo_build[le2mtrans(u"Decision")] = "TT_decision"
        self._histo_build[le2mtrans(u"Period\npayoff")] = "TT_periodpayoff"
        self._histo_build[le2mtrans(u"Cumulative\npayoff")] = "TT_cumulativepayoff"
        self._histo_content = [list(self._histo_build.viewkeys())]
        self.periods = {}
        self._currentperiod = None

    @property
    def currentperiod(self):
        return self._currentperiod

    @defer.inlineCallbacks
    def configure(self):
        logger.debug(u"{} Configure".format(self.joueur))
        yield (self.remote.callRemote("configure", get_module_attributes(pms)))
        self.joueur.info(u"Ok")

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
            del self._histo_content[1:]
        self._currentperiod = RepetitionsTT(period)
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
        self.currentperiod.TT_decision = yield(self.remote.callRemote(
            "display_decision"))
        self.currentperiod.TT_decisiontime = (datetime.now() - debut).seconds
        self.joueur.info(u"{}".format(self.currentperiod.TT_decision))
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        """
        Compute the payoff for the period
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))
        self.currentperiod.TT_periodpayoff = 0

        # cumulative payoff since the first period
        if self.currentperiod.TT_period < 2:
            self.currentperiod.TT_cumulativepayoff = \
                self.currentperiod.TT_periodpayoff
        else: 
            previousperiod = self.periods[self.currentperiod.TT_period - 1]
            self.currentperiod.TT_cumulativepayoff = \
                previousperiod.TT_cumulativepayoff + \
                self.currentperiod.TT_periodpayoff

        # we store the period in the self.periodes dictionnary
        self.periods[self.currentperiod.TT_period] = self.currentperiod

        logger.debug(u"{} Period Payoff {}".format(
            self.joueur,
            self.currentperiod.TT_periodpayoff))

    @defer.inlineCallbacks
    def display_summary(self, *args):
        """
        Create the summary (txt and historic) and then display it on the
        remote
        :param args:
        :return:
        """
        logger.debug(u"{} Summary".format(self.joueur))
        self._texte_recapitulatif = texts.get_recapitulatif(self.currentperiod)
        self._histo_content.append(
            [getattr(self.currentperiod, e) for e
             in self._histo_build.viewvalues()])
        yield(self.remote.callRemote(
            "display_summary", self._texte_recapitulatif, self._histo_content))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()
    
    def compute_partpayoff(self):
        """
        Compute the payoff of the part
        :return:
        """
        logger.debug(u"{} Part Payoff".format(self.joueur))
        # gain partie
        self.TT_gain_ecus = self.currentperiod.TT_cumulativepayoff
        self.TT_gain_euros = \
            float(self.TT_gain_ecus) * float(pms.TAUX_CONVERSION)

        # texte final
        self._texte_final = texts.get_texte_final(
            self.TT_gain_ecus,
            self.TT_gain_euros)

        logger.debug(u"{} Final text {}".format(self.joueur, self._texte_final))
        logger.info(u'{} Payoff ecus {} Payoff euros {:.2f}'.format(
            self.joueur, self.TT_gain_ecus, self.TT_gain_euros))


class RepetitionsTT(Base):
    __tablename__ = 'partie_test_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_test.partie_id"))

    TT_period = Column(Integer)
    TT_treatment = Column(Integer)
    TT_group = Column(Integer)
    TT_decision = Column(Integer)
    TT_decisiontime = Column(Integer)
    TT_periodpayoff = Column(Float)
    TT_cumulativepayoff = Column(Float)

    def __init__(self, period):
        self.TT_treatment = pms.TREATMENT
        self.TT_period = period
        self.TT_decisiontime = 0
        self.TT_periodpayoff = 0
        self.TT_cumulativepayoff = 0

    def todict(self, joueur):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        temp["joueur"] = joueur
        return temp

