# -*- coding: utf-8 -*-

from __future__ import division
from twisted.internet import defer
import pandas as pd
import matplotlib.pyplot as plt
import logging
from collections import OrderedDict
from util import utiltools
import PublicGoodGameSolidarityParams as pms
from PublicGoodGameSolidarityTexts import _PGGS
from PublicGoodGameSolidarityGui import DConfigure, DGains
from PyQt4 import QtGui
from server.servgest import servgestgroups


logger = logging.getLogger("le2m".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        actions = OrderedDict()
        actions[_PGGS(u"Configure")] = self._configure
        actions[_PGGS(u"Display parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                text=utiltools.get_module_info(pms), titre=u"Paramètres")
        actions[_PGGS(u"Start")] = lambda _: self._demarrer()
        actions[_PGGS(u"Display payoffs")] = self._display_payoffs
        actions[_PGGS(u"Show graph")] = self._show_fig
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Public Good Game Solidarity", actions)

        self._fig = None
        self._currentsequence = -1

    def _configure(self):
        screenconf = DConfigure(self._le2mserv.gestionnaire_graphique.screen)
        if screenconf.exec_():
            pms.TRAITEMENT = screenconf.get_infos()
            self._le2mserv.gestionnaire_graphique.infoserv(
                "Traitement: {}".format(pms.get_treatments(pms.TRAITEMENT)))

    @defer.inlineCallbacks
    def _demarrer(self):

        # vérif nb joueurs compatible
        if self._le2mserv.gestionnaire_joueurs.get_nombre_joueurs() % \
                (2 * pms.TAILLE_GROUPES) != 0:
            self._le2mserv.gestionnaire_graphique.display_error(
                u"Il faut un nombre de joueurs multiple de {}.".format(
                    2 * pms.TAILLE_GROUPES))
            return

        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(u"Démarrer PublicGoodGameSolidarity?")
        if not confirmation:
            return

        # formation des groupes
        try:
            self._le2mserv.gestionnaire_groupes.former_groupes(
                self._le2mserv.gestionnaire_joueurs.get_players(),
                pms.TAILLE_GROUPES, forcer_nouveaux=False)
        except ValueError as e:
            self._le2mserv.gestionnaire_graphique.display_error(e.message)
            return

        # initialisation et configuration
        self._currentsequence += 1
        self._fig = None
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "PublicGoodGameSolidarity", "PartiePGGS", "RemotePGGS", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'PublicGoodGameSolidarity')
        yield (self._le2mserv.gestionnaire_experience.run_func(
            self._tous, "configure", self._currentsequence))

        # selon le traitement certains groupes se retrouvent sinistrés
        if pms.TRAITEMENT == pms.get_treatments("WITHOUT_SOLIDARITY") or \
            pms.TRAITEMENT == pms.get_treatments("SOLIDARITY_AUTO") or \
            pms.TRAITEMENT == pms.get_treatments("SOLIDARITY_VOTE"):
            # form ens, définit sinistrés et affiche résultat sinistrés
            self._ensembles = self._former_ensembles()
            self._set_sinistres()
            yield (self._le2mserv.gestionnaire_experience.run_step(
                step_name=u"Information sinistre",
                step_participants=self._tous, step_function="display_sinistre"))

            # vote pour ou contre intégration et affichage résultat
            if pms.TRAITEMENT == pms.get_treatments("SOLIDARITY_VOTE"):
                votants = [j for j in self._tous if not j.sinistre]
                yield (self._le2mserv.gestionnaire_experience.run_step(
                    step_name=u"Vote intégration", step_participants=votants,
                    step_function="display_vote"))
                self._traiter_votes()
                yield (self._le2mserv.gestionnaire_experience.run_step(
                    step_name=u"Information votes",
                    step_participants=self._tous,
                    step_function="display_resultvotes"))

        # DEBUT DES RÉPÉTITIONS ================================================
        for period in xrange(1 if pms.NOMBRE_PERIODES else 0,
                             pms.NOMBRE_PERIODES + 1):

            if self._le2mserv.gestionnaire_experience.stop_repetitions:
                break

            # initialisation période
            self._le2mserv.gestionnaire_graphique.infoserv(
                [None, u"Période {}".format(period)])
            self._le2mserv.gestionnaire_graphique.infoclt(
                [None, u"Période {}".format(period)], fg="white", bg="gray")
            yield (self._le2mserv.gestionnaire_experience.run_func(
                self._tous, "newperiod", period))
            
            # décision
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Décision", self._tous, "display_decision"))

            # compute total amount in the public account by group
            self._le2mserv.gestionnaire_graphique.infoserv(
                _PGGS(u"Total amount by group"))
            for g, m in self._le2mserv.gestionnaire_groupes.get_groupes(
                    "PublicGoodGameSolidarity").iteritems():
                total = sum([p.currentperiod.PGGS_public for p in m])
                for p in m:
                    p.currentperiod.PGGS_publicgroup = total
                self._le2mserv.gestionnaire_graphique.infoserv(
                    u"G{}: {}".format(g.split("_")[2], total))
            
            # calcul des gains de la période ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "PublicGoodGameSolidarity")
        
            # summary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Summary", self._tous, "display_summary"))

            # stats and graph
            self._dostats(period)

        # FIN DE LA PARTIE =====================================================
        self._le2mserv.gestionnaire_graphique.infoserv(
            [None, u"Av. for the whole game"])
        datapandall = pd.DataFrame(self._dataall)
        datapandall = datapandall.groupby(datapandall.PGGS_group)
        self._le2mserv.gestionnaire_graphique.infoserv(
            datapandall.mean()["PGGS_public"].to_string())
        self._le2mserv.gestionnaire_experience.finalize_part(
            "PublicGoodGameSolidarity")

    def _dostats(self, period):
        # stats period
        self._le2mserv.gestionnaire_graphique.infoserv(
            u"Av. for the period")
        dataperiod = [p.currentperiod.todict(p.joueur) for p in self._tous]
        df_dataperiod = pd.DataFrame(dataperiod)
        df_dataperiod = df_dataperiod.groupby(
            df_dataperiod.PGGS_group).mean()
        self._le2mserv.gestionnaire_graphique.infoserv(
            df_dataperiod["PGGS_public"].to_string())

        # graph period
        if self._fig is None:
            self._fig, self._graph = plt.subplots()
            self._graph.set_ylim(0, pms.DOTATION)
            self._graph.set_xlim(1, pms.NOMBRE_PERIODES)
            self._graph.set_ylabel("Amount put in the public account")
            self._graph.set_xlabel("Periods")
            self._dataall = []
            self._groups = df_dataperiod.index
            self._colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
            self._xval, self._yval = range(len(self._groups)), range(len(self._groups))
            for g in range(len(self._groups)):
                self._xval[g] = []
                self._yval[g] = []
        del self._graph.lines[:]
        for c, g in enumerate(self._groups):
            self._xval[c].append(period)
            self._yval[c].append(df_dataperiod["PGGS_public"].ix[g])
            self._graph.plot(self._xval[c], self._yval[c], color=self._colors[c],
                             label="G{}".format(g.split("_")[2]))
        if len(self._xval[0]) == 1:
            self._graph.legend(loc=9, ncol=len(self._groups), frameon=False,
                               fontsize=10)
        self._fig.canvas.draw()
        self._dataall.extend(dataperiod)

    def _show_fig(self):
        if not self._fig:
            return
        self._fig.show()

    def _display_payoffs(self):
        gains_txt = []
        gains, textes_finaux = {}, {}
        if self._currentsequence >= 0:
            sequence, ok = QtGui.QInputDialog.getInt(
                self._le2mserv.gestionnaire_graphique.screen, u"Choix séquence",
                u"Choisir la séquence", 0, 0, self._currentsequence, 1)
            for j in self._tous:
                gtemp = j.get_sequencesgains(sequence)
                gains[j.joueur] = gtemp["gain"]
                gains_txt.append(
                    [str(j.joueur), u"{}".format(gains[j.joueur])])
                textes_finaux[j.joueur] = gtemp["texte"]
        self._ecran_gains = DGains(
            self._le2mserv, gains_txt, textes_finaux, gains)
        self._ecran_gains.show()

    def _former_ensembles(self):
        groupskeys = list(self._le2mserv.gestionnaire_groupes.get_groupes(
            "PublicGoodGameSolidarity").viewkeys())
        ensembles = servgestgroups.former_groupes(
            taille=2, population=groupskeys, prefixeid="{}_e_".format(
                self._le2mserv.nom_session))
        self._le2mserv.gestionnaire_graphique.infoserv(u"Ensembles")
        self._le2mserv.gestionnaire_graphique.infoserv(
            [u"{}: {}".format(k, v) for k, v in ensembles.viewitems()])
        for e, g in ensembles.viewitems():
            for j in self._le2mserv.gestionnaire_groupes.get_composition_groupe(g):
                j.get_part("PublicGoodGameSolidarity").ensemble = e
        return ensembles

    def _set_sinistres(self):
        for v in self._ensembles.viewvalues():
            for j in self._le2mserv.gestionnaire_groupes.get_composition_groupe(v[0]):
                j.get_part("PublicGoodGameSolidarity").sinistre = True
            for j in self._le2mserv.gestionnaire_groupes.get_composition_groupe(v[1]):
                j.get_part("PublicGoodGameSolidarity").sinistre = False

    def _traiter_votes(self):
        self._le2mserv.gestionnaire_graphique.infoserv(u"Votes")
        for v in self._ensembles.viewvalues():
            # composition groupes
            g0 = [j.get_part("PublicGoodGameSolidarity") for j in
                  self._le2mserv.gestionnaire_groupes.get_composition_groupe(v[0])]
            g1 = [j.get_part("PublicGoodGameSolidarity") for j in
                  self._le2mserv.gestionnaire_groupes.get_composition_groupe(v[1])]

            # votes de g0
            votes_pour = [j.vote for j in g0].count(pms.get_votes("pour"))
            majorite = pms.get_votes("pour") if \
                votes_pour > pms.TAILLE_GROUPES / 2 else pms.get_votes("contre")

            # set des infos dans données joueurs
            for j in g0:
                j.currentperiod.nbvotespour = votes_pour
                j.currentperiod.votemajoritaire = majorite
            for j in g1:
                j.currentperiod.nbvotespour = votes_pour
                j.currentperiod.votemajoritaire = majorite

            self._le2mserv.gestionnaire_graphique.infoserv(
                u"{}: {} -> {}".format(g0.split("_")[2], votes_pour, u"Pour" if
                majorite == pms.get_votes("pour") else u"Contre"))
