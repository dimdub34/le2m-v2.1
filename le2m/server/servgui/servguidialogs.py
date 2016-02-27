# -*- coding: utf-8 -*-

import os
import logging
import csv
from PyQt4 import QtGui, QtCore
from PyQt4.QtWebKit import QWebView
from configuration import configparam as params
from configuration.configconst import HOMME, FEMME
from configuration.configvar import Experiment
from util.utili18n import le2mtrans
from server.servgui.servguisrc import servguipartsload, servguiinfo, \
    servguipayoffs, servguigenders, servguipartsplayed
from servguitablemodels import TableModelPaiements
from util.utilwidgets import WDice, WRandint, WHeadtail


logger = logging.getLogger("le2m.{}".format(__name__))


class GuiGenres(QtGui.QDialog):
    """
    Boite de dialogue qui permet de cocher les femmes dans la listes des postes
    connectés au serveur
    """
    def __init__(self, liste_joueurs, parent=None):
        super(GuiGenres, self).__init__(parent)

        # variables
        self._liste_joueurs = liste_joueurs

        # création gui
        self.ui = servguigenders.Ui_Dialog()
        self.ui.setupUi(self)

        # explication
        self.ui.textEdit_explication.setFixedSize(350, 30)
        self.ui.textEdit_explication.setText(
            le2mtrans(u"Please check the men and let the women unchecked."))

        # listView
        self.ui.listView.setFixedSize(350, 350)
        self._model = QtGui.QStandardItemModel()
        for j in self._liste_joueurs:
            item = QtGui.QStandardItem(str(j))
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            item.setEditable(False)
            self._model.appendRow(item)
        self.ui.listView.setModel(self._model)

        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle(le2mtrans(u"Set subjects' gender"))
        self.setFixedSize(400, 550)

    def _accept(self):
        self._dict_genres = {}
        for ligne in xrange(self._model.rowCount()):
            item = self._model.item(ligne)
            if item.checkState() == QtCore.Qt.Checked:
                self._liste_joueurs[ligne].gender = HOMME
            else:
                self._liste_joueurs[ligne].gender = FEMME
        self.accept()


class GuiInformation(QtGui.QDialog):
    """
    Dialog qui affiche du texte (format plain ou html).
    """
    def __init__(self, text, titre=le2mtrans(u"Information"), parent=None,
                 size=(450, 450), html=False):
        super(GuiInformation, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)

        if html:
            browser = QtGui.QTextBrowser(self)
            browser.setText(text)
            browser.setOpenExternalLinks(True)
            browser.setFixedSize(size[0], size[1])
            layout.addWidget(browser)
        else:
            textedit = QtGui.QTextEdit()
            textedit.setReadOnly(True)
            textedit.setFixedSize(size[0], size[1])
            textedit.setText(text)
            layout.addWidget(textedit)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setWindowTitle(titre)
        self.adjustSize()
        self.setFixedSize(self.size())


class GuiPartLoad(QtGui.QDialog):
    def __init__(self, parent=None):
        super(GuiPartLoad, self).__init__(parent)

        self.ui = servguipartsload.Ui_Dialog()
        self.ui.setupUi(self)

        # parts list
        self.ui.label_explication.setText(
            le2mtrans(u"Please select in the list below the parts you want "
                      u"to load"))
        self.ui.listView.setToolTip(QtCore.QString(
            le2mtrans(u"Select the part(s) you want to load")))

        # database directory
        self.ui.label_basepath.setText(
            le2mtrans(u"Directory in which to store the database"))
        self.ui.label_basepath1.setText(le2mtrans(u"Directory path (check)"))
        self.ui.label_basepath2.setText("...")

        # database name
        self.ui.label_basename.setText(
            le2mtrans(u"Database name (without the sqlite extension"))
        self.ui.lineEdit_nom_base.setText(u"data")
        self.ui.label_nom_base_extension.setText(u".sqlite")

        # test session
        self.ui.label_test.setText(le2mtrans(u"Test session"))
        self.ui.checkBox_test.setToolTip(
            le2mtrans(u"Uncheck if this is not a test session"))
        self.ui.checkBox_test.setChecked(True)

        self.ui.pushButton_base.setText(le2mtrans(u"Browse"))

        # connections
        self.ui.pushButton_base.clicked.connect(self._set_directorydatabase)
        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        # list of parts in the PARTSDIR directory
        partslist = [f for f in os.listdir(params.getp("PARTSDIR")) if
                     os.path.isdir(os.path.join(params.getp("PARTSDIR"), f)) and
                     not f.startswith(".")]

        self._model = QtGui.QStandardItemModel()
        for p in partslist:
            item = QtGui.QStandardItem(p)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            item.setEditable(False)
            self._model.appendRow(item)
        self._model.itemChanged.connect(self._onitemchanged)
        self.ui.listView.setModel(self._model)

        self.setWindowTitle(le2mtrans(u"List of parts that can be loaded"))
        self.adjustSize()

    def _onitemchanged(self, item):
        """
        This is for setting a dir to the database
        We use the item just checked
        If the item is just unchecked then search for a checked one
        If no item we set ...
        """
        if item.checkState() == QtCore.Qt.Checked:
            part = str(item.text())
            self.ui.label_basepath2.setText(
                os.path.join(params.getp("PARTSDIR"), part))
        elif item.checkState() == QtCore.Qt.Unchecked:
            self.ui.label_basepath2.setText("...")
            i = 0
            while self._model.item(i):
                if self._model.item(i).checkState() == QtCore.Qt.Checked:
                    part = str(self._model.item(i).text())
                    self.ui.label_basepath2.setText(
                        os.path.join(params.getp("PARTSDIR"), part))
                    break
                i += 1

    def _set_directorydatabase(self):
        """
        Permet de choisir le dossier dans lequel sera sauvegardée la base
        de données sqlite
        :return:
        """
        dirbase = str(QtGui.QFileDialog.getExistingDirectory(
            self,
            le2mtrans(u"Select the directory in which to store the database."),
            params.getp("PARTSDIR"))
        )
        if not dirbase:
            return
        else:
            self._databasepath = dirbase
            self.ui.label_basepath2.setText(dirbase)

    def _accept(self):
        # parts
        parts = []
        i = 0
        while self._model.item(i):
            if self._model.item(i).checkState() == QtCore.Qt.Checked:
                parts.append(str(self._model.item(i).text()))
            i += 1
        if not parts:
            QtGui.QMessageBox.critical(
                self,
                le2mtrans(u"Error"),
                le2mtrans(u"You must choose at least one part"))
            return

        # dirbase
        dirbase = unicode(self.ui.label_basepath2.text().toUtf8(), "utf-8")
        if not (dirbase and os.path.isdir(dirbase)):
            QtGui.QMessageBox.critical(
                self,
                le2mtrans(u"Error"),
                le2mtrans(u"You must choose a directory in which to store the "
                          u"database"))
            return

        # basename
        basename = unicode(self.ui.lineEdit_nom_base.text().toUtf8(), "utf-8")
        if not basename:
            QtGui.QMessageBox.critical(
                self,
                le2mtrans(u"Error"),
                le2mtrans(u"You must provide a database name"))
            return
        basename += u".sqlite"

        if len(parts) > 1:
            confirmation = QtGui.QMessageBox.question(
                self, le2mtrans(u"Warning"),
                le2mtrans(u"You have selected several parts.\nNote that the "
                          u"database will be store in {d}.\n"
                          u"Please confirm that it is in this directory that "
                          u"you will store the database.".format(d=dirbase)),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes:
                return

        self._experiment = Experiment(
            parts, dirbase, basename, self.ui.checkBox_test.isChecked())
        self.accept()

    def get_expeinfos(self):
        return self._experiment


class GuiPartsPlayed(QtGui.QDialog):
    """
    Dialogue qui affiche la liste des parties jouées.
    Permet ensuite:
    - de tirer au sort une des parties parmi un ensemble sélectionné
    - de faire afficher les gains de la partie sélectionnée sur les 
    postes clients."""

    def __init__(self, liste_parties, parent=None):
        super(GuiPartsPlayed, self).__init__(parent)
        self._liste_parties = liste_parties

        self.ui = servguipartsplayed.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.listView_parties.setToolTip(
            QtCore.QString(u"Sélectionner une ou plusieurs parties"))
        self.ui.listView_parties.setFixedSize(300, 350)
        self.ui.buttonBox.accepted.connect(self._set_parties_selectionnees)
        self.ui.buttonBox.rejected.connect(self.reject)

        self._model = QtGui.QStandardItemModel()
        for partie in self._liste_parties:
            item = QtGui.QStandardItem('{}'.format(partie))
            item.setCheckState(QtCore.Qt.Checked)
            item.setCheckable(True)
            item.setEditable(False)
            self._model.appendRow(item)
        self.ui.listView_parties.setModel(self._model)

        self.adjustSize()

    def _set_parties_selectionnees(self):
        if not self._liste_parties:
            self.reject()
        self._parties_selectionnees = []
        for ligne in range(self._model.rowCount()):
            item = self._model.item(ligne)
            if item.checkState() == QtCore.Qt.Checked:
                self._parties_selectionnees.append(str(item.text()))
        if not self._parties_selectionnees:
            QtGui.QMessageBox.warning(self, u"Attention",
                                      u"Aucune partie sélectionnée")
            self.reject()
        self.accept()

    def get_parties_selectionnees(self):
        return self._parties_selectionnees


class GuiPayoffs(QtGui.QDialog):
    """
    Fenetre qui affiche les gains de la partie
    Elle permet d'imprimer ces gains, de les enregistrer mais aussi de les
    faire afficher sur les postes clients
    """
    def __init__(self, le2mserv, partname, payoffs):
        super(GuiPayoffs, self).__init__()
        self._le2mserv = le2mserv
        self._partname = partname
        self._payoffs = payoffs

        # creation gui
        self.ui = servguipayoffs.Ui_Dialog()
        self.ui.setupUi(self)

        # table model for displaying payoffs
        self._tableModel = TableModelPaiements(self._payoffs)
        self.ui.tableView.setModel(self._tableModel)
        self.ui.tableView.horizontalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch)

        # slot
        self.ui.pushButton_imprimer.clicked.connect(self._print)
        self.ui.pushButton_enregistrer.clicked.connect(self._save)
        self.ui.pushButton_afficher.clicked.connect(self._display_onremotes)
        self.ui.pushButton_ajouter.clicked.connect(self._addto_finalpayoffs)

        if self._partname == "base":
            self.setWindowTitle(le2mtrans(u"Payoffs for the experiment"))
            self.ui.pushButton_ajouter.setEnabled(False)
        else:
            self.setWindowTitle(le2mtrans(u"Payoffs of part {}").format(
                self._partname))
        self.setFixedSize(550, 608)

    def _print(self):
        """
        Print the table with the subjects' payoffs
        """
        if not self._payoffs:
            return
        html = u"<table align='center' border=1>\n<tr>" \
               u"<td align='center'><b>"
        html += le2mtrans(u"Hostname")
        html += u"</b></td>" \
                u"<td align='center'><b>"
        html += le2mtrans(u"Payoff")
        html += u"</b></td></tr>\n"
        for l in self._payoffs:
            html += u"<tr><td align='center'>{}</>" \
                    u"<td align='center'>{}&euro;</td>" \
                    u"</tr>\n".format(l[0], l[1])
        html += u"</table>\n"
        doc = QtGui.QTextDocument()
        doc.setHtml(html)
        printer = QtGui.QPrinter()
        dialog = QtGui.QPrintDialog(printer)
        dialog.setModal(True)
        dialog.setWindowTitle(le2mtrans(u"Payoffs"))
        if dialog.exec_():
            doc.print_(printer)

    def _save(self):
        """
        Open the dialog box for choosing/creating the location file and
        save the table in the csv format
        """
        if not self._payoffs:
            return
        fichier = QtGui.QFileDialog.getSaveFileName(
            self, le2mtrans("Export payoffs in csv file"), ".",
            le2mtrans(u"csv file (*.csv)"))
        if fichier:
            with open(fichier, 'wb') as csvfile:
                csv_writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"',
                    quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(
                    [le2mtrans(u"Hostname"), le2mtrans(u"Payoff")])
                for ligne in self._payoffs:
                    csv_writer.writerow(ligne)

    def _display_onremotes(self):
        text_temp = le2mtrans(u"the experiment") if \
            self._partname == "base" else self._partname
        confirmation = self._le2mserv.gestionnaire_graphique.question(
            le2mtrans(u"Display the payoffs of {}?").format(text_temp))
        if not confirmation:
            return

        if self._partname == "base":
            self._le2mserv.gestionnaire_experience.display_finalscreen()
        else:
            self._le2mserv.gestionnaire_experience.display_payoffs_onremotes(
                self._partname)

    def _addto_finalpayoffs(self):
        confirmation = QtGui.QMessageBox.question(
            self,
            u"Confirmation",
            u"Ajouter les gains de la partie aux gains finaux?",
            QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
        if confirmation != QtGui.QMessageBox.Yes:
            return
        self._le2mserv.gestionnaire_experience.add_tofinalpayoffs(
            self._partname)


class DDice(QtGui.QDialog):
    def __init__(self, parent):
        super(DDice, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)
        self._widdice = WDice(parent=self)
        layout.addWidget(self._widdice)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Dice roller"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        if self._widdice.ui.pushButton_start.isEnabled():
            QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"),
                le2mtrans(u"You must roll the dice"))
            return
        self.accept()

    def get_dicevalue(self):
        return self._widdice.get_dicevalue()


class DRandint(QtGui.QDialog):
    def __init__(self, parent):
        super(DRandint, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)
        self._widrandint = WRandint(parent=self)
        layout.addWidget(self._widrandint)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Random number"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        if self._widrandint.ui.pushButton_start.isEnabled():
            QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"),
                le2mtrans(u"You must drawn a random number"))
            return
        self.accept()

    def get_value(self):
        return self._widrandint.get_value()


class DHeadtail(QtGui.QDialog):
    def __init__(self, parent):
        super(DHeadtail, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)
        self._widheadtail = WHeadtail(parent=self)
        layout.addWidget(self._widheadtail)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Head and Tail"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        if self._widheadtail.ui.pushButton_start.isEnabled():
            QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"),
                le2mtrans(u"You must play"))
            return
        self.accept()

    def get_value(self):
        return self._widheadtail.get_value()


class DWebview(QtGui.QDialog):
    def __init__(self, html_file, title=u"Information", parent=None):
        QtGui.QDialog.__init__(self, parent)

        layout = QtGui.QVBoxLayout(self)

        self._webview = QWebView(self)
        self._webview.load(QtCore.QUrl(html_file))
        layout.addWidget(self._webview)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setWindowTitle(title)
        self.adjustSize()
