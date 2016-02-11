# -*- coding: utf-8 -*-
__author__ = "Dimitri DUBOIS"

import os
import gettext
import logging
import tempfile
# from logging.handlers import RotatingFileHandler

_current_directory = os.path.dirname(os.path.realpath(__file__))
_localedir = os.path.join(_current_directory, "locale")
creatortrans = gettext.translation("creator", _localedir).ugettext


def get_appdir():
    return _current_directory


def create_logger():
    logger = logging.getLogger("creator")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(name)s | %(asctime)s | %(levelname)s | %(message)s',
        datefmt="%d/%m/%Y - %H:%M:%S")
    # file_handler = RotatingFileHandler('creator.log', 'a', 1000000, 1)
    file_handler = logging.FileHandler(
        os.path.join(tempfile.gettempdir(), "creator.log"))
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.DEBUG)
    logger.addHandler(steam_handler)

    logger.info(creatortrans(u"Logger creator created!"))
