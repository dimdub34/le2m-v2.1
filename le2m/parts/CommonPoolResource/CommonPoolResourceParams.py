# -*- coding: utf-8 -*-

# variables
TREATMENTS = {0: "baseline"}

# parameters
TREATMENT = 0
DOTATION = 10
TAUX_CONVERSION = 0.05
NOMBRE_PERIODES = 10
TAILLE_GROUPES = 4
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"ecu"

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


def get_gain(extraction_indiv, extraction_grpe):
    """
    :param extraction_indiv: player's extraction
    :param extraction_grpe: group's extraction
    :return: float
    """
    const = 120 / TAILLE_GROUPES
    indiv = 3 * extraction_indiv
    grpe = - (0.075 / TAILLE_GROUPES) * pow(extraction_grpe, 2)
    return float("{:.2f}".format(const + indiv + grpe))
