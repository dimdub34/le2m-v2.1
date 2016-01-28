# -*- coding: utf-8 -*-
"""
Ce module contient les variables et les paramètres de la partie
Les variables ne doivent pas être changées
Les paramètres peuvent être changés, mais, par sécurité, demander au développeur
"""
from util.utiltools import get_dictinfos

# variables
_treatments = {0: "baseline", 1: "without_solidarity", 2: "solidarity_auto",
               3: "solidarity_vote"}
_votes = {0: "Pour", 1: "Contre"}


def get_treatments(which=None):
    return get_dictinfos(_treatments, which)


def get_votes(which=None):
    return get_dictinfos(_votes, which)

# paramètres
DOTATION = 20
MPCR = 0.4
MPCR_ens = 0.2
TRAITEMENT = get_treatments("baseline")
TAUX_CONVERSION = 0.04
NOMBRE_PERIODES = 10
TAILLE_GROUPES = 5
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"ecu"

# DECISION
DECISION_MIN = 0
DECISION_MAX = DOTATION
DECISION_STEP = 1

