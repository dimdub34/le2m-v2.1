# -*- coding: utf-8 -*-
"""
Ce module contient les variables et les paramètres de la partie
Les variables ne doivent pas être changées
Les paramètres peuvent être changés, mais, par sécurité, demander au développeur
"""

# variables
BASELINE = 0
POUR = 0
CONTRE = 1
RADIOS = (u"Pour", u"Contre")

# paramètres
PROFILS = {
    "A": (8, 8, 8, 8),
    "B": (2, 8, 8, 8),
    "C": (8, 2, 8, 2),
    "D": (8, 8, 8, 2),
    "E": (2, 2, 8, 8),
    "F": (8, 8, 2, 2),
    "G": (8, 2, 8, 2),
    "H": (2, 8, 8, 2),
    "I": (2, 8, 2, 8),
    "J": (8, 2, 2, 8)
}
PROFILS_APPLIQUES = None  # set by the experimenter (configure menu)
COUT = 5
DOTATION = 14
TREATMENT = BASELINE
TAUX_CONVERSION = 0.5
NOMBRE_PERIODES = 4
TAILLE_GROUPES = 4
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"ecu"

