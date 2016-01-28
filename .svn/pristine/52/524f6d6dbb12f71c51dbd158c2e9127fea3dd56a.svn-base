# -*- coding: utf-8 -*-
"""
Ce module contient les variables et les paramètres de la partie
Les variables ne doivent pas être changées
Les paramètres peuvent être changés, mais, par sécurité, demander au développeur
"""

# variables
BASELINE = 0

# paramètres
TREATMENT = BASELINE
DOTATION = 10
TAUX_CONVERSION = 1
NOMBRE_PERIODES = 10
TAILLE_GROUPES = 4
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"ecu"

# DECISION
DECISION_MIN = 0
DECISION_MAX = DOTATION
DECISION_STEP = 1


def get_gain(extraction_indiv, extraction_grpe):
    """
    Renvoi le gain du joueur
    :param extraction_indiv: extraction du joueur
    :param extraction_grpe: extraction du groupe
    :return: float
    """
    const = 120 / TAILLE_GROUPES
    indiv = 3 * extraction_indiv
    grpe = - (0.075 / TAILLE_GROUPES) * pow(extraction_grpe, 2)
    return float("{:.2f}".format(const + indiv + grpe))
