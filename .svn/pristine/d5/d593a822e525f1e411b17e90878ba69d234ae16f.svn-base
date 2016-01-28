# -*- coding: utf-8 -*-
"""
Ce module contient les textes des écrans
"""
__author__ = "Dimitri DUBOIS"


from collections import namedtuple
from util.utiltools import get_pluriel
import oathAndLiesParams as pms

# pour i18n:
# 1)  décommenter les lignes ci-après,
# 2) entourer les expressions à traduire par _OL()
# 3) dans le projet créer les dossiers locale/fr_FR/LC_MESSAGES
# en remplaçant fr_FR par la langue souhaitée
# 4) créer le fichier oathAndLies.po: dans invite de commande, taper:
# xgettext fichierTextes.py -p locale/fr_FR/LC_MESSAGES -d oathAndLies
# 5) avec poedit, éditer le fichier oathAndLies.po qui a été créé

# import os
# import configuration.configparam as params
# import gettext
# localedir = os.path.join(params.getp("PARTSDIR"), "oathAndLies", "locale")
# _OL = gettext.translation(
#   "oathAndLies", localedir, languages=[params.getp("LANG")]).ugettext


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
def get_recapitulatif(currentperiod, role):
    if role == pms.JOUEUR_A:
        txt = u"Option X: {}, Option Y: {}.".format(
            pms.CODES_PERIODES[pms.GAME][0], pms.CODES_PERIODES[pms.GAME][1])
        txt += u"\nRésultat du lancé de dé: {}.\nMessage transmis à B: " \
               u"\"Le résultat du lancé de dé est {}.\".".format(
                currentperiod.OL_tirage, currentperiod.OL_message)
        txt += u"\nNombre choisi par B: {}.".format(currentperiod.OL_decision)
        txt += u"\nOption appliquée: {}.\nVotre gain pour la période: " \
               u"{} ecus.".format(
                u"X" if currentperiod.OL_appliedoption == pms.OPTION_X else u"Y",
                currentperiod.OL_periodpayoff)

    else:
        txt = u"Message transmis par A: \"Le résultat du lancé de dé " \
              u"est {}\".".format(currentperiod.OL_message)
        txt += u"\nVotre choix de nombre: {}. \nVotre gain pour la période: " \
               u"{} ecus.".format(currentperiod.OL_decision,
                                  currentperiod.OL_periodpayoff)

    return txt


# TEXTE FINAL PARTIE ===========================================================
def get_texte_final(gain_ecus, gain_euros):
    txt = u"Vous avez gagné {gain_en_ecu}, soit {gain_en_euro}.".format(
        gain_en_ecu=get_pluriel(gain_ecus, u"ecu"),
        gain_en_euro=get_pluriel(gain_euros, u"euro")
    )
    return txt


def get_role(role):
    return u"Vous êtes joueur {}".format(u"A" if role == pms.JOUEUR_A else u"B")


def get_explication(role):
    if role == pms.JOUEUR_A:
        txt = u"Vous êtes un participant A.\nVous devez prendre connaissance " \
              u"des gains associés à l'option X et à l'option Y.\nVous devez " \
              u"ensuite lancer le dé.\nVous devez enfin choisir le message " \
              u"que vous transmettez à B."

    elif role == pms.JOUEUR_B:
        txt = u"Vous êtes un participant B.\nVous devez prendre connaissance " \
              u"du message transmis par le joueur A.\nVous devez ensuite " \
              u"choisir un nombre compris entre 1 et 6."

    return txt

