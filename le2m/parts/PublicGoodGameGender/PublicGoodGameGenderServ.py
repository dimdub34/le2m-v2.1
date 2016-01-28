# -*- coding: utf-8 -*-

from twisted.internet import defer
import pandas as pd
import matplotlib.pyplot as plt
import logging
from collections import OrderedDict
from util import utiltools
import PublicGoodGameGenderParams as pms
from PublicGoodGameGenderTexts import _PGGG
import PublicGoodGameGenderPart  # for sqlalchemy
from PublicGoodGameGenderGui import DConfigure
from configuration.configconst import HOMME
from server.servgest.servgestgroups import GestionnaireGroupes
import random


logger = logging.getLogger("le2m".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen
        actions = OrderedDict()
        actions[_PGGG(u"Configure")] = self._configure
        actions[_PGGG(u"Display parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), u"Paramètres")
        actions[_PGGG(u"Start")] = lambda _: self._demarrer()
        actions[_PGGG(u"Display payoffs")] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs("PublicGoodGameGender")
        actions[_PGGG(u"Show graph")] = self._show_fig
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Public Good Game Gender", actions)

        self._gestionnaire_groupes = GestionnaireGroupesPGGG(self._le2mserv)
        self._fig = None

    def _configure(self):
        screen_config = DConfigure(self._le2mserv.gestionnaire_graphique.screen)
        if screen_config.exec_():
            pms.TRAITEMENT, pms.NB_HOMMES, pms.GROUPES = \
                screen_config.get_infos()
            self._le2mserv.gestionnaire_graphique.infoserv(
                [
                    _PGGG(u"Treatment {}").format(
                    pms.get_treatments(pms.TRAITEMENT)),
                    _PGGG(u"Number of men: {}").format(pms.NB_HOMMES),
                    u"Nb groupes par type",
                    u"  ".join([u"{}H: {}".format(k, pms.GROUPES[k]) for
                                k in range(5)])
                ])

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(u"Démarrer PublicGoodGameGender?")
        if not confirmation:
            return

        nbhommes = len(
            [h for h in self._le2mserv.gestionnaire_joueurs.get_players() if
             h.gender == HOMME])
        if nbhommes != pms.NB_HOMMES:
            self._le2mserv.gestionnaire_graphique.display_error(
                u"Le nombre d'hommes ne correspond pas à celui saisi dans la "
                u"configuration")
            return
        
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "PublicGoodGameGender", "PartiePGGG", "RemotePGGG", pms))
        self._fig = None
        
        self._gestionnaire_groupes.former_groupes()
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'PublicGoodGameGender')
        for m in self._le2mserv.gestionnaire_groupes.get_groupes().itervalues():
            groupcomp = sum([j.gender for j in m])  # j.genre == 1 si homme
            for j in m:
                j.groupComposition = groupcomp

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

            # compute total amount in the public account by group
            self._le2mserv.gestionnaire_graphique.infoserv(
                _PGGG(u"Total amount by group"))
            for g, m in self._gestionnaire_groupes.get_groupes(
                    "PublicGoodGameGender").iteritems():
                total = sum([p.currentperiod.PGGG_public for p in m])
                for p in m:
                    p.currentperiod.PGGG_publicgroup = total
                self._le2mserv.gestionnaire_graphique.infoserv(
                    u"G{}: {}".format(g.split("_")[2], total))
            
            # calcul des gains de la période ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "PublicGoodGameGender")
        
            # summary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Summary", self._tous, "display_summary"))

            # stats period
            self._le2mserv.gestionnaire_graphique.infoserv(
                u"Av. for the period")
            dataperiod = []
            for part in self._tous:
                dataperiod.append(part.currentperiod.todict(part.joueur))
            df_dataperiod = pd.DataFrame(dataperiod)
            df_dataperiod = df_dataperiod.groupby(df_dataperiod.PGGG_group).mean()
            self._le2mserv.gestionnaire_graphique.infoserv(
                df_dataperiod["PGGG_public"].to_string())

            # graph period
            if self._fig is None:
                self._fig, self._graph = plt.subplots()
                self._graph.set_ylim(0, pms.DOTATION)
                self._graph.set_xlim(1, pms.NOMBRE_PERIODES)
                self._graph.set_ylabel("Amount put in the public account")
                self._graph.set_xlabel("Periods")
                self._dataall = []
                self._groups = df_dataperiod.index
                colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
                xval, yval = range(len(self._groups)), range(len(self._groups))
                for g in range(len(self._groups)):
                    xval[g] = []
                    yval[g] = []
            del self._graph.lines[:]
            for c, g in enumerate(self._groups):
                xval[c].append(period)
                yval[c].append(df_dataperiod["PGGG_public"].loc[g])
                self._graph.plot(xval[c], yval[c], color=colors[c],
                                 label="G{}".format(g.split("_")[2]))
            if len(xval[0]) == 1:
                self._graph.legend(loc=9, ncol=len(self._groups), frameon=False,
                                   fontsize=10)
            self._fig.canvas.draw()
            self._dataall.extend(dataperiod)

        self._le2mserv.gestionnaire_graphique.infoserv(
            [None, u"Av. for the whole game"])
        datapandall = pd.DataFrame(self._dataall)
        datapandall = datapandall.groupby(datapandall.PGGG_group)
        self._le2mserv.gestionnaire_graphique.infoserv(
            datapandall.mean()["PGGG_public"].to_string())
        
        # FIN DE LA PARTIE =====================================================
        self._le2mserv.gestionnaire_experience.finalize_part(
            "PublicGoodGameGender")

    def _show_fig(self):
        if not self._fig:
            return
        self._fig.show()


class GestionnaireGroupesPGGG(GestionnaireGroupes):
    def __init__(self, le2mserv):
        super(GestionnaireGroupesPGGG, self).__init__(le2mserv)
        self._le2mserv = le2mserv

    def former_groupes(self):
        """
        on forme les groupes en fonction du genre
        :return:
        """
        self._groupes.clear()
        self._le2mserv.gestionnaire_graphique.infoserv(u"Groupes")
        liste_joueurs = self._le2mserv.gestionnaire_joueurs.get_players()
        groupes_types = pms.GROUPES
        femmes_dispo = [f for f in liste_joueurs if f.gender != HOMME]
        hommes_dipo = [h for h in liste_joueurs if h.gender == HOMME]
        cpteur = 0
        for g in range(5):  # tous les types
            for i in range(groupes_types[g]):  # nb groupe de ce type
                cle = "{}_g_{}".format(self._nom_session, cpteur)
                self._groupes[cle] = []
                nbhommes = 0
                while nbhommes != g:  # hommes
                    select = random.choice(hommes_dipo)
                    self._groupes[cle].append(select)
                    hommes_dipo.remove(select)
                    nbhommes += 1
                while len(self._groupes[cle]) != pms.TAILLE_GROUPES:  # femmes
                    select = random.choice(femmes_dispo)
                    self._groupes[cle].append(select)
                    femmes_dispo.remove(select)
                for m in self._groupes[cle]:  # set in players
                    m.get_part("PublicGoodGameGender").set_groupinfos(cle, g)
                self._le2mserv.gestionnaire_graphique.infoserv(
                    u"G{}: {}".format(cle.split("_")[2], self._groupes[cle]))
                cpteur += 1
