# -*- coding: utf-8 -*-
"""
Ce module contient les textes des écrans
"""

import os
import configuration.configparam as params
from collections import namedtuple
from util.utiltools import get_pluriel
import CommonPoolResourceParams as pms
import gettext
from util.utili18n import le2mtrans


localedir = os.path.join(
    params.getp("PARTSDIR"), "CommonPoolResource", "locale")
trans_CPR = gettext.translation(
    "CommonPoolResource", localedir, languages=[params.getp("LANG")]).ugettext


TITLE_MSG = namedtuple("TITLE_MSG", "titre message")

# MULTI-ECRANS =================================================================
PERIODE_label = lambda periode: trans_CPR(u"Period {}").format(periode)

# ECRAN DECISION ===============================================================
DECISION_explication = \
    trans_CPR(u"You have two accounts: a private account and a public account. "
         u"The public account has {}. Each group member can extract a maximum "
         u"of {} from the public account to put on his/her private account. "
         u"The payoff of each member depends on the number of tokens he/she "
         u"has put on his/her private account as well as on the total number "
         u"of tokens extracted by the group from the public account.").format(
        get_pluriel(pms.DECISION_MAX * pms.TAILLE_GROUPES, trans_CPR(u"token")),
        get_pluriel(pms.DECISION_MAX, trans_CPR(u"token")))

DECISION_label = trans_CPR(u"Please choose how much you want to extract from the "
                      u"public account")

DECISION_titre = trans_CPR(u"Decision")

DECISION_confirmation = TITLE_MSG(
    trans_CPR(u"Confirmation"), trans_CPR(u"Do you confirm your choice?"))


def get_histo_head():
    return [le2mtrans(u"Period"), le2mtrans(u"Decision"),
             le2mtrans(u"Period\npayoff"), le2mtrans(u"Cumulative\npayoff")]



def get_recapitulatif(period_content):
    texte = trans_CPR(u"You extracted {} and you group extracted a total of {}.\n "
                 u"Your payoff is equal to {}").format(
        get_pluriel(period_content.get("CPR_decision"), trans_CPR(u"token")),
        get_pluriel(period_content.get("CPR_decisiongroup"), trans_CPR(u"token")),
        get_pluriel(period_content.get("CPR_periodpayoff"), u"ecu"))
    return texte
