# -*- coding: utf-8 -*-

from twisted.internet import defer
import logging
from collections import OrderedDict
from util import utiltools
import PublicGoodGlobalLocalParams as pms
import PublicGoodGlobalLocalTextes as texts
from PublicGoodGlobalLocalTextes import _PGGL
from PublicGoodGlobalLocalPart import PartiePGGL  # for sqlalchemy
from PublicGoodGlobalLocalGui import GuiConfiguration


logger = logging.getLogger("le2m")
    

class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv
        self._currentsequence = 0

        actions = OrderedDict()
        actions[_PGGL(u"Configure")] = self._configure
        actions[_PGGL(u"Display parameters")] = lambda _: \
            self._le2mserv.gestionnaire_graphique.display_information2(
                titre=u"Paramètres", texte=utiltools.get_module_info(pms))
        actions[_PGGL(u"Start")] = lambda _: self._demarrer()
        actions[_PGGL(u"Display payoffs")] = \
            lambda _: self._le2mserv.gestionnaire_experience.display_payoffs(
                "PublicGoodGlobalLocal")
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            _PGGL(u"Local/Global Public Good"), actions)

    def _configure(self):
        """
        Display a dialog box. Inside it is possible to change some of the
        parameters
        :return:
        """
        traitements = [U"BASELINE", u"CARTONS_LOCAL_AUTRE",
                       u"CARTONS_LOCAL", u"CARTONS_GLOBAL",
                       u"CARTONS_LOCAL_GLOBAL"]
        communications = [u"SANS_COMMUNICATION", U"COMMUNICATION_LOCAL",
                          U"COMMUNICATION_GLOBAL"]

        ecran_config = GuiConfiguration(
            pms.NOMBRE_PERIODES, traitements, communications,
            pms.COMMUNICATION_TEMPS,
            u" ".join(map(str, pms.COMMUNICATION_PERIODES)))

        if ecran_config.exec_():
            configuration = ecran_config.get_configuration()
            pms.NOMBRE_PERIODES = configuration.nombreperiodes
            pms.TRAITEMENT = configuration.traitement
            pms.COMMUNICATION = configuration.communication
            pms.COMMUNICATION_TEMPS = configuration.communication_temps
            pms.COMMUNICATION_PERIODES = \
                configuration.communication_periodes

            self._le2mserv.gestionnaire_graphique.infoserv(
                _PGGL(u"Treatment: {}").format(
                    traitements[configuration.traitement]))
            self._le2mserv.gestionnaire_graphique.infoserv(
                _PGGL(u"Communication: {}").format(
                    communications[configuration.communication]))
            if configuration.communication == pms.COMMUNICATION_LOCAL or \
                    configuration.communication == pms.COMMUNICATION_GLOBAL:
                self._le2mserv.gestionnaire_graphique.infoserv(
                    _PGGL(u"Communication time: {} seconds").format(
                        configuration.communication_temps))
                self._le2mserv.gestionnaire_graphique.infoserv(
                    _PGGL(u"Communication periods: {}").format(
                        configuration.communication_periodes))

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(_PGGL(u"Start PublicGoodGlobalLocal?"))
        if not confirmation:
            return
        
        # initiate part --------------------------------------------------------
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "PublicGoodGlobalLocal", "PartiePGGL", "RemotePGGL", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'PublicGoodGlobalLocal')

        # form groups ----------------------------------------------------------
        try:
            self._le2mserv.gestionnaire_groupes.former_groupes(
                self._le2mserv.gestionnaire_joueurs.get_players(),
                pms.TAILLE_GROUPES, forcer_nouveaux=False)
            self._le2mserv.gestionnaire_groupes.former_sousgroupes(
                pms.TAILLE_SOUS_GROUPES, forcer_nouveaux=False)
        except ValueError as e:
            self._le2mserv.gestionnaire_graphique.display_error(e.message)
            return

        # set id and othermembers ----------------------------------------------
        for j in self._tous:
            group_id = self._le2mserv.gestionnaire_groupes.\
                get_identifiant_dansgroupe(j.joueur)
            group_othermembers = \
                [m.get_part("PublicGoodGlobalLocal") for m in
                 self._le2mserv.gestionnaire_groupes.
                 get_autres_membres_groupe(j.joueur)]
            subgroup_id = self._le2mserv.gestionnaire_groupes.\
                get_identifiant_danssousgroupe(j.joueur)
            subgroup_othermembers = \
                [m.get_part("PublicGoodGlobalLocal") for m in
                 self._le2mserv.gestionnaire_groupes.
                 get_autres_membres_sousgroupe(j.joueur)]
            j.set_othermembersandid(group_id, group_othermembers,
                                    subgroup_id, subgroup_othermembers)

        # configure players and remotes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._currentsequence += 1
        self._le2mserv.gestionnaire_graphique.infoserv(
            [None, _PGGL(u"Sequence {}").format(self._currentsequence),
             _PGGL(u"Treatment: {}").format(
                 texts.get_traitement(pms.TRAITEMENT)),
             _PGGL(u"Communication: {}").format(
                 texts.get_communication(pms.COMMUNICATION))])

        yield (self._le2mserv.gestionnaire_experience.run_func(
            self._tous, "configure", self._currentsequence))

        # Repetitions ==========================================================
        for period in xrange(1, pms.NOMBRE_PERIODES + 1):

            if self._le2mserv.gestionnaire_experience.stop_repetitions:
                break 

            # period ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._le2mserv.gestionnaire_graphique.infoserv(
                [None, _PGGL(u"Period {}").format(period)])
            self._le2mserv.gestionnaire_graphique.infoclt(
                [None, _PGGL(u"Period {}").format(period)],
                fg="white", bg="gray")
            yield (self._le2mserv.gestionnaire_experience.run_func(
                self._tous, "newperiod", period))

            # communication ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if (pms.COMMUNICATION == pms.COMMUNICATION_LOCAL or
                pms.COMMUNICATION == pms.COMMUNICATION_GLOBAL) and \
                    period in pms.COMMUNICATION_PERIODES:
                yield (self._le2mserv.gestionnaire_experience.run_step(
                    u"Communication", self._tous, "display_communication"))
            
            # decision ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Decision", self._tous, "display_decision"))

            # computation of contribution by groups and subgroups ~~~~~~~~~~~~~~
            self._le2mserv.gestionnaire_graphique.infoserv(
                _PGGL(u"Groups' and subgroups' contributions"))
            for g, m in self._le2mserv.gestionnaire_groupes.get_groupes(
                    "PublicGoodGlobalLocal").iteritems():
                loc_tot, glob_tot = 0, 0
                txt_loc = u""
                # in each subgroup
                for sg, m2 in self._le2mserv.gestionnaire_groupes.\
                        get_sousgroupes(g).iteritems():
                    # get and compute quantities
                    m3 = [j.get_part("PublicGoodGlobalLocal") for j in m2]
                    loc_sg = sum([j.currentperiod.PGGL_local for j in m3])
                    loc_tot += loc_sg
                    glob_sg = sum([j.currentperiod.PGGL_global for j in m3])
                    glob_tot += glob_sg
                    txt_loc += u" SG{}: loc {} glob {}".format(
                        sg.split("_")[2], loc_sg, glob_sg)
                    # set in parts
                    for j in m3:
                        j.currentperiod.PGGL_local_sousgroupe = loc_sg
                        j.currentperiod.PGGL_global_sousgroupe = glob_sg
                # each player in the group
                for j in m:
                    j.currentperiod.PGGL_local_total = loc_tot
                    j.currentperiod.PGGL_local_autresousgroupe = \
                        j.currentperiod.PGGL_local_total - \
                        j.currentperiod.PGGL_local_sousgroupe
                    j.currentperiod.PGGL_global_total = glob_tot
                    j.currentperiod.PGGL_global_autresousgroupe = \
                        j.currentperiod.PGGL_global_total - \
                        j.currentperiod.PGGL_global_sousgroupe
                self._le2mserv.gestionnaire_graphique.infoserv(
                    u"G{}: loc {} glob {} {}".format(
                        g.split("_")[2], loc_tot, glob_tot, txt_loc))
            self._le2mserv.gestionnaire_base.enregistrer()

            # information and disapprovals ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield (self._le2mserv.gestionnaire_experience.run_step(
                u"Information", self._tous, "display_information"))

            # period payoffs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "PublicGoodGlobalLocal")
        
            # summary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield(
                self._le2mserv.gestionnaire_experience.run_step(
                    u"Summary", self._tous, "display_summary"))

            # stats ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        # End of  repetitions ==================================================
        self._le2mserv.gestionnaire_experience.finalize_part(
            "PublicGoodGlobalLocal")
