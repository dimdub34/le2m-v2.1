# -*- coding: utf-8 -*-
"""
Ce module contient les textes des écrans
"""

import os
import configuration.configparam as params
from configuration.configconst import PILE
from collections import namedtuple
from util.utiltools import get_pluriel
import GneezyPotterParams as pms
import gettext


localedir = os.path.join(params.getp("PARTSDIR"), "GneezyPotter", "locale")
_GP = gettext.translation(
    "GneezyPotter", localedir, languages=[params.getp("LANG")]).ugettext

TITLE_MSG = namedtuple("TITLE_MSG", "titre message")


# ECRAN DECISION ===============================================================
DECISION_titre = _GP(u"Decision")
DECISION_explication = \
    _GP(u"You have an endowment of {}. You can invest amount you want in the "
        u"risky option").format(get_pluriel(pms.DOTATION, pms.MONNAIE))
DECISION_label = _GP(u"Choose the amount you want to invest in the risky "
                     u"option")
DECISION_erreur = TITLE_MSG(
    _GP(u"Warning"),
    _GP(u"Warning message"))
DECISION_confirmation = TITLE_MSG(
    _GP(u"Confirmation"),
    _GP(u"Do you confirm you choice?"))


# ECRAN RECAPITULATIF ==========================================================
def get_recapitulatif(currentperiod):
    txt = _GP(u"You invested {} in the risky option.").format(
        get_pluriel(currentperiod.GP_decision, pms.MONNAIE))
    txt += u" " + _GP(u"The random draw was {}.").format(
        _GP(u"Head") if currentperiod.GP_randomdraw == PILE else _GP(u"Tail"))
    txt += u" " + _GP(u"Your payoff is equal to {}.").format(
        get_pluriel(currentperiod.GP_periodpayoff, pms.MONNAIE))
    return txt


# TEXTE FINAL PARTIE ===========================================================
def get_texte_final(currentperiod):
    return get_recapitulatif(currentperiod)
