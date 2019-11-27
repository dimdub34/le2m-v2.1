# -*- coding: utf-8 -*-

# built-in
import logging
from collections import OrderedDict
from datetime import datetime

from PyQt4.QtCore import QTimer, pyqtSlot
from PyQt4.QtGui import QMessageBox
from twisted.internet import defer

from .murielle_jeu_group import GroupGA
import murielle_jeu_params as pms
from murielle_jeu_gui import DConfigure
from murielle_jeu_texts import trans_GA
from server.servgui.servguidialogs import DSequence, GuiPayoffs
from util import utiltools
from util.utili18n import le2mtrans
from util.utiltools import timedelta_to_time

logger = logging.getLogger("le2m")


class Serveur(object):
    def __init__(self, le2mserv):
        self.le2mserv = le2mserv
        self.current_sequence = 0
        self.current_period = 0
        self.all = []
        self.groups = []
        self.the_n = 0  # n=second in continus time and n=period in discrete time
        # menu ---------------------------------------------------------------------------------------------------------
        actions = OrderedDict()
        actions[le2mtrans(u"Configure")] = self.configure
        actions[le2mtrans(u"Display parameters")] = lambda _: self.le2mserv.gestionnaire_graphique.display_information2(
            utiltools.get_module_info(pms), le2mtrans(u"Parameters"))
        actions[le2mtrans(u"Start")] = lambda _: self.demarrer()
        actions[le2mtrans(u"Display payoffs")] = lambda _: self.display_payoffs()
        self.le2mserv.gestionnaire_graphique.add_topartmenu(u"Jeu", actions)

    def configure(self):
        screen_conf = DConfigure(self.le2mserv.gestionnaire_graphique.screen)
        if screen_conf.exec_():
            pms_list = [None, "Game - parameters"]
            pms_list.append("PARTIE_ESSAI: {}".format(pms.PARTIE_ESSAI))
            pms_list.append(
                "DYNAMIC_TYPE: {}".format("continuous" if pms.DYNAMIC_TYPE == pms.CONTINUOUS else "discrete"))
            pms_list.append("TAU: {}".format(pms.tau))
            if pms.DYNAMIC_TYPE == pms.CONTINUOUS:
                continuous_time_duration = timedelta_to_time(pms.CONTINUOUS_TIME_DURATION)
                pms_list.append("CONTINUOUS_TIME_DURATION: {}".format(continuous_time_duration.strftime("%H:%M:%S")))
            else:
                pms_list.append("NOMBRE_PERIODES: {}".format(pms.NOMBRE_PERIODES))
                discrete_time_duration = timedelta_to_time(pms.DISCRETE_DECISION_TIME)
                pms_list.append("DISCRETE_DECISION_TIME: {}".format(discrete_time_duration.strftime("%H:%M:%S")))
            self.le2mserv.gestionnaire_graphique.infoserv(pms_list)

    @defer.inlineCallbacks
    def demarrer(self):
        if not self.le2mserv.gestionnaire_graphique.question(le2mtrans("Start") + " game ?"):
            return
        #  INIT PART ---------------------------------------------------------------------------------------------------
        self.current_sequence += 1
        yield (self.le2mserv.gestionnaire_experience.init_part("murielle_jeu", "PartieGA",
                                                               "RemoteGA", pms,
                                                               current_sequence=self.current_sequence))
        self.all = self.le2mserv.gestionnaire_joueurs.get_players('murielle_jeu')
        yield (self.le2mserv.gestionnaire_experience.run_step(le2mtrans(u"Configure"), self.all, "configure"))

        # FORMATION DES GROUPES ----------------------------------------------------------------------------------------
        del self.groups[:]
        try:
            gps = utiltools.form_groups(self.le2mserv.gestionnaire_joueurs.get_players(), pms.TAILLE_GROUPES,
                                        self.le2mserv.nom_session)
        except ValueError as e:
            QMessageBox.critical(None, "Group error", e.message)
            self.current_sequence -= 1
            return
        logger.debug(gps)
        self.le2mserv.gestionnaire_graphique.infoserv("Groups", bg="gray", fg="white")
        for g, m in sorted(gps.items()):
            group = GroupGA(self.le2mserv, g, m, self.current_sequence)
            self.le2mserv.gestionnaire_base.ajouter(group)
            self.groups.append(group)
            self.le2mserv.gestionnaire_graphique.infoserv("G{}".format(group.uid.split("_")[2]))
            for j in m:
                j.group = group
                self.le2mserv.gestionnaire_graphique.infoserv("{}".format(j))

        # INITIAL EXTRACTION -------------------------------------------------------------------------------------------
        yield (self.le2mserv.gestionnaire_experience.run_func(self.groups, "new_instant", 0))
        yield (self.le2mserv.gestionnaire_experience.run_step(trans_GA(u"Initial extraction"), self.all,
                                                              "set_initial_extraction"))
        yield (self.le2mserv.gestionnaire_experience.run_func(self.groups, "update_data"))

        # START GAME: loop every second or period ----------------------------------------------------------------------
        self.le2mserv.gestionnaire_graphique.infoserv("Start time: {}".format(datetime.now().strftime("%H:%M:%S")))
        self.the_n = 0  # n=second in continuous time and n=period in discrete time

        if pms.DYNAMIC_TYPE == pms.CONTINUOUS:
            self.timer_update = QTimer()
            self.timer_update.timeout.connect(self.slot_update_data)
            self.timer_update.start(int(pms.TIMER_UPDATE.total_seconds()) * 1000)
            yield (self.le2mserv.gestionnaire_experience.run_step(trans_GA("Decision"), self.all,
                                                                  "display_decision", self.the_n))
        elif pms.DYNAMIC_TYPE == pms.DISCRETE:
            for period in range(1, pms.NOMBRE_PERIODES + 1):
                self.the_n = period
                self.le2mserv.gestionnaire_graphique.infoclt([u"Période {}".format(self.the_n)], fg="white", bg="gray")
                yield (self.le2mserv.gestionnaire_experience.run_func(self.groups, "new_instant", self.the_n))
                yield (self.le2mserv.gestionnaire_experience.run_step("Decision", self.all, "display_decision",
                                                                      self.the_n))
                yield (self.le2mserv.gestionnaire_experience.run_func(self.groups, "update_data"))
            yield (self.le2mserv.gestionnaire_experience.run_func(self.all, "end_update_data"))

        # summary ------------------------------------------------------------------------------------------------------
        yield (self.le2mserv.gestionnaire_experience.run_step(le2mtrans(u"Summary"), self.all, "display_summary"))

        # End of part --------------------------------------------------------------------------------------------------
        yield (self.le2mserv.gestionnaire_experience.finalize_part("murielle_jeu"))

    @defer.inlineCallbacks
    @pyqtSlot()
    def slot_update_data(self):
        self.the_n += 1
        if self.the_n <= pms.CONTINUOUS_TIME_DURATION.total_seconds():
            yield (self.le2mserv.gestionnaire_experience.run_func(self.groups, "new_instant", self.the_n))
            yield (self.le2mserv.gestionnaire_experience.run_func(self.groups, "update_data"))
        else:
            self.le2mserv.gestionnaire_graphique.infoserv("End time: {}".format(datetime.now().strftime("%H:%M:%S")))
            self.timer_update.stop()
            yield (self.le2mserv.gestionnaire_experience.run_func(self.all, "end_update_data"))

    def display_payoffs(self):
        sequence_screen = DSequence(self.current_sequence)
        if sequence_screen.exec_():
            sequence = sequence_screen.sequence
            players = self.le2mserv.gestionnaire_joueurs.get_players()
            payoffs = sorted([(j.hostname, p.GA_gain_euros) for j in players
                              for p in j.parties if p.nom == "murielle_jeu" and p.GA_sequence == sequence])
            screen_payoffs = GuiPayoffs(self.le2mserv, "murielle_jeu", payoffs)
            screen_payoffs.exec_()
