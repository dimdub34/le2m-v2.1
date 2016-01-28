# -*- coding: utf-8 -*-

from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
import logging
from datetime import datetime
from util.utili18n import le2mtrans
from server.servbase import Base
from server.servparties import Partie
import PublicGoodGameParams as parametres
import PublicGoodGameTexts as textes
from PublicGoodGameTexts import _PGG


logger = logging.getLogger("le2m")


class PartiePGG(Partie):
    __tablename__ = "partie_PublicGoodGame"
    __mapper_args__ = {'polymorphic_identity': 'PublicGoodGame'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsPGG')

    def __init__(self, le2mserv, joueur):
        super(PartiePGG, self).__init__("PublicGoodGame", "PGG")
        self._le2mserv = le2mserv
        self.joueur = joueur
        self._texte_recapitulatif = u""
        self._texte_final = u""
        self.PGG_gain_ecus = 0
        self.PGG_gain_euros = 0
        self._histo_vars = ["PGG_period", "PGG_indiv", "PGG_public",
                            "PGG_publicgroup", "PGG_periodpayoff",
                            "PGG_cumulativepayoff"]
        self._histo = [
            [le2mtrans(u"Period"), _PGG(u"Individual\naccount"),
             _PGG(u"Public\naccount"), _PGG(u"Total\npublic\naccount"),
             _PGG(u"Period\npayoff"), _PGG(u"Cumulative\npayoff")]
        ]
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
        :param period:
        :return:
        """
        logger.debug(u"{} New Period".format(self.joueur))
        if period == 1:
            del self._histo[1:]
        self.currentperiod = RepetitionsPGG(period)
        self.currentperiod.PGG_group = self.joueur.groupe
        self._le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (
            self.remote.callRemote("newperiod", period))
        logger.info(u"{} Ready for periode {}".format(self.joueur, period))

    @defer.inlineCallbacks
    def display_decision(self):
        """
        Display the decision screen on the remote
        Get back the decision
        :return:
        """
        logger.debug(u"{} Decision".format(self.joueur))
        debut = datetime.now()
        self.currentperiod.PGG_public = \
            yield(
                self.remote.callRemote("display_decision"))
        self.currentperiod.PGG_decisiontime = \
            (datetime.now() - debut).seconds
        self.currentperiod.PGG_indiv = \
            parametres.DOTATION - self.currentperiod.PGG_public
        self.joueur.info(u"{}".format(
            self.currentperiod.PGG_public))
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        """
        Compute the payoff for the period
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))
        self.currentperiod.PGG_indivpayoff = self.currentperiod.PGG_indiv * 1
        self.currentperiod.PGG_publicpayoff = \
            self.currentperiod.PGG_publicgroup * parametres.MPCR
        self.currentperiod.PGG_periodpayoff = \
            self.currentperiod.PGG_indivpayoff + \
            self.currentperiod.PGG_publicpayoff

        # cumulative payoff since the first period
        if self.currentperiod.PGG_period < 2:
            self.currentperiod.PGG_cumulativepayoff = \
                self.currentperiod.PGG_periodpayoff
        else: 
            previousperiod = self.periods[
                self.currentperiod.PGG_period - 1]
            self.currentperiod.PGG_cumulativepayoff = \
                previousperiod.PGG_cumulativepayoff + \
                self.currentperiod.PGG_periodpayoff

        # we store the period in the self.periodes dictionnary
        self.periods[self.currentperiod.PGG_period] = self.currentperiod

        logger.debug(u"{} Period Payoff {}".format(
            self.joueur, self.currentperiod.PGG_periodpayoff))

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
        self.PGG_gain_ecus = \
            self.currentperiod.PGG_cumulativepayoff
        self.PGG_gain_euros = \
            float(self.PGG_gain_ecus) * \
            float(parametres.TAUX_CONVERSION)

        # texte final
        self._texte_final = textes.get_texte_final(
            self.PGG_gain_ecus, self.PGG_gain_euros)

        logger.debug(u"{} Final Text {}".format(
            self.joueur, self._texte_final))
        logger.info(u'{} Part Payoff ecus {} Part Payoff euros {:.2f}'.format(
            self.joueur, self.PGG_gain_ecus, self.PGG_gain_euros))


class RepetitionsPGG(Base):
    __tablename__ = 'partie_PublicGoodGame_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_PublicGoodGame.partie_id"))

    PGG_period = Column(Integer)
    PGG_treatment = Column(Integer)
    PGG_group = Column(Integer)
    PGG_indiv = Column(Integer)
    PGG_public = Column(Integer)
    PGG_publicgroup = Column(Integer)
    PGG_decisiontime = Column(Integer)
    PGG_indivpayoff = Column(Float)
    PGG_publicpayoff = Column(Float)
    PGG_periodpayoff = Column(Float)
    PGG_cumulativepayoff = Column(Float)

    def __init__(self, periode):
        self.PGG_treatment = parametres.TRAITEMENT
        self.PGG_period = periode
        self.PGG_decisiontime = 0
        self.PGG_periodpayoff = 0
        self.PGG_cumulativepayoff = 0

    def todict(self, joueur):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        temp["joueur"] = joueur
        return temp
