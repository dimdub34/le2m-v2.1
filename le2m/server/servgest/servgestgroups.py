# -*- coding: utf-8 -*-

import logging
from util import utiltools
import random
import datetime
from util.utili18n import le2mtrans


logger = logging.getLogger("le2m.{}".format(__name__))
compteur_groupe = 0


def former_groupes(population, taille, prefixeid=None):
    """
    Forme des groupes
    :param population: une liste d'identifiants
    :param taille: la taille des groupes à former
    :param prefixeid: le préfixe d'identifiant de groupe. Par défaut la
    date du jour avec l'heure, selon format %Y%m%d%H%m
    :return: dict
    """
    if type(population) is not list:
        raise ValueError(u"population doit être une liste")
    elif len(population) % taille > 0:
        raise ValueError(u"il faut pouvoir former un nombre entier de groupes")

    nb = len(population) / taille
    dispos = population[:]
    pre_id = prefixeid or datetime.datetime.now().strftime("%Y%m%d%H%M")
    groupes = dict()
    global compteur_groupe

    for i in range(nb):
        g_id = pre_id + str(compteur_groupe)
        groupes[g_id] = []
        for j in range(taille):
            selec = random.choice(dispos)
            groupes[g_id].append(selec)
            dispos.remove(selec)
        compteur_groupe += 1

    return groupes


class RoundRobin(object):
    """
    This class forms groups in which for every member the other
    group members are differents form previous rounds
    Can form (population_size / groupsize) -1 differents groups. After that
    there is a cycle, where groups are the same as in the first round and so on
    """
    def __init__(self, population, taille, prefixe=None):
        if type(population) is not list:
            raise ValueError(u"population type must be a list")
        elif len(population) % taille > 0:
            raise ValueError(u"population % taille greater than zero")

        self._population = population
        self._taille = taille
        self._prefixe = prefixe or datetime.datetime.now().strftime("%Y%m%d%H%M")
        group_pool = former_groupes(
            self._population, len(self._population) / self._taille)
        group_pool = list(group_pool.viewvalues())
        self._group_pool_cycle = [utiltools.cyclelist(g, c) for c, g in
                                  enumerate(group_pool)]

    def next(self):
        global compteur_groupe
        group_pool = [g.next() for g in self._group_pool_cycle]
        group_temp = zip(*group_pool[0:self._taille])
        groups = {}
        for g in group_temp:
            groups["{}{}".format(self._prefixe, compteur_groupe)] = list(g)
            compteur_groupe += 1
        return groups


class GestionnaireGroupes(object):
    """
    Classe qui gère les groupes.
    Les groupes sont formés de manière aléatoire.
    Chaque groupe a un identifiant unique du type nom_session_numero.
    Les groupes sont stockés dans un dictionnaire, qui est vidé à chaque fois 
    que les groupes sont reformés.
    Cette classe ne doit etre instanciée qu'une fois.
    """
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv
        self._nom_session = self._le2mserv.nom_session
        self._groupes = dict()
        self._sousgroupes = dict()
        self._roundrobin = None

    @property
    def groupes(self):
        return self._groupes

    @property
    def sousgroupes(self):
        return self._sousgroupes

    @property
    def nom_session(self):
        return self._nom_session

    def former_groupes(self, liste_joueurs, taille_groupes, roundrobin=False,
                       forcer_nouveaux=True, **kwargs):
        """
        Forme des groupes et les stocke dans un dictionnaire.
        Utilise la fonction former_groupes de le2mUtile.utiltools
        :param liste_joueurs:
        :param taille_groupes:
        :param forcer_nouveaux
        :param roundrobin: whether or not to apply round robin tournament
        :param kwargs: pour pouvoir améliorer cette fonction
        :return: None
        """
        # checks
        if self._groupes and not forcer_nouveaux:
            self._le2mserv.gestionnaire_graphique.infoserv(
                self.get_groupes_string())
            return

        if roundrobin:  # each round all other members are new for each member
            self._roundrobin = RoundRobin(
                population=liste_joueurs, taille=taille_groupes,
                prefixe="{}_g_".format(self._nom_session))
            self._groupes = self._roundrobin.next()
        else:  # normal (random) groups
            self._groupes = former_groupes(
                liste_joueurs, taille_groupes, "{}_g_".format(self._nom_session))

        # add groupe attribute to players
        self.set_attributes()

        # display groups on the server list
        self._le2mserv.gestionnaire_graphique.infoserv(
            self.get_groupes_string())

    def set_attributes(self):
        for g, m in self._groupes.viewitems():
            for j in m:
                setattr(j, "groupe", g)

    def get_groupes(self, nom_partie=None):
        """
        Par défaut renvoi une copie du dictionnaire qui stocke les groupes
        Si nom_partie est donné renvoie directement les joueurs des parties
        :param nom_partie
        :return dict
        """
        if nom_partie:
            groupes_parties = {}
            for k, v in self._groupes.viewitems():
                groupes_parties[k] = [j.get_part(nom_partie) for j in v]
            return groupes_parties
        else:
            return self._groupes.copy()

    def set_groupes(self, groupes):
        self._groupes = groupes

    def roundrobinnext(self):
        """
        Do a new round of round robin tournament
        :return:
        """
        if not self._roundrobin:
            raise AttributeError(u"Round Robin must be instanciated!")
        self._groupes = self._roundrobin.next()
        self.set_attributes()
        self._le2mserv.gestionnaire_graphique.infoserv(
            self.get_groupes_string())
 
    def get_composition_groupe(self, groupe):
        """
        Renvoi une liste avec les membres du groupe
        :param groupe: l'identifiant de groupe
        :return: list
        """
        return self.get_groupes().get(groupe)[:]

    def get_composition_groupe_du_joueur(self, joueur):
        """
        Renvoie la liste des membres du groupe du joueur
        :param joueur:
        :return:list
        """
        return self.get_composition_groupe(self.get_groupe(joueur))
    
    def get_groupe(self, joueur):
        """
        Renvoi l'identifiant du groupe du joueur
        :param joueur:
        :return: string
        """
        for k, v in self._groupes.viewitems():
            if joueur in v:
                return k
        return None

    def get_groupe2(self, joueur, partie=None):
        """
        Renvoi un tuple avec l'identifiant du groupe et sa composition.
        Si partie est donné alors renvoi directement les parties correspondantes
        dans la composition du groupe
        :param joueur:
        :param partie:
        :return: un tuple
        """
        for g, m in self._groupes.viewitems():
            if joueur in m:
                if partie:
                    return g, [j.get_part(partie) for j in m]
                else:
                    return g, m[:]
        return None, None

    def get_place_joueur_dans_groupe(self, joueur):
        """
        Renvoi la place du joueur dans le groupe
        :param joueur:
        :return: int
        """
        return self.get_composition_groupe_du_joueur(joueur).index(joueur)

    def get_autres_membres_groupe(self, joueur):
        """
        Renvoi la liste des autres membres du groupe du joueur
        :param joueur:
        :return: list
        """
        g_comp = self.get_composition_groupe_du_joueur(joueur)[:]
        g_comp.remove(joueur)
        return g_comp
        
    def get_groupes_string(self):
        """
        Return a string representation of the groups.
        """
        if self._groupes:
            texte = le2mtrans("Groups\n")
            cles = self._groupes.keys()
            cles.sort()
            for g in cles:
                texte += "-- G{} --:\n{}\n".format(
                    g.split("_")[2],
                    "\n".join(map(str, self.get_composition_groupe(g))))
            return texte[:-1]
        else: 
            return "No groups"
    
    def get_nombre_groupes(self):
        return len(self._groupes)

    def get_taille_groupes(self):
        if not self._groupes:
            return 0
        return len(self._groupes.keys()[0])

    def get_identifiant_dansgroupe(self, joueur):
        """
        Renvoi l'identifiant du joueur dans le groupe.
        Une lettre qui dépend de la place du joueur dans le groupe.
        Ex: place 0 => A, place 1 => B etc.
        :param joueur:
        :return: une lettre
        """
        return utiltools.get_letter(
            self.get_place_joueur_dans_groupe(joueur))

    def get_identifiantrelatif_dansgroupe(self, joueur, autrejoueur):
        """
        Permet d'attribuer à chaque membre du groupe un identifiant sans que
        les sujets puissent s'identifier à l'issue de l'expérience.
        En effet le demandeur (ici joueur) est toujours le joueur A et les
        autres membres de son groupe sont B, C, D ...
        Rmq: si joueur == autrejoueur renvoie A
        :param joueur: le joueur qui fait la demande
        :param autrejoueur: le membre du groupe dont le joueur veut connaître
        l'identifiant, en fonction de la place du joueur et de la place de ce
        membre dans le groupe.
        :return: string
        """
        place_joueur = self.get_place_joueur_dans_groupe(joueur)
        place_autrejoueur = self.get_place_joueur_dans_groupe(autrejoueur)
        if place_autrejoueur >= place_joueur:
            return utiltools.get_letter(place_autrejoueur - place_joueur)
        else:
            _, g_com = self.get_groupe2(joueur)
            taille_groupe = len(g_com)
            return utiltools.get_letter(
                taille_groupe - place_joueur + place_autrejoueur)

    def former_sousgroupes(self, taille, **kwargs):
        """
        Forme des sous-groupes dans chaque groupe
        :param taille:
        :param kwargs: pour améliorations de la fonction
        :return:
        """
        # vérifications ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if not self._groupes:
            raise ValueError(u"Aucun groupe formé")
        forcer_nouveaux = kwargs.get("forcer_nouveaux")
        if self._sousgroupes and not forcer_nouveaux:
            self._le2mserv.gestionnaire_graphique.infoserv(
                self.get_sousgroupes_tostring())
            return

        # formation des sous-groupes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._sousgroupes = dict()
        for g, m in self._groupes.viewitems():
            self._sousgroupes[g] = former_groupes(
                m, taille, "{}_sg_".format(self._nom_session))

        # ajout de l'attribut sous-groupe chez les joueurs ~~~~~~~~~~~~~~~~~~~~~
        for g, v in self._sousgroupes.viewitems():
            for sg, m in v.viewitems():
                for j in m:
                    setattr(j, "sousgroupe", sg)

        # affichage des sousgroupes sur la liste serveur ~~~~~~~~~~~~~~~~~~~~~~~
        self._le2mserv.gestionnaire_graphique.infoserv(
            self.get_sousgroupes_tostring())

    def get_sousgroupes(self, groupe):
        """
        Renvoi un dictionnaire avec comme clé l'identifiant du
        sous-groupe et comme valeur les membres de ce sous-groupe (objet joueur)
        :param groupe:
        :return: dict
        """
        return self._sousgroupes.get(groupe)

    def get_sousgroupes_tostring(self):
        """
        Création d'un texte avec les sous-groupes de chaque groupe
        :return:string
        """
        txt = le2mtrans(u"Sub-groups\n")
        for g in self._groupes.viewkeys():
            txt += u"--G{}--\n".format(g.split("_")[2])
            cles = self.get_sousgroupes(g).keys()
            cles.sort()
            for sg in cles:
                txt += u"--SG{}--:\n{}\n".format(
                    sg.split("_")[2],
                    "\n".join(map(str, self.get_composition_sousgroupe(sg))))
        return txt[:-1]  # on enlève le dernier \n

    def get_sousgroupe(self, joueur):
        """
        Renvoie l'identifiant du sous-groupe du joueur et la composition du
        sous-groupe
        :param joueur:
        :return: string, list
        """
        groupe = self.get_groupe(joueur)
        sousgroupes = self.get_sousgroupes(groupe)
        for k, v in sousgroupes.viewitems():
            if joueur in v:
                return k, v[:]
        return None, None

    def get_place_joueur_dans_sousgroupe(self, joueur):
        """
        Renvoi la place du joueur dans le sous-groupe. Utilisé pour affecter
        un identifiant dans le sous-groupe
        :param joueur:
        :return: int
        """
        _, comp = self.get_sousgroupe(joueur)
        return comp.index(joueur)

    def get_identifiant_danssousgroupe(self, joueur):
        """
        Renvoi la lettre qui correspond à la place du joueur dans son
        sous-groupe
        :param joueur:
        :return: string
        """
        return utiltools.get_letter(
            self.get_place_joueur_dans_sousgroupe(joueur))

    def get_identifiantrelatif_danssousgroupe(self, joueur, autrejoueur):
        """
        Permet d'attribuer à chaque membre du sous-groupe un identifiant sans
        que les sujets puissent s'identifier à l'issue de l'expérience.
        En effet le demandeur (ici joueur) est toujours le joueur A et les
        autres membres de son sous-groupe sont B, C, D ...
        Rmq: si joueur == autrejoueur renvoie A
        :param joueur: le joueur qui fait la demande
        :param autrejoueur: le membre du sous-groupe dont le joueur veut
        connaître l'identifiant, en fonction de la place du joueur et de la
        place de ce membre dans le groupe.
        :return: string
        """
        place_joueur = self.get_place_joueur_dans_sousgroupe(joueur)
        place_autrejoueur = self.get_place_joueur_dans_sousgroupe(autrejoueur)
        if place_autrejoueur >= place_joueur:
            return utiltools.get_letter(place_autrejoueur - place_joueur)
        else:
            _, g_com = self.get_groupe2(joueur)
            taille_groupe = len(g_com)
            return utiltools.get_letter(
                taille_groupe - place_joueur + place_autrejoueur)

    def get_composition_sousgroupe(self, sousgroupe):
        for k, v in self._sousgroupes.viewitems():
            for sg, membres in v.viewitems():
                if sg == sousgroupe:
                    return membres[:]
        return []

    def get_composition_sousgroupe_joueur(self, joueur):
        logger.debug("get_composition_sousgroupe_joueur ({})".format(joueur))
        _, comp = self.get_sousgroupe(joueur)
        logger.debug("get_composition_sousgroupe_joueur renvoi {}".format(comp))
        return comp

    def get_autres_membres_sousgroupe(self, joueur):
        logger.debug("get_autres_membres_sousgroupe ({})".format(joueur))
        sg_comp = self.get_composition_sousgroupe_joueur(joueur)
        sg_comp.remove(joueur)
        logger.debug("get_autres_membres_sousgroupe renvoi {}".format(
            sg_comp))
        return sg_comp