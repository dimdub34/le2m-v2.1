# -*- coding: utf-8 -*-
"""
This module contains the texts of the part (server and remote)
"""

from util.utiltools import get_pluriel
import murielle_controle_params as pms
from util.utili18n import le2mtrans
import os
import configuration.configparam as params
import gettext
import logging

logger = logging.getLogger("le2m")
try:
    localedir = os.path.join(params.getp("PARTSDIR"), "murielle_controle",
                             "locale")
    trans_CO = gettext.translation(
      "murielle_controle", localedir, languages=[params.getp("LANG")]).ugettext
except (AttributeError, IOError):
    logger.critical(u"Translation file not found")
    trans_CO = lambda x: x  # if there is an error, no translation


# ==============================================================================
# EXPLANATIONS
# ==============================================================================

INITIAL_EXTRACTION = trans_CO(
    u"Please choose an initial extraction level")

EXTRACTION = trans_CO(u"Please choose an extraction level")


def get_histo_vars():
    return ["CO_period", "CO_decision",
            "CO_periodpayoff",
            "CO_cumulativepayoff"]


def get_histo_head():
    return [le2mtrans(u"Period"), le2mtrans(u"Decision"),
             le2mtrans(u"Period\npayoff"), le2mtrans(u"Cumulative\npayoff")]


def get_text_explanation():
    return trans_CO(u"Explanation text")


def get_text_label_decision():
    return trans_CO(u"Decision label")


def get_text_summary(part_payoff):
    txt = trans_CO(u"Your payoff for this part is ") + \
          u" {:.2f} ecus, ".format(part_payoff) + \
          trans_CO(u"which corresponds to ") + \
          u"{:.2f} euros".format(part_payoff * pms.TAUX_CONVERSION)
    return txt


