# -*- coding: utf-8 -*-

import os
import configuration.configparam as params
from configuration.configconst import PILE
from collections import namedtuple
from util.utiltools import get_pluriel
import GneezyPotterParams as pms
import gettext


localedir = os.path.join(params.getp("PARTSDIR"), "GneezyPotter", "locale")
trans_GP = gettext.translation(
    "GneezyPotter", localedir, languages=[params.getp("LANG")]).ugettext

TITLE_MSG = namedtuple("TITLE_MSG", "titre message")


def get_text_explanation():
    txt = trans_GP(u"You have an endowment of {}. You can invest amount you want in the "
        u"risky option").format(get_pluriel(pms.DOTATION, pms.MONNAIE))
    return txt


def get_text_summary(period_content):
    txt = trans_GP(u"You invested {} in the risky option.").format(
        get_pluriel(period_content.get("GP_decision"), pms.MONNAIE))
    txt += u" " + trans_GP(u"The random draw was {}.").format(
        trans_GP(u"Head") if period_content.get("GP_randomdraw") == PILE else \
            trans_GP(u"Tail"))
    txt += u" " + trans_GP(u"Your payoff is equal to {}.").format(
        get_pluriel(period_content.get("GP_periodpayoff"), pms.MONNAIE))
    return txt

