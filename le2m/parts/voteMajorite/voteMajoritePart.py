# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from collections import OrderedDict
from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey, String
from server.servbase import Base
from server.servparties import Partie
from util.utili18n import le2mtrans
from util.utiltools import get_module_attributes
import voteMajoriteParams as pms
import voteMajoriteTexts as texts


logger = logging.getLogger("le2m")


class PartieVM(Partie):
    __tablename__ = "partie_voteMajorite"
    __mapper_args__ = {'polymorphic_identity': 'voteMajorite'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsVM')

    def __init__(self, le2mserv, joueur):
        super(PartieVM, self).__init__("voteMajorite", "VM")
        self._le2mserv = le2mserv
        self.joueur = joueur
        self._texte_recapitulatif = u""
        self._texte_final = u""
        self.VM_gain_ecus = 0
        self.VM_gain_euros = 0
        self._histo_build = OrderedDict()
        self._histo_build["Politique"] = "VM_period"
        self._histo_build["Votre vote"] = "VM_decision"
        self._histo_build["Vote majoritaire"] = "VM_majority"
        self._histo_build["Votre gain"] = "VM_periodpayoff"
        self._histo_content = [list(self._histo_build.viewkeys())]
        self.periods = {}
        self._currentperiod = None
        self._profil = None

    @property
    def profil(self):
        return self._profil

    @profil.setter
    def profil(self, val):
        self._profil = val

    @property
    def currentperiod(self):
        return self._currentperiod

    @defer.inlineCallbacks
    def configure(self):
        """
        Send the parameters to the remote
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
        :param period:
        :return:
        """
        logger.debug(u"{} New Period".format(self.joueur))
        if period == 1:
            del self._histo_content[1:]
        self._currentperiod = RepetitionsVM(period)
        self.currentperiod.VM_group = self.joueur.groupe
        self.currentperiod.VM_profil = self.profil
        self.currentperiod.VM_treatment = pms.TREATMENT
        self.currentperiod.VM_dotation = pms.DOTATION
        self.currentperiod.VM_cout = pms.COUT
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
        self.currentperiod.VM_decision = yield(self.remote.callRemote(
            "display_decision", self.profil))
        self.currentperiod.VM_decisiontime = (datetime.now() - debut).seconds
        self.joueur.info(u"{}".format(self.currentperiod.VM_decision))
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        """
        Compute the payoff for the period
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))

        if self.currentperiod.VM_majority == pms.POUR:
            benef = pms.PROFILS[self.currentperiod.VM_profil][
                self.currentperiod.VM_period-1]
            cout = self.currentperiod.VM_cout
            self.currentperiod.VM_periodpayoff = benef - cout
        else:
            self.currentperiod.VM_periodpayoff = 0

        # cumulative payoff since the first period
        if self.currentperiod.VM_period < 2:
            self.currentperiod.VM_cumulativepayoff = \
                self.currentperiod.VM_periodpayoff
        else: 
            previousperiod = self.periods[self.currentperiod.VM_period - 1]
            self.currentperiod.VM_cumulativepayoff = \
                previousperiod.VM_cumulativepayoff + \
                self.currentperiod.VM_periodpayoff

        # we store the period in the self.periodes dictionnary
        self.periods[self.currentperiod.VM_period] = self.currentperiod

        logger.debug(u"{} Period Payoff {}".format(
            self.joueur,
            self.currentperiod.VM_periodpayoff))

    @defer.inlineCallbacks
    def display_summary(self, *args):
        """
        Create the summary (txt and historic) and then display it on the
        remote
        :param args:
        :return:
        """
        logger.debug(u"{} Summary".format(self.joueur))
        # gain partie
        self.VM_gain_ecus = \
            pms.DOTATION + self.currentperiod.VM_cumulativepayoff
        self.VM_gain_euros = \
            float(self.VM_gain_ecus) * float(pms.TAUX_CONVERSION)
        self._texte_recapitulatif = texts.get_recapitulatif(
            self.periods, self.VM_gain_ecus, self.VM_gain_euros)

        for i in range(1, pms.NOMBRE_PERIODES + 1):
            period = self.periods[i]
            line = []
            for v in self._histo_build.viewvalues():
                val = getattr(period, v)
                if v == "VM_decision" or v == "VM_majority":
                    line.append(u"Pour" if val == pms.POUR else u"Contre")
                else:
                    line.append(val)
            self._histo_content.append(line)

        yield(self.remote.callRemote(
            "display_summary", self._texte_recapitulatif, self._histo_content,
            self.profil))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()
    
    def compute_partpayoff(self):
        """
        Compute the payoff of the part
        :return:
        """
        logger.debug(u"{} Part Payoff".format(self.joueur))
        # gain déterminé dans display_summary
        # texte final
        self._texte_final = texts.get_texte_final(
            self.VM_gain_ecus, self.VM_gain_euros)

        logger.debug(u"{} Final text {}".format(self.joueur, self._texte_final))
        logger.info(u'{} Payoff ecus {} Payoff euros {:.2f}'.format(
            self.joueur, self.VM_gain_ecus, self.VM_gain_euros))


class RepetitionsVM(Base):
    __tablename__ = 'partie_voteMajorite_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_voteMajorite.partie_id"))

    VM_period = Column(Integer)
    VM_treatment = Column(Integer)
    VM_group = Column(Integer)
    VM_profil = Column(String)
    VM_dotation = Column(Integer)
    VM_cout = Column(Float)
    VM_decision = Column(Integer)
    VM_decisiontime = Column(Integer)
    VM_pour = Column(Integer)
    VM_contre = Column(Integer)
    VM_majority = Column(Integer)
    VM_periodpayoff = Column(Float)
    VM_cumulativepayoff = Column(Float)

    def __init__(self, period):
        self.VM_treatment = pms.TREATMENT
        self.VM_period = period
        self.VM_decisiontime = 0
        self.VM_periodpayoff = 0
        self.VM_cumulativepayoff = 0

    def todict(self, joueur):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        temp["joueur"] = joueur
        return temp

