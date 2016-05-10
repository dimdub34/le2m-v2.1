#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Ce module est le modèle du serveur. Il crée une instance de chacun des
gestionnaires (graphique, joueurs, groupes, expérience ...)
"""

import os
import socket
import logging
from time import strftime
from twisted.internet import defer
from twisted.spread import pb
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


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    """
    Main server object
    """
    def __init__(self, **kwargs):

        # network infos
        self._port_ecoute = kwargs["port"]
        self._hostname = socket.gethostname()
        self._ip = socket.gethostbyname(self._hostname)
        logger.info("Hostname: {}".format(self._hostname))
        logger.info("IP: {}".format(self._ip))
        
        # création de la session
        self._heure_debut = strftime("%H:%M:%S")
        self._nom_session = strftime('%Y%m%d%H%M')
        logger.info("Session name: {}".format(self._nom_session))
        
        # les gestionnaires
        self.gestionnaire_graphique = GestionnaireGraphique(self)
        self.gestionnaire_base = GestionnaireBase(self)
        self.gestionnaire_joueurs = GestionnaireJoueurs(self)
        self.gestionnaire_groupes = GestionnaireGroupes(self)
        self.gestionnaire_experience = GestionnaireExperience(self)

        # we connect some slot now, after instanciating the other gestionnaires
        self.gestionnaire_graphique.screen.connect_slots()
        self.gestionnaire_graphique.screen.show()
        
        # if option -e in the command line
        if kwargs["parts"]:
            expeinfos = Experiment(
                kwargs["parts"],
                kwargs["dirbase"] or os.path.join(
                    params.getp("PARTSDIR"), kwargs["parts"][0]),
                kwargs["namebase"], kwargs["test"])
            self.gestionnaire_experience.load_experiment(expeinfos)

    def start(self):
        """
        Start the server.
        """
        factory = pb.PBServerFactory(self.gestionnaire_joueurs)
        reactor.listenTCP(self._port_ecoute, factory)
        logger.info(u"Server is listening on port {}".format(self._port_ecoute))
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

    @property
    def heure_debut(self):
        return self._heure_debut

    @property
    def nom_session(self):
        return self._nom_session

    @property
    def hostname(self):
        return self._hostname

    @property
    def ip(self):
        return self._ip

    @property
    def port_ecoute(self):
        return self._port_ecoute

