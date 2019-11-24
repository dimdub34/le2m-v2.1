# -*- coding: utf-8 -*-
"""
This module contains the texts of the part (server and remote)
"""

from util.utiltools import get_pluriel
import murielle_jeu_params as pms
from util.utili18n import le2mtrans
import os
import configuration.configparam as params
import gettext
import logging

logger = logging.getLogger("le2m")
try:
    localedir = os.path.join(params.getp("PARTSDIR"), "murielle_jeu", "locale")
    trans_GA = gettext.translation("murielle_jeu", localedir, languages=[params.getp("LANG")]).ugettext
except (AttributeError, IOError):
    logger.critical(u"Translation file not found")
    trans_GA = lambda x: x  # if there is an error, no translation


# ==============================================================================
# EXPLANATIONS
# ==============================================================================

INITIAL_EXTRACTION = trans_GA(
    u"Please choose an initial extraction level")

EXTRACTION = trans_GA(u"Please choose an extraction level")


def get_histo_vars():
    return ["CO_period", "CO_decision", "CO_periodpayoff", "CO_cumulativepayoff"]


def get_histo_head():
    return [le2mtrans(u"Period"), le2mtrans(u"Decision"),
             le2mtrans(u"Period\npayoff"), le2mtrans(u"Cumulative\npayoff")]


def get_text_explanation():
    return trans_GA(u"Explanation text")


def get_text_label_decision():
    return trans_GA(u"Decision label")


def get_text_summary(part_payoff):
    txt = trans_GA(u"Your payoff for this part is ") + \
          u" {:.2f} ecus, ".format(part_payoff) + \
          trans_GA(u"which corresponds to ") + \
          u"{:.2f} euros".format(part_payoff * pms.TAUX_CONVERSION)
    return txt


