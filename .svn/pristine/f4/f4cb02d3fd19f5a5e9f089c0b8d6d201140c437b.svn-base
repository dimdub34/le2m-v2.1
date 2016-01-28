# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from util import utiltools
import oathAndLiesParams as pms
import oathAndLiesPart  # for sqlalchemy
from oathAndLiesGui import DConfiguration


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
            display_payoffs("oathAndLies")
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Oath and Lies", actions)

    def _configure(self):
        """
        To make changes in the parameters
        :return:
        """
        screenconf = DConfiguration(self._le2mserv.gestionnaire_graphique.screen)
        if screenconf.exec_():
            infos = screenconf.get_infos()
            pms.TREATMENT = infos["treatment"]
            pms.GAME = infos["game"]
            self._le2mserv.gestionnaire_graphique.infoserv(
                ["Treatment: {}".format(pms.get_treatment(pms.TREATMENT)),
                 "Game: {}: {}".format(pms.GAME, pms.CODES_PERIODES[pms.GAME])])

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(u"Démarrer oathAndLies?")
        if not confirmation:
            return

        # création partie
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "oathAndLies", "PartieOL", "RemoteOL", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'oathAndLies')
        
        # formation des groupes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            self._le2mserv.gestionnaire_groupes.former_groupes(
                self._le2mserv.gestionnaire_joueurs.get_players(),
                pms.TAILLE_GROUPES, forcer_nouveaux=True)
        except ValueError as e:
            self._le2mserv.gestionnaire_graphique.display_error(e.message)
            return

        # attribution des roles
        self._le2mserv.gestionnaire_graphique.infoserv(u"Roles (A, B)")
        for g, m in self._le2mserv.gestionnaire_groupes.get_groupes(
                "oathAndLies").iteritems():
            m[0].role = pms.JOUEUR_A
            m[1].role = pms.JOUEUR_B
            self._le2mserv.gestionnaire_graphique.infoserv(
                u"G{}: A: {}, B: {}".format(
                    g.split("_")[2], m[0].joueur, m[1].joueur))
        self._tous_A = [j for j in self._tous if j.role == pms.JOUEUR_A]
        self._tous_B = [j for j in self._tous if j.role == pms.JOUEUR_B]

        # pour configure les clients et les remotes ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        yield (self._le2mserv.gestionnaire_experience.run_step(
            u"Configure", self._tous, "configure"))
    
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

            # affichage roles
            yield (self._le2mserv.gestionnaire_experience.run_step(
                "Roles", self._tous, "display_role"))
            
            # décision des A ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Décision A", self._tous_A, "display_decision"))

            # set tirage et message de A dans base de B
            for m in self._le2mserv.gestionnaire_groupes.get_groupes(
                    "oathAndLies").itervalues():
                m[1].currentperiod.OL_tirage = m[0].currentperiod.OL_tirage
                m[1].currentperiod.OL_message = m[0].currentperiod.OL_message

            # décision des B ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Décision B", self._tous_B, "display_decision"))

            # set décision B dans base A
            for m in self._le2mserv.gestionnaire_groupes.get_groupes(
                    "oathAndLies").itervalues():
                m[0].currentperiod.OL_decision = m[1].currentperiod.OL_decision

            # calcul des gains de la période ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "oathAndLies")
        
            # affichage du récapitulatif ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Récapitulatif", self._tous, "display_summary"))
        
        # FIN DE LA PARTIE =====================================================
        self._le2mserv.gestionnaire_experience.finalize_part(
            "oathAndLies")
