# -*- coding: utf-8 -*-

from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey, String
import logging
from datetime import datetime
from util.utili18n import le2mtrans
from util.utiltools import get_module_attributes
from server.servbase import Base
from server.servparties import Partie
import PublicGoodGameSolidarityParams as pms
import PublicGoodGameSolidarityTexts as textes
from PublicGoodGameSolidarityTexts import _PGGS
from collections import OrderedDict


logger = logging.getLogger("le2m")


class PartiePGGS(Partie):
    __tablename__ = "partie_PublicGoodGameSolidarity"
    __mapper_args__ = {'polymorphic_identity': 'PublicGoodGameSolidarity'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsPGGS')

    def __init__(self, le2mserv, joueur):
        super(PartiePGGS, self).__init__("PublicGoodGameSolidarity", "PGGS")
        self._le2mserv = le2mserv
        self.joueur = joueur
        self._texte_recapitulatif = u""
        self._texte_final = u""
        self.PGGS_gain_ecus = 0
        self.PGGS_gain_euros = 0
        self._histo_build = OrderedDict()
        self._histo_build[_PGGS(u"Period")] = "PGGS_period"
        self._histo_build[_PGGS(u"Individual\naccount")] = "PGGS_indiv"
        self._histo_build[_PGGS(u"Public\naccount")] = "PGGS_public"
        self._histo_build[_PGGS(u"Total\npublic\naccount")] = "PGGS_publicgroup"
        self._histo_build[_PGGS(u"Period\npayoff")] = "PGGS_periodpayoff"
        self._histo_build[_PGGS(u"Cumulative\npayoff")] = "PGGS_cumulativepayoff"
        self._histo_content = [list(self._histo_build.viewkeys())]
        self._currentsequence = None
        self._currentperiod = None
        self._periods = {}
        self._sequencesgains = {}
        self._ensemble = None
        self._sinistre = False
        self._vote = None
        self._votetime = None
        self._nbvotespour = None
        self._votemajoritaire = None

    @property
    def currentperiod(self):
        return self._currentperiod

    @property
    def sinistre(self):
        return self._sinitre

    @sinistre.setter
    def sinistre(self, torf):
        self._sinistre = torf

    @property
    def ensemble(self):
        return self._ensemble

    @ensemble.setter
    def ensemble(self, val):
        self._ensemble = val

    @property
    def vote(self):
        return self._vote

    @vote.setter
    def vote(self, val):
        self._vote = val

    @property
    def votetime(self):
        return self._votetime

    @votetime.setter
    def votetime(self, val):
        self._votetime = val

    @property
    def nbvotespour(self):
        return self._nbvotespour

    @nbvotespour.setter
    def nbvotespour(self, val):
        self._nbvotespour = val

    @property
    def votemajoritaire(self):
        return self._votemajoritaire

    @votemajoritaire.setter
    def votemajoritaire(self, val):
        self._votemajoritaire = val

    @defer.inlineCallbacks
    def configure(self, current_sequence):
        """
        :param current_sequence:
        :return:
        """
        logger.debug(u"{} Configure".format(self.joueur))
        self._currentsequence = current_sequence
        self._ensemble = None
        self._sinistre = False
        self._vote = None
        self._nbvotespour = None
        self._votemajoritaire = None
        self._periods[self._currentsequence] = {}
        del self._histo_content[1:]
        yield (self.remote.callRemote("configure", get_module_attributes(pms)))

    @defer.inlineCallbacks
    def newperiod(self, period):
        """
        Create a new period and inform the remote
        If this is the first period then empty the history
        :param period:
        :return:
        """
        logger.debug(u"{} New Period".format(self.joueur))
        self._currentperiod = RepetitionsPGGS(period)
        self.currentperiod.PGGS_sequence = self._currentsequence
        self.currentperiod.PGGS_group = self.joueur.groupe
        self.currentperiod.PGGS_ensemble = self.ensemble
        self.currentperiod.PGGS_vote = self.vote
        self.currentperiod.PGGS_votetime = self.votetime
        self.currentperiod.PGGS_nbvotespour = self.nbvotespour
        self.currentperiod.PGGS_votemajoritaire = self.votemajoritaire
        self._le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (self.remote.callRemote("newperiod", period))
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
        self.currentperiod.PGGS_public = \
            yield(self.remote.callRemote("display_decision"))
        self.currentperiod.PGGS_decisiontime = (datetime.now() - debut).seconds
        if self.currentperiod.PGGS_treatment == pms.get_treatments("baseline") \
                or not self.sinistre:
            self.currentperiod.PGGS_indiv = \
                pms.DOTATION - self.currentperiod.PGGS_public
            self.joueur.info(u"{}".format(self.currentperiod.PGGS_public))
        else:
            self.currentperiod.PGGS_indiv = 0
            self.joueur.info(u"-")
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        """
        Compute the payoff for the period
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))
        # sans sinistre
        if self.currentperiod.PGGS_treatment == pms.get_treatments("baseline"):
            self.currentperiod.PGGS_indivpayoff = \
                self.currentperiod.PGGS_indiv * 1
            self.currentperiod.PGGS_publicpayoff = \
                self.currentperiod.PGGS_publicgroup * pms.MPCR
            self.currentperiod.PGGS_periodpayoff = \
                self.currentperiod.PGGS_indivpayoff + \
                self.currentperiod.PGGS_publicpayoff

        else:  # avec sinistre

            if not self.sinistre:  # groupes non sinistrés
                if self.currentperiod.PGGS_treatment == pms.get_treatments(
                        "solidarity_vote"):
                    mpcr = pms.MPCR_ens if \
                        self.votemajoritaire == pms.get_votes("pour") else pms.MPCR
                elif self.currentperiod.PGGS_treatment == pms.get_treatments(
                        "without_solidarity"):
                    mpcr = pms.MPCR
                elif self.currentperiod.PGGS_treatment == pms.get_treatments(
                        "solidarity_auto"):
                    mpcr = pms.MPCR_ens

                self.currentperiod.PGGS_indivpayoff = \
                    self.currentperiod.PGGS_indiv * 1
                self.currentperiod.PGGS_publicpayoff = \
                    self.currentperiod.PGGS_publicgroup * mpcr
                self.currentperiod.PGGS_periodpayoff = \
                    self.currentperiod.PGGS_indivpayoff + \
                    self.currentperiod.PGGS_publicpayoff

            else:  # groupes sinistrés
                if self.currentperiod.PGGS_treatment == pms.get_treatments(
                        "without_solidarity"):
                    self.currentperiod.PGGS_indivpayoff = 0
                    self.currentperiod.PGGS_publicpayoff = 0
                    self.currentperiod.PGGS_periodpayoff = 0
                else:
                    if self.currentperiod.PGGS_treatment == pms.get_treatments(
                            "solidarity_auto"):
                        mpcr = pms.MPCR_ens
                    elif self.currentperiod.PGGS_treatment == pms.get_treatments(
                            "solidarity_vote"):
                        mpcr = pms.MPCR_ens if \
                            self.votemajoritaire == pms.get_votes("pour") else \
                            pms.MPCR
                    self.currentperiod.PGGS_indivpayoff = 0
                    self.currentperiod.PGGS_publicpayoff = \
                        self.currentperiod.PGGS_publicgroup * mpcr
                    self.currentperiod.PGGS_periodpayoff = \
                        self.currentperiod.PGGS_publicpayoff

        # cumulative payoff since the first period
        if self.currentperiod.PGGS_period < 2:
            self.currentperiod.PGGS_cumulativepayoff = \
                self.currentperiod.PGGS_periodpayoff
        else: 
            previousperiod = self._periods[self._currentsequence][
                self.currentperiod.PGGS_period - 1]
            self.currentperiod.PGGS_cumulativepayoff = \
                previousperiod.PGGS_cumulativepayoff + \
                self.currentperiod.PGGS_periodpayoff

        # we store the period in the self.periodes dictionnary
        self._periods[self._currentsequence][self.currentperiod.PGGS_period] = \
            self.currentperiod

        logger.debug(u"{} Period Payoff {}".format(
            self.joueur, self.currentperiod.PGGS_periodpayoff))

    @defer.inlineCallbacks
    def display_summary(self):
        """
        Create the summary (txt and historic) and then display it on the
        remote
        :param args:
        :return:
        """
        logger.debug(u"{} Summary".format(self.joueur))

        self._texte_recapitulatif = textes.get_recapitulatif(self.currentperiod)
        self._histo_content.append(
            [getattr(self.currentperiod, e) for e in
             self._histo_build.viewvalues()])
        yield(self.remote.callRemote(
                "display_summary", self._texte_recapitulatif,
                self._histo_content))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()
    
    def compute_partpayoff(self):
        """
        Compute the payoff of the part
        :return:
        """
        logger.debug(u"{} Part Payoff".format(self.joueur))
        # gain partie
        self.PGGS_gain_ecus = \
            self.currentperiod.PGGS_cumulativepayoff
        self.PGGS_gain_euros = \
            float(self.PGGS_gain_ecus) * \
            float(pms.TAUX_CONVERSION)

        # texte final
        self._texte_final = textes.get_texte_final(
            self.PGGS_gain_ecus, self.PGGS_gain_euros)

        logger.debug(u"{} Final Text {}".format(
            self.joueur, self._texte_final))
        logger.info(u'{} Part Payoff ecus {} Part Payoff euros {:.2f}'.format(
            self.joueur, self.PGGS_gain_ecus, self.PGGS_gain_euros))

        self._sequencesgains[self._currentsequence] = {
            "gain": self.PGGS_gain_euros, "texte": self._texte_final}

    def get_sequencesgains(self, which=None):
        return self._sequencesgains.get(which) or self._sequencesgains.copy()

    @defer.inlineCallbacks
    def display_sinistre(self):
        yield (self.joueur.get_part("base").display_information(
            u"Sinistré" if self.sinistre else u"Non sinistré"))
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def display_vote(self):
        deb = datetime.now()
        self.vote = yield (
            self.remote.callRemote("display_vote"))
        self.votetime = (datetime.now() - deb).seconds
        self.joueur.info(pms.get_votes(self.vote))

    @defer.inlineCallbacks
    def display_resultvotes(self):
        yield (self.joueur.get_part("base").display_information(
            textes.get_resultvote(self.sinistre, self.nbvotespour,
                                  self.votemajoritaire)))
        self.joueur.remove_waitmode()


class RepetitionsPGGS(Base):
    __tablename__ = 'partie_PublicGoodGameSolidarity_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_PublicGoodGameSolidarity.partie_id"))

    PGGS_sequence = Column(Integer)
    PGGS_period = Column(Integer)
    PGGS_treatment = Column(Integer)
    PGGS_ensemble = Column(String)
    PGGS_group = Column(String)
    PGGS_dotation = Column(Integer)
    PGGS_indiv = Column(Integer)
    PGGS_public = Column(Integer)
    PGGS_publicgroup = Column(Integer)
    PGGS_decisiontime = Column(Integer)
    PGGS_vote = Column(Integer)
    PGGS_votetime = Column(Integer)
    PGGS_nbvotespour = Column(Integer)
    PGGS_votemajoritaire = Column(Integer)
    PGGS_indivpayoff = Column(Float)
    PGGS_publicpayoff = Column(Float)
    PGGS_periodpayoff = Column(Float)
    PGGS_cumulativepayoff = Column(Float)

    def __init__(self, periode):
        self.PGGS_treatment = pms.TRAITEMENT
        self.PGGS_period = periode
        self.PGGS_dotation = pms.DOTATION
        self.PGGS_decisiontime = 0
        self.PGGS_periodpayoff = 0
        self.PGGS_cumulativepayoff = 0

    def todict(self, joueur):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        temp["joueur"] = joueur
        return temp
