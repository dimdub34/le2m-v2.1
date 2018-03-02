#! /usr/bin/python
# -*- coding: utf-8 -*-

""" ============================================================================

This modules only contains the server. It creates an instance of the various
models (experiment, groups, base and so on).

============================================================================ """

# built-in
import os
import socket
import logging
from time import strftime
from twisted.internet import defer
from twisted.spread import pb

# le2m
from configuration import configparam as params
from configuration.configvar import Experiment
from servgest.servgestgui import GestionnaireGraphique
from servgest.servgestexpe import GestionnaireExperience
from servgest.servgestbase import GestionnaireBase
from servgest.servgestplayers import GestionnaireJoueurs
from servgest.servgestgroups import GestionnaireGroupes

# twisted reactor is imported after gestionnaire_graphique because PyQt
# install a common reactor for PyQt and twisted
from twisted.internet import reactor


logger = logging.getLogger("le2m")


class Serveur(object):
    """
    Main server object
    """
    def __init__(self, **kwargs):

        # ----------------------------------------------------------------------
        # network infos
        # ----------------------------------------------------------------------
        self.port_ecoute = kwargs["port"]
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)

        logger.info("Hostname: {}".format(self.hostname))
        logger.info("IP: {}".format(self.ip))
        
        # ----------------------------------------------------------------------
        # create the session
        # ----------------------------------------------------------------------
        self.heure_debut = strftime("%H:%M:%S")
        self.nom_session = strftime('%Y%m%d%H%M')
        logger.info("Session name: {}".format(self.nom_session))

        # ----------------------------------------------------------------------
        # Instantiate the models
        # ----------------------------------------------------------------------
        self.gestionnaire_base = GestionnaireBase(self)
        self.gestionnaire_joueurs = GestionnaireJoueurs(self)
        self.gestionnaire_groupes = GestionnaireGroupes(self)
        self.gestionnaire_experience = GestionnaireExperience(self)
        self.gestionnaire_graphique = GestionnaireGraphique(self)

        # ----------------------------------------------------------------------
        # we connect some slot now, after the instantiation of the other
        # gestionnaires
        # ----------------------------------------------------------------------
        self.screen = self.gestionnaire_graphique.screen  # just a shortcut
        # self.screen.connect_slots()
        self.screen.show()

        # ----------------------------------------------------------------------
        # load a part if it is in the command line options (arg -e)
        # ----------------------------------------------------------------------
        if kwargs["parts"]:
            expeinfos = Experiment(
                kwargs["parts"],
                kwargs["dirbase"] or os.path.join(
                    params.getp("PARTSDIR"), kwargs["parts"][0]),
                kwargs["namebase"], kwargs["test"])
            self.gestionnaire_experience.load_experiment(expeinfos)

    # --------------------------------------------------------------------------
    # METHODS
    # --------------------------------------------------------------------------

    def start(self):
        """
        Start the server.
        """
        factory = pb.PBServerFactory(self.gestionnaire_joueurs)
        reactor.listenTCP(self.port_ecoute, factory)
        logger.info(u"Server is listening on port {}".format(self.port_ecoute))
        # boucle réseau et graphique
        reactor.run()
  
    @defer.inlineCallbacks
    def arreter(self):
        """
        Stop the server.
        """
        logger.info(u"The server is going to shutdown")
        yield (self.gestionnaire_joueurs.deconnecter_joueurs())
        self.gestionnaire_base.fermer_base(strftime("%H:%M:%S"))
        logging.shutdown()
        reactor.callLater(2, reactor.stop)


