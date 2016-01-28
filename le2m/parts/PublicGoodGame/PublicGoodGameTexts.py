# -*- coding: utf-8 -*-
"""
Ce module contient les textes des écrans
"""
__author__ = "Dimitri DUBOIS"

import os
import configuration.configparam as params
from collections import namedtuple
from util.utiltools import get_pluriel
import PublicGoodGameParams as pms
import gettext


localedir = os.path.join(params.getp("PARTSDIR"), "PublicGoodGame", "locale")
_PGG = gettext.translation(
    "PublicGoodGame", localedir, languages=[params.getp("LANG")]).ugettext


TITLE_MSG = namedtuple("TITLE_MSG", "titre message")


# ECRAN DECISION ===============================================================
DECISION_titre = _PGG(u"Decision")
DECISION_explication = _PGG(u"You have an endowment of {} tokens. Please "
                            u"choose how much token(s) you want to put "
                            u"in the public account.").format(pms.DOTATION)
DECISION_label = _PGG(u"How much token(s) do you want to put in the public "
                      u"account?")
DECISION_erreur = TITLE_MSG(
    u"Warning",
    _PGG(u"Warning message"))
DECISION_confirmation = TITLE_MSG(
    u"Confirmation",
    _PGG(u"Do you confirm your choice?"))


# ECRAN RECAPITULATIF ==========================================================
def get_recapitulatif(currentperiod):
    txt = _PGG(u"You put {} in your individual account and {} in the public "
               u"account. Your group put {} in the public account.\n"
               u"Your payoff for the current period is equal to {}.").format(
        get_pluriel(currentperiod.PGG_indiv, _PGG(u"token")),
        get_pluriel(currentperiod.PGG_public, _PGG(u"token")),
        get_pluriel(currentperiod.PGG_publicgroup, _PGG(u"token")),
        get_pluriel(currentperiod.PGG_periodpayoff, pms.MONNAIE))
    return txt


# TEXTE FINAL PARTIE ===========================================================
def get_texte_final(gain_ecus, gain_euros):
    txt = _PGG(u"You've won {}, which corresponds to {}.").format(
        get_pluriel(gain_ecus, pms.MONNAIE),
        get_pluriel(gain_euros, params.getp("CURRENCY")))
    return txt