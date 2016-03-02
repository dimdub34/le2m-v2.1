# -*- coding: utf-8 -*-

"""
This module contains some parameters used both by the remotes and the server.
"""

import os
import tempfile

# ------------------------------------------------------------------------------
# In the dictionary below the values can be changed
# When the server is started with the arg -p it changes the server port and
# when it is started with -l it changes the langage
# The client/remote can change the server ip (-i), the serveur port (-p),
# as well as the language (-l)
# This means that these parameters can be changed either manually here or
# at the start of the application with options in the command line:
# ex: serverrun -p 7000 or clientrun -i "192.168.159.2"
# ------------------------------------------------------------------------------
__parameters = {
    "SERVPORT": 9998,
    "SERVIP": "192.168.159.2",
    "REMOTELOGDIR": tempfile.gettempdir(),
    "LABNAME": u"Laboratoire d'Economie Expérimentale de Montpellier",
    "WELCOMETEXT": u"Laboratoire d'Economie Expérimentale de Montpellier",
    "CURRENCY": u"euro",
    "LOGGING_FORMATTER": '%(name)s | %(asctime)s | %(levelname)s | %(message)s',
    "LOGGING_FORMATTER_DATE": "%d/%m/%Y - %H:%M:%S",
    "LANG": "fr"
}


def getp(key):
    """
    get parameter
    :param key:
    :return:
    """
    global __parameters
    return __parameters.get(key, None)


def setp(key, value):
    """
    set parameters
    :param key:
    :param value:
    :return:
    """
    global __parameters
    __parameters[key] = value


def setp_appdir(value):
    """
    Set some parameters that depend on the application directory
    Lines with *** can be changed, if you want to change the lab logo,
    the main picture and the experimental lab picture
    The other parameters cannot be changed
    :param value:
    :return:
    """
    setp("APPDIR", value)
    setp("LOGDIR", getp("APPDIR"))
    setp("IMGDIR", os.path.join(getp("APPDIR"), "img"))
    setp("HTMLDIR", os.path.join(getp("APPDIR"), "html"))
    setp("PARTSDIR", os.path.join(getp("APPDIR"), "parts"))
    setp("LABLOGO", os.path.join(getp("IMGDIR"), "logo_lameta.gif"))  # ***
    setp("LABPICTURE", os.path.join(getp("IMGDIR"), "mix.jpg"))  # ***
    setp("WELCOMEPICTURE", os.path.join(getp("IMGDIR"), "leem.jpg"))  # ***
