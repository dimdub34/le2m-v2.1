# -*- coding: utf-8 -*-

import logging

from twisted.internet import defer
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from util.utili18n import le2mtrans
from util.utiltools import get_pluriel
from servbase import Base
import configuration.configparam as params


logger = logging.getLogger("le2m")


class Partie(Base):
    """
    Every part, on the server side, will inherit from that object
    """
    __tablename__ = "parties"
    id = Column(Integer, autoincrement=True,  primary_key=True)
    nom = Column(String(50))
    __mapper_args__ = {'polymorphic_on': nom} 
    
    def __init__(self, nom, nom_court=None):
        self.nom = nom
        self._nom_court = nom_court or self.nom[:2].upper()
        self._remote = None
        self._currentperiod = None  # a repetition not a number
        self._periods = {}  # store the currentperiods

    @property
    def remote(self):
        return self._remote

    @remote.setter
    def remote(self, value):
        self._remote = value

    @property
    def nom_court(self):
        return self._nom_court

    @nom_court.setter
    def nom_court(self, value):
        self._nom_court = value

    @property
    def currentperiod(self):
        return self._currentperiod

    @currentperiod.setter
    def currentperiod(self, val):
        self._currentperiod = val

    @property
    def periods(self):
        return self._periods


class PartieBase(Partie, object):
    """
    This object is a table with some information about the player
    It is also called by the server to run several tasks on the remote
    """
    __tablename__ = 'partie_base'
    __mapper_args__ = {'polymorphic_identity': 'base'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)    
    simulation = Column(Integer)
    automatique = Column(Integer)
    fautesComprehension = Column(Integer)
    paiementFinal = Column(Float)
    commentaires = Column(String(1000))  # commentaires écrits par le sujet
    
    def __init__(self, joueur):
        super(PartieBase, self).__init__("base")
        self.joueur = joueur
        self.automatique = 0
        self.simulation = 0
        self.fautesComprehension = 0
        self.paiementFinal = 0

    @defer.inlineCallbacks
    def set_automatique(self, automatique):
        """
        Passe le remote en mode automatique ou manuel.
        En mode automatique, les écrans s'affichent et se remplissent seuls. 
        Permet de tester le programme avec les interfaces graphiques.
        """
        self.automatique = automatique
        auto = yield(self.remote.callRemote('set_automatique', automatique))
        logger.info('{} - automatique {}'.format(self.joueur, bool(auto)))

    @defer.inlineCallbacks
    def set_simulation(self, simulation):
        """
        Passe le remote en mode simulation ou non.
        En mode simulation les écrans ne s'affichent pas, le remote renvoie 
        directement des valeurs aléatoires. Permet de tester le programme 
        sans les interfaces graphiques.
        """
        self.simulation = simulation
        simul = yield(self.remote.callRemote('set_simulation', simulation))
        logger.info('{} - simulation {}'.format(self.joueur, bool(simul)))

    @defer.inlineCallbacks
    def display_welcome(self):
        """
        Affiche l'écran d'accueil sur le poste client
        """
        yield(self.remote.callRemote('display_welcome'))
        self.joueur.info('ok')
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def display_questcomp(self, questions):
        """
        On envoie les questions du questionnaire au fur et à mesure
        """
        questions_fautes = []
        for i, ques in enumerate(questions):
            logger.debug(ques)
            faute = yield(self.remote.callRemote(
                'display_questcomp', ques))
            if faute:
                questions_fautes.append(i+1)
        self.fautesComprehension = len(questions_fautes)
        self.joueur.info('{} - {}'.format(
            get_pluriel(self.fautesComprehension, le2mtrans(u"fault")),
            questions_fautes))
        txt = le2mtrans(u"You've done {faults}").format(
            faults=get_pluriel(self.fautesComprehension, le2mtrans(u"fault")))
        yield(self.remote.callRemote('display_information', txt))
        self.joueur.remove_waitmode()
        
    @defer.inlineCallbacks
    def display_finalscreen(self):
        """
        Display the final screen, with the final payoffs and the possibility
        for subjects to let a comment
        """
        self.commentaires = yield(
            self.remote.callRemote('display_finalscreen', self.paiementFinal))
        self.joueur.info(u'Ok')
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def display_payoffs(self, partname_or_dictOfParts):
        """
        Display a dialog box on remotes with their payoff for the part(s) and
        also an explanation (optional)
        """
        if type(partname_or_dictOfParts) is str:
            player_part = self.joueur.get_part(partname_or_dictOfParts)
            if player_part is not None:
                yield (player_part.remote.callRemote("display_payoffs"))
            else:
                logger.warning(u"{} ".format(partname_or_dictOfParts) +
                               le2mtrans(u"is not in the player list of parts"))
        elif type(partname_or_dictOfParts) is dict:
            yield (self.remote.callRemote(
                "display_payoffs", partname_or_dictOfParts))
        else:
            raise TypeError(le2mtrans(u"Either a str or a dict"))
        self.joueur.info(u'Ok')
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def display_information(self, texte):
        """
        Affiche une boite de dialogue d'information avec le texte
        passé en paramètres sur le poste client.
        :param texte:
        """
        yield(self.remote.callRemote("display_information", texte))
        self.joueur.info("ok")
        self.joueur.remove_waitmode()


class PartieQuestionnaireFinal(Partie, object):
    __tablename__ = 'partie_questionnaireFinal'
    __mapper_args__ = {'polymorphic_identity': 'questionnaireFinal'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)    
    
    naissance = Column(Integer)
    genre = Column(Integer) 
    nationalite = Column(Integer) 
    couple = Column(Integer) 
    etudiant = Column(Integer)
    etudiant_discipline = Column(Integer)
    etudiant_niveau = Column(Integer)
    experiences = Column(Integer) 
    fratrie_nombre = Column(Integer)
    fratrie_rang = Column(Integer)
    sportif = Column(Integer)
    sportif_type = Column(Integer)
    sportif_competition = Column(Integer)
    religion_place = Column(Integer)
    religion_croyance = Column(Integer)
    religion_nom = Column(Integer)

    def __init__(self, joueur):
        Partie.__init__(self, "questionnaireFinal")
        self.joueur = joueur
    
    @defer.inlineCallbacks
    def start(self):
        inputs = yield (self.remote.callRemote('demarrer'))
        for k, v in inputs.iteritems(): 
            setattr(self, k, v)
        self.joueur.info('ok')
        self.joueur.remove_waitmode()
