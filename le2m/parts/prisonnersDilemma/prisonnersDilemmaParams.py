# -*- coding: utf-8 -*-
"""
Ce module contient les variables et les paramètres de la partie
Les variables ne doivent pas être changées
Les paramètres peuvent être changés, mais, par sécurité, demander au développeur
"""

# variables
TREATMENTS = {0: "baseline"}
OPTIONS = {0: u"X", 1: u"Y"}

# paramètres
TREATMENT = 0
TAUX_CONVERSION = 0.02
NOMBRE_PERIODES = 10
TAILLE_GROUPES = 2
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"ecu"
XX = 75
XY = 25
YX = 100
YY = 50


def get_treatment(code_or_name):
    if type(code_or_name) is int:
        return TREATMENTS.get(code_or_name, None)
    elif type(code_or_name) is str:
        for k, v in TREATMENTS.viewitems():
            if v.lower() == code_or_name.lower():
                return k
    return None


def get_option(code_or_name):
    if type(code_or_name) is int:
        return OPTIONS.get(code_or_name, None)
    elif type(code_or_name) is str:
        for k, v in OPTIONS.viewitems():
            if v.lower() == code_or_name.lower():
                return k
    return None
