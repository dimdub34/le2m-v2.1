# -*- coding: utf-8 -*-

from twisted.internet import defer
import pandas as pd
import matplotlib.pyplot as plt
import logging
import random
from collections import OrderedDict
import inspect
from configuration.configconst import PILE, FACE
from util import utiltools
from util.utili18n import le2mtrans
import GneezyPotterParams as pms
from GneezyPotterTexts import _GP
from GneezyPotterGui import GuiConfigure
import GneezyPotterPart  # for sqlalchemy


logger = logging.getLogger("le2m")
    

class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        actions = OrderedDict()
        actions[le2mtrans(u"Settings")] = self._configure
        actions[le2mtrans(u"Display settings")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
                display_information2(utiltools.get_contenu_fichier(
                inspect.getsourcefile(pms)))
        actions[le2mtrans(u"Start")] = lambda _: self._demarrer()
        actions[le2mtrans(u"Payoffs")] = \
            lambda _: self._le2mserv.gestionnaire_experience.display_payoffs(
                "GneezyPotter")
        actions[le2mtrans(u"View graph")] = self._show_fig
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Gneezy Potter", actions)

        self._fig = None

    def _configure(self):
        screenconfig = GuiConfigure(
            self._le2mserv.gestionnaire_graphique.screen)
        if screenconfig.exec_():
            pms.DISPLAY_SUMMARY = screenconfig.get_responses()
            self._le2mserv.gestionnaire_graphique.infoserv(
                u"Display summary: {}".format(
                    u"Yes" if pms.DISPLAY_SUMMARY else u"No"))

    @defer.inlineCallbacks
    def _demarrer(self):
        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(_GP(u"Start Gneezy Potter?"))
        if not confirmation:
            return

        # init part ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "GneezyPotter", "PartieGP", "RemoteGP", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            "GneezyPotter")

        # to makes parameter changes remotes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        yield (self._le2mserv.gestionnaire_experience.run_func(
            self._tous, "configure"))

        # start of part ========================================================
        for period in xrange(1 if pms.NOMBRE_PERIODES else 0,
                             pms.NOMBRE_PERIODES + 1):

            if self._le2mserv.gestionnaire_experience.stop_repetitions:
                break

            # initiate the period ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._le2mserv.gestionnaire_graphique.infoserv(
                [None, le2mtrans(u"Period {}").format(period)])
            self._le2mserv.gestionnaire_graphique.infoclt(
                [None, le2mtrans(u"Period {}").format(period)],
                fg="white", bg="gray")
            yield (self._le2mserv.gestionnaire_experience.run_func(
                self._tous, "newperiod", period))

            # decision ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Decision", self._tous, "display_decision"))

            self._le2mserv.gestionnaire_graphique.infoserv(_GP(u"Random draws"))
            for p in self._tous:
                tirage = random.random()
                if tirage <= pms.PROBA:
                    p.currentperiod.GP_randomdraw = PILE
                else:
                    p.currentperiod.GP_randomdraw = FACE
                self._le2mserv.gestionnaire_graphique.infoserv(
                    "{}: {:.3f} => {}".format(
                        p.joueur, tirage,
                        u"pile" if p.currentperiod.GP_randomdraw == PILE else
                        u"face"))

            # calcul des gains de la période ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "GneezyPotter")

            # affichage du récapitulatif ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if pms.DISPLAY_SUMMARY:
                yield(self._le2mserv.gestionnaire_experience.run_step(
                    u"Summary", self._tous, "display_summary"))

        # Stats ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        data = pd.DataFrame(
            [p.currentperiod.todict(p.joueur) for p in self._tous])
        data = data.groupby(data.joueur).mean()["GP_decision"]
        self._le2mserv.gestionnaire_graphique.infoserv(
            _GP(u"Av. amount invested"))
        self._le2mserv.gestionnaire_graphique.infoserv(data.to_string())
        self._fig, graph = plt.subplots(figsize=(6, 6))
        data.plot(kind="bar", ax=graph)
        graph.set_xticklabels([str(i)[-3:-1] for i in data.index])
        graph.set_ylim(0, pms.DOTATION)
        graph.set_xlabel("Players")
        graph.set_ylabel("Amount invested")
        graph.set_title("Amount invested in the risky option")

        # end of part ==========================================================
        self._le2mserv.gestionnaire_experience.finalize_part("GneezyPotter")

    def _show_fig(self):
        if not self._fig:
            return
        self._fig.show()