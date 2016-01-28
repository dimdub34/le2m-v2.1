#! /usr/bin/env python2
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import pandas as pd
import os
import sys
import sqlite3
import logging
import extractorutil
from extractorutil import extrans
from extractorgui import GuiExtractor

# for i18n
if sys.platform.startswith("win"):
    import locale
    if os.getenv('LANG') is None:
        lang, enc = locale.getdefaultlocale()
        os.environ['LANG'] = lang


def extractor():
    """
    Script to extract data from an le2m sqlite file to a csv file
    :return:
    """
    extractorutil.create_logger()
    logger = logging.getLogger("extractor")

    filebase = str(QtGui.QFileDialog.getOpenFileName(
        None, extrans(u"Please select the sqlite database you want to extract"),
        "", u"sqlite (*.sqlite)"))
    if not filebase:
        if __name__ == "__main__":
            sys.exit(0)
        else:
            return

    database = sqlite3.connect(filebase)
    parts = get_parts(database)
    partslist = get_splittedparts(parts)

    screen = GuiExtractor(partslist)
    if not screen.exec_():
        if __name__ == "__main__":
            sys.exit(0)
        else:
            return

    dirout, partsextract = screen.get_extractinfos()

    partsdata = dict()
    for p in partsextract:
        partsdata[p] = get_partdata(database, p)
    datatemp = partsdata.values()
    data = pd.DataFrame(datatemp[0])
    nbparts = len(datatemp)
    if nbparts > 1:
        for i in range(1, nbparts):
            data = pd.merge(data, datatemp[i], on="joueur")

    sessions = get_partdata(database, "sessions")
    base = get_partdata(database, "partie_base")

    data.to_csv(os.path.join(dirout, "data.csv"), sep=";", encoding="utf-8",
                na_rep=None, index=False)
    sessions.to_csv(os.path.join(dirout, "sessions.csv"), sep=";",
                    encoding="utf-8", na_rep=False, index=False)
    base.to_csv(os.path.join(dirout, "joueurs.csv"), sep=";", encoding="utf-8",
                na_rep=False, index=False)

    QtGui.QMessageBox.information(
        None, extrans(u"Sucess"),
        extrans(u"Data successfully extracted to {dirout}").format(
            dirout=dirout))
    logger.info(extrans(u"Data successfully extracted to {dirout}").format(
        dirout=dirout))

    # if the function has been launched as a script then exit
    if __name__ == "__main__":
        sys.exit(0)
    else:
        return


def get_parts(database):
    parts = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table';", database)
    return [p for p in parts.name]


def get_splittedparts(parts):
    repeatedparts = [p for p in parts if "repetitions" in p]
    myfilter = lambda x: "partie_" in x and "base" not in x and \
                         "repetitions" not in x
    oneshotparts = [p for p in parts if myfilter(p) and
                    not any(q.find(p) != -1 for q in repeatedparts)]
    oneshotparts.extend(repeatedparts)
    return oneshotparts


def get_partdata(database, partname):
    parts = get_parts(database)
    if partname not in parts:
        return None

    if partname is "sessions":
        req = \
            "select sessions.* " \
            "from sessions " \
            "where sessions.isTest = 0 " \
            "order by sessions.nom"

    elif "repetitions" in partname:
        part_withoutrep = "_".join(partname.split("_")[:-1])
        req = \
            "SELECT s.nom as session, j.uid as joueur, r.* " \
            "from sessions s, joueurs j, parties p, " \
            "parties_joueurs__joueurs_parties q, {} m, " \
            "{} r " \
            "where s.isTest = 0 " \
            "and j.session_id = s.id " \
            "and q.joueurs_uid = j.uid " \
            "and p.id = q.parties_id " \
            "and m.partie_id = p.id " \
            "and r.partie_partie_id = m.partie_id " \
            "order by s.nom".format(part_withoutrep, partname)
    else:
        req = \
            "SELECT s.nom as session, j.uid as joueur, m.* " \
            "from sessions s, joueurs j, parties p, " \
            "parties_joueurs__joueurs_parties q, {} m " \
            "where s.isTest = 0 " \
            "and j.session_id = s.id " \
            "and q.joueurs_uid = j.uid " \
            "and p.id = q.parties_id " \
            "and m.partie_id = p.id " \
            "order by s.nom".format(partname)

    return pd.read_sql(req, database)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    extractor()
    sys.exit(app.exec_())