# -*- coding: utf-8 -*-
"""
Ce module contient les textes des écrans
"""

from collections import namedtuple
from util.utiltools import get_pluriel
import voteMajoriteParams as pms

# pour i18n:
# 1)  décommenter les lignes ci-après,
# 2) entourer les expressions à traduire par _VM()
# 3) dans le projet créer les dossiers locale/fr_FR/LC_MESSAGES
# en remplaçant fr_FR par la langue souhaitée
# 4) créer le fichier voteMajorite.po: dans invite de commande, taper:
# xgettext fichierTextes.py -p locale/fr_FR/LC_MESSAGES -d voteMajorite
# 5) avec poedit, éditer le fichier voteMajorite.po qui a été créé

# import os
# import configuration.configparam as params
# import gettext
# localedir = os.path.join(params.getp("PARTSDIR"), "voteMajorite", "locale")
# _VM = gettext.translation(
#   "voteMajorite", localedir, languages=[params.getp("LANG")]).ugettext


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


# ECRAN RECAPITULATIF ==========================================================
def get_recapitulatif(periods, gainecus, gaineuros):
    txt = u""
    gains = []
    for i in range(1, pms.NOMBRE_PERIODES+1):
        txt += u"Politique {}: {} \"Pour\", {} \"Contre\", " \
               u"majorité: \"{}\". La politique {} en application.\n".format(
                i, get_pluriel(periods[i].VM_pour, u"personne"),
                get_pluriel(periods[i].VM_contre, u"personne"),
                u"Pour" if periods[i].VM_majority == pms.POUR else u"Contre",
                u"est mise" if periods[i].VM_majority == pms.POUR else
                u"n'est pas mise")
        gains.append(periods[i].VM_periodpayoff)
    txt += u"\nVotre gain est de {} = {} + {}, soit {}.".format(
            pms.DOTATION,
            u" + ".join(map(str, gains)), get_pluriel(gainecus, u"ecu"),
            get_pluriel(gaineuros, u"euro"))
    return txt


# TEXTE FINAL PARTIE ===========================================================
def get_texte_final(gain_ecus, gain_euros):
    txt = u"Vous avez gagné {}, soit {}.".format(
        get_pluriel(gain_ecus, u"ecu"), get_pluriel(gain_euros, u"euro"))
    return txt