# -*- coding: utf-8 -*-

# built-in
import logging
from datetime import datetime

from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from twisted.internet import defer
from twisted.spread import pb  # because some functions can be called remotely

import murielle_jeu_params as pms
from server.servbase import Base
from server.servparties import Partie
from util.utiltools import get_module_attributes

logger = logging.getLogger("le2m")


class PartieGA(Partie, pb.Referenceable):
    __tablename__ = "partie_murielle_jeu"
    __mapper_args__ = {'polymorphic_identity': 'murielle_jeu'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    instants = relationship("InstantsGA")
    curves = relationship("CurveGA")
    GA_dynamic_type = Column(Integer)
    GA_trial = Column(Boolean)
    GA_sequence = Column(Integer)
    GA_treatment = Column(Integer)
    GA_group = Column(String)
    GA_gain_ecus = Column(Float)
    GA_gain_euros = Column(Float)

    def __init__(self, le2mserv, joueur, **kwargs):
        super(PartieGA, self).__init__(nom="murielle_jeu", nom_court="GA",
                                       joueur=joueur, le2mserv=le2mserv)
        self.GA_sequence = kwargs.get("current_sequence", 0)
        self.GA_gain_ecus = 0
        self.GA_gain_euros = 0

    @defer.inlineCallbacks
    def configure(self):
        logger.debug(u"{} Configure".format(self.joueur))
        self.GA_dynamic_type = pms.DYNAMIC_TYPE
        self.GA_treatment = pms.TREATMENT
        self.GA_trial = pms.PARTIE_ESSAI
        yield (self.remote.callRemote("configure", get_module_attributes(pms), self))
        self.joueur.info(u"Ok")

    def new_instant(self, the_n):
        self.current_instant = InstantsGA(instant=the_n)
        if the_n == 0:
            self.current_instant.GA_extraction = 0
        else:
            self.previous_instant = self.instants[-1]
            self.current_instant.GA_extraction = self.previous_instant.GA_extraction
            logger.debug("previous_instant: {}".format(self.previous_instant.to_dict()))
        self.le2mserv.gestionnaire_base.ajouter(self.current_instant)
        self.instants.append(self.current_instant)

    @defer.inlineCallbacks
    def set_initial_extraction(self):
        self.current_instant.GA_extraction = yield (self.remote.callRemote("set_initial_extraction"))
        self.joueur.info(self.current_instant.GA_extraction)
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def display_decision(self, the_n):
        if pms.DYNAMIC_TYPE == pms.DISCRETE:
            self.new_instant(the_n)
            extraction = yield (self.remote.callRemote("display_decision", the_n))
            self.remote_new_extraction(extraction)
        else:
            yield (self.remote.callRemote("display_decision", the_n))
        self.joueur.remove_waitmode()

    def remote_new_extraction(self, extraction):
        self.current_instant.GA_extraction = extraction
        self.joueur.info(self.current_instant.GA_extraction)

    @defer.inlineCallbacks
    def update_data(self, the_n, ressource):
        self.current_instant.GA_resource = ressource
        cost = (pms.c0 - pms.c1 * self.current_instant.GA_resource) * self.current_instant.GA_extraction
        if cost < 0:
            cost = 0
        self.current_instant.GA_cost = cost
        self.current_instant.GA_instant_payoff = pms.get_gain_instantane(
            self.current_instant.GA_instant, self.current_instant.GA_extraction, self.current_instant.GA_resource)
        if the_n == 0:
            self.current_instant.GA_cumulative_instant_payoff = self.current_instant.GA_instant_payoff * pms.tau
        else:
            self.current_instant.GA_cumulative_instant_payoff = self.previous_instant.GA_cumulative_instant_payoff + \
                                                                self.current_instant.GA_instant_payoff * pms.tau
        self.current_instant.GA_part_payoff = self.current_instant.GA_cumulative_instant_payoff + pms.get_infinite_payoff(
            self.current_instant.GA_instant, self.current_instant.GA_resource, self.current_instant.GA_extraction)
        logger.debug("current_instant: {}".format(self.current_instant.to_dict()))
        yield(self.remote.callRemote("update_data", self.current_instant.to_dict()))

    @defer.inlineCallbacks
    def end_update_data(self):
        yield (self.remote.callRemote("end_update_data"))

    @defer.inlineCallbacks
    def display_summary(self, *args):
        logger.debug(u"{} Summary".format(self.joueur))
        data_indiv = yield (self.remote.callRemote("display_summary", self.current_instant.to_dict()))
        logger.debug("{}: {}".format(self.joueur, data_indiv.keys()))

        try:
            extrac_indiv = data_indiv["extractions"]
            for x, y in extrac_indiv:
                curve_data = CurveGA(pms.EXTRACTION, x, y)
                self.le2mserv.gestionnaire_base.ajouter(curve_data)
                self.curves.append(curve_data)
        except Exception as err:
            logger.warning(err.message)

        try:
            payoff_indiv = data_indiv["payoffs"]
            for x, y in payoff_indiv:
                curve_data = CurveGA(pms.PAYOFF, x, y)
                self.le2mserv.gestionnaire_base.ajouter(curve_data)
                self.curves.append(curve_data)
            # we collect the part payoff
            self.GA_gain_ecus = payoff_indiv[-1][1]
        except Exception as err:
            logger.warning(err.message)

        try:
            resource = data_indiv["resource"]
            for x, y in resource:
                curve_data = CurveGA(pms.RESOURCE, x, y)
                self.le2mserv.gestionnaire_base.ajouter(curve_data)
                self.curves.append(curve_data)
        except Exception as err:
            logger.warning(err.message)

        self.joueur.info("Ok")
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def compute_partpayoff(self):
        logger.debug(u"{} Part Payoff".format(self.joueur))
        self.GA_gain_ecus = self.current_instant.GA_part_payoff
        self.GA_gain_euros = float("{:.2f}".format(self.GA_gain_ecus * pms.TAUX_CONVERSION))
        yield (self.remote.callRemote("set_payoffs", self.GA_gain_euros, self.GA_gain_ecus))
        logger.info(u'{} Payoff ecus {:.2f} Payoff euros {:.2f}'.format(
            self.joueur, self.GA_gain_ecus, self.GA_gain_euros))


class InstantsGA(Base):
    __tablename__ = "partie_murielle_jeu_instants"
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_murielle_controle_id = Column(Integer, ForeignKey("partie_murielle_jeu.partie_id"))
    GA_instant = Column(Integer)
    GA_extraction = Column(Float, default=None)
    GA_resource = Column(Float)
    GA_cost = Column(Float)
    GA_instant_payoff = Column(Float)
    GA_cumulative_instant_payoff = Column(Float)
    GA_part_payoff = Column(Float)

    def __init__(self, instant):
        self.GA_instant = instant

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CurveGA(Base):
    __tablename__ = "partie_murielle_jeu_curves"
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_id = Column(Integer, ForeignKey("partie_murielle_jeu.partie_id"))
    GA_curve_type = Column(Integer)
    GA_curve_x = Column(Integer)
    GA_curve_y = Column(Float)

    def __init__(self, c_type, x, y):
        self.GA_curve_type = c_type
        self.GA_curve_x = x
        self.GA_curve_y = y
