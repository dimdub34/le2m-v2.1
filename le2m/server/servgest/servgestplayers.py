# -*- coding: utf-8 -*-

from PyQt4.QtCore import QObject, pyqtSignal
from twisted.spread import pb
from twisted.internet import defer
import logging
from util import utiltwisted
from util.utili18n import le2mtrans
from configuration.configconst import HOMME, FEMME
from server.servplayers import Joueur

logger = logging.getLogger("le2m")


class GestionnaireJoueurs(pb.Root, QObject):
    """
    Classe qui gère les joueurs en local: connexion, déconnexion, liste.
    """
    playeradded = pyqtSignal(object, int)  # player, nb of connected
    playerremoved = pyqtSignal(object, int)  # player, nb of connected

    def __init__(self, main_serveur):
        super(GestionnaireJoueurs, self).__init__()
        self._main_serveur = main_serveur
        self._joueurs = {}  # keep a ref to the players
        self._compteur_joueurs = 0

    @property
    def nombre_joueurs(self):
        return len(self.get_players())

    def remote_connect(self, hostname, ip, simulation, automatique,
                       remote_base, remote_questfinal):
        """
        This method is called by the remote who tries to connect to the
        server.
        Return the uid of the player
        """
        logger.info(le2mtrans(u"Connection of {host}, with ip {addr}").format(
            host=hostname, addr=ip))

        # creation of the player
        uid = "{}_j_{}".format(self._main_serveur.nom_session,
                               self._compteur_joueurs)
        self._compteur_joueurs += 1
        joueur = Joueur(
            uid, hostname, ip, self._main_serveur.gestionnaire_graphique)
        self._main_serveur.gestionnaire_base.add_player(joueur)
        self._joueurs[joueur.uid] = joueur
        joueur.get_part("base").remote = remote_base
        joueur.get_part("base").automatique = automatique
        joueur.get_part("base").simulation = simulation
        joueur.get_part("questionnaireFinal").remote = remote_questfinal

        # emit a signal
        self.playeradded.emit(joueur, self.get_nombre_joueurs())

        # sends back player's uid
        return uid

    def remote_disconnect(self, joueur_uid):
        """
        called by the remote when disconnecting.
        """
        joueur = self.get_joueur(joueur_uid)
        logger.info(le2mtrans(u"Deconnection of {host}").format(
            host=joueur.hostname))
        # we delete the player
        try:
            del self._joueurs[joueur.uid]
        except KeyError:
            logger.warning(
                le2mtrans(u"{host} was not in the list of connected "
                          u"hosts").format(joueur.hostname))
            pass
        self.playerremoved.emit(joueur, self.get_nombre_joueurs())

    def get_players(self, partname=None):
        """
        Return a list with the connected players or their corresponding part
        :param partname:
        :return: list
        """
        # logger.debug(u"get_players with arg {}".format(partname))
        if partname:
            players = [p.get_part(partname) for p in self._joueurs.viewvalues()]
            if players.count(None) == len(players):
                return None
            else:
                return players
        else:
            return list(self._joueurs.viewvalues())

    def get_joueur(self, joueur_uid):
        try:
            return self._joueurs[joueur_uid]
        except KeyError:
            logger.warning(u"{} ".format(joueur_uid) +
                           le2mtrans(u"is not in the list of connected players"))
            return None

    def get_nombre_joueurs(self):
        return len(self.get_players())

    @defer.inlineCallbacks
    def deconnecter_joueurs(self):
        if self.get_nombre_joueurs > 0:
            logger.info(
                le2mtrans(u"Disconnection of the players still connected"))
            yield (
                utiltwisted.forEach(self.get_players(), "disconnect"))

    def set_genres(self, dict_genres):
        for k, v in dict_genres.iteritems():
            k.set_genre(v)
        hommes = [j for j in self.get_players() if j.genre == HOMME]
        femmes = [j for j in self.get_players() if j.genre == FEMME]
        self._main_serveur.gestionnaire_graphique.infoserv(
            [None, le2mtrans(u"Subjects' gender"),
             le2mtrans(u"Men: {m}").format(m=hommes),
             le2mtrans(u"Women: {w}").format(w=femmes)])
