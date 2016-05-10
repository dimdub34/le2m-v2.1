# -*- coding: utf-8 -*-

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from util.utili18n import le2mtrans
from server.servbase import Base, DB


logger = logging.getLogger("le2m")


class GestionnaireBase():
    """
    Classe qui gère la base de données.
    Cette classe ne doit etre instanciée qu'une fois.
    """
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv
        self._heure_debut = self._le2mserv.heure_debut
        self._nom_session = self._le2mserv.nom_session
        self._db = None
        self._session = None
        self._compteur_joueurs = 0
        self._playerstoadd = []
    
    def creer_base(self, dossier, nom_fichier, istest):
        """
        Create the database.
        The database is named data.sqlite and is located in the directory that 
        starts the software.
        """
        fichier = "{}".format(os.path.join(dossier, nom_fichier))
        logger.info("database path: {}".format(fichier))
        engine = create_engine("sqlite:///{}".format(fichier), echo=True)
        DB.configure(bind=engine)
        self._db = DB()
        Base.metadata.create_all(engine)
        logger.info(le2mtrans("database created"))

        # add the session to the database
        self._session = Session(self._nom_session, self._heure_debut, istest)
        self.ajouter(self._session)
        logger.info(le2mtrans(u"Session {s} added to the database").format(
            s=self._nom_session))

        # add the connected players to the database
        for j in self._playerstoadd:
            logger.info(le2mtrans(u"Player {p} added to the "
                                  u"session").format(p=j))
            self.ajouter(j)
            self._session.joueurs.append(j)
        del self._playerstoadd[:]

        self.enregistrer()
    
    def is_created(self):
        return self._db is not None
    
    def add_player(self, player):
        try:
            self.ajouter(player)
            self._session.joueurs.append(player)
            self.enregistrer()
            logger.info(le2mtrans(u"Player {p} added to the database").format(
                p=player))
        except AttributeError:
            self._playerstoadd.append(player)

    def enregistrer(self):
        try:
            self._db.commit()
        except AttributeError:
            pass  # when the database is not yet created
        
    def ajouter(self, contenu):
        self._db.add(contenu)
        
    def fermer_base(self, heure):
        try: 
            self._session.fin = heure
            self.enregistrer()
            self._db.close()        
        except AttributeError as e:  # si pas de session lancée
            logger.warning("{}".format(e.message))
            
    def get_session(self):
        return self._session
                

class Session (Base):
    __tablename__ = "sessions"
    id = Column(Integer,  autoincrement=True,  primary_key=True)
    nom = Column(String(50))
    debut = Column(String(20))
    fin = Column(String(20))
    isTest = Column(Integer)
    parametres = Column(String)
    commentaires = Column(String)
    joueurs = relationship('Joueur')
    
    def __init__(self, nom, debut, istest=True):
        self.nom = nom
        self.debut = debut
        self.isTest = istest
        
    def is_test(self): 
        return self.isTest
    
    def set_test(self, valeur): 
        self.isTest = valeur
    

