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
trans_PGG = gettext.translation(
    "PublicGoodGame", localedir, languages=[params.getp("LANG")]).ugettext


TITLE_MSG = namedtuple("TITLE_MSG", "titre message")


def get_histo_head():
    return [trans_PGG(u"Period"), trans_PGG(u"Individual\naccount"),
            trans_PGG(u"Public\naccount"), trans_PGG(u"Public\naccount\ngroup"),
            trans_PGG(u"Period\npayoff"), trans_PGG(u"Cumulative\npayoff")]


def get_text_explanation():
    return trans_PGG(u"You have an endowment of {} tokens.").format(pms.DOTATION)


def get_text_label_decision():
    return trans_PGG(u"Please enter the number of token(s) you put on the "
                     u"public account")


def get_text_summary(period_content):
    txt = trans_PGG(u"You put {} in your individual account and {} in the "
                    u"public account. Your group put {} in the public "
                    u"account.\nYour payoff for the current period is equal "
                    u"to {}.").format(
        get_pluriel(period_content.get("PGG_indiv"), trans_PGG(u"token")),
        get_pluriel(period_content.get("PGG_public"), trans_PGG(u"token")),
        get_pluriel(period_content.get("PGG_publicgroup"), trans_PGG(u"token")),
        get_pluriel(period_content.get("PGG_periodpayoff"), pms.MONNAIE))
    return txt

