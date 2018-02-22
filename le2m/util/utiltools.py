# -*- coding: utf-8 -*-
"""
Contains usefull functions
"""

import datetime
import string
import os
import logging
import inspect
from PyQt4.QtCore import QObject, QTimer, pyqtSignal, QThread
from random import randint
import numpy as np
import threading
import time
import random

logger = logging.getLogger("le2m")


class RepeatedTimer(object):
    def __init__(self, interval, func, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.func(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class QThreadWaiting(QThread):
    """
    A thread that calls a function repeatedly at a definite interval
    """

    def __init__(self, interval, func, *args, **kwargs):
        """

        :param interval: the interval the func is called
        :param func: the func to call
        :param args: args of the func
        :param kwargs: kwargs of the func
        """
        QThread.__init__(self)
        self.interval = interval
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        time.sleep(self.interval)
        self.func(*self.args, **self.kwargs)

    def stop(self):
        if self.timer.isAlive():
            self.timer.cancel()  # to kill the timer


def get_formatedtimefromseconds(nombre_secondes):
    """
    Return a formated string; HH:mm:ss
    :param nombre_secondes:
    :return: str
    """
    # we do the test because if type is float the str returned does not
    # correspond to what is expected
    if type(nombre_secondes) is not int:
        try:
            nombre_secondes = int(nombre_secondes)
            return get_formatedtimefromseconds(nombre_secondes)
        except ValueError:
            return u"? (ValueError)"
    minutes, secondes = divmod(nombre_secondes, 60)
    heures, minutes = divmod(minutes, 60)
    return "{}".format(datetime.time(heures, minutes, secondes).strftime(
        "%H:%M:%S"))


def get_letter(numero):
    """
    Renvoi la lettre majuscule correspondant au numéro.
    Si le numéro est supérieur à 25 alors ajoute 1; 2 si supérieur à 50 etc.
    :param numero:
    :return:string
    """
    if numero < 0:
        raise ValueError(u"Nombre négatif passé en paramètre")
    multiplicateur = numero / 26
    if multiplicateur > 0:
        return "{}{}".format(
            string.ascii_uppercase[numero - (multiplicateur * 26)],
            multiplicateur)
    else:
        return string.ascii_uppercase[numero]


def get_letternumber(lettre):
    """
    Renvoi le numéro de la lettre dans l'alphabet
    :param lettre:
    :return: int
    """
    num = -1
    try:
        num = string.ascii_uppercase.index(lettre)
    except ValueError as e:
        logger.warning(u"La lettre demandée n'a pas été trouvée: {}".format(e))
    finally:
        return num


def get_parent_folder(fichier):
    """
    Renvoi le chemin du dossier parent au fichier
    :param fichier:
    :return: str
    """
    return os.path.abspath(os.path.join(os.path.normpath(fichier),
                                        os.path.pardir))


def get_contenu_fichier(fichier):
    """
    Ouvre le fichier et renvoi son contenu.
    :param fichier: le fichier dont il faut récupérer le contenu
    :return str
    """
    texte = u""
    try:
        with open(fichier, "rb") as fichier:
            texte = fichier.read().decode("utf-8")
    except IOError as e:
        logger.critical(
            u"Problem while opening the file {}: {}".format(
                fichier, e.message))
    finally:
        return texte


def get_monnaie(nombre, monnaie=u"ecu"):
    """
    DEPRECATED: Utiliser get_pluriel à la place
    Renvoi la monnnaie avec ou sans s selon le nombre
    :param nombre: le nombre utilisé avec la monnaie
    :param monnaie: la monnaie (par défaut ecu)
    :return: string
    """
    return u"{}s".format(monnaie) if nombre > 1 else monnaie


def get_pluriel(quantite, mot):
    """
    Renvoi la quantité + le mot, avec un s si quantité sup à 1
    :param quantite
    :param mot
    :return str
    """
    def get_format(val):
        return u"{:.2f}".format(val) if type(val) is float else \
            u"{}".format(val)
    try:
        if abs(quantite) > 1:
            mots = mot.split()
            motsplu = [u"{}s".format(m) for m in mots]
            txt = u"{} {}".format(get_format(quantite), u" ".join(motsplu))
        else:
            txt = u"{} {}".format(get_format(quantite), mot)
    except TypeError:
        type_q = type(quantite)
        if not (type_q is int or type_q is float or type_q is str):
            return u"? (not int or float or str) " + mot
        if type_q is str:
            try:
                quantite = int(quantite)
            except ValueError:
                try:
                    quantite = float(quantite)
                except ValueError:
                    return u"? (str) " + mot
                else:
                    return get_pluriel(quantite, mot)
            else:
                return get_pluriel(quantite, mot)
    else:
        return txt


def get_module_attributes(module):
    """
    Extract attributes from the module
    :param module:
    :return: a dictionary with the keys and values of the module's attributes
    """
    if not inspect.ismodule(module):
        return None
    temp = module.__dict__.copy()

    # we delete some elements from this dictionary
    keys_to_del = ["__builtins__", "__name__", "__file__", "__doc__",
                 "__package__"]
    keys_to_del.extend([k for k, v in temp.viewitems() if inspect.isfunction(v)
                 or inspect.ismodule(v) or inspect.isclass(v) or
                 inspect.ismethod(v)])
    for k in keys_to_del:
        del temp[k]
    return temp


def get_module_info(module):
    """
    Return a list with the keys and values of the attributes of the module
    :param module:
    :return: str
    """
    temp = get_module_attributes(module)
    templist = [u"- {}: {}".format(k, v) for k, v in sorted(temp.viewitems())]
    return u"\n".join(templist)


class CompteARebours(QObject):

    changetime = pyqtSignal(str)
    endoftime = pyqtSignal()

    def __init__(self, tempsensecondes):
        QObject.__init__(self)
        self._temps = tempsensecondes + 1
        self._timer = QTimer()
        self._timer.setSingleShot(False)
        self._timer.timeout.connect(self._change_time)

    def start(self):
        self._timer.start(1000)

    def _change_time(self):
        if self._temps > 0:
            self._temps -= 1
            self.changetime.emit(get_formatedtimefromseconds(self._temps))
        else:
            self._timer.stop()
            self.endoftime.emit()

    def stop(self):
        self._timer.stop()

    def is_running(self):
        return self._timer.isActive()


def get_dictkeyfromvalue(dictio, value):
    """
    Return a key corresponding to the value
    :param dictio: the dict object
    :param value: the value for which to find the key
    :return: the corresponding key if value is in the dict
    """
    if type(dictio) is not dict:
        raise ValueError(u"dictio must be a dictionary")
    if type(value) is str:
        return dict(
                zip(map(string.upper, dictio.viewvalues()),
                    dictio.viewkeys())).get(string.upper(value), None)
    return dict(zip(
        dictio.viewvalues(), dictio.viewkeys())).get(value, None)


def get_dictinfos(dictio, which=None):
    """
    Suppose that all keys are strictly different from values
    :param dictio: the dict object
    :param which: None, a key or a value of the dict
    :return: either the whole dict (if which is None) or the corresponding
    value if which is a key a the dict or the corresponding key if which is
    a value of the dict
    """
    if type(dictio) is not dict:
        raise ValueError(u"dictio must be a dictionary")
    if which is None:
        return dictio.copy()
    if which in dictio:
        return dictio.get(which)
    return get_dictkeyfromvalue(dictio, which)


def cyclelist(mylist, numberoftime=1):
    """
    Send back the list but the first item becomes the last one.
    If numberoftime is greater than one, for example two, then the two first
    items become the last ones and so on.
    :param mylist:
    :param numberoftime:
    :return: a generator
    """
    if type(mylist) is not list:
        raise ValueError("A list is expected")
    while True:
        for _ in range(numberoftime):
            first = mylist.pop(0)
            mylist.append(first)
        yield mylist


def get_grids(how_much, size):
    grids = list()
    for g in range(how_much):
        somme, grille = 0, []
        while somme < (0.2 * size**2) or somme > (0.8 * size**2):
            grille = [[randint(0, 1) for _ in range(size)]
                      for _ in range(size)]
            somme = np.sum(grille)
        grids.append(grille)
    return grids


# ==============================================================================
# GROUPS
# ==============================================================================

__group_counter = 0


def form_groups(players, group_size, prefix_id=None):
    """
    Form groups
    :param players: the players
    :param group_size: the size of the groups to form
    :param prefix_id: optional - serve as id for groups
    :return: a dict with the group id as key and a list with the players as
    value
    """
    # --------------------------------------------------------------------------
    # CHECK CONDITIONS
    # --------------------------------------------------------------------------
    if type(players) is not list:
        raise ValueError("parameter players must be a list")
    elif len(players) % group_size > 0:
        raise ValueError("len(players) must be a multiple of {}".format(
            group_size))

    nb = len(players) / group_size
    dispos = players[:]
    pre_id = prefix_id or datetime.datetime.now().strftime("%Y%m%d%H%M")
    groups = dict()
    global __group_counter

    for i in range(nb):
        g_id = pre_id + "_g_" + str(__group_counter)
        groups[g_id] = []
        for j in range(group_size):
            selec = random.choice(dispos)
            groups[g_id].append(selec)
            dispos.remove(selec)
        __group_counter += 1

    return groups
