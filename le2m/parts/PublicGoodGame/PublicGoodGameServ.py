# -*- coding: utf-8 -*-

from twisted.internet import defer
import pandas as pd
import matplotlib.pyplot as plt
import logging
from collections import OrderedDict
from util import utiltools
import PublicGoodGameParams as pms
from PublicGoodGameTexts import trans_PGG


logger = logging.getLogger("le2m".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen
        actions = OrderedDict()
        actions[trans_PGG(u"Configure")] = self._configure
        actions[trans_PGG(u"Display parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), u"Paramètres")
        actions[trans_PGG(u"Start")] = lambda _: self._demarrer()
        actions[trans_PGG(u"Display payoffs")] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs_onserver("PublicGoodGame")
        actions[trans_PGG(u"Show graph")] = self._show_fig
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Public Good Game", actions)

        self._fig = None

    def _configure(self):
        self._le2mserv.gestionnaire_graphique.display_information(
            trans_PGG(u"There is no nothing to configure"))
        return

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        # check conditions =====================================================
        if self._le2mserv.gestionnaire_joueurs.nombre_joueurs % \
                pms.TAILLE_GROUPES != 0 :
            self._le2mserv.gestionnaire_graphique.display_error(
                trans_PGG(u"The number of players is not compatible "
                          u"with the group size"))
            return
        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(u"Démarrer PublicGoodGame?")
        if not confirmation:
            return

        # init part ============================================================
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "PublicGoodGame", "PartiePGG", "RemotePGG", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'PublicGoodGame')

        # groups
        self._le2mserv.gestionnaire_groupes.former_groupes(
            self._le2mserv.gestionnaire_joueurs.get_players(),
            pms.TAILLE_GROUPES, forcer_nouveaux=True)

        # set parameters on remotes
        yield (self._le2mserv.gestionnaire_experience.run_func(
            self._tous, "configure"))

        # stats
        self._fig = None
        self._data = []

        # start ================================================================
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

            # compute total amount in the public account by group
            self._le2mserv.gestionnaire_graphique.infoserv(
                trans_PGG(u"Total amount by group"))
            for g, m in self._le2mserv.gestionnaire_groupes.get_groupes(
                    "PublicGoodGame").iteritems():
                total = sum([p.currentperiod.PGG_public for p in m])
                for p in m:
                    p.currentperiod.PGG_publicgroup = total
                self._le2mserv.gestionnaire_graphique.infoserv(
                    u"G{}: {}".format(g.split("_")[2], total))
            
            # period payoff
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "PublicGoodGame")
        
            # stats period
            self._do_stats(period)

            # summary
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Summary", self._tous, "display_summary"))

        # end of part ==========================================================
        # stats
        self._le2mserv.gestionnaire_graphique.infoserv(
            [None, u"Av. for the whole game"])
        datapandall = pd.DataFrame(self._data)
        datapandall = datapandall.groupby(datapandall.PGG_group)
        self._le2mserv.gestionnaire_graphique.infoserv(
            datapandall.mean()["PGG_public"].to_string())
        yield (self._le2mserv.gestionnaire_experience.finalize_part(
            "PublicGoodGame"))

    def _show_fig(self):
        if not self._fig:
            return
        self._fig.show()

    def _do_stats(self, period):
        self._le2mserv.gestionnaire_graphique.infoserv(
            u"Av. for the period")
        dataperiod = [p.currentperiod.todict(p.joueur) for p in self._tous]
        df_dataperiod = pd.DataFrame(dataperiod)
        df_dataperiod = df_dataperiod.groupby(df_dataperiod.PGG_group).mean()
        self._le2mserv.gestionnaire_graphique.infoserv(
            df_dataperiod["PGG_public"].to_string())

        # graph period
        if self._fig is None:
            self._fig, self._graph = plt.subplots()
            self._graph.set_ylim(0, pms.DOTATION)
            self._graph.set_xlim(1, pms.NOMBRE_PERIODES)
            self._graph.set_ylabel("Amount put in the public account")
            self._graph.set_xlabel("Periods")
            self._groups = df_dataperiod.index
            self._colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
            self._xval, self._yval = range(len(self._groups)), range(len(self._groups))
            for g in range(len(self._groups)):
                self._xval[g] = []
                self._yval[g] = []
        del self._graph.lines[:]
        for c, g in enumerate(self._groups):
            self._xval[c].append(period)
            self._yval[c].append(df_dataperiod["PGG_public"].ix[g])
            self._graph.plot(self._xval[c], self._yval[c],
                             color=self._colors[c],
                             label="G{}".format(g.split("_")[2]))
        if len(self._xval[0]) == 1:
            self._graph.legend(loc=9, ncol=len(self._groups), frameon=False,
                               fontsize=10)
        self._fig.canvas.draw()
        self._data.extend(dataperiod)
