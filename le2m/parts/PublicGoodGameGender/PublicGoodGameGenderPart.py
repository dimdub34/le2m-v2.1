# -*- coding: utf-8 -*-

from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
import logging
from datetime import datetime
from util.utili18n import le2mtrans
from server.servbase import Base
from server.servparties import Partie
import PublicGoodGameGenderParams as pms
import PublicGoodGameGenderTexts as textes
from PublicGoodGameGenderTexts import _PGGG
from util.utiltools import get_module_attributes


logger = logging.getLogger("le2m")


class PartiePGGG(Partie):
    __tablename__ = "partie_PublicGoodGameGender"
    __mapper_args__ = {'polymorphic_identity': 'PublicGoodGameGender'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsPGGG')

    def __init__(self, le2mserv, joueur):
        super(PartiePGGG, self).__init__("PublicGoodGameGender", "PGGG")
        self._le2mserv = le2mserv
        self.joueur = joueur
        self._texte_recapitulatif = u""
        self._texte_final = u""
        self.PGGG_gain_ecus = 0
        self.PGGG_gain_euros = 0
        self._histo_vars = ["PGGG_period", "PGGG_indiv", "PGGG_public",
                            "PGGG_publicgroup", "PGGG_periodpayoff",
                            "PGGG_cumulativepayoff"]
        self._histo = [
            [le2mtrans(u"Period"), _PGGG(u"Individual\naccount"),
             _PGGG(u"Public\naccount"), _PGGG(u"Total\npublic\naccount"),
             _PGGG(u"Period\npayoff"), _PGGG(u"Cumulative\npayoff")]
        ]
        self.periods = {}
        self._currentperiod = None
        self._groupe = None
        self._groupetype = None

    @property
    def currentperiod(self):
        return self._currentperiod

    def set_groupinfos(self, numgroupe, groupetype):
        """
        :param numgroupe: id of the player's group
        :param groupetype: group type (# of men in the group)
        :return:
        """
        self._groupe = numgroupe
        self._groupetype = groupetype

    @defer.inlineCallbacks
    def configure(self):
        """
        Allow to make changes in the part parameters
        :param args:
        :return:
        """
        logger.debug(u"{} Configure".format(self.joueur))
        yield (self.remote.callRemote("configure", get_module_attributes(pms)))

    @defer.inlineCallbacks
    def newperiod(self, period):
        """
        Create a new period and inform the remote
        If this is the first period then empty the historic
        :param period:
        :return:
        """
        logger.debug(u"{} New Period".format(self.joueur))
        if period == 1:
            del self._histo[1:]
        self._currentperiod = RepetitionsPGGG(period)
        self.currentperiod.PGGG_group = self._groupe
        self.currentperiod.PGGG_grouptype = self._groupetype
        self._le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (
            self.remote.callRemote("newperiod", period, self._groupetype))
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
        self.currentperiod.PGGG_public = \
            yield(
                self.remote.callRemote("display_decision"))
        self.currentperiod.PGGG_decisiontime = \
            (datetime.now() - debut).seconds
        self.currentperiod.PGGG_indiv = \
            pms.DOTATION - self.currentperiod.PGGG_public
        self.joueur.info(u"{}".format(
            self.currentperiod.PGGG_public))
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        """
        Compute the payoff for the period
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))
        self.currentperiod.PGGG_indivpayoff = self.currentperiod.PGGG_indiv * 1
        self.currentperiod.PGGG_publicpayoff = \
            self.currentperiod.PGGG_publicgroup * pms.MPCR
        self.currentperiod.PGGG_periodpayoff = \
            self.currentperiod.PGGG_indivpayoff + \
            self.currentperiod.PGGG_publicpayoff

        # cumulative payoff since the first period
        if self.currentperiod.PGGG_period < 2:
            self.currentperiod.PGGG_cumulativepayoff = \
                self.currentperiod.PGGG_periodpayoff
        else: 
            previousperiod = self.periods[
                self.currentperiod.PGGG_period - 1]
            self.currentperiod.PGGG_cumulativepayoff = \
                previousperiod.PGGG_cumulativepayoff + \
                self.currentperiod.PGGG_periodpayoff

        # we store the period in the self.periodes dictionnary
        self.periods[self.currentperiod.PGGG_period] = self.currentperiod

        logger.debug(u"{} Period Payoff {}".format(
            self.joueur, self.currentperiod.PGGG_periodpayoff))

    @defer.inlineCallbacks
    def display_summary(self, *args):
        """
        Create the summary (txt and historic) and then display it on the
        remote
        :param args:
        :return:
        """
        logger.debug(u"{} Summary".format(self.joueur))
        self._texte_recapitulatif = textes.get_recapitulatif(self.currentperiod)
        self._histo.append(
            [getattr(self.currentperiod, e) for e in self._histo_vars])
        yield(
            self.remote.callRemote(
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
        self.PGGG_gain_ecus = \
            self.currentperiod.PGGG_cumulativepayoff
        self.PGGG_gain_euros = \
            float(self.PGGG_gain_ecus) * \
            float(pms.TAUX_CONVERSION)

        # texte final
        self._texte_final = textes.get_texte_final(
            self.PGGG_gain_ecus, self.PGGG_gain_euros)

        logger.debug(u"{} Final Text {}".format(
            self.joueur, self._texte_final))
        logger.info(u'{} Part Payoff ecus {} Part Payoff euros {:.2f}'.format(
            self.joueur, self.PGGG_gain_ecus, self.PGGG_gain_euros))


class RepetitionsPGGG(Base):
    __tablename__ = 'partie_PublicGoodGameGender_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_PublicGoodGameGender.partie_id"))

    PGGG_period = Column(Integer)
    PGGG_treatment = Column(Integer)
    PGGG_group = Column(Integer)
    PGGG_grouptype = Column(Integer)
    PGGG_indiv = Column(Integer)
    PGGG_public = Column(Integer)
    PGGG_publicgroup = Column(Integer)
    PGGG_decisiontime = Column(Integer)
    PGGG_indivpayoff = Column(Float)
    PGGG_publicpayoff = Column(Float)
    PGGG_periodpayoff = Column(Float)
    PGGG_cumulativepayoff = Column(Float)

    def __init__(self, periode):
        self.PGGG_treatment = pms.TRAITEMENT
        self.PGGG_period = periode
        self.PGGG_decisiontime = 0
        self.PGGG_periodpayoff = 0
        self.PGGG_cumulativepayoff = 0

    def todict(self, joueur):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        temp["joueur"] = joueur
        return temp
