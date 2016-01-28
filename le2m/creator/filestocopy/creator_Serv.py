# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from util import utiltools
import EXPERIENCE_NOMParams as pms


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen)
        actions = OrderedDict()
        actions[u"Configurer"] = self._configure
        actions[u"Afficher les paramètres"] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), u"Paramètres")
        actions[u"Démarrer"] = lambda _: self._demarrer()
        actions[u"Afficher les gains"] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs("EXPERIENCE_NOM")
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"EXPERIENCE_MENU", actions)

    def _configure(self):
        """
        To make changes in the parameters
        :return:
        """
        pass

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(u"Démarrer EXPERIENCE_NOM?")
        if not confirmation:
            return

        # init part
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "EXPERIENCE_NOM", "PartieEXPERIENCE_NOM_COURT",
            "RemoteEXPERIENCE_NOM_COURT", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'EXPERIENCE_NOM')

        # configure part (player and remote)
        yield (self._le2mserv.gestionnaire_experience.run_step(
            u"Configure", self._tous, "configure"))
        
        # form groups
        if pms.TAILLE_GROUPES > 0:
            try:
                self._le2mserv.gestionnaire_groupes.former_groupes(
                    self._le2mserv.gestionnaire_joueurs.get_players(),
                    pms.TAILLE_GROUPES, forcer_nouveaux=True)
            except ValueError as e:
                self._le2mserv.gestionnaire_graphique.display_error(
                    e.message)
                return
    
        # Start repetitions ----------------------------------------------------
        for period in xrange(1 if pms.NOMBRE_PERIODES else 0,
                        pms.NOMBRE_PERIODES + 1):

            if self._le2mserv.gestionnaire_experience.stop_repetitions:
                break

            # init period
            self._le2mserv.gestionnaire_graphique.infoserv(
                [None, u"Période {}".format(period)])
            self._le2mserv.gestionnaire_graphique.infoclt(
                [None, u"Période {}".format(period)], fg="white", bg="gray")
            yield (self._le2mserv.gestionnaire_experience.run_func(
                self._tous, "newperiod", period))
            
            # decision
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Décision", self._tous, "display_decision"))
            
            # period payoffs
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "EXPERIENCE_NOM")
        
            # summary
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Récapitulatif", self._tous, "display_summary"))
        
        # End of part ----------------------------------------------------------
        self._le2mserv.gestionnaire_experience.finalize_part(
            "EXPERIENCE_NOM")
