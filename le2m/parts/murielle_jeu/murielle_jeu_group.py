# -*- coding: utf-8 -*-

# built-in
from server.servbase import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean
import logging
from twisted.internet import defer
import numpy as np
from datetime import datetime
from server.srvgroup import Group
# dynamicCPR
import murielle_jeu_params as pms
# from murielle_jeuPart import ExtractionsGA_

logger = logging.getLogger("le2m")


class GroupGA(Base, Group):
    __tablename__ = "group_GA"
    uid = Column(String(30), primary_key=True)
    session_id = Column(Integer)
    instants = relationship("GroupInstantsGA")
    GA_dynamic_type = Column(Integer)
    GA_trial = Column(Boolean)
    GA_sequence = Column(Integer)
    GA_treatment = Column(Integer)

    def __init__(self, le2mserv, group_id, player_list, sequence):
        Group.__init__(self, le2mserv, uid=group_id, players=player_list)
        self.GA_dynamic_type = pms.DYNAMIC_TYPE
        self.GA_sequence = sequence
        self.GA_treatment = pms.TREATMENT
        self.GA_trial = pms.PARTIE_ESSAI
        for p in self.get_players_parts("murielle_jeu"):  # add group.uid to players.group field
            p.GA_group = self.uid

    def new_instant(self, the_n):
        self.current_instant = GroupInstantsGA(the_n)
        if the_n == 0:
            self.current_instant.GA_extraction = 0
        else:
            self.previous_instant = self.instants[-1]
            self.current_instant.GA_extraction = self.previous_instant.GA_extraction
            logger.debug("previous_instant: {}".format(self.previous_instant.to_dict()))
        self.le2mserv.gestionnaire_base.ajouter(self.current_instant)
        self.instants.append(self.current_instant)

    @defer.inlineCallbacks
    def update_data(self, the_n):
        self.current_instant.GA_extraction = np.sum([p.current_instant.GA_extraction for p in self.get_players_part("murielle_jeu")])
        if the_n == 0:
            self.current_instant.GA_ressource = pms.get_ressource(
                self.current_instant.GA_instant, pms.RESOURCE_INITIAL_STOCK, self.current_instant.GA_extraction)
        else:
            if self.current_instant.GA_extraction > self.previous_instant.GA_resource:
                for p in self.get_players_part("murielle_jeu"):
                    p.current_instant.GA_extraction = 0
                self.current_instant.GA_extraction = 0
            self.current_instant.GA_ressource = pms.get_ressource(
                self.current_instant.GA_instant, self.previous_instant.GA_resource, self.current_instant.GA_extraction)
        logger.debug("current_instant: {}".format(self.current_instant.to_dict()))
        yield (self.le2mserv.gestionnaire_experience.run_func(self.get_players_part("murielle_jeu"), "update_data",
                                                              self.the_n, self.current_instant.GA_ressource))


class GroupInstantsGA(Base):
    __tablename__ = "group_instants"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_uid = Column(String, ForeignKey("group_GA.uid"))

    GA_instant = Column(Integer, default=None)
    GA_extraction = Column(Float, default=0)
    GA_ressource = Column(Float)

    def __init__(self, the_n):
        self.GA_instant = the_n

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
