# -*- coding: utf-8 -*-

# built-in
import logging
from datetime import datetime

from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from twisted.internet import defer
from twisted.spread import pb  # because some functions can be called remotely

import murielle_controle_params as pms
from server.servbase import Base
from server.servparties import Partie
from util.utiltools import get_module_attributes

logger = logging.getLogger("le2m")


class PartieCO(Partie, pb.Referenceable):
    __tablename__ = "partie_murielle_controle"
    __mapper_args__ = {'polymorphic_identity': 'murielle_controle'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    instants = relationship("InstantsCO")
    curves = relationship("CurveCO")
    CO_dynamic_type = Column(Integer)
    CO_trial = Column(Boolean)
    CO_sequence = Column(Integer)
    CO_treatment = Column(Integer)
    CO_gain_ecus = Column(Float)
    CO_gain_euros = Column(Float)

    def __init__(self, le2mserv, joueur, **kwargs):
        super(PartieCO, self).__init__(nom="murielle_controle", nom_court="CO",
                                       joueur=joueur, le2mserv=le2mserv)
        self.CO_sequence = kwargs.get("current_sequence", 0)
        self.CO_gain_ecus = 0
        self.CO_gain_euros = 0

    @defer.inlineCallbacks
    def configure(self):
        logger.debug(u"{} Configure".format(self.joueur))
        self.CO_dynamic_type = pms.DYNAMIC_TYPE
        self.CO_treatment = pms.TREATMENT
        self.CO_trial = pms.PARTIE_ESSAI
        yield (self.remote.callRemote("configure", get_module_attributes(pms), self))
        self.joueur.info(u"Ok")

    def new_instant(self, the_n):
        self.current_instant = InstantsCO(instant=the_n)
        if the_n == 0:
            self.current_instant.CO_extraction = 0
        else:
            self.previous_instant = self.instants[-1]
            self.current_instant.CO_extraction = self.previous_instant.CO_extraction
            logger.debug("previous_instant: {}".format(self.previous_instant.to_dict()))
        self.le2mserv.gestionnaire_base.ajouter(self.current_instant)
        self.instants.append(self.current_instant)

    @defer.inlineCallbacks
    def set_initial_extraction(self):
        self.new_instant(0)
        self.current_instant.CO_extraction = yield (self.remote.callRemote("set_initial_extraction"))
        self.joueur.info(self.current_instant.CO_extraction)
        self.joueur.remove_waitmode()
        yield(self.update_data(0))

    @defer.inlineCallbacks
    def display_decision(self, the_n):
        if pms.DYNAMIC_TYPE == pms.DISCRETE:
            self.new_instant(the_n)
            extraction = yield (self.remote.callRemote("display_decision", the_n))
            self.remote_new_extraction(extraction)
            yield(self.update_data(the_n))
        else:
            yield (self.remote.callRemote("display_decision", the_n))
        self.joueur.remove_waitmode()

    def remote_new_extraction(self, extraction):
        self.current_instant.CO_extraction = extraction
        if self.current_instant.CO_instant > 0:
            if self.current_instant.CO_extraction > self.previous_instant.CO_resource:
                self.current_instant.CO_extraction = 0
        self.joueur.info(self.current_instant.CO_extraction)

    @defer.inlineCallbacks
    def update_data(self, the_n):
        if the_n == 0:
            self.current_instant.CO_resource = pms.get_ressource(
                self.current_instant.CO_instant, pms.RESOURCE_INITIAL_STOCK, self.current_instant.CO_extraction)
        else:
            self.current_instant.CO_resource = pms.get_ressource(
                self.current_instant.CO_instant, self.previous_instant.CO_resource, self.current_instant.CO_extraction)
        cost = (pms.c0 - pms.c1 * self.current_instant.CO_resource) * self.current_instant.CO_extraction
        if cost < 0:
            cost = 0
        self.current_instant.CO_cost = cost
        self.current_instant.CO_instant_payoff = pms.get_gain_instantane(
            self.current_instant.CO_instant, self.current_instant.CO_extraction, self.current_instant.CO_resource)
        if the_n == 0:
            self.current_instant.CO_cumulative_instant_payoff = self.current_instant.CO_instant_payoff * pms.tau
        else:
            self.current_instant.CO_cumulative_instant_payoff = self.previous_instant.CO_cumulative_instant_payoff + \
                                                                self.current_instant.CO_instant_payoff * pms.tau
        self.current_instant.CO_part_payoff = self.current_instant.CO_cumulative_instant_payoff + pms.get_infinite_payoff(
            self.current_instant.CO_instant, self.current_instant.CO_resource, self.current_instant.CO_extraction)
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
                curve_data = CurveCO(pms.EXTRACTION, x, y)
                self.le2mserv.gestionnaire_base.ajouter(curve_data)
                self.curves.append(curve_data)
        except Exception as err:
            logger.warning(err.message)

        try:
            payoff_indiv = data_indiv["payoffs"]
            for x, y in payoff_indiv:
                curve_data = CurveCO(pms.PAYOFF, x, y)
                self.le2mserv.gestionnaire_base.ajouter(curve_data)
                self.curves.append(curve_data)
            # we collect the part payoff
            self.CO_gain_ecus = payoff_indiv[-1][1]
        except Exception as err:
            logger.warning(err.message)

        try:
            resource = data_indiv["resource"]
            for x, y in resource:
                curve_data = CurveCO(pms.RESOURCE, x, y)
                self.le2mserv.gestionnaire_base.ajouter(curve_data)
                self.curves.append(curve_data)
        except Exception as err:
            logger.warning(err.message)

        # try:
        #     cost = data_indiv["cost"]
        #     for x, y in cost:
        #         curve_data = CurveCO(pms.COST, x, y)
        #         self.le2mserv.gestionnaire_base.ajouter(curve_data)
        #         self.curves.append(curve_data)
        # except Exception as err:
        #     logger.warning(err.message)

        self.joueur.info("Ok")
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def compute_partpayoff(self):
        logger.debug(u"{} Part Payoff".format(self.joueur))
        self.CO_gain_ecus = self.current_instant.CO_part_payoff
        self.CO_gain_euros = float("{:.2f}".format(self.CO_gain_ecus * pms.TAUX_CONVERSION))
        yield (self.remote.callRemote("set_payoffs", self.CO_gain_euros, self.CO_gain_ecus))
        logger.info(u'{} Payoff ecus {:.2f} Payoff euros {:.2f}'.format(
            self.joueur, self.CO_gain_ecus, self.CO_gain_euros))


class InstantsCO(Base):
    __tablename__ = "partie_murielle_controle_instants"
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_murielle_controle_id = Column(Integer, ForeignKey("partie_murielle_controle.partie_id"))
    CO_instant = Column(Integer)
    CO_extraction = Column(Float, default=None)
    CO_resource = Column(Float)
    CO_cost = Column(Float)
    CO_instant_payoff = Column(Float)
    CO_cumulative_instant_payoff = Column(Float)
    CO_part_payoff = Column(Float)

    def __init__(self, instant):
        self.CO_instant = instant

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CurveCO(Base):
    __tablename__ = "partie_murielle_controle_curves"
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_id = Column(Integer, ForeignKey("partie_murielle_controle.partie_id"))
    CO_curve_type = Column(Integer)
    CO_curve_x = Column(Integer)
    CO_curve_y = Column(Float)

    def __init__(self, c_type, x, y):
        self.CO_curve_type = c_type
        self.CO_curve_x = x
        self.CO_curve_y = y
