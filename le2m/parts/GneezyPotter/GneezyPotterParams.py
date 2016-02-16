# -*- coding: utf-8 -*-

# variables: do not change the values
TREATMENTS = {0: "baseline"}

# Parameters: you can change some values but please contact the developer
TREATMENT = 0
PROBA = 0.5  # proba pile
DOTATION = 10
FACTEUR_PILE = 0
FACTEUR_FACE = 3
NOMBRE_PERIODES = 0
TAILLE_GROUPES = 0
GROUPES_CHAQUE_PERIODE = False
TAUX_CONVERSION = 1
MONNAIE = u"euro"
DISPLAY_SUMMARY = False  # if True the summary is displayed, else not

# DECISION
DECISION_MIN = 0
DECISION_MAX = DOTATION
DECISION_STEP = 1


def get_treatment(code_or_name):
    if type(code_or_name) is int:
        return TREATMENTS.get(code_or_name, None)
    elif type(code_or_name) is str:
        for k, v in TREATMENTS.viewitems():
            if v.lower() == code_or_name.lower():
                return k
    return None
