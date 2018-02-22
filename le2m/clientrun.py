#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains the main fonction that starts the application on the
client side.
The client can be started with some options, do clientrun -h to get the
list of these options with some comments to explain them
"""

from PyQt4 import QtGui, QtCore
application = QtGui.QApplication([''])
QtGui.QApplication.setApplicationName("LE2M")

from util import utilqtreactor
utilqtreactor.install()

translator = QtCore.QTranslator()
localelang = QtCore.QLocale.system().name()
translator.load(QtCore.QString("qt_") + localelang,
                QtCore.QLibraryInfo.location(
                    QtCore.QLibraryInfo.TranslationsPath))
application.installTranslator(translator)

import sys
import os
if sys.platform.startswith("win"):
    import locale
    if os.getenv('LANG') is None:
        lang, enc = locale.getdefaultlocale()
        os.environ['LANG'] = lang
import logging
import argparse
from configuration import configparam as params
params.setp_appdir(os.path.realpath(os.path.dirname(__file__)))
import util.utili18n as i18n  # after appdir


def main():
    parser = argparse.ArgumentParser()

    # application language: by default the system language
    parser.add_argument("-l", "--lang", action="store",
                        default=params.getp("LANG"),
                        help=i18n.le2mtrans(u"Language of the application"))

    # automatic mode: with GUI and random decisions
    parser.add_argument(
        "-a", "--automatique", action="store_true",
        default=False,
        help=i18n.le2mtrans(u"Run the application in the automatic mode."))

    # simulation mode: random decisions without GUI
    parser.add_argument(
        "-s", "--simulation", action="store_true",
        default=False,
        help=i18n.le2mtrans(u"Run the application in the simulation mode"))

    # server ip
    parser.add_argument(
        "-i", "--ip", action="store",
        default=params.getp("SERVIP"),
        help=i18n.le2mtrans(u"IP adress of the server"))

    # server port
    parser.add_argument(
        "-p", "--port", action="store", type=int,
        default=params.getp("SERVPORT"), help=i18n.le2mtrans(u"Server port"))

    # check the options ========================================================
    args = parser.parse_args()
    options = vars(args)
    params.setp("LANG", args.lang)
    i18n.install()
    params.setp("SERVIP", args.ip)
    params.setp("SERVPORT", args.port)

    # LOGGER  ------------------------------------------------------------------
    logger = logging.getLogger("le2m")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(params.getp("LOGGING_FORMATTER"),
                                  datefmt=params.getp("LOGGING_FORMATTER_DATE"))
    # file handler
    fichier_log = logging.FileHandler(
        os.path.join(params.getp("REMOTELOGDIR"), 'le2m.log'))
    fichier_log.setLevel(logging.INFO)  
    fichier_log.setFormatter(formatter)
    logger.addHandler(fichier_log)
    # console handler
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.DEBUG)
    console_log.setFormatter(formatter)
    logger.addHandler(console_log)

    # first log
    logger.info("Logger created")
    logger.info("Command ligne options: {}".format(options))

    # start remote -------------------------------------------------------------
    from client import clt  # after appdir and le2mtrans

    client = clt.Client(args.automatique, args.simulation)
    client.start()


if __name__ == '__main__':
    main()
