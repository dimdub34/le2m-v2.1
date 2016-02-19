#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import sys
import os
import logging
import argparse
application = QtGui.QApplication([''])  # application before utilqtreactor
from util import utilqtreactor
utilqtreactor.install()
# in order that system dialog box to be in the appropriate language
translator = QtCore.QTranslator()
localelang = QtCore.QLocale.system().name()
translator.load(QtCore.QString("qt_") + localelang,
                QtCore.QLibraryInfo.location(
                    QtCore.QLibraryInfo.TranslationsPath))
application.installTranslator(translator)
# for windows, set lang
if sys.platform.startswith("win"):
    import locale
    if os.getenv('LANG') is None:
        lang, enc = locale.getdefaultlocale()
        os.environ['LANG'] = lang
from configuration import configparam as params
params.setp_appdir(os.path.realpath(os.path.dirname(__file__)))
import util.utili18n as i18n  # after the set of APPDIR


def main():
    parser = argparse.ArgumentParser()

    # application language
    parser.add_argument("-l", "--lang", action="store",
                        default=params.getp("LANG"),
                        help=i18n.le2mtrans(u"Language of the application"))

    # directory for the database
    parser.add_argument("-db", "--dirbase", action="store",
                        default=None,
                        help=i18n.le2mtrans(
                            u"Directory in which to store the database. "
                            u"This argument is not an option if several "
                            u"parts are started with arg -e"))

    # database name
    parser.add_argument("-nb", "--namebase", action="store",
                        default="data.sqlite",
                        help=i18n.le2mtrans(u"Name of the sqlite file, if not data"))

    # server port
    parser.add_argument("-p", "--port", action="store", type=int,
                        default=params.getp("SERVPORT"))

    # names of parts to load directly
    parser.add_argument("-e", "--parts", nargs='+', default=[],
                        dest="parts",
                        help=i18n.le2mtrans(u"The name(s) of the part(s) to load)."))

    # whether it is a test session or not
    test_parser = parser.add_mutually_exclusive_group(required=False)
    test_parser.add_argument('--test', dest='test', action='store_true',
                             help=i18n.le2mtrans(u"The session is launched in "
                                                 u"test mode"))
    test_parser.add_argument('--no-test', dest='test', action='store_false',
                             help=i18n.le2mtrans(u"The session is launched for "
                                                 u"real (not test mode)"))
    parser.set_defaults(test=True)
    # parser.add_argument("-nt", "--notest", action="store_false", default=True,
    #                     help=i18n.le2mtrans(
    #                         u"With this option the experiment is launched for "
    #                         u"real"))

    # check the options ========================================================
    args = parser.parse_args()
    params.setp("LANG", args.lang)
    i18n.install()

    if args.parts:
        for e in args.parts:
            if e not in os.listdir(params.getp("PARTSDIR")):
                parser.error(i18n.le2mtrans(u"Part {p} does not exist").format(p=e))
    # check database if several parts
    if len(args.parts) > 1 and not args.dirbase:
        parser.error(i18n.le2mtrans(
            u"The directory in which store the database has to be provided "
            u"with arg -db"))

    params.setp("SERVPORT", args.port)
    options = vars(args)  # we put the args in a dict

    # creation logger ==========================================================
    logger = logging.getLogger("le2m")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        params.getp("LOGGING_FORMATTER"),
        datefmt=params.getp("LOGGING_FORMATTER_DATE"))
    fichier_log = logging.FileHandler(
        os.path.join(params.getp("LOGDIR"), 'le2m.log'))
    fichier_log.setLevel(logging.INFO)
    fichier_log.setFormatter(formatter)
    logger.addHandler(fichier_log)
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.DEBUG)
    console_log.setFormatter(formatter)
    logger.addHandler(console_log)
    logger.info(30 * "=")
    logger.info("Logger LE2M created")
    logger.info("APPDIR: {}".format(params.getp("APPDIR")))
    logger.info("PARTSDIR: {}".format(params.getp("PARTSDIR")))
    logger.info("Command ligne options: {}".format(options))

    # start server -------------------------------------------------------------
    from server.serv import Serveur

    serveur = Serveur(**options)
    serveur.start()


if __name__ == "__main__":
    main()
