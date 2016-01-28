# -*- coding: utf-8 -*-
"""
Ce module contient les variables et les paramètres de la partie
Les variables ne doivent pas être changées
Les paramètres peuvent être changés, mais, par sécurité, demander au développeur
"""

import os
from configuration import configparam

# variables
BASELINE = 0
ICONES = 1

# paramètres
DOTATION = 20
MPCR = 0.5
TRAITEMENT = BASELINE
TAUX_CONVERSION = 0.04
NOMBRE_PERIODES = 10
TAILLE_GROUPES = 4
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"ecu"

# DECISION
DECISION_MIN = 0
DECISION_MAX = DOTATION
DECISION_STEP = 1
NB_HOMMES = 0
# type groupe = nombre d'hommes dans le groupe
GROUPES = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}


_treatments = {0: "BASELINE", 1: "ICONES"}
_imgdir = os.path.join(
    configparam.getp("PARTSDIR"), "PublicGoodGameGender",
    "PublicGoodGameGenderImg")
_imgh = os.path.join(_imgdir, "homme.jpg")
_imgf = os.path.join(_imgdir, "femme.jpg")


def get_treatments(which=None):
    return _treatments.get(which) or _treatments.copy()


def get_icone(which="H"):
    if which == "H":
        return _imgh
    else:
        return _imgf