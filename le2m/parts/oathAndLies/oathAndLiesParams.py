# -*- coding: utf-8 -*-
"""
Ce module contient les variables et les paramètres de la partie
Les variables ne doivent pas être changées
Les paramètres peuvent être changés, mais, par sécurité, demander au développeur
"""

# variables
BASELINE = 0
JOUEUR_A = 0
JOUEUR_B = 1
SANS_SERMENT = 0
AVEC_SERMENT = 1
OPTION_X = 0
OPTION_Y = 1
CODES_PERIODES = {1: [(20, 20), (15, 30)], 2: [(20, 20), (21, 15)],
                  3: [(20, 20), (30, 30)], 4: [(30, 30), (20, 20)]}


# paramètres
ORDRE_CODES_PERIODES = [1, 3, 2, 4]
TREATMENT = SANS_SERMENT
GAME = 1  # correspond à codes_periodes
TAUX_CONVERSION = 0.3
NOMBRE_PERIODES = 0
TAILLE_GROUPES = 2
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"ecu"

_treatmentscodes = {0: "SANS_SERMENT", 1: "AVEC_SERMENT"}


def get_treatment(code):
    return _treatmentscodes.get(code, None)