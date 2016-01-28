# -*- coding: utf-8 -*-

from twisted.internet import defer
from twisted.spread import pb
import logging
from datetime import datetime
from sqlalchemy.orm import relationship 
from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from server.servbase import Base
from server.servparties import Partie
from collections import OrderedDict
import PublicGoodGlobalLocalParams as pms
import PublicGoodGlobalLocalTextes as texts
from PublicGoodGlobalLocalTextes import _PGGL


logger = logging.getLogger("le2m")


class PartiePGGL(Partie, pb.Referenceable):
    __tablename__ = "partie_PublicGoodGlobalLocal"
    __mapper_args__ = {'polymorphic_identity': 'PublicGoodGlobalLocal'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsPGGL')
    messages = relationship('MessagesPGGL')

    def __init__(self, le2mserv, joueur):
        super(PartiePGGL, self).__init__("PublicGoodGlobalLocal", "PGGL")
        self._le2mserv = le2mserv
        self._pgglserv = None
        self.joueur = joueur
        self.PGGL_gain_ecus = 0
        self.PGGL_gain_euros = 0
        self._texte_recapitulatif = u""
        self._texte_final = u""

        # history
        self._histo_headvars = OrderedDict()
        self._histo_headvars[_PGGL(u"Period")] = "PGGL_period"
        self._histo_headvars[_PGGL(u"Individual\naccount")] = "PGGL_individuel"
        self._histo_headvars[_PGGL(u"Local\naccount")] = "PGGL_local"
        self._histo_headvars[_PGGL(u"Global\naccount")] = "PGGL_global"
        self._histo_headvars[_PGGL(u"Total\nlocal\naccount\n(your\ngroup)")] = \
            "PGGL_local_sousgroupe"
        self._histo_headvars[
            _PGGL(u"Total\nglobal\naccount\n(the other\ngroup)")] = \
            "PGGL_global_autresousgroupe"
        self._histo_headvars[
            _PGGL(u"Total\nglobal\naccount\n(both\ngroups)")] = \
            "PGGL_global_total"
        self._histo_headvars[_PGGL(u"Period\npayoff")] = "PGGL_periodpayoff"
        self._histo_headvars[_PGGL(u"Cumulative\npayoff")] = \
            "PGGL_cumulativepayoff"

        # history display on the information dialog
        self._histoinfo_headvars = OrderedDict()
        self._histoinfo_headvars[_PGGL(u"Period")] = "PGGL_period"
        self._histoinfo_headvars[_PGGL(u"Local\naccount\n(your group)")] = \
            "PGGL_local_sousgroupe"
        self._histoinfo_headvars[_PGGL(u"Global\naccount\n(your group)")] = \
            "PGGL_global_sousgroupe"
        self._histoinfo_headvars[
            _PGGL(u"Global\naccount\n(the other\ngroup)")] = \
            "PGGL_global_autresousgroupe"
        self._histoinfo_headvars[_PGGL(u"Global\naccount\n(both\ngroups)")] = \
            "PGGL_global_total"

        self._histo = [self._histo_headvars.keys()]
        self._histoinfo = [self._histoinfo_headvars.keys()]
        self.periodes = {}
        self.currentperiod = None
        self._currentsequence = 0
        # variables for communication
        self._group_id = None
        self._group_othermembers = None  # to send message to group members
        self._subgroup_id = None
        self._subgroup_othermembers = None  # to send message to subgroup members
        self._othermembers = None  # becomes one of the above variable
        self._playerid = None  # used for communication treatments

    def set_othermembersandid(self, group_id, othermembers_group,
                              subgroup_id, othermembers_subgroup):
        self._group_id = group_id
        self._group_othermembers = othermembers_group
        self._subgroup_id = subgroup_id
        self._subgroup_othermembers = othermembers_subgroup

    @defer.inlineCallbacks
    def configure(self, sequence):
        """
        Configure les clients et les remotes
        :param sequence: le numéro de la séquence courante
        :return: rien
        """
        self._currentsequence = sequence
        if pms.COMMUNICATION == pms.COMMUNICATION_GLOBAL:
            self._othermembers = self._group_othermembers
            self._playerid = self._group_id
        elif pms.COMMUNICATION == pms.COMMUNICATION_LOCAL:
            self._othermembers = self._subgroup_othermembers
            self._playerid = self._subgroup_id

        yield (self.remote.callRemote(
            "configure",
            self, sequence, pms.TRAITEMENT, pms.COMMUNICATION,
            pms.COMMUNICATION_TEMPS))

    @defer.inlineCallbacks
    def newperiod(self, periode):
        """
        Configuration d'une nouvelle période.
        Informe le remote du numéro de la période courante
        :param periode:
        :return:
        """
        if periode == 1: 
            del self._histo[1:]
            del self._histoinfo[1:]

        self.currentperiod = RepetitionsPGGL()
        self.currentperiod.PGGL_sequence = self._currentsequence
        self.currentperiod.PGGL_period = periode
        self.currentperiod.PGGL_group = self.joueur.groupe
        self.currentperiod.PGGL_groupid = self._group_id
        self.currentperiod.PGGL_subgroup = self.joueur.sousgroupe
        self.currentperiod.PGGL_subgroupid = self._subgroup_id
        self._le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)

        yield (self.remote.callRemote(
            "newperiod", self.currentperiod.PGGL_period))
        logger.info(u"Période {} -> Ok".format(periode))

    @defer.inlineCallbacks
    def display_communication(self):
        """
        Démarre une session de communication
        :return: lorsque la session de communication est terminée
        """
        yield (self.remote.callRemote("display_communication"))
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def remote_sendmessage(self, message):
        """
        Cette méthode est appelée par le remote
        Enregistre le message
        :param message:
        :return:
        """
        self.joueur.info(u"{}".format(
            message if len(message) < 20 else u"{} ...".format(message[:19])))
        msg = MessagesPGGL()
        msg.PGGL_sequence = self.currentperiod.PGGL_sequence
        msg.PGGL_group = self.currentperiod.PGGL_group
        msg.PGGL_subgroup = self.currentperiod.PGGL_subgroup
        msg.PGGL_period = self.currentperiod.PGGL_period
        msg.PGGL_message = message
        self.messages.append(msg)
        # send message to othermembers
        for m in self._othermembers:
            mess = u"Joueur {}: {}".format(self._playerid, message)
            yield (m.display_message(mess))
        yield (self.display_message, u"Vous: {}".format(message))

    @defer.inlineCallbacks
    def display_message(self, message):
        yield (self.remote.callRemote("display_message", message))

    @defer.inlineCallbacks
    def display_decision(self):
        """
        Affiche l'écran de décision sur les remotes, récupère les contributions
        dans chaque compte
        :return: void
        """
        debut = datetime.now()
        decisions = yield (self.remote.callRemote("display_decision"))
        fin = datetime.now()
        self.currentperiod.PGGL_decisiontime = (fin - debut).seconds
        self.currentperiod.PGGL_individuel = decisions["individuel"]
        self.currentperiod.PGGL_local = decisions["local"]
        self.currentperiod.PGGL_global = decisions["global"]
        self.joueur.info(u"{}".format(decisions))
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def display_information(self):
        """
        Affiche l'écran d'information sur les remote
        Si traitement avec désapprobation récupère les points affectés
        :return:
        """
        texte_info = texts.get_information(self.currentperiod)
        del self._histoinfo[1:]
        self._histoinfo.append(
            [getattr(self.currentperiod, e) for e in
             self._histoinfo_headvars.values()])
        logger.debug(u"texte_info: {}\nhisto_info: {}".format(
            texte_info, self._histoinfo[-1]))
        desapprobation = yield (self.remote.callRemote(
            "display_information", texte_info, self._histoinfo))
        if pms.TRAITEMENT == pms.CARTONS_LOCAL or \
            pms.TRAITEMENT == pms.CARTONS_LOCAL_AUTRE or \
            pms.TRAITEMENT == pms.CARTONS_LOCAL_GLOBAL or \
            pms.TRAITEMENT == pms.CARTONS_GLOBAL:
            self.currentperiod.PGGL_desapprobation = desapprobation
        self.joueur.info(desapprobation)
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        """
        Calcul le gain de la période, à savoir: gain cpte indiv + gain cpte
        local + gain cpte global.
        :return:
        """
        logger.debug(u"{} - compute_periodpayoff".format(self.joueur))

        cpte_indiv = self.currentperiod.PGGL_individuel
        self.currentperiod.PGGL_local_gain = \
            float(self.currentperiod.PGGL_local_sousgroupe) * \
            float(pms.FACTEUR_COMPTE_LOCAL)
        self.currentperiod.PGGL_global_gain = \
            float(self.currentperiod.PGGL_global_total) * \
            float(pms.FACTEUR_COMPTE_GLOBAL)
        self.currentperiod.PGGL_periodpayoff = \
            cpte_indiv + self.currentperiod.PGGL_local_gain + \
            self.currentperiod.PGGL_global_gain

        if self.currentperiod.PGGL_period == 1:
            self.currentperiod.PGGL_cumulativepayoff = \
                self.currentperiod.PGGL_periodpayoff
        else: 
            previousperiod = self.periodes[self.currentperiod.PGGL_period - 1]
            self.currentperiod.PGGL_cumulativepayoff = \
                previousperiod.PGGL_cumulativepayoff + \
                self.currentperiod.PGGL_periodpayoff
        self.periodes[self.currentperiod.PGGL_period] = \
            self.currentperiod

    @defer.inlineCallbacks
    def display_summary(self):
        """
        Affiche l'écran récapitulatif sur les remotes
        :return:
        """
        logger.debug(u"{} - display_summary".format(self.joueur))
        self._texte_recapitulatif = texts.get_recapitulatif(self.currentperiod)
        logger.debug(u"Recapitulatif {}: {}".format(
            self.joueur, self._texte_recapitulatif))
        self._histo.append(
            [getattr(self.currentperiod, e) for e in
             self._histo_headvars.values()])
        yield(self.remote.callRemote(
            "display_summary", self._texte_recapitulatif, self._histo))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()
    
    def compute_partpayoff(self):
        """
        Le gain de la partie correspond au gain cumulé de chacune des séquences
        jouées
        :return:
        """
        logger.debug(u"Calcul du gain de la partie")
        self.PGGL_gain_ecus += self.currentperiod.PGGL_cumulativepayoff
        self.PGGL_gain_euros += float("{:.2f}".format(
            float(self.PGGL_gain_ecus) * float(pms.TAUX_CONVERSION)))
        self._texte_final = texts.get_texte_final(
            self.PGGL_gain_ecus, self.PGGL_gain_euros)
        logger.debug(u"Texte final {}: {}".format(
            self.joueur, self._texte_final))
        logger.info(u'{}: gain ecus:{}, gain euros: {:.2f}'.format(
            self.joueur, self.PGGL_gain_ecus, self.PGGL_gain_euros))


class RepetitionsPGGL(Base):
    """
    Champs de la table du jeu répété.
    Ces champs sont les variables des données créées
    """
    __tablename__ = 'partie_PublicGoodGlobalLocal_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_PublicGoodGlobalLocal.partie_id"))
    PGGL_sequence = Column(Integer)
    PGGL_period = Column(Integer)
    PGGL_treatment = Column(Integer)
    PGGL_group = Column(Integer)
    PGGL_groupid = Column(String)  # id du joueur ds le grpe
    PGGL_subgroup = Column(Integer)
    PGGL_subgroupid = Column(String)  # id du joueur ds le sg
    PGGL_individuel = Column(Integer)
    PGGL_local = Column(Integer)
    PGGL_global = Column(Integer)
    PGGL_decisiontime = Column(Integer)
    PGGL_local_sousgroupe = Column(Integer)
    PGGL_local_autresousgroupe = Column(Integer)
    PGGL_local_total = Column(Integer)
    PGGL_global_sousgroupe = Column(Integer)
    PGGL_global_autresousgroupe = Column(Integer)
    PGGL_global_total = Column(Integer)
    PGGL_desapprobation = Column(Integer)
    PGGL_local_gain = Column(Float)
    PGGL_global_gain = Column(Float)
    PGGL_periodpayoff = Column(Float)
    PGGL_cumulativepayoff = Column(Float)

    def __init__(self):
        self.PGGL_treatment = pms.TRAITEMENT
        self.PGGL_temps_decision = 0
        self.PGGL_periodpayoff = 0
        self.PGGL_cumulativepayoff = 0

    def todict(self, joueur):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        temp["joueur"] = joueur
        return temp


class MessagesPGGL(Base):
    __tablename__ = 'partie_PublicGoodGlobalLocal_messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer, ForeignKey("partie_PublicGoodGlobalLocal.partie_id"))
    PGGL_sequence = Column(Integer)
    PGGL_period = Column(Integer)
    PGGL_group = Column(Integer)
    PGGL_subgroup = Column(Integer)
    PGGL_message = Column(String)
    PGGL_messagetime = Column(DateTime)

    def __init__(self):
        self.PGGL_messagetime = datetime.now()
