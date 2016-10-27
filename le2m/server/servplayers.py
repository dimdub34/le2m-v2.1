# -*- coding: utf-8 -*-

import importlib
import logging
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from twisted.internet import defer
from twisted.spread import pb  # pour gestion erreur à la déconnexion
from servbase import Base
import servparties


logger = logging.getLogger("le2m.{}".format(__name__))

parties_joueurs_table = Table(
    'parties_joueurs__joueurs_parties', Base.metadata,
    Column('parties_id', Integer, ForeignKey('parties.id'), primary_key=True),
    Column('joueurs_uid', String(30), ForeignKey('joueurs.uid'),
           primary_key=True))


class Joueur(Base):
    """
    Le joueur est un des champs de la table session
    Le joueur participe à une session, mais au sein de la session il peut 
    participer à plusieurs parties. 
    Champs:
        | - uid: identique unique du joueur, sert de clé
        | - hostname: le hostname du poste du joueur
        | - ip: l'adresse ip du poste du joueur
        | - nom: le nom du joueur (pas utilisé)
        | - prenom: le prénom du joueur (pas utilisé)
        | - commentaires: pour que l'expérimentateur puisse mettre des 
        remarques à propos du joueur. Attention ce ne sont pas les commentaires 
        | du joueur, ces derniers sont dans partie_base
    """
    __tablename__ = "joueurs"
    session_id = Column(Integer, ForeignKey("sessions.id"))
    parties = relationship("Partie", backref="joueurs",
                           secondary=parties_joueurs_table)

    uid = Column(String(30), primary_key=True)
    hostname = Column(String(100))
    ip = Column(String(20))
    nom = Column(String(100))
    prenom = Column(String(100))
    commentaires = Column(String(300))  # for experimenters, about the subject

    def __init__(self, uid, hostname, ip, gestionnaire_graphique):
        super(Joueur, self).__init__()
        self.uid = uid
        self.hostname = hostname
        self.ip = ip
        self._gestionnaire_graphique = gestionnaire_graphique
        # store parts
        self._parts = {
            "base": servparties.PartieBase(self),
            "questionnaireFinal": servparties.PartieQuestionnaireFinal(self)}
        self.parties.append(self._parts["base"])
        self.parties.append(self._parts["questionnaireFinal"])
        self._gender = None
        self._groupe = None  # obsolete, use group rather
        self._group = None
        self._other_group_members = None
        self._subgroup = None
        self._other_subgroup_members = None

    @defer.inlineCallbacks
    def add_part(self, le2mserv, partname, partclassname, remoteclassname):
        """
        On ajoute la partie au joueur (ou le joueur à la partie) dans la
        base de données.
        La partie va chercher automatiquement son remote, c'est à dire la
        partie de code accessible depuis le serveur et exécutable sur le poste
        client.
        """
        if partname not in self._parts:
            # load the module which contains the part
            partmodule = importlib.import_module("parts.{p}.{p}Part".format(
                p=partname))

            # get the class and instantiate it
            partclass = getattr(partmodule, partclassname)
            partinstance = partclass(le2mserv, self)

            # get the remote of the part and set the attribute remote in the
            # corresponding part
            try:
                partremoteinstance = yield (
                    self.get_part("base").remote.callRemote(
                        "get_remote", partname, remoteclassname))
                if not partremoteinstance:
                    raise ValueError("The player {} didn't get the remote of "
                                     "part {}".format(self.uid, partname))
                partinstance.remote = partremoteinstance
            except (ValueError, pb.RemoteError) as e:
                logger.critical(e.message)
                raise

            # add the part to the dict with the part instances and to the list
            # of played parts
            self._parts[partname] = partinstance
            self.parties.append(self._parts[partname])

            self.info(u"Part {} loaded".format(partname))
            self.remove_waitmode()

    def info(self, texte, couleur="black"):
        self._gestionnaire_graphique.infoclt(
            u"{}: {}".format(self, texte), fg=couleur, bg="white")

    def set_waitmode(self):
        self._gestionnaire_graphique.set_waitmode(self)

    def remove_waitmode(self):
        self._gestionnaire_graphique.remove_waitmode(self)

    def get_part(self, partname):
        """
        return part or None
        """
        return self._parts.get(partname, None)

    @defer.inlineCallbacks
    def disconnect(self):
        """
        Disconnect the player (and close the app on the remote side)
        """
        logger.info(u"Player {} is deconnecting".format(self))
        try:
            yield (self.get_part("base").remote.callRemote('disconnect'))
        except pb.DeadReferenceError as e:
            logger.warning(u"Player {} is not connected".format(self))

    def __repr__(self):
        return '{} (j{})'.format(
            self.hostname.split('.')[0], self.uid.split('_')[2])

    def __str__(self):
        return self.__repr__()

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        self._gender = value

    @property
    def groupe(self):
        return self._groupe

    @groupe.setter
    def groupe(self, val):
        self._groupe = val

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, val):
        self._group = val

    @property
    def other_group_members(self):
        """
        :return: a tuple with the other members of the group
        """
        return self._other_group_members

    @other_group_members.setter
    def other_group_members(self, tuple_members):
        """
        :param tuple_members: a tuple with the other members of the group
        :return:
        """
        self._other_group_members = tuple_members

    @property
    def subgroup(self):
        return self._subgroup

    @subgroup.setter
    def subgroup(self, val):
        self._subgroup = val

    @property
    def other_subgroup_members(self):
        return self._other_subgroup_members

    @other_subgroup_members.setter
    def other_subgroup_members(self, tuple_members):
        self._other_subgroup_members = tuple_members