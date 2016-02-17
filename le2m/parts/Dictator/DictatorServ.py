# -*- coding: utf-8 -*-

from twisted.internet import defer
import pandas as pd
import matplotlib.pyplot as plt
import logging
from collections import OrderedDict
from util import utiltools
from util.utili18n import le2mtrans
import DictatorParams as pms
from DictatorTexts import trans_DIC
from DictatorGui import DConfigure

logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv
        actions = OrderedDict()
        actions[le2mtrans(u"Settings")] = self._configure
        actions[le2mtrans(u"Display settings")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), u"Paramètres")
        actions[le2mtrans(u"Start")] = lambda _: self._demarrer()
        actions[le2mtrans(u"Display payoffs")] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs_onserver("Dictator")
        actions[le2mtrans(u"Show graph")] = self._show_fig
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Dictator", actions)

    def _configure(self):
        """
        Pour configure la partie (traitement ...)
        :return:
        """
        screen_config = DConfigure(self._le2mserv.gestionnaire_graphique.screen)
        if screen_config.exec_():
            pms.GAME = screen_config.get_game()
            self._le2mserv.gestionnaire_graphique.infoserv(u"Game {}".format(
                pms.get_game(pms.GAME)))

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Lancement de la partie. Définit tout le déroulement
        :return:
        """
        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(u"Démarrer Dictator?")
        if not confirmation:
            return

        # INIT PART ============================================================
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "Dictator", "PartieDIC", "RemoteDIC", pms))

        # groups
        if pms.TAILLE_GROUPES > 0:
            try:
                self._le2mserv.gestionnaire_groupes.former_groupes(
                    self._le2mserv.gestionnaire_joueurs.get_players(),
                    pms.TAILLE_GROUPES, forcer_nouveaux=True)
            except ValueError as e:
                self._le2mserv.gestionnaire_graphique.display_error(
                    e.message)
                return

        # roles
        for g, m in self._le2mserv.gestionnaire_groupes. \
                get_groupes("Dictator").iteritems():
            m[0].role = pms.PLAYER_A
            m[1].role = pms.PLAYER_B

        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'Dictator')
        self._playersA = [p for p in self._tous if p.role == pms.PLAYER_A]
        self._le2mserv.gestionnaire_graphique.infoserv(trans_DIC("Players A"))
        self._le2mserv.gestionnaire_graphique.infoserv(
            map(str, [p.joueur for p in self._playersA]))

        # configure remotes
        yield (self._le2mserv.gestionnaire_experience.run_func(
            self._tous, "configure"))

        # display role ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if pms.GAME == pms.STANDARD:
            yield (self._le2mserv.gestionnaire_experience.run_step(
                u"Role", self._tous, "display_role"))
    
        # START OF REPETITIONS =================================================
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
            if pms.GAME == pms.STANDARD:
                yield(self._le2mserv.gestionnaire_experience.run_step(
                    le2mtrans(u"Decision"), self._playersA, "display_decision"))
            elif pms.GAME == pms.STRATEGY_METHOD:
                yield(self._le2mserv.gestionnaire_experience.run_step(
                    le2mtrans(u"Decision"), self._tous, "display_decision"))

            # display role ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if pms.GAME == pms.STRATEGY_METHOD:
                yield (self._le2mserv.gestionnaire_experience.run_step(
                    u"Role", self._tous, "display_role"))

            # store A's decisions in B's data set
            for m in self._le2mserv.gestionnaire_groupes. \
            get_groupes("Dictator").viewvalues():
                m[1].currentperiod.DIC_recu = m[0].currentperiod.DIC_decision

            # compute period payoffs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "Dictator")

            # summary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Summary", self._tous, "display_summary"))

        # END OF PART ==========================================================
        self._do_stats()
        self._le2mserv.gestionnaire_experience.finalize_part("Dictator")

    def _show_fig(self):
        if not hasattr(self, "_fig"):
            return
        self._fig.show()

    def _do_stats(self):
        df_data = None
        if pms.GAME == pms.STANDARD:
            df_data = pd.DataFrame(
                [p.currentperiod.todict(p.joueur) for p in self._playersA])
        elif pms.GAME == pms.STRATEGY_METHOD:
            df_data = pd.DataFrame(
                [p.currentperiod.todict(p.joueur) for p in self._tous])

        df_data = df_data.groupby(df_data.joueur).mean()["DIC_decision"]
        self._fig, graph = plt.subplots(figsize=(6, 6))
        df_data.plot(kind="bar", ax=graph)
        graph.set_xticklabels([str(i)[-3:-1] for i in df_data.index])
        graph.set_ylim(0, pms.DOTATION)
        graph.set_xlabel(trans_DIC(u"Players"))
        graph.set_ylabel(trans_DIC(u"Amount sent"))
        graph.set_title(trans_DIC(u"Average amount sent by A players"))

        self._le2mserv.gestionnaire_graphique.infoserv(
            trans_DIC(u"Av. amount sent by players A\n{}").format(
                df_data.to_string()))
