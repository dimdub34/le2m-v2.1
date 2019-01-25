# -*- coding: utf-8 -*-

# built-in
import os
from PyQt4.QtCore import QObject, pyqtSignal
from PyQt4 import QtGui
from time import strftime
import random
import importlib
import logging
from twisted.internet import defer
from datetime import datetime

# le2m
from util.utili18n import le2mtrans
from util import utiltools, utiltwisted
from server.servgui.servguidialogs import GuiPayoffs


logger = logging.getLogger("le2m")


class GestionnaireExperience(QObject):
    """
    Cet objet gère tout ce qui touche à l'expérience, cad lance les
    étapes, gère les paiements.
    """

    stoprepetitions = pyqtSignal(bool)

    def __init__(self, le2msrv):
        super(GestionnaireExperience, self).__init__()
        self.le2msrv = le2msrv
        self._parts = []  # list of parts
        self._servs = {}  # keep a ref to the loaded partserv
        self._stop_repetitions = False  # to stop the part at the next period
        self._screenpayoffs = None

    # ==========================================================================
    # Load and init
    # ==========================================================================

    def load_experiment(self, expeinfos):
        """
        - Load the experiment, i.e. the parts selected by the experimenter
        - Create the database
        :param expeinfos: namedtuplue with the informations for creating the
        experiment
        """
        # load of parts
        for p in expeinfos.parts:
            try:
                module = importlib.import_module("parts.{0}.{0}Serv".format(p))
                serv = getattr(module, "Serveur")
                self._servs[p] = serv(self.le2msrv)
                self.le2msrv.gestionnaire_graphique.infoserv(
                    le2mtrans(u"Part") + " {} ".format(p) + le2mtrans(u"loaded"))
            except ImportError as e:
                logger.critical(
                    u"Error while loading part {p}: {msg}".format(
                        p=p, msg=e.message))

        # database creation
        if not self.le2msrv.gestionnaire_base.is_created():
            self.le2msrv.gestionnaire_base.creer_base(
                expeinfos.dirbase, expeinfos.basename, expeinfos.istest)

    @defer.inlineCallbacks
    def init_part(self, partname, partclassname, remoteclassname,
                  partparameters, **kwargs):
        """
        init the part:
        - each player loads the part and instanciate the object
        - we add the part to the list of parts
        - we store the parameters of the part in the session table
        :param partname: name of the part
        :param partclassname: class name of the part
        :param remoteclassname: class name of the remote part
        :param partparameters: parameters of the part
        :return:
        """
        self.le2msrv.gestionnaire_graphique.infoserv(None)
        self.le2msrv.gestionnaire_graphique.infoserv(
            partname.upper(), fg="white", bg="blue")
        self.le2msrv.gestionnaire_graphique.infoclt(None)
        self.le2msrv.gestionnaire_graphique.infoclt(
            partname.upper(), fg="white", bg="blue")

        # the players instantiate the part and get the corresponding remote
        players = self.le2msrv.gestionnaire_joueurs.get_players()
        self.le2msrv.gestionnaire_graphique.set_waitmode(players)
        yield (self.run_func(players, "add_part", self.le2msrv,
                             partname, partclassname, remoteclassname, **kwargs))


        self._parts.append(partname)
        self.stop_repetitions = False

        # we store the parameters in the database (in table session)
        paramcontent = utiltools.get_module_info(partparameters)
        sesscontent = \
            self.le2msrv.gestionnaire_base.get_session().parametres or u""
        sesscontent += u"{}PART {}\n{}".format(
            u"\n\n" if sesscontent else u"", partname, paramcontent)
        logger.debug(sesscontent)
        self.le2msrv.gestionnaire_base.get_session().parametres = sesscontent
        self.le2msrv.gestionnaire_base.enregistrer()

        self.le2msrv.gestionnaire_graphique.infoserv(
            le2mtrans(u"Start time: {st}").format(st=strftime("%H:%M:%S")))

    # ==========================================================================
    # Generic functions
    # ==========================================================================

    @defer.inlineCallbacks
    def run_step(self, step_name, step_participants, step_function, *args,
                 **kwargs):
        """
        Run the step:
        - display the name of the step on the client list
        - run the function with the parameters on the given participants
        - display the end of the step on the server list
        """
        logger.info(u"run_step: {}".format(step_name))
        self.le2msrv.gestionnaire_graphique.infoclt(step_name.upper(), fg="gray")
        self.le2msrv.gestionnaire_graphique.set_waitmode(step_participants)
        yield (utiltwisted.forAll(
            step_participants, step_function, *args, **kwargs))
        self.le2msrv.gestionnaire_graphique.infoserv(
            u"Ok {}".format(step_name), fg="green")
        self.le2msrv.gestionnaire_base.enregistrer()

    @defer.inlineCallbacks
    def run_func(self, who, func, *args, **kwargs):
        """
        Run the func with the given parameters on the given participants
        """
        logger.info(u"run_func: {}".format(func))
        if not type(who) is list:
            raise ValueError(le2mtrans(u"The arg must be of type list"))
        yield (utiltwisted.forAll(who, func, *args, **kwargs))

    # ==========================================================================
    # functions that only affect the server
    # ==========================================================================

    def draw_part(self, parts):
        """
        Draw randomly a part among thoses played
        """
        drawnpart = random.choice(parts)
        partnum = self._parts.index(drawnpart) + 1
        logger.info(u"Part randomly drawn: {}".format(drawnpart))
        self.le2msrv.gestionnaire_graphique.infoserv(
            le2mtrans(u"Part randomly drawn: {} (part {})").format(
                drawnpart, partnum))

    def display_payoffs_onserver(self, partname):
        """
        Open a dialog box with the payoffs
        """
        payoffs = []
        try:
            joueurs = sorted(self.le2msrv.gestionnaire_joueurs.get_players(
                partname), key=lambda x: x.joueur.hostname)
        except TypeError:  # no client connected
            QtGui.QMessageBox.warning(
                self.le2msrv.gestionnaire_graphique.screen,
                le2mtrans(u"warning"), le2mtrans(u"No client connected"))
            return
        try:
            if partname == "base":
                for j in joueurs:
                    payoffs.append(
                        [j.joueur.hostname, "{:.2f}".format(j.paiementFinal)])
            else:
                for j in joueurs:
                    gain_partie = getattr(j, "{}_gain_euros".format(
                        j.nom_court))
                    payoffs.append(
                        [j.joueur.hostname, "{:.2f}".format(gain_partie)])

        except (AttributeError, KeyError) as e:
            QtGui.QMessageBox.critical(
                self.le2msrv.gestionnaire_graphique.screen,
                le2mtrans(u"Error"),
                le2mtrans(u"Error while getting payoffs for "
                          u"part {}: {}").format(partname, e.message))
            return

        self._screenpayoffs = GuiPayoffs(self.le2msrv, partname, payoffs)
        self._screenpayoffs.show()

    def add_tofinalpayoffs(self, partname):
        """
        Add the part payoffs to the final payoffs
        """
        for p in self.le2msrv.gestionnaire_joueurs.get_players(partname):
            gain_euros = getattr(p, "{}_gain_euros".format(
                    p.nom_court))
            p.joueur.get_part('base').paiementFinal += gain_euros
        self.le2msrv.gestionnaire_base.enregistrer()
        self.le2msrv.gestionnaire_graphique.infoserv(
            le2mtrans(u"Payoffs of part {} added to final payoffs").format(
                partname), fg="red")

    # ==========================================================================
    # Functions that call the players' remote
    # ==========================================================================

    @defer.inlineCallbacks
    def display_welcome(self):
        """
        Display the welcome screen on remotes
        """
        participants = self.le2msrv.gestionnaire_joueurs.get_players("base")
        if not participants:
            return

        self.le2msrv.gestionnaire_graphique.infoclt(None)
        yield (self.run_step(u"Instructions", participants, "display_welcome"))

    @defer.inlineCallbacks
    def start_questcomp(self, questionnaire):
        """
        Start the understanding questionnaire.
        """
        participants = self.le2msrv.gestionnaire_joueurs. \
            get_players("base")
        if not participants:
            return

        yield (
            self.run_step(
                le2mtrans(u"Understanding questionnaire"), participants,
                "display_questcomp", questionnaire))

    def compute_periodpayoffs(self, partname):
        """
        Compute the period's payoff for each player.
        Call the method "compute_periodpayoff" in each player's partie.
        :param partname: the name of the part for which the payoffs must be
        computed
        """
        if not self.has_part(partname):
            raise ValueError(le2mtrans(
                u"Part {} not in the list").format(partname))

        logger.info(le2mtrans(
            u"Computation of period payoffs for part {}").format(partname))
        self.le2msrv.gestionnaire_graphique.\
            infoclt(le2mtrans(u"PAYOFFS"), fg="gray")
        for p in self.le2msrv.gestionnaire_joueurs.get_players(partname):
            p.compute_periodpayoff()
            payoff = getattr(p.currentperiod,
                             "{}_periodpayoff".format(p.nom_court))
            self.le2msrv.gestionnaire_graphique.infoclt(
                u"{}: {}".format(p.joueur, payoff))
        self.le2msrv.gestionnaire_base.enregistrer()

    @defer.inlineCallbacks
    def finalize_part(self, partname, *args, **kwargs):
        """
        Calcule le gain de la partie puis ajoute l'heure de fin et les
        textes de fin
        """
        if not self.has_part(partname):
            raise ValueError(le2mtrans(u"Part {p} not in the list").format(
                p=partname))

        # computation of part's payoffs
        logger.info(
            le2mtrans(u"Computation of payoffs for part {p}").format(
                p=partname))
        self.le2msrv.gestionnaire_graphique.infoclt(
            [None, le2mtrans(u'Payoffs of part {p}').format(
                p=partname.upper())], fg="red")

        players = self.le2msrv.gestionnaire_joueurs.get_players(partname)
        yield (self.run_func(players, "compute_partpayoff", *args, **kwargs))

        for p in players:
            payoff = getattr(p, "{}_gain_euros".format(p.nom_court))
            self.le2msrv.gestionnaire_graphique.infoclt(
                u"{}: {:.2f}".format(p.joueur, payoff))
        self.le2msrv.gestionnaire_base.enregistrer()

        # Finalization of part
        self.le2msrv.gestionnaire_graphique.infoserv(
            le2mtrans(u"End time: {}").format(strftime("%H:%M:%S")))
        self.le2msrv.gestionnaire_graphique.infoclt(
            u'Ok {}'.format(partname).upper(), fg="white", bg="blue")
        self.le2msrv.gestionnaire_graphique.infoserv(
            u'Ok {}'.format(partname).upper(), fg="white", bg="blue")

    @defer.inlineCallbacks
    def display_finalquestionnaire(self):
        """
        Start the final questionnaire
        """
        participants = self.le2msrv.gestionnaire_joueurs. \
            get_players('questionnaireFinal')
        if not participants:
            return
        self.le2msrv.gestionnaire_graphique.infoclt(None)
        yield (self.run_step(
            u"Questionnaire final", participants, "start"))

    @defer.inlineCallbacks
    def display_finalscreen(self):
        self.le2msrv.gestionnaire_graphique.infoclt(None)
        yield (self.run_step(
            le2mtrans(u"Final screen"),
            self.le2msrv.gestionnaire_joueurs.get_players("base"),
            "display_finalscreen"))

    @defer.inlineCallbacks
    def display_payoffs_onremotes(self, part_or_listOfParts):
        """
        Display the final text of each parts on the remote
        """
        self.le2msrv.gestionnaire_graphique.infoclt(None)
        players = self.le2msrv.gestionnaire_joueurs.get_players("base")
        if type(part_or_listOfParts) is str:
            yield (self.run_step(
                le2mtrans(u"Display part payoffs"), players, "display_payoffs",
                part_or_listOfParts))

        elif type(part_or_listOfParts) is list:
            orderedparts = {}
            for p in part_or_listOfParts:
                orderedparts[self._parts.index(p)+1] = p
            step = le2mtrans(u"Display details of payoffs for parts") + \
                    u" {}".format(u", ".join(
                        [v for k, v in sorted(orderedparts.viewitems())]))
            self.le2msrv.gestionnaire_graphique.infoclt(None)
            yield (self.run_step(
                step, players, "display_payoffs", orderedparts))

    # ==========================================================================
    # properties, setters and getters
    # ==========================================================================

    @property
    def stop_repetitions(self):
        return self._stop_repetitions

    @stop_repetitions.setter
    def stop_repetitions(self, yes_or_no):
        """
        Stop (or cancel) the part at the next period. Emit a signal in order
        the le2m server screen to update (menu options)
        :param yes_or_no:
        :return:
        """
        self._stop_repetitions = yes_or_no
        if self._stop_repetitions:
            logger.info(le2mtrans(u"The game will stop next period"))
        else:
            logger.info(le2mtrans(u"The game won't stop next period"))
        self.stoprepetitions.emit(self.stop_repetitions)

    def has_part(self, partname):
        return partname in self._parts

    def get_parts(self):
        return self._parts[:]
