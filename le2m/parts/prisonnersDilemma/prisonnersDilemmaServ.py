# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from util import utiltools
import prisonnersDilemmaParams as pms
import prisonnersDilemmaPart  # for sqlalchemy


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen
        actions = OrderedDict()
        actions[u"Configurer"] = self._configure
        actions[u"Afficher les paramètres"] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), u"Paramètres")
        actions[u"Démarrer"] = lambda _: self._demarrer()
        actions[u"Afficher les gains"] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs("prisonnersDilemma")
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Prisonner's dillemma", actions)

    def _configure(self):
        """
        To make changes in the parameters
        :return:
        """
        self._le2mserv.gestionnaire_graphique.display_information2(
            u"Aucun paramètre à configurer")

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(u"Démarrer prisonnersDilemma?")
        if not confirmation:
            return
        
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "prisonnersDilemma", "PartieDP",
            "RemoteDP", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'prisonnersDilemma')
        
        # formation des groupes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if pms.TAILLE_GROUPES > 0:
            try:
                self._le2mserv.gestionnaire_groupes.former_groupes(
                    self._le2mserv.gestionnaire_joueurs.get_players(),
                    pms.TAILLE_GROUPES, forcer_nouveaux=True)
            except ValueError as e:
                self._le2mserv.gestionnaire_graphique.display_error(
                    e.message)
                return
    
        # pour configure les clients et les remotes ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        yield (self._le2mserv.gestionnaire_experience.run_func(
            self._tous, "configure"))
    
        # DEBUT DES RÉPÉTITIONS ================================================
        for period in xrange(1 if pms.NOMBRE_PERIODES else 0,
                        pms.NOMBRE_PERIODES + 1):

            if self._le2mserv.gestionnaire_experience.stop_repetitions:
                break

            # initialisation période ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._le2mserv.gestionnaire_graphique.infoserv(
                [None, u"Période {}".format(period)])
            self._le2mserv.gestionnaire_graphique.infoclt(
                [None, u"Période {}".format(period)], fg="white", bg="gray")
            yield (self._le2mserv.gestionnaire_experience.run_func(
                self._tous, "newperiod", period))
            
            # décision ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Décision", self._tous, "display_decision"))

            # save decision in the other group member data ---------------------
            for g, m in self._le2mserv.gestionnaire_groupes.\
                    get_groupes("prisonnersDilemma").iteritems():
                txtchoix = u""
                m[0].currentperiod.DP_decisionother = \
                    m[1].currentperiod.DP_decision
                txtchoix += \
                    u"X" if m[0].currentperiod.DP_decision == pms.OPTION_X else \
                        u"Y"
                m[1].currentperiod.DP_decisionother = \
                    m[0].currentperiod.DP_decision
                txtchoix += \
                    u"X" if m[1].currentperiod.DP_decision == pms.OPTION_X else \
                        u"Y"
                self._le2mserv.gestionnaire_graphique.infoserv(
                    u"G{}: {}".format(g.split("_")[2], txtchoix))
            
            # calcul des gains de la période ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "prisonnersDilemma")
        
            # affichage du récapitulatif ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Récapitulatif", self._tous, "display_summary"))
        
        # FIN DE LA PARTIE =====================================================
        self._le2mserv.gestionnaire_experience.finalize_part(
            "prisonnersDilemma")
