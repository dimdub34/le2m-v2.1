# -*- coding: utf-8 -*-
"""
Ce module contient les variables et les paramètres de la partie
Les variables ne doivent pas être changées
Les paramètres peuvent être changés, mais, par sécurité, demander au développeur
"""

# variables
BASELINE = 0
PLAYER_A = 0
PLAYER_B = 1
STANDARD = 0  # only players A take a decision
STRATEGY_METHOD = 1  # all players take a decision

# paramètres
DOTATION = 10
TRAITEMENT = BASELINE
GAME = STANDARD
TAUX_CONVERSION = 1
NOMBRE_PERIODES = 0
TAILLE_GROUPES = 2
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"euro"

# DECISION
DECISION_MIN = 0
DECISION_MAX = DOTATION
DECISION_STEP = 1

_game = {0: "STANDARD", 1: "STRATEGY_METHOD"}


def get_game(which=None):
    if which is not None:
        return _game.get(which, None)
    return _game.copy()

