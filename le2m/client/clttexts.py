# -*- coding: utf-8 -*-
__author__ = "Dimitri DUBOIS"

from util.utili18n import le2mtrans
from util.utiltools import get_pluriel
from configuration import configparam as params

PERIODE_label = lambda periode: le2mtrans(u"Period {p}").format(p=periode)

# ECRAN ACCUEIL
ACCUEIL_label_welcome = le2mtrans(u"Welcome to {welctext}").format(
    welctext=params.getp("WELCOMETEXT"))
ACCUEIL_label_image_accueil = le2mtrans(u"Here the welcome picture")
ACCUEIL_titre = le2mtrans(u"Welcome to the LEEM")
ACCUEIL_bouton = le2mtrans(u"Instructions read")


# QUESTIONNAIRE_FINAL
QUESTFINAL_explication = \
    le2mtrans(u"Please fill in the questionnaire below.\nThis questionnaire "
              u"is anonymous, so please answer sincerily.")


def get_final_text(final_payoff):
    txt = le2mtrans(u"Your payoff for the experiment is equal to ") + \
        u" {}".format(get_pluriel(final_payoff, params.getp("CURRENCY")))
    return txt
