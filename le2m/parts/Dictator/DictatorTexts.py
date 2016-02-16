# -*- coding: utf-8 -*-
"""
Ce module contient les textes des écrans
"""
__author__ = "Dimitri DUBOIS"

import os
from collections import OrderedDict
import configuration.configparam as params
import gettext
localedir = os.path.join(params.getp("PARTSDIR"), "Dictator", "locale")
trans_DIC = gettext.translation(
    "Dictator", localedir, languages=[params.getp("LANG")], fallback=True).ugettext
from collections import namedtuple
from util.utiltools import get_pluriel
from parts.Dictator import DictatorParams as pms
import logging

logger = logging.getLogger("le2m")
TITLE_MSG = namedtuple("TITLE_MSG", "titre message")


# HISTO ========================================================================
histo_build = {}
def get_histo_build(role):
    global histo_build
    if not histo_build.get(role):
        hb = OrderedDict()
        if role == pms.PLAYER_A:
            hb["DIC_decision"] = trans_DIC(u"Decision")
        elif role == pms.PLAYER_B:
            hb["DIC_recu"] = trans_DIC(u"Received")
        hb["DIC_periodpayoff"] = trans_DIC(u"Payoff")
        histo_build[role] = hb
    return histo_build[role]


# ROLE =========================================================================
def get_role(role):
    return trans_DIC(u"You are player {}").format(
        u"A" if role == pms.PLAYER_A else u"B")


# DECISION =====================================================================
DECISION_titre = trans_DIC(u"Decision")
DECISION_explication = trans_DIC(u"You have an endowment of {}. You can send any "
                            u"amount you want to player B").format(
    get_pluriel(pms.DOTATION, pms.MONNAIE))
DECISION_label = trans_DIC(u"Choose the amount you want to send to player B")
DECISION_confirmation = TITLE_MSG(
    trans_DIC(u"Confirmation"),
    trans_DIC(u"Do you confirm you choice?"))


# SUMMARY ======================================================================
def get_recapitulatif(currentperiod):
    """
    return the text of the summary
    :param currentperiod: a dict
    :return: str
    """
    txt = trans_DIC(u"You were player {}.").format(
        u"A" if currentperiod.get("DIC_role") == pms.PLAYER_A else u"B")
    if currentperiod.get("DIC_role") == pms.PLAYER_A:
        txt += trans_DIC(u" You sent {} to player B.").format(
            get_pluriel(currentperiod.get("DIC_decision"), pms.MONNAIE))
    else:
        txt += trans_DIC(u" Player A sent {} to you.").format(
            get_pluriel(currentperiod.get("DIC_recu"), pms.MONNAIE))
    txt += trans_DIC(u" Your payoff is equal to {}.").format(
        get_pluriel(currentperiod.get("DIC_periodpayoff"), pms.MONNAIE))
    return txt
