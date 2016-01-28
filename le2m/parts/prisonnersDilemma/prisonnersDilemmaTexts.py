# -*- coding: utf-8 -*-
"""
Ce module contient les textes des écrans
"""

from collections import namedtuple
from util.utiltools import get_pluriel
import prisonnersDilemmaParams as pms
import os
import configuration.configparam as params
import gettext
localedir = os.path.join(params.getp("PARTSDIR"), "prisonnersDilemma", "locale")
_DP = gettext.translation("prisonnersDilemma", localedir,
                          languages=[params.getp("LANG")]).ugettext


TITLE_MSG = namedtuple("TITLE_MSG", "titre message")


# ECRAN DECISION ===============================================================
DECISION_titre = _DP(u"Decision")
DECISION_explication = _DP(u"Choose option X or option Y")
DECISION_erreur = TITLE_MSG(
    _DP(u"Warning"),
    _DP(u"You have to choose between option X and option Y"))
DECISION_confirmation = TITLE_MSG(
    _DP(u"Confirmation"),
    _DP(u"Do you confirm your choice?"))


# ECRAN RECAPITULATIF ==========================================================
def get_recapitulatif(currentperiod):
    txt = _DP(u"You chose {} and the other player chose {}.").format(
        u"X" if currentperiod.DP_decision == pms.OPTION_X else u"Y",
        u"X" if currentperiod.DP_decisionother == pms.OPTION_X else u"Y")
    txt += u" " + _DP(u"Your payoff is {}.").format(
        get_pluriel(currentperiod.DP_periodpayoff, pms.MONNAIE))
    return txt


# TEXTE FINAL PARTIE ===========================================================
def get_texte_final(gain_ecus, gain_euros):
    txt = _DP(u"You've won {}, which is equal to {}.").format(
        get_pluriel(gain_ecus, u"ecu"), get_pluriel(gain_euros, u"euro"))
    return txt
