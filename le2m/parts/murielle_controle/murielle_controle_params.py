# -*- coding: utf-8 -*-

"""=============================================================================
This modules contains the variables and the parameters.
Do not change the variables.
Parameters that can be changed without any risk of damages should be changed
by clicking on the configure sub-menu at the server screen.
If you need to change some parameters below please be sure of what you do,
which means that you should ask to the developer ;-)
============================================================================="""

import logging
from datetime import timedelta

import numpy as np
from scipy.integrate import quad

logger = logging.getLogger("le2m")

# ------------------------------------------------------------------------------
# VARIABLES - do not change any value below
# ------------------------------------------------------------------------------

BASELINE = 0
TREATMENTS_NAMES = {BASELINE: "Baseline"}

# used to set DYNCPR_dynamic_type
CONTINUOUS = 0
DISCRETE = 1

# used to store the curve (CO_curve_type)
EXTRACTION = 0
PAYOFF = 1
RESOURCE = 2
COST = 3

# ------------------------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------------------------

TREATMENT = BASELINE  # for future treatments
TAUX_CONVERSION = 0.05
NOMBRE_PERIODES = 60  # only for dynamic == discrete
TAILLE_GROUPES = 2  # should not be changed without asking Dimitri
MONNAIE = u"ecu"

# DECISION
DECISION_MIN = 0
DECISION_MAX = 2.8
DECISION_STEP = 0.01

PARTIE_ESSAI = False

DYNAMIC_TYPE = DISCRETE
# continuous game
CONTINUOUS_TIME_DURATION = timedelta(seconds=600)  # can be changed in config screen
# time for the player to take a decision
DISCRETE_DECISION_TIME = timedelta(seconds=10)
# milliseconds
TIMER_UPDATE = timedelta(seconds=1)  # refresh the group data and the graphs

# ------------------------------------------------------------------------------
# RESOURCE
# ------------------------------------------------------------------------------

RESOURCE_INITIAL_STOCK = R0 = 15
RESOURCE_GROWTH = pluie = 0.56

# ------------------------------------------------------------------------------
# FONCTION DE GAIN
# ------------------------------------------------------------------------------

param_a = a = 2.5
param_b = b = 1.8
param_c0 = c0 = 2
param_c1 = c1 = 0.1
param_r = r = 0.005
tau_continu = 0.1
tau_discret = 1
param_tau = tau = tau_continu if DYNAMIC_TYPE == CONTINUOUS else tau_discret


def get_ressource(n, ressource_prec, extraction):
    return float(ressource_prec + quad(lambda x: pluie - extraction, (n - 1) * tau, n * tau)[0])


def get_gain_instantane(n, extraction, ressource):
    instant = n * tau
    cost = (c0 - c1 * ressource) * extraction
    if cost < 0:
        cost = 0
    return float(np.exp(-r * instant) * (a * extraction - (b / 2) * pow(extraction, 2) - cost))


def get_infinite_payoff(n, resource, extraction):
    t = n * tau
    constante = pluie - extraction
    try:
        tm = ((param_c0 / param_c1) + constante * t - resource) / constante
        t0 = (constante * t - resource) / constante
    except ZeroDivisionError:
        tm = t0 = 0

    if resource >= (param_c0 / param_c1):

        if constante >= 0:  # cas 1.1
            calcul = (param_a * extraction - (param_b / 2) * pow(extraction,
                                                                 2)) * \
                     (np.exp(- param_r * t) / param_r)

        else:  # cas 1.2
            calcul = (param_a * extraction - (param_b / 2) * pow(extraction,
                                                                 2)) * \
                     ((np.exp(- param_r * t) - np.exp(
                         - param_r * t0)) / param_r) - \
                     extraction * (
                             param_c0 - param_c1 * resource + constante * param_c1 * t) * \
                     ((np.exp(- param_r * tm) - np.exp(
                         - param_r * t0)) / param_r) + \
                     (extraction * param_c1 * constante) * \
                     ((1 + param_r * tm) * np.exp(-param_r * tm) - (
                             1 + param_r * t0) * np.exp(
                         -param_r * t0)) / pow(param_r, 2)

    else:

        if constante > 0:  # cas 1.3
            calcul = (param_a * extraction - (param_b / 2) * pow(extraction,
                                                                 2)) * \
                     (np.exp(- param_r * t) / param_r) - \
                     extraction * (
                             param_c0 - param_c1 * resource + constante * param_c1 * t) * \
                     ((np.exp(- param_r * t) - np.exp(
                         - param_r * tm)) / param_r) + \
                     (extraction * param_c1 * constante) * \
                     ((1 + param_r * t) * np.exp(-param_r * t) - (
                             1 + param_r * tm) * np.exp(
                         -param_r * tm)) / pow(param_r, 2)

        elif constante < 0:  # cas 1.4
            calcul = (param_a * extraction - (param_b / 2) * pow(extraction,
                                                                 2) -
                      extraction * (
                              param_c0 - param_c1 * resource + constante * param_c1 * t)) * \
                     ((np.exp(- param_r * t) - np.exp(
                         - param_r * t0)) / param_r) + \
                     (extraction * param_c1 * constante) * \
                     ((1 + param_r * t) * np.exp(-param_r * t) - (
                             1 + param_r * t0) * np.exp(
                         -param_r * t0)) / pow(param_r, 2)

        else:  # cas 1.5
            calcul = (param_a * extraction - (param_b / 2) * pow(extraction,
                                                                 2) -
                      extraction * (param_c0 - param_c1 * resource)) * \
                     (np.exp(- param_r * t) / param_r)

    return float(calcul)


def get_extraction_os(n):
    instant = n * tau
    if instant < 19.48:
        return float(
            0.5487208184 * np.exp(0.01935312368 * instant) - 1.058211486 * np.exp(-0.01435312368 * instant) + pluie)
    else:
        return pluie


def get_extraction_my(n):
    instant = n * tau
    return float(pluie + 0.5511111112 * np.exp(-0.05555555556 * instant))
