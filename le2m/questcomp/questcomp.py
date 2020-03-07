#! /usr/bin/env python2
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import os
import sys
import questcompmod
from questcompgui import GuiQuestComp

# for i18n
if sys.platform.startswith("win"):
    import locale
    if os.getenv('LANG') is None:
        lang, enc = locale.getdefaultlocale()
        os.environ['LANG'] = lang

_screen = None


def questcomp():
    global _screen
    _screen = GuiQuestComp()
    _screen.show()


def get_questions(xmlfile):
    return questcompmod.get_questions(xmlfile)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    questcomp()
    sys.exit(app.exec_())