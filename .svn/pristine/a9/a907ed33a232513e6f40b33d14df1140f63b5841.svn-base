# -*- coding: utf-8 -*-

from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column,  Integer, Float, ForeignKey
import logging
from datetime import datetime
from server.servbase import Base
from server.servparties import Partie
import GneezyPotterParams as pms
import GneezyPotterTexts as texts
from GneezyPotterTexts import _GP
from util.utiltools import get_module_attributes
from collections import OrderedDict
from configuration.configconst import PILE


logger = logging.getLogger("le2m")


class PartieGP(Partie):
    __tablename__ = "partie_GneezyPotter"
    __mapper_args__ = {'polymorphic_identity': 'GneezyPotter'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsGP')

    def __init__(self, le2mserv, joueur):
        Partie.__init__(self, "GneezyPotter", "GP")
        self._le2mserv = le2mserv
        self.joueur = joueur
        self._texte_recapitulatif = u""
        self._texte_final = u""
        self.GP_gain_ecus = 0
        self.GP_gain_euros = 0
        self.periods = {}
        self.currentperiod = None
        self._histo_build = OrderedDict()
        self._histo_build[_GP(u"Decision")] = "GP_decision"
        self._histo_build[_GP(u"Random draw")] = "GP_randomdraw"
        self._histo_build[_GP(u"Payoff")] = "GP_periodpayoff"
        self._histo_content = [list(self._histo_build.viewkeys())]

    @defer.inlineCallbacks
    def configure(self):
        logger.debug(u"{} Configure".format(self.joueur))
        yield (self.remote.callRemote("configure", get_module_attributes(pms)))

    @defer.inlineCallbacks
    def newperiod(self, period):
        logger.debug(u"{} New Period".format(self.joueur))
        if period == 1:
            del self._histo_content[1:]
        self.currentperiod = RepetitionsGP(period)
        self._le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (self.remote.callRemote("newperiod", period))
        logger.info(u"{} Ready for periode {}".format(self.joueur, period))

    @defer.inlineCallbacks
    def display_decision(self):
        logger.debug(u"{} Decision".format(self.joueur))
        debut = datetime.now()
        self.currentperiod.GP_decision = yield(self.remote.callRemote(
            "display_decision"))
        self.currentperiod.GP_decisiontime = (datetime.now() - debut).seconds
        self.joueur.info(u"{}".format(self.currentperiod.GP_decision))
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        logger.debug(u"{} Period Payoff".format(self.joueur))
        self.currentperiod.GP_periodpayoff = \
            self.currentperiod.GP_dotation - self.currentperiod.GP_decision
        factor = pms.FACTEUR_PILE if \
            self.currentperiod.GP_randomdraw == PILE else pms.FACTEUR_FACE
        self.currentperiod.GP_periodpayoff += \
            self.currentperiod.GP_decision * factor

        # cumulative payoff
        if self.currentperiod.GP_period < 2:
            self.currentperiod.GP_cumulativepayoff = \
                self.currentperiod.GP_periodpayoff
        else: 
            previousperiod = self.periods[
                self.currentperiod.GP_period - 1]
            self.currentperiod.GP_cumulativepayoff = \
                previousperiod.GP_cumulativepayoff + \
                self.currentperiod.GP_periodpayoff

        # store the current period in a dict
        self.periods[self.currentperiod.GP_period] = self.currentperiod
        logger.info(u"{} Period Payoff {}".format(
            self.joueur, self.currentperiod.GP_periodpayoff))

    @defer.inlineCallbacks
    def display_summary(self):
        logger.debug(u"{} Summary".format(self.joueur))
        line = []
        for v in self._histo_build.viewvalues():
            attrib = getattr(self.currentperiod, v)
            if v == "GP_randomdraw":
                line.append(_GP(u"Head") if attrib == PILE else _GP(u"Tail"))
            else:
                line.append(attrib)
        self._histo_content.append(line)
        self._texte_recapitulatif = texts.get_recapitulatif(self.currentperiod)
        yield(self.remote.callRemote(
            "display_summary", self._texte_recapitulatif, self._histo_content))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()

    def compute_partpayoff(self):
        logger.debug(u"{} Part payoff".format(self.joueur))
        self.GP_gain_ecus = self.currentperiod.GP_cumulativepayoff
        self.GP_gain_euros = \
            float(self.GP_gain_ecus) * float(pms.TAUX_CONVERSION)
        self._texte_final = texts.get_texte_final(self.currentperiod)
        logger.info(u'{} gain ecus: {}, gain euros: {:.2f}'.format(
            self.joueur, self.GP_gain_ecus, self.GP_gain_euros))


class RepetitionsGP(Base):
    __tablename__ = 'partie_GneezyPotter_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_GneezyPotter.partie_id"))

    GP_period = Column(Integer)
    GP_treatment = Column(Integer)
    GP_dotation = Column(Integer)
    GP_decision = Column(Integer)
    GP_decisiontime = Column(Integer)
    GP_randomdraw = Column(Integer)
    GP_periodpayoff = Column(Float)
    GP_cumulativepayoff = Column(Float)

    def __init__(self, period):
        self.GP_treatment = pms.TREATMENT
        self.GP_dotation = pms.DOTATION
        self.GP_period = period
        self.GP_decisiontime = 0
        self.GP_periodpayoff = 0
        self.GP_cumulativepayoff = 0
        
    def todict(self, joueur):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        temp["joueur"] = joueur  # often useful
        return temp
