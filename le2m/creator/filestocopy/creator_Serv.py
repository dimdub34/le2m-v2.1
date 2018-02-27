# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
from util import utiltools
from util.utili18n import le2mtrans
import EXPERIENCE_NOMParams as pms
from EXPERIENCE_NOMGui import DConfigure


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self.le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen)
        actions = OrderedDict()
        actions[le2mtrans(u"Configure")] = self.configure
        actions[le2mtrans(u"Display parameters")] = \
            lambda _: self.le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), le2mtrans(u"Parameters"))
        actions[le2mtrans(u"Start")] = lambda _: self.demarrer()
        actions[le2mtrans(u"Display payoffs")] = \
            lambda _: self.le2mserv.gestionnaire_experience.\
            display_payoffs_onserver("EXPERIENCE_NOM")
        self.le2mserv.gestionnaire_graphique.add_topartmenu(
            u"EXPERIENCE_MENU", actions)

    def configure(self):
        # self._le2mserv.gestionnaire_graphique.display_information(
        #     le2mtrans(u"There is no parameter to configure"))
        # return
        screen_conf = DConfigure(self.le2mserv.gestionnaire_graphique.screen)
        if screen_conf.exec_():
            self.le2mserv.gestionnaire_graphique.infoserv(u"Traitement: {}".format(
                pms.TREATMENTS_NAMES.get(pms.TREATMENT)))
            self.le2mserv.gestionnaire_graphique.infoserv(u"Période d'essai: {}".format(
                u"oui" if pms.PERIODE_ESSAI else u"non"))

    @defer.inlineCallbacks
    def demarrer(self):
        """
        Start the part
        :return:
        """
        # check conditions =====================================================
        if not self.le2mserv.gestionnaire_graphique.question(
                        le2mtrans(u"Start") + u" EXPERIENCE_NOM?"):
            return

        # init part ============================================================
        yield (self.le2mserv.gestionnaire_experience.init_part(
            "EXPERIENCE_NOM", "PartieEXPERIENCE_NOM_COURT",
            "RemoteEXPERIENCE_NOM_COURT", pms))
        self._tous = self.le2mserv.gestionnaire_joueurs.get_players(
            'EXPERIENCE_NOM')

        # set parameters on remotes
        yield (self.le2mserv.gestionnaire_experience.run_step(
            le2mtrans(u"Configure"), self._tous, "configure"))
        
        # form groups
        if pms.TAILLE_GROUPES > 0:
            try:
                self.le2mserv.gestionnaire_groupes.former_groupes(
                    self.le2mserv.gestionnaire_joueurs.get_players(),
                    pms.TAILLE_GROUPES, forcer_nouveaux=True)
            except ValueError as e:
                self.le2mserv.gestionnaire_graphique.display_error(
                    e.message)
                return
    
        # Start part ===========================================================
        period_start = 0 if pms.NOMBRE_PERIODES == 0 or pms.PERIODE_ESSAI else 1
        for period in range(period_start, pms.NOMBRE_PERIODES + 1):

            if self.le2mserv.gestionnaire_experience.stop_repetitions:
                break

            # init period
            self.le2mserv.gestionnaire_graphique.infoserv(
                [None, le2mtrans(u"Period") + u" {}".format(period)])
            self.le2mserv.gestionnaire_graphique.infoclt(
                [None, le2mtrans(u"Period") + u" {}".format(period)],
                fg="white", bg="gray")
            yield (self.le2mserv.gestionnaire_experience.run_func(
                self._tous, "newperiod", period))
            
            # decision
            yield(self.le2mserv.gestionnaire_experience.run_step(
                le2mtrans(u"Decision"), self._tous, "display_decision"))
            
            # period payoffs
            self.le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "EXPERIENCE_NOM")
        
            # summary
            yield(self.le2mserv.gestionnaire_experience.run_step(
                le2mtrans(u"Summary"), self._tous, "display_summary"))
        
        # End of part ==========================================================
        yield (self.le2mserv.gestionnaire_experience.finalize_part(
            "EXPERIENCE_NOM"))
