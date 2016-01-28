# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
from collections import OrderedDict
from server.servbase import Base
from server.servparties import Partie
from util.utili18n import le2mtrans
from util.utiltools import get_module_attributes
import oathAndLiesParams as pms
import oathAndLiesTexts as texts


logger = logging.getLogger("le2m")


class PartieOL(Partie):
    __tablename__ = "partie_oathAndLies"
    __mapper_args__ = {'polymorphic_identity': 'oathAndLies'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsOL')

    def __init__(self, le2mserv, joueur):
        super(PartieOL, self).__init__("oathAndLies", "OL")
        self._le2mserv = le2mserv
        self.joueur = joueur
        self._texte_recapitulatif = u""
        self._texte_final = u""
        self.OL_gain_ecus = 0
        self.OL_gain_euros = 0

        self._histoA = OrderedDict()
        self._histoA[u"Lancé de\ndé"] = "OL_tirage"
        self._histoA[u"Votre message\nà B"] = "OL_message"
        self._histoA[u"Decision de B"] = "OL_decision"
        self._histoA[u"Option\nappliquée"] = "OL_appliedoption"
        self._histoA[u"Gain"] = "OL_periodpayoff"

        self._histoB = OrderedDict()
        self._histoB[u"Message de A"] = "OL_message"
        self._histoB[u"Votre décision"] = "OL_decision"
        self._histoB[u"Gain"] = "OL_periodpayoff"

        self.periods = {}
        self._currentperiod = None
        self._role = None

    @property
    def currentperiod(self):
        return self._currentperiod

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, val):
        self._role = val

    @defer.inlineCallbacks
    def configure(self):
        """
        Allow to make changes in the part parameters
        :return:
        """
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
            del self._histo[1:]
        self._currentperiod = RepetitionsOL(period)
        self.currentperiod.OL_role = self.role
        self.currentperiod.OL_periodcode = pms.GAME
        self.currentperiod.OL_group = self.joueur.groupe
        self.currentperiod.OL_treatment = pms.TREATMENT
        self._le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (self.remote.callRemote("newperiod", period))
        logger.info(u"{} Ready for period {}".format(self.joueur, period))

    @defer.inlineCallbacks
    def display_role(self):
        txt = texts.get_role(self.role)
        yield (self.joueur.get_part("base").remote.callRemote(
            "display_information", txt))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def display_decision(self):
        """
        Display the decision screen on the remote
        Get back the decision
        :return:
        """
        logger.debug(u"{} Decision".format(self.joueur))
        debut = datetime.now()
        if self.role == pms.JOUEUR_A:
            temp = yield(self.remote.callRemote("display_decision_A"))
            self.currentperiod.OL_tirage = temp["dice"]
            self._currentperiod.OL_message = temp["message"]
            self.joueur.info(u"{} - {}".format(
                self.currentperiod.OL_tirage, self.currentperiod.OL_message))
        elif self.role == pms.JOUEUR_B:
            self.currentperiod.OL_decision = yield (
                self.remote.callRemote(
                    "display_decision_B", self.currentperiod.OL_message))
            self.joueur.info(u"{}".format(self.currentperiod.OL_decision))
        self.currentperiod.OL_decisiontime = (datetime.now() - debut).seconds
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        """
        Compute the payoff for the period
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))
        self.currentperiod.OL_periodpayoff = 0
        xa, xb = pms.CODES_PERIODES[pms.GAME][0]
        ya, yb = pms.CODES_PERIODES[pms.GAME][1]
        if self.currentperiod.OL_decision == self.currentperiod.OL_tirage:
            self.currentperiod.OL_appliedoption = pms.OPTION_X
        else:
            self.currentperiod.OL_appliedoption = pms.OPTION_Y

        if self.role == pms.JOUEUR_A:
            if self.currentperiod.OL_appliedoption == pms.OPTION_X:
                self.currentperiod.OL_periodpayoff = xa
            else:
                self.currentperiod.OL_periodpayoff = ya
        else:
            if self.currentperiod.OL_appliedoption == pms.OPTION_X:
                self.currentperiod.OL_periodpayoff = xb
            else:
                self.currentperiod.OL_periodpayoff = yb

        # cumulative payoff since the first period
        if self.currentperiod.OL_period < 2:
            self.currentperiod.OL_cumulativepayoff = \
                self.currentperiod.OL_periodpayoff
        else: 
            previousperiod = self.periods[self.currentperiod.OL_period - 1]
            self.currentperiod.OL_cumulativepayoff = \
                previousperiod.OL_cumulativepayoff + \
                self.currentperiod.OL_periodpayoff

        # we store the period in the self.periodes dictionnary
        self.periods[self.currentperiod.OL_period] = self.currentperiod

        logger.debug(u"{} Period Payoff {}".format(
            self.joueur,
            self.currentperiod.OL_periodpayoff))

    @defer.inlineCallbacks
    def display_summary(self, *args):
        """
        Create the summary (txt and historic) and then display it on the
        remote
        :param args:
        :return:
        """
        logger.debug(u"{} Summary".format(self.joueur))
        self._texte_recapitulatif = texts.get_recapitulatif(
            self.currentperiod, self.role)
        histemp = self._histoA if self.role == pms.JOUEUR_A else self._histoB
        histotemp2 = OrderedDict()
        for k, v in histemp.iteritems():
            histotemp2[k] = getattr(self.currentperiod, v)
            if v == "OL_appliedoption":
                histotemp2[k] = u"X" if histotemp2[k] == pms.OPTION_X else u"Y"

        histo = [list(histotemp2.viewkeys()), list(histotemp2.viewvalues())]
        yield(self.remote.callRemote(
            "display_summary", self._texte_recapitulatif, histo))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()
    
    def compute_partpayoff(self):
        """
        Compute the payoff of the part
        :return:
        """
        logger.debug(u"{} Part Payoff".format(self.joueur))
        # gain partie
        self.OL_gain_ecus = self.currentperiod.OL_cumulativepayoff
        self.OL_gain_euros = \
            float(self.OL_gain_ecus) * float(pms.TAUX_CONVERSION)

        # texte final
        self._texte_final = texts.get_texte_final(
            self.OL_gain_ecus,
            self.OL_gain_euros)

        logger.debug(u"{} Final text {}".format(self.joueur, self._texte_final))
        logger.info(u'{} Payoff ecus {} Payoff euros {:.2f}'.format(
            self.joueur, self.OL_gain_ecus, self.OL_gain_euros))


class RepetitionsOL(Base):
    __tablename__ = 'partie_oathAndLies_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_oathAndLies.partie_id"))

    OL_period = Column(Integer)
    OL_treatment = Column(Integer)
    OL_role = Column(Integer)
    OL_group = Column(Integer)
    OL_periodcode = Column(Integer)
    OL_tirage = Column(Integer)
    OL_message = Column(Integer)
    OL_decision = Column(Integer)
    OL_decisiontime = Column(Integer)
    OL_appliedoption = Column(Integer)
    OL_periodpayoff = Column(Float)
    OL_cumulativepayoff = Column(Float)

    def __init__(self, period):
        self.OL_treatment = pms.TREATMENT
        self.OL_period = period
        self.OL_decisiontime = 0
        self.OL_periodpayoff = 0
        self.OL_cumulativepayoff = 0

    def todict(self, joueur):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        temp["joueur"] = joueur
        return temp

