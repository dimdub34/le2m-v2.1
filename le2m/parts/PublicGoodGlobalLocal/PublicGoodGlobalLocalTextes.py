# -*- coding: utf-8 -*-
__author__ = 'irtimid'

import os
import configuration.configparam as params
import PublicGoodGlobalLocalParams as pms
from util.utiltools import get_pluriel
from collections import namedtuple
import gettext


localedir = os.path.join(params.getp("PARTSDIR"), "PublicGoodGlobalLocal",
                         "locale")
_PGGL = gettext.translation(
    "PublicGoodGlobalLocal", localedir, languages=[params.getp("LANG")]).ugettext


TITLE_MSG = namedtuple("TITLE_MSG", ["titre", "texte"])

PERIODE_label = lambda periode: _PGGL(u"Period {}").format(periode)
HISTORIQUE_button = _PGGL(u"History")

# ECRAN COMMUNICATION ==========================================================
COMMUNICATION_title = _PGGL(u"Communication")

# ECRAN DECISION ===============================================================
DECISION_explication = _PGGL(u"You have an endowment of {}. You have to choose "
                             u"you share these tokens between your private "
                             u"account, the local account and the global "
                             u"account.").format(
    get_pluriel(pms.DOTATION, _PGGL(u"token")))

DECISION_label_individuel = _PGGL(u"Tokens you put on your private account")
DECISION_label_local = _PGGL(u"Tokens you put on the local account")
DECISION_label_global = _PGGL(u"Tokens you put on the global account")

DECISION_error = TITLE_MSG(
    _PGGL(u"Warning"), _PGGL(u"You must use the {}.").format(
        get_pluriel(pms.DOTATION, _PGGL(u"token"))))

DECISION_confirmation = TITLE_MSG(
    _PGGL(u"Confirmation"), _PGGL(u"Do you confirm your choice?"))
DECISION_title = _PGGL(u"Decision")


# ECRAN INFORMATION ============================================================
INFORMATION_title = _PGGL(u"Information")
INFORMATION_confirmation = TITLE_MSG(
    _PGGL(u"Confirmation"), _PGGL(u"Do you confirm your choice?"))


def get_information(currentperiod):
    txt = _PGGL(u"Your group put {} on the local account and {} on the global "
                u"account. The other group put {} on the global account. The "
                u"total number of tokens on the global account is "
                u"therefore {}.").format(
        get_pluriel(currentperiod.PGGL_local_sousgroupe, _PGGL(u"token")),
        get_pluriel(currentperiod.PGGL_global_sousgroupe, _PGGL(u"token")),
        get_pluriel(currentperiod.PGGL_global_autresousgroupe, _PGGL(u"token")),
        get_pluriel(currentperiod.PGGL_global_total, _PGGL(u"token")))
    return txt


# ECRAN RECAPITULATIF ==========================================================
def get_recapitulatif(currentperiod):

    txt = _PGGL(u"You put {} on your individual account, {} on the local "
                u"account and {} on the global account.").format(
                    get_pluriel(currentperiod.PGGL_individuel, _PGGL(u"token")),
                    get_pluriel(currentperiod.PGGL_local, _PGGL(u"token")),
                    get_pluriel(currentperiod.PGGL_global, _PGGL(u"token")))

    txt += u"\n" + _PGGL(u"Your group put {} on the local account and {} on "
                         u"the global account. The other group put {} on the "
                         u"global account. The total number of tokens put on "
                         u"the global account is therefore {}.").format(
        get_pluriel(currentperiod.PGGL_local_sousgroupe, _PGGL(u"token")),
        get_pluriel(currentperiod.PGGL_global_sousgroupe, _PGGL(u"token")),
        get_pluriel(currentperiod.PGGL_global_autresousgroupe, _PGGL(u"token")),
        get_pluriel(currentperiod.PGGL_global_total, _PGGL(u"token")))

    txt += u"\n" + _PGGL(u"Your payoff for the current period is {}").format(
        get_pluriel(currentperiod.PGGL_periodpayoff, u"ecu"))
    return txt


# TEXTE FINAL PARTIE ===========================================================
def get_texte_final(gain_ecus, gain_euros):
    txt = u"You earned {} which corresponds to {}.".format(
        get_pluriel(gain_ecus, u"ecu"), get_pluriel(gain_euros, u"euro"))
    return txt


# TRAITEMENT EN TEXTE ==========================================================
def get_traitement(traitement):
    if traitement == pms.BASELINE:
        return _PGGL(u"Baseline")
    elif traitement == pms.CARTONS_LOCAL:
        return _PGGL(u"Disapproval - local")
    elif traitement == pms.CARTONS_GLOBAL:
        return _PGGL(u"Disapproval - global")
    elif traitement == pms.CARTONS_LOCAL_GLOBAL:
        return _PGGL(u"Disapprobal - local and global")
    elif traitement == pms.CARTONS_LOCAL_AUTRE:
        return _PGGL(u"Disapproval - local other group")


def get_communication(communication):
    if communication == pms.SANS_COMMUNICATION:
        return _PGGL(u"Without communication")
    elif communication == pms.COMMUNICATION_LOCAL:
        return _PGGL(u"Communication - local")
    elif communication == pms.COMMUNICATION_GLOBAL:
        return _PGGL(u"Communication - global")
