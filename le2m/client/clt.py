#! /usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet import defer
from twisted.spread import pb
from twisted.internet import reactor
import socket
import logging
import importlib
from cltremote import RemoteBase, RemoteQuestionnaireFinal
from util.utili18n import le2mtrans
from configuration import configparam as params
from client.cltgui.cltguiforms import GuiAttente


logger = logging.getLogger("le2m")


class Client(object):
    def __init__(self, auto, simul):
        self._uid = None
        self._hostname = socket.gethostname()
        self._ip = socket.gethostbyname(self._hostname)
        # simul et auto
        self._automatique = auto
        self._simulation = simul
        # a dict that stores the remote, i.e. the object accessibles through
        # the network.We initially instanciate base and questionnaireFinal
        self._remotes = {'base': RemoteBase(self),
                         "questionnaireFinal": RemoteQuestionnaireFinal(self)}
        self._screen = GuiAttente()
        logger.info("{} created".format(self))

    def start(self):
        """
        Démarrage du client, il se connecte au serveur, et récupère une
        instance de la partie visible sur le réseau du serveur (fonctions qui 
        commencent par remote)/
        Ensuite se connecte au serveur.
        """
        logger.info(u"{} connecting".format(self))
        factory = pb.PBClientFactory()
        reactor.connectTCP(params.getp("SERVIP"), params.getp("SERVPORT"),
                           factory)
        defered = factory.getRootObject()
        defered.addCallback(self._connect)
        reactor.run()
    
    @defer.inlineCallbacks
    def _connect(self, le2mservpb):
        self._le2mservpb = le2mservpb

        # connection to the server. Get back an uid
        self._uid = yield(
            self._le2mservpb.callRemote(
                "connect", self._hostname, self._ip, self._simulation,
                self._automatique, self.get_remote("base"),
                self.get_remote("questionnaireFinal")))
        logger.info(u"{} ({}) connected => {}".format(self.hostname,self.ip, self))

        if not self.simulation:
            self.screen.showFullScreen()

    def load_part(self, partname, remoteclassname):
        """
        Try to load the part
        this method is called by the connect method of this object and by
        cltremote.RemoteBase
        RemoteBase
        :param partname: a dict with 3 keys: remote_partie_name,
        remote_classname and remote_parametres
        :param remoteclassname
        """
        success = False
        logger.info(u"{} Loading of part: {}".format(self.uid, partname))
        try:

            module = importlib.import_module("parts.{p}.{p}Remote".format(
                p=partname))
            logger.info(
                le2mtrans(u"{j} Module parts.{p}.{p}Remote loaded").format(
                    j=self.uid, p=partname))
            rem_temp = getattr(module, remoteclassname)
            remote = rem_temp(self)
            self._remotes[partname] = remote
            logger.info(u"{} Part {} loaded successfully".format(
                self.uid, partname))
            success = True

        except (KeyError, ImportError, AttributeError) as e:
            logger.critical(
                u"{} Error while loading part: {}".format(self.uid, e.message))

        finally:
            return success
    
    @defer.inlineCallbacks
    def disconnect(self):
        yield (self._le2mservpb.callRemote("disconnect", self._uid))
        logging.shutdown()
        reactor.callLater(2, reactor.stop)

    def get_remote(self, nom_remote):
        return self._remotes.get(nom_remote)
        
    @property
    def uid(self):
        return self._uid

    @property
    def ip(self):
        return self._ip

    @property
    def hostname(self):
        return self._hostname

    @property
    def simulation(self):
        return self._simulation

    @simulation.setter
    def simulation(self, value):
        self._simulation = bool(value)
        logger.info(u"{} Simulation {}".format(self.uid, bool(self.simulation)))

    @property
    def automatique(self):
        return self._automatique

    @automatique.setter
    def automatique(self, value):
        self._automatique = bool(value)
        logger.info(u"{} Automatic {}".format(self.uid, bool(self.automatique)))

    @property
    def screen(self):
        return self._screen

    def __repr__(self):
        if self.uid is None:
            return "{} ({})".format(self.hostname, self.ip)
        else:
            return self.uid