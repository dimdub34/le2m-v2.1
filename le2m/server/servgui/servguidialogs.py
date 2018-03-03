# -*- coding: utf-8 -*-

import os
import logging
import csv
from PyQt4 import QtGui, QtCore
from PyQt4.QtWebKit import QWebView
from PyQt4.phonon import Phonon
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
        self.ui.listView.setMinimumHeight(480)

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
        partslist.sort()

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
        logger.info("Experiment parameters: {}".format(self._experiment))
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
        confirmation = QtGui.QMessageBox.question(
            self, u"Confirmation",
            le2mtrans(u"Display the payoffs of {}?").format(text_temp),
            QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
        if confirmation != QtGui.QMessageBox.Yes:
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


class DUnderstandingVisual(QtGui.QDialog):
    def __init__(self, txt_questions):
        QtGui.QDialog.__init__(self)

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        textEdit = QtGui.QTextEdit()
        textEdit.setReadOnly(True)
        textEdit.setFixedSize(600, 600)
        textEdit.setText(txt_questions)
        layout.addWidget(textEdit)

        button = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        button.accepted.connect(self.accept)
        layout.addWidget(button)

        self.adjustSize()
        self.setWindowTitle(le2mtrans(u"Understanding questionnaire"))


class DEditGroups(QtGui.QDialog):
    def __init__(self, le2mserv, joueurs):
        QtGui.QDialog.__init__(self)

        self.le2mserv = le2mserv
        self.joueurs = joueurs
        self.group_size = 0

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        label_header = QtGui.QLabel(le2mtrans(u"Groups' formation"))
        label_header.setStyleSheet("font-weight: bold;")
        layout.addWidget(label_header)

        layout_size = QtGui.QHBoxLayout()
        layout.addLayout(layout_size)
        layout_size.addWidget(QtGui.QLabel(le2mtrans(u"Groups' size")))
        self.spinbox_size = QtGui.QSpinBox()
        self.spinbox_size.setMinimum(0)
        self.spinbox_size.setMaximum(99)
        self.spinbox_size.setSingleStep(1)
        self.spinbox_size.setFixedWidth(50)
        self.spinbox_size.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        layout_size.addWidget(self.spinbox_size)
        button_form_groups = QtGui.QPushButton(le2mtrans(u"Form groups"))
        button_form_groups.clicked.connect(self.form_groups)
        layout_size.addWidget(button_form_groups)
        layout_size.addSpacerItem(
            QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Expanding))

        grid_joueurs = QtGui.QGridLayout()
        layout.addLayout(grid_joueurs)
        self.groups = self.le2mserv.gestionnaire_groupes.get_groupes().keys()
        self.combos_joueurs = {}
        row, col = 0, 0
        for index, joueur in enumerate(self.joueurs):
            combo = QtGui.QComboBox()
            combo.addItems(self.groups)
            combo.setFixedWidth(200)
            try:
                combo.setCurrentIndex(self.groups.index(joueur.group))
            except ValueError:
                pass
            self.combos_joueurs[joueur] = combo
            grid_joueurs.addWidget(QtGui.QLabel(str(joueur)), row, col)
            grid_joueurs.addWidget(self.combos_joueurs[joueur], row, col+1)
            row += 1
            if row > 0 and row % 5 == 0:
                row = 0
                col += 2

        layout_buttons = QtGui.QHBoxLayout()
        layout.addLayout(layout_buttons)
        layout_buttons.addSpacerItem(
            QtGui.QSpacerItem(20 ,20, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Expanding))
        button_save = QtGui.QPushButton(le2mtrans(u"Save"))
        button_save.clicked.connect(self.save)
        layout_buttons.addWidget(button_save)
        button_close = QtGui.QPushButton(le2mtrans(u"Close"))
        button_close.clicked.connect(self.reject)
        layout_buttons.addWidget(button_close)

        self.adjustSize()
        self.setWindowTitle(le2mtrans(u"Edit groups"))

    def form_groups(self):
        self.group_size = self.spinbox_size.value()
        if self.group_size == 0:
            QtGui.QMessageBox.critical(
                self, le2mtrans(u"Warning"),
                le2mtrans(u"Impossible to form groups of size 0!"))
            return
        try:
            self.le2mserv.gestionnaire_groupes.former_groupes(
                self.joueurs, self.group_size, display=False)
        except ValueError as e:
            QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"), str(e))
            return
        else:
            self.groups = self.le2mserv.gestionnaire_groupes.get_groupes().keys()
            for joueur, combo in self.combos_joueurs.items():
                combo.clear()
                combo.addItems(self.groups)
                combo.setCurrentIndex(self.groups.index(joueur.group))

    def save(self):
        # confirmation
        confirmation = QtGui.QMessageBox.question(
            self, le2mtrans(u"Confirmation"),
            le2mtrans(u"Do you want to save the groups?"),
            QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
        if confirmation != QtGui.QMessageBox.Yes:
            return
        # check that groups are ok
        new_groups = dict()
        for joueur, combo in self.combos_joueurs.items():
            group_joueur = str(combo.currentText())
            if group_joueur not in new_groups:
                new_groups[group_joueur] = [joueur]
            else:
                new_groups[group_joueur].append(joueur)
        # test group size
        for group in new_groups.values():
            if len(group) != self.group_size:
                QtGui.QMessageBox.critical(
                    self, le2mtrans(u"Error"),
                    le2mtrans(u"At least one group has a size different "
                              u"from {}".format(self.group_size)))
                return
        # set group in player data
        for group, joueurs in new_groups.items():
            for j in joueurs:
                j.group = group
        # set group in gestionnaire_groupes
        self.le2mserv.gestionnaire_groupes.set_groupes(new_groups)
        self.le2mserv.gestionnaire_graphique.infoserv(
            self.le2mserv.gestionnaire_groupes.get_groupes_string())
        self.accept()


class DDisplayImages(QtGui.QDialog):
    def __init__(self, le2msrv, directory):
        QtGui.QDialog.__init__(self)

        self.le2msrv = le2msrv
        self.directory = directory
        self.images = [i for i in os.listdir(self.directory) if
                       i.endswith(".jpg") or i.endswith(".png")]
        self.images.sort()
        logger.debug("Images: {}".format(self.images))

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        self.label_image_path = QtGui.QLabel()
        layout.addWidget(self.label_image_path)

        self.label_image = QtGui.QLabel()
        layout.addWidget(self.label_image)
        if self.images:
            self._display_image(self.images[0])

        layout_buttons = QtGui.QHBoxLayout()
        self.button_previous = QtGui.QPushButton(le2mtrans(u"Previous"))
        self.button_next = QtGui.QPushButton(le2mtrans(u"Next"))
        self.button_send = QtGui.QPushButton(le2mtrans(u"Display on clients' screen"))
        self.button_close = QtGui.QPushButton(le2mtrans(u"Close clients' screen"))
        layout_buttons.addWidget(self.button_previous)
        layout_buttons.addWidget(self.button_next)
        layout_buttons.addWidget(self.button_send)
        layout_buttons.addWidget(self.button_close)
        layout_buttons.addSpacerItem(
            QtGui.QSpacerItem(2, 20, QtGui.QSizePolicy.Fixed,
                              QtGui.QSizePolicy.Expanding))
        layout.addLayout(layout_buttons)
        self.button_previous.clicked.connect(self._display_previous)
        self.button_next.clicked.connect(self._display_next)
        self.button_send.clicked.connect(self._display_on_clients)
        self.button_close.clicked.connect(self._close_clients_screen)

    def _display_image(self, image):
        self.current_image = image
        self.current_image_path = os.path.join(self.directory, self.current_image)
        self.label_image_path.setText(os.path.join(self.directory, self.images[0]))
        self.label_image.setPixmap(QtGui.QPixmap(self.current_image_path))

    def _display_previous(self):
        index_current = self.images.index(self.current_image)
        if index_current == 0:
            return
        else:
            self._display_image(self.images[index_current - 1])

    def _display_next(self):
        index_current = self.images.index(self.current_image)
        if index_current == len(self.images) - 1:
            return
        else:
            self._display_image(self.images[index_current + 1])

    def _display_on_clients(self):
        self.le2msrv.gestionnaire_experience.run_step(
            le2mtrans(u"Display image {}".format(self.current_image)),
            self.le2msrv.gestionnaire_joueurs.get_players("base"),
            "display_image", self.current_image_path)

    def _close_clients_screen(self):
        self.le2msrv.gestionnaire_experience.run_step(
            le2mtrans(u"Close clients' screen"),
            self.le2msrv.gestionnaire_joueurs.get_players("base"),
            "display_image", None)


class DDisplayVideo(QtGui.QDialog):
    def __init__(self, le2msrv, video_file):
        QtGui.QDialog.__init__(self)

        self.le2msrv = le2msrv
        self.video_file = video_file

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        label_video_path = QtGui.QLabel(str(self.video_file) + " " +
                                        le2mtrans(u"is ready to be played"))
        layout.addWidget(label_video_path)

        self.video_widget = Phonon.VideoWidget()
        layout.addWidget(self.video_widget)

        layout_buttons = QtGui.QHBoxLayout()
        self.pushbutton_play = QtGui.QPushButton(le2mtrans(u"Play"))
        self.pushbutton_play_on_clients = QtGui.QPushButton(
            le2mtrans(u"Play on the server and on clients' screen"))
        layout_buttons.addWidget(self.pushbutton_play)
        layout_buttons.addWidget(self.pushbutton_play_on_clients)
        layout_buttons.addSpacerItem(
            QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Fixed))
        layout.addLayout(layout_buttons)
        self.pushbutton_play.clicked.connect(self.play)
        self.pushbutton_play_on_clients.clicked.connect(self.play_on_clients)

    def play(self):
        media_src = Phonon.MediaSource(self.video_file)
        self.media_obj = Phonon.MediaObject()
        self.media_obj.setCurrentSource(media_src)
        Phonon.createPath(self.media_obj, self.video_widget)
        self.media_obj.play()


    def play_on_clients(self):
        self.le2msrv.gestionnaire_experience.run_step(
            le2mtrans(u"Display video") + u" {}".format(self.video_file),
            self.le2msrv.gestionnaire_joueurs.get_players("base"),
            "display_video", self.video_file)
        self.play()
