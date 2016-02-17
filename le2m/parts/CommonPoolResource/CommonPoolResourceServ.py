# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
from util import utiltools
import pandas as pd
import matplotlib.pyplot as plt
import CommonPoolResourceParams as pms
from CommonPoolResourceTexts import trans_CPR


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen
        actions = OrderedDict()
        actions[trans_CPR(u"Configure")] = self._configure
        actions[trans_CPR(u"Display parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), u"Paramètres")
        actions[trans_CPR(u"Start")] = lambda _: self._demarrer()
        actions[trans_CPR(u"Display payoffs")] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs_onserver("CommonPoolResource")
        actions[trans_CPR(u"Show graph")] = self._show_fig
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Common Pool Resource", actions)

        self._fig = None

    def _configure(self):
        """
        To make changes in the parameters
        :return:
        """
        self._le2mserv.gestionnaire_graphique.display_information(
            u"Aucun paramètre configurable")

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """

        # check conditions =====================================================
        if self._le2mserv.gestionnaire_joueurs.nombre_joueurs % \
                pms.TAILLE_GROUPES != 0:
            self._le2mserv.gestionnaire_graphique.display_error(
                trans_CPR(u"The number of players is not compatible with the "
                          u"size of groups"))
            return

        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(trans_CPR(u"Start CommonPoolResource?"))
        if not confirmation:
            return

        # init part ============================================================
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "CommonPoolResource", "PartieCPR", "RemoteCPR", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'CommonPoolResource')

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
    
        # start of repetitions =================================================
        for period in xrange(1 if pms.NOMBRE_PERIODES else 0,
                        pms.NOMBRE_PERIODES + 1):

            if self._le2mserv.gestionnaire_experience.stop_repetitions:
                break

            # init period
            self._le2mserv.gestionnaire_graphique.infoserv(
                [None, trans_CPR(u"Period {}").format(period)])
            self._le2mserv.gestionnaire_graphique.infoclt(
                [None, trans_CPR(u"Period {}").format(period)], fg="white", bg="gray")
            yield (self._le2mserv.gestionnaire_experience.run_func(
                self._tous, "newperiod", period))
            
            # decision
            yield(self._le2mserv.gestionnaire_experience.run_step(
                trans_CPR(u"Decision"), self._tous, "display_decision"))

            self._le2mserv.gestionnaire_graphique.infoserv(
                trans_CPR(u"Sum of decisions"))
            for g, p in self._le2mserv.gestionnaire_groupes. \
                    get_groupes("CommonPoolResource").iteritems():
                total = sum([i.currentperiod.CPR_decision for i in p])
                for i in p:
                    i.currentperiod.CPR_decisiongroup = total
                self._le2mserv.gestionnaire_graphique.infoserv("G{}: {}".format(
                    g.split("_")[2], total))
            
            # period payoff
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "CommonPoolResource")

            # stats
            self._do_stats(period)
        
            # summary
            yield(self._le2mserv.gestionnaire_experience.run_step(
                trans_CPR(u"Summary"), self._tous, "display_summary"))

        # End of part ==========================================================
        # stats
        self._le2mserv.gestionnaire_graphique.infoserv(
            [None, trans_CPR(u"Av. for the whole game")])
        datapandall = pd.DataFrame(self._data)
        datapandall = datapandall.groupby(datapandall.CPR_group)
        self._le2mserv.gestionnaire_graphique.infoserv(
            datapandall.mean()["CPR_decision"].to_string())
        # finalization
        self._le2mserv.gestionnaire_experience.finalize_part(
            "CommonPoolResource")

    def _do_stats(self, period):
        # stats
        self._le2mserv.gestionnaire_graphique.infoserv(
            trans_CPR(u"Av. for the period"))
        dataperiod = [p.currentperiod.todict(p.joueur) for p in self._tous]
        df_dataperiod = pd.DataFrame(dataperiod)
        df_dataperiod = df_dataperiod.groupby(["CPR_group"]).mean()
        self._le2mserv.gestionnaire_graphique.infoserv(
            df_dataperiod["CPR_decision"].to_string())

        # graph period
        if self._fig is None:  # first period
            self._fig, self._graph = plt.subplots()
            self._graph.set_ylim(0, pms.DOTATION)
            self._graph.set_xlim(1, pms.NOMBRE_PERIODES)
            self._graph.set_ylabel("Amount put in the public account")
            self._graph.set_xlabel("Periods")
            self._groups = df_dataperiod.index
            self._colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
            self._xval = range(len(self._groups))
            self._yval = range(len(self._groups))
            for g in range(len(self._groups)):
                self._xval[g] = []
                self._yval[g] = []
        del self._graph.lines[:]
        for c, g in enumerate(self._groups):
            self._xval[c].append(period)
            self._yval[c].append(df_dataperiod["CPR_decision"].loc[g])
            self._graph.plot(self._xval[c], self._yval[c], color=self._colors[c],
                             label="G{}".format(g.split("_")[2]))
        if len(self._xval[0]) == 1:
            self._graph.legend(loc=9, ncol=len(self._groups), frameon=False,
                               fontsize=10)
        self._fig.canvas.draw()
        self._data.extend(dataperiod)

    def _show_fig(self):
        if self._fig is None:
            return
        self._fig.show()