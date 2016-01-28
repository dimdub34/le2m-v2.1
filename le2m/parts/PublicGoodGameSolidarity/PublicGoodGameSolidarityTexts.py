# -*- coding: utf-8 -*-
"""
Ce module contient les textes des écrans
"""
__author__ = "Dimitri DUBOIS"

import os
import configuration.configparam as params
from collections import namedtuple
from util.utiltools import get_pluriel
import PublicGoodGameSolidarityParams as pms
import gettext

localedir = os.path.join(params.getp("PARTSDIR"), "PublicGoodGame", "locale")
_PGGS = gettext.translation(
    "PublicGoodGame", localedir, languages=[params.getp("LANG")]).ugettext

TITLE_MSG = namedtuple("TITLE_MSG", "titre message")

# ECRAN DECISION ===============================================================
DECISION_titre = _PGGS(u"Decision")
DECISION_explication = _PGGS(u"You have an endowment of {} tokens. Please "
                             u"choose how much token(s) you want to put "
                             u"in the public account.").format(pms.DOTATION)
DECISION_label = _PGGS(u"How much token(s) do you want to put in the public "
                       u"account?")
DECISION_erreur = TITLE_MSG(
    u"Warning",
    _PGGS(u"Warning message"))
DECISION_confirmation = TITLE_MSG(
    u"Confirmation",
    _PGGS(u"Do you confirm your choice?"))


# ECRAN RECAPITULATIF ==========================================================
def get_recapitulatif(currentperiod):
    txt = _PGGS(u"You put {} in your individual account and {} in the public "
                u"account. Your group put {} in the public account.\n"
                u"Your payoff for the current period is equal to {}.").format(
        get_pluriel(currentperiod.PGGS_indiv, _PGGS(u"token")),
        get_pluriel(currentperiod.PGGS_public, _PGGS(u"token")),
        get_pluriel(currentperiod.PGGS_publicgroup, _PGGS(u"token")),
        get_pluriel(currentperiod.PGGS_periodpayoff, pms.MONNAIE))
    return txt


# TEXTE FINAL PARTIE ===========================================================
def get_texte_final(gain_ecus, gain_euros):
    txt = _PGGS(u"You've won {}, which corresponds to {}.").format(
        get_pluriel(gain_ecus, pms.MONNAIE),
        get_pluriel(gain_euros, params.getp("CURRENCY")))
    return txt


VOTE_explication = u"Votre groupe n'a pas été sinistré. Vous devez voter " \
                   u"\"pour\" ou \"contre\" l'intégration d'un groupe sinistré."


def get_resultvote(sinistre, votespour, majorite):
    txt = u"{} a voté pour ou " \
          u"contre l'intégration {}. Le résultat du vote " \
          u"est le suivant: {} \"Pour\" et {} \"Contre\". " \
          u"La majorité est donc \"{}\".".format(
            u"Le groupe auquel votre groupe est associé" if sinistre else
            u"Votre groupe", u"de votre groupe" if sinistre else
            u"du groupe auquel votre groupe est associé", votespour,
            pms.TAILLE_GROUPES - votespour,
            u"Pour" if majorite == pms.get_votes("pour") else u"Contre")
    return txt
