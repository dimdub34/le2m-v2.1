# -*- coding: utf-8 -*-
__author__ = "Dimitri DUBOIS"

import os
import gettext

import configuration.configparam as params

localedir = os.path.join(params.getp("APPDIR"), "locale")
le2mtrans = None


def install():
    global le2mtrans
    try:
        le2mtrans = gettext.translation(
            "le2m", localedir, languages=[params.getp("LANG")]).ugettext
    except IOError:
        le2mtrans = gettext.translation("le2m", localedir).ugettext

install()