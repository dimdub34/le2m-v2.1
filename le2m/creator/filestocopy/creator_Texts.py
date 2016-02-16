# -*- coding: utf-8 -*-
"""
Ce module contient les textes des écrans
"""
__author__ = "Dimitri DUBOIS"

from collections import namedtuple
from util.utiltools import get_pluriel
import EXPERIENCE_NOMParams as pms
from util.utili18n import le2mtrans
import os
import configuration.configparam as params
import gettext


localedir = os.path.join(params.getp("PARTSDIR"), "EXPERIENCE_NOM", "locale")
trans_EXPERIENCE_NOM_COURT = gettext.translation(
  "EXPERIENCE_NOM", localedir, languages=[params.getp("LANG")]).ugettext

TITLE_MSG = namedtuple("TITLE_MSG", "titre message")


# ECRAN DECISION ===============================================================
DECISION_titre = u"Decision"
DECISION_explication = u"Explanation text"
DECISION_label = u"Decision label text"
DECISION_erreur = TITLE_MSG(
    u"Warning",
    u"Warning message")
DECISION_confirmation = TITLE_MSG(
    u"Confirmation",
    u"Confirmation message")


def get_histo_head():
    return [le2mtrans(u"Period"), le2mtrans(u"Decision"),
             le2mtrans(u"Period\npayoff"), le2mtrans(u"Cumulative\npayoff")]


def get_text_summary(period_content):
    txt = trans_EXPERIENCE_NOM_COURT(u"Summary text")
    return txt

