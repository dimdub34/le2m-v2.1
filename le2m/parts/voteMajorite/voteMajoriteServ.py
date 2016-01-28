# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
from util import utiltools
import voteMajoriteParams as pms
from voteMajoriteGui import DConfigure
import random

logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        actions = OrderedDict()
        actions[u"Configurer"] = self._configure
        actions[u"Afficher les paramètres"] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), u"Paramètres")
        actions[u"Démarrer"] = lambda _: self._demarrer()
        actions[u"Afficher les gains"] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs("voteMajorite")
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Vote majorité", actions)

    def _configure(self):
        dconf = DConfigure(parent=self._le2mserv.gestionnaire_graphique.screen)
        if dconf.exec_():
            pms.PROFILS_APPLIQUES = dconf.get_infos()
            self._le2mserv.gestionnaire_graphique.infoserv(
                u"Profils: {}".format(pms.PROFILS_APPLIQUES))

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        # tests of consistency
        if not pms.PROFILS_APPLIQUES:
            self._le2mserv.gestionnaire_graphique.display_error(
                u"Il faut choisir les profils à appliquer")
            return
        if self._le2mserv.gestionnaire_joueurs.nombre_joueurs % \
            pms.TAILLE_GROUPES != 0:
            self._le2mserv.gestionnaire_graphique.display_error(
                u"Nombre de clients connectés incompatible avec taille des "
                u"groupes")
            return

        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(u"Démarrer voteMajorite?")
        if not confirmation:
            return

        # initiate part
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "voteMajorite", "PartieVM",
            "RemoteVM", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'voteMajorite')

        # configure part
        yield (self._le2mserv.gestionnaire_experience.run_step(
            u"Configure", self._tous, "configure"))
        
        # groupes de 4 pour attribution profil
        try:
            self._le2mserv.gestionnaire_groupes.former_groupes(
                self._le2mserv.gestionnaire_joueurs.get_players(),
                pms.TAILLE_GROUPES, forcer_nouveaux=True)
        except ValueError as e:
            self._le2mserv.gestionnaire_graphique.display_error(
                e.message)
            return
    
        # attribution des profils
        self._le2mserv.gestionnaire_graphique.infoserv(u"Profils")
        cpteur = 0
        for g, m in self._le2mserv.gestionnaire_groupes.get_groupes(
                "voteMajorite").iteritems():
            self._le2mserv.gestionnaire_graphique.infoserv(
                u"G{}: {}".format(
                    g.split("_")[2], pms.PROFILS_APPLIQUES[cpteur]))
            for j in m:
                j.profil = pms.PROFILS_APPLIQUES[cpteur]
            cpteur += 1
    
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

            # compte les pour et les contre
            dec = [j.currentperiod.VM_decision for j in self._tous]
            pour = dec.count(pms.POUR)
            contre = dec.count(pms.CONTRE)
            if pour > contre:
                majority = pms.POUR
            elif pour < contre:
                majority = pms.CONTRE
            else:
                majority = pms.POUR if random.random() >= 0.5 else pms.CONTRE
            for j in self._tous:
                j.currentperiod.VM_pour = pour
                j.currentperiod.VM_contre = contre
                j.currentperiod.VM_majority = majority
            self._le2mserv.gestionnaire_graphique.infoserv(
                u"Majorité: {}".format(
                    u"Pour" if majority == pms.POUR else u"Contre"))
            
            # period payoff
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "voteMajorite")
        
        # summary
        yield(self._le2mserv.gestionnaire_experience.run_step(
            u"Récapitulatif", self._tous, "display_summary"))
        
        # end of part ----------------------------------------------------------
        self._le2mserv.gestionnaire_experience.finalize_part(
            "voteMajorite")
