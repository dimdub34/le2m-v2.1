# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
from util import utiltools
from util.utili18n import le2mtrans
import prisonnersDilemmaParams as pms


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen
        actions = OrderedDict()
        actions[le2mtrans(u"Configure")] = self._configure
        actions[le2mtrans(u"Display parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), u"Paramètres")
        actions[le2mtrans(u"Start")] = lambda _: self._demarrer()
        actions[le2mtrans(u"Display payoffs")] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs_onserver("prisonnersDilemma")
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Prisonner's dillemma", actions)

    def _configure(self):
        self._le2mserv.gestionnaire_graphique.display_information(
            u"Aucun paramètre à configurer")

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        # check conditions =====================================================
        if self._le2mserv.gestionnaire_joueurs.nombre_joueurs % \
            pms.TAILLE_GROUPES:
            self._le2mserv.gestionnaire_graphique.display_error(
                le2mtrans(u"The number of players is not compatible with "
                          u"the group size"))
            return

        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(u"Démarrer prisonnersDilemma?")
        if not confirmation:
            return

        # init part ============================================================
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "prisonnersDilemma", "PartieDP",
            "RemoteDP", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'prisonnersDilemma')
        
        self._le2mserv.gestionnaire_groupes.former_groupes(
            self._le2mserv.gestionnaire_joueurs.get_players(),
            pms.TAILLE_GROUPES, forcer_nouveaux=True)

        # set parameters on remotes
        yield (self._le2mserv.gestionnaire_experience.run_func(
            self._tous, "configure"))
    
        # Start part ===========================================================
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

            for g, m in self._le2mserv.gestionnaire_groupes.\
                    get_groupes("prisonnersDilemma").iteritems():
                txtchoix = u""
                m[0].currentperiod.DP_decisionother = \
                    m[1].currentperiod.DP_decision
                txtchoix += pms.get_option(m[0].currentperiod.DP_decision)
                m[1].currentperiod.DP_decisionother = \
                    m[0].currentperiod.DP_decision
                txtchoix += pms.get_option(m[1].currentperiod.DP_decision)
                self._le2mserv.gestionnaire_graphique.infoserv(
                    u"G{}: {}".format(g.split("_")[2], txtchoix))
            
            # period payoff
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "prisonnersDilemma")
        
            # summary
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Récapitulatif", self._tous, "display_summary"))
        
        # End of part ==========================================================
        yield (self._le2mserv.gestionnaire_experience.finalize_part(
            "prisonnersDilemma"))
