# -*- coding: utf-8 -*-
"""
Ce module contient les textes des écrans
"""
__author__ = "Dimitri DUBOIS"

import os
import configuration.configparam as params
from collections import namedtuple
from util.utiltools import get_pluriel
import PublicGoodGameGenderParams as pms
import gettext


localedir = os.path.join(params.getp("PARTSDIR"), "PublicGoodGame", "locale")
_PGGG = gettext.translation(
    "PublicGoodGame", localedir, languages=[params.getp("LANG")]).ugettext


TITLE_MSG = namedtuple("TITLE_MSG", "titre message")


# ECRAN DECISION ===============================================================
DECISION_titre = _PGGG(u"Decision")
DECISION_explication = _PGGG(u"You have an endowment of {} tokens. Please "
                             u"choose how much token(s) you want to put "
                             u"in the public account.").format(pms.DOTATION)
DECISION_label = _PGGG(u"How much token(s) do you want to put in the public "
                      u"account?")
DECISION_erreur = TITLE_MSG(
    u"Warning",
    _PGGG(u"Warning message"))
DECISION_confirmation = TITLE_MSG(
    u"Confirmation",
    _PGGG(u"Do you confirm your choice?"))


# ECRAN RECAPITULATIF ==========================================================
def get_recapitulatif(currentperiod):
    txt = _PGGG(u"You put {} in your individual account and {} in the public "
                u"account. Your group put {} in the public account.\n"
                u"Your payoff for the current period is equal to {}.").format(
        get_pluriel(currentperiod.PGGG_indiv, _PGGG(u"token")),
        get_pluriel(currentperiod.PGGG_public, _PGGG(u"token")),
        get_pluriel(currentperiod.PGGG_publicgroup, _PGGG(u"token")),
        get_pluriel(currentperiod.PGGG_periodpayoff, pms.MONNAIE))
    return txt


# TEXTE FINAL PARTIE ===========================================================
def get_texte_final(gain_ecus, gain_euros):
    txt = _PGGG(u"You've won {}, which corresponds to {}.").format(
        get_pluriel(gain_ecus, pms.MONNAIE),
        get_pluriel(gain_euros, params.getp("CURRENCY")))
    return txt