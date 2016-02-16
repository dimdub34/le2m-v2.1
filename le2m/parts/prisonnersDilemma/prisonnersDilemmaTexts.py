# -*- coding: utf-8 -*-

from util.utili18n import le2mtrans
from util.utiltools import get_pluriel
import prisonnersDilemmaParams as pms
import os
import configuration.configparam as params
import gettext


localedir = os.path.join(params.getp("PARTSDIR"), "prisonnersDilemma", "locale")
trans_DP = gettext.translation("prisonnersDilemma", localedir,
                          languages=[params.getp("LANG")]).ugettext


def get_text_explanation():
    return trans_DP(u"Choose option X or option Y")


def get_histo_head():
    return [le2mtrans(u"Period"), le2mtrans(u"Decision"),
            trans_DP(u"Decision other"), le2mtrans(u"Period\npayoff"),
            le2mtrans(u"Cumulative\npayoff")]


def get_text_summary(period_content):
    txt = trans_DP(u"You chose {} and the other player chose {}.").format(
        pms.get_option(period_content.get("DP_decision")),
        pms.get_option(period_content.get("DP_decisionother")))
    txt += u" " + trans_DP(u"Your payoff is {}.").format(
        get_pluriel(period_content.get("DP_periodpayoff"), pms.MONNAIE))
    return txt
