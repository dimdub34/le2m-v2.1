# -*- coding: utf-8 -*-

""" ============================================================================

This module contains all the dialog box used on the server side

============================================================================ """

# built-in
import os
import logging
import csv
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, QUrl, QString
from PyQt4.QtWebKit import QWebView
from PyQt4.phonon import Phonon

# le2m
from configuration import configparam as params
from configuration.configconst import HOMME, FEMME
from configuration.configvar import Experiment
from util.utili18n import le2mtrans
from server.servgui.servguisrc import (servguipartsload, servguipayoffs,
                                       servguipartsplayed)
from servguitablemodels import TableModelPaiements
from util.utilwidgets import WDice, WRandint, WHeadtail


logger = logging.getLogger("le2m")


class GuiGenres(QDialog):
    """
    This dialog box is used to select the men among the participants
    """
    def __init__(self, players_list, parent=None):
        super(GuiGenres, self).__init__(parent)

        # variables
        self.players_list = players_list

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # explanation
        self.label_explanation = QLabel()
        self.label_explanation.setText(
            le2mtrans(u"Please check the men and let the women unchecked."))
        self.layout.addWidget(self.label_explanation, 0, Qt.AlignCenter)

        # list of players
        self.players_list_view = QListView()
        self.players_model = QStandardItemModel()
        for j in self.players_list:
            item = QStandardItem(str(j))
            item.setCheckable(True)
            item.setEditable(False)
            if j.gender == HOMME:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.players_model.appendRow(item)
        self.players_list_view.setModel(self.players_model)
        self.players_list_view.setMinimumSize(350, 500)
        self.layout.addWidget(self.players_list_view, 0, Qt.AlignCenter)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttons.accepted.connect(self._accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

        self.setWindowTitle(le2mtrans(u"Set subjects' gender"))
        self.adjustSize()

    def _accept(self):
        for row in range(self.players_model.rowCount()):
            item = self.players_model.item(row)
            if item.checkState() == Qt.Checked:
                self.players_list[row].gender = HOMME
            else:
                self.players_list[row].gender = FEMME
        self.accept()


class GuiInformation(QDialog):
    """
    Dialog qui affiche du texte (format plain ou html).
    """
    def __init__(self, text, titre=le2mtrans(u"Information"), parent=None,
                 size=(450, 450), html=False):
        super(GuiInformation, self).__init__(parent)

        layout = QVBoxLayout(self)

        if html:
            browser = QTextBrowser(self)
            browser.setText(text)
            browser.setOpenExternalLinks(True)
            browser.setFixedSize(size[0], size[1])
            layout.addWidget(browser)
        else:
            textedit = QTextEdit()
            textedit.setReadOnly(True)
            textedit.setFixedSize(size[0], size[1])
            textedit.setText(text)
            layout.addWidget(textedit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setWindowTitle(titre)
        self.adjustSize()
        self.setFixedSize(self.size())


class GuiPartLoad(QDialog):
    def __init__(self, parent=None):
        super(GuiPartLoad, self).__init__(parent)

        self.ui = servguipartsload.Ui_Dialog()
        self.ui.setupUi(self)

        # parts list
        self.ui.label_explication.setText(
            le2mtrans(u"Please select in the list below the parts you want "
                      u"to load"))
        self.ui.listView.setToolTip(QString(
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

        self._model = QStandardItemModel()
        for p in partslist:
            item = QStandardItem(p)
            item.setCheckState(Qt.Unchecked)
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
        if item.checkState() == Qt.Checked:
            part = str(item.text())
            self.ui.label_basepath2.setText(
                os.path.join(params.getp("PARTSDIR"), part))
        elif item.checkState() == Qt.Unchecked:
            self.ui.label_basepath2.setText("...")
            i = 0
            while self._model.item(i):
                if self._model.item(i).checkState() == Qt.Checked:
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
        dirbase = str(QFileDialog.getExistingDirectory(
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
            if self._model.item(i).checkState() == Qt.Checked:
                parts.append(str(self._model.item(i).text()))
            i += 1
        if not parts:
            QMessageBox.critical(
                self,
                le2mtrans(u"Error"),
                le2mtrans(u"You must choose at least one part"))
            return

        # dirbase
        dirbase = unicode(self.ui.label_basepath2.text().toUtf8(), "utf-8")
        if not (dirbase and os.path.isdir(dirbase)):
            QMessageBox.critical(
                self,
                le2mtrans(u"Error"),
                le2mtrans(u"You must choose a directory in which to store the "
                          u"database"))
            return

        # basename
        basename = unicode(self.ui.lineEdit_nom_base.text().toUtf8(), "utf-8")
        if not basename:
            QMessageBox.critical(
                self,
                le2mtrans(u"Error"),
                le2mtrans(u"You must provide a database name"))
            return
        basename += u".sqlite"

        if len(parts) > 1:
            confirmation = QMessageBox.question(
                self, le2mtrans(u"Warning"),
                le2mtrans(u"You have selected several parts.\nNote that the "
                          u"database will be store in {d}.\n"
                          u"Please confirm that it is in this directory that "
                          u"you will store the database.".format(d=dirbase)),
                QMessageBox.No | QMessageBox.Yes)
            if confirmation != QMessageBox.Yes:
                return

        self._experiment = Experiment(
            parts, dirbase, basename, self.ui.checkBox_test.isChecked())
        logger.info("Experiment parameters: {}".format(self._experiment))
        self.accept()

    def get_expeinfos(self):
        return self._experiment


class GuiPartsPlayed(QDialog):
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
            QString(u"Sélectionner une ou plusieurs parties"))
        self.ui.listView_parties.setFixedSize(300, 350)
        self.ui.buttonBox.accepted.connect(self._set_parties_selectionnees)
        self.ui.buttonBox.rejected.connect(self.reject)

        self._model = QStandardItemModel()
        for partie in self._liste_parties:
            item = QStandardItem('{}'.format(partie))
            item.setCheckState(Qt.Checked)
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
            if item.checkState() == Qt.Checked:
                self._parties_selectionnees.append(str(item.text()))
        if not self._parties_selectionnees:
            QMessageBox.warning(self, u"Attention",
                                      u"Aucune partie sélectionnée")
            self.reject()
        self.accept()

    def get_parties_selectionnees(self):
        return self._parties_selectionnees


class GuiPayoffs(QDialog):
    """
    Fenetre qui affiche les gains de la partie
    Elle permet d'imprimer ces gains, de les enregistrer mais aussi de les
    faire afficher sur les postes clients
    """
    def __init__(self, le2mserv, partname, payoffs):
        super(GuiPayoffs, self).__init__()
        
        self.le2mserv = le2mserv
        self.partname = partname
        self.payoffs = payoffs

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # ----------------------------------------------------------------------
        # table
        # ----------------------------------------------------------------------
        
        self.table_view = QTableView()
        self.table_model = TableModelPaiements(self.payoffs)
        self.table_view.setModel(self.table_model)
        self.table_view.horizontalHeader().setResizeMode(
            QHeaderView.Stretch)
        self.layout.addWidget(self.table_view)
        
        # ----------------------------------------------------------------------
        # pushbuttons
        # ----------------------------------------------------------------------
        
        self.pushbutton_layout = QHBoxLayout()
        self.layout.addLayout(self.pushbutton_layout)
        
        self.pushbutton_print = QPushButton(le2mtrans(u"Print"))
        self.pushbutton_print.clicked.connect(self.print_content)
        self.pushbutton_layout.addWidget(self.pushbutton_print)
        
        self.pushbutton_save = QPushButton(le2mtrans(u"Save"))
        self.pushbutton_save.clicked.connect(self.save_content)
        self.pushbutton_layout.addWidget(self.pushbutton_save)
        
        self.pushbutton_display_remote = QPushButton(le2mtrans(u"Display on remotes"))
        self.pushbutton_display_remote.clicked.connect(self.display_on_remotes)
        self.pushbutton_layout.addWidget(self.pushbutton_display_remote)
        
        self.pushbutton_add_to_payoffs = QPushButton(le2mtrans(u"Add to final payoffs"))
        self.pushbutton_add_to_payoffs.clicked.connect(self.add_to_payoffs)
        self.pushbutton_layout.addWidget(self.pushbutton_add_to_payoffs)

        if self.partname == "base":
            self.setWindowTitle(le2mtrans(u"Payoffs for the experiment"))
            self.pushbutton_add_to_payoffs.setEnabled(False)
        else:
            self.setWindowTitle(le2mtrans(u"Payoffs of part {}").format(
                self.partname))

        self.setMinimumSize(500, 700)

    def print_content(self):
        """
        Print the table with the subjects' payoffs
        """
        if not self.payoffs:
            return
        html = u"<table align='center' border=1>\n<tr>" \
               u"<td align='center'><b>"
        html += le2mtrans(u"Hostname")
        html += u"</b></td>" \
                u"<td align='center'><b>"
        html += le2mtrans(u"Payoff")
        html += u"</b></td></tr>\n"
        for l in self.payoffs:
            html += u"<tr><td align='center'>{}</>" \
                    u"<td align='center'>{}&euro;</td>" \
                    u"</tr>\n".format(l[0], l[1])
        html += u"</table>\n"
        doc = QTextDocument()
        doc.setHtml(html)
        printer = QPrinter()
        dialog = QPrintDialog(printer)
        dialog.setModal(True)
        dialog.setWindowTitle(le2mtrans(u"Payoffs"))
        if dialog.exec_():
            doc.print_(printer)

    def save_content(self):
        """
        Open the dialog box for choosing/creating the location file and
        save the table in the csv format
        """
        if not self.payoffs:
            return
        fichier = QFileDialog.getSaveFileName(
            self, le2mtrans("Export payoffs in csv file"), ".",
            le2mtrans(u"csv file (*.csv)"))
        if fichier:
            with open(fichier, 'wb') as csvfile:
                csv_writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"',
                    quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(
                    [le2mtrans(u"Hostname"), le2mtrans(u"Payoff")])
                for ligne in self.payoffs:
                    csv_writer.writerow(ligne)

    def display_on_remotes(self):
        text_temp = le2mtrans(u"the experiment") if \
            self.partname == "base" else self.partname
        confirmation = QMessageBox.question(
            self, u"Confirmation",
            le2mtrans(u"Display the payoffs of {}?").format(text_temp),
            QMessageBox.No | QMessageBox.Yes)
        if confirmation != QMessageBox.Yes:
            return

        if self.partname == "base":
            self.le2mserv.gestionnaire_experience.display_finalscreen()
        else:
            self.le2mserv.gestionnaire_experience.display_payoffs_onremotes(
                self.partname)

    def add_to_payoffs(self):
        confirmation = QMessageBox.question(
            self,
            u"Confirmation",
            u"Ajouter les gains de la partie aux gains finaux?",
            QMessageBox.No | QMessageBox.Yes)
        if confirmation != QMessageBox.Yes:
            return
        self.le2mserv.gestionnaire_experience.add_tofinalpayoffs(
            self.partname)


class DWebview(QDialog):
    def __init__(self, html_file, title=u"Information", parent=None):
        QDialog.__init__(self, parent)

        layout = QVBoxLayout(self)

        self._webview = QWebView(self)
        self._webview.load(QUrl(html_file))
        layout.addWidget(self._webview)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setWindowTitle(title)
        self.adjustSize()


class DUnderstandingVisual(QDialog):
    def __init__(self, txt_questions):
        QDialog.__init__(self)

        layout = QVBoxLayout()
        self.setLayout(layout)

        textEdit = QTextEdit()
        textEdit.setReadOnly(True)
        textEdit.setFixedSize(600, 600)
        textEdit.setText(txt_questions)
        layout.addWidget(textEdit)

        button = QDialogButtonBox(QDialogButtonBox.Ok)
        button.accepted.connect(self.accept)
        layout.addWidget(button)

        self.adjustSize()
        self.setWindowTitle(le2mtrans(u"Understanding questionnaire"))


class DEditGroups(QDialog):
    def __init__(self, le2mserv, joueurs):
        QDialog.__init__(self)

        self.le2mserv = le2mserv
        self.joueurs = joueurs
        self.group_size = 0

        layout = QVBoxLayout()
        self.setLayout(layout)

        label_header = QLabel(le2mtrans(u"Groups' formation"))
        label_header.setStyleSheet("font-weight: bold;")
        layout.addWidget(label_header)

        layout_size = QHBoxLayout()
        layout.addLayout(layout_size)
        layout_size.addWidget(QLabel(le2mtrans(u"Groups' size")))
        self.spinbox_size = QSpinBox()
        self.spinbox_size.setMinimum(0)
        self.spinbox_size.setMaximum(99)
        self.spinbox_size.setSingleStep(1)
        self.spinbox_size.setFixedWidth(50)
        self.spinbox_size.setButtonSymbols(QSpinBox.NoButtons)
        layout_size.addWidget(self.spinbox_size)
        button_form_groups = QPushButton(le2mtrans(u"Form groups"))
        button_form_groups.clicked.connect(self.form_groups)
        layout_size.addWidget(button_form_groups)
        layout_size.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Expanding,
                              QSizePolicy.Expanding))

        grid_joueurs = QGridLayout()
        layout.addLayout(grid_joueurs)
        self.groups = self.le2mserv.gestionnaire_groupes.get_groupes().keys()
        self.combos_joueurs = {}
        row, col = 0, 0
        for index, joueur in enumerate(self.joueurs):
            combo = QComboBox()
            combo.addItems(self.groups)
            combo.setFixedWidth(200)
            try:
                combo.setCurrentIndex(self.groups.index(joueur.group))
            except ValueError:
                pass
            self.combos_joueurs[joueur] = combo
            grid_joueurs.addWidget(QLabel(str(joueur)), row, col)
            grid_joueurs.addWidget(self.combos_joueurs[joueur], row, col+1)
            row += 1
            if row > 0 and row % 5 == 0:
                row = 0
                col += 2

        layout_buttons = QHBoxLayout()
        layout.addLayout(layout_buttons)
        layout_buttons.addSpacerItem(
            QSpacerItem(20 ,20, QSizePolicy.Expanding,
                              QSizePolicy.Expanding))
        button_save = QPushButton(le2mtrans(u"Save"))
        button_save.clicked.connect(self.save)
        layout_buttons.addWidget(button_save)
        button_close = QPushButton(le2mtrans(u"Close"))
        button_close.clicked.connect(self.reject)
        layout_buttons.addWidget(button_close)

        self.adjustSize()
        self.setWindowTitle(le2mtrans(u"Edit groups"))

    def form_groups(self):
        self.group_size = self.spinbox_size.value()
        if self.group_size == 0:
            QMessageBox.critical(
                self, le2mtrans(u"Warning"),
                le2mtrans(u"Impossible to form groups of size 0!"))
            return
        try:
            self.le2mserv.gestionnaire_groupes.former_groupes(
                self.joueurs, self.group_size, display=False)
        except ValueError as e:
            QMessageBox.warning(
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
        confirmation = QMessageBox.question(
            self, le2mtrans(u"Confirmation"),
            le2mtrans(u"Do you want to save the groups?"),
            QMessageBox.No | QMessageBox.Yes)
        if confirmation != QMessageBox.Yes:
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
                QMessageBox.critical(
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


# ==============================================================================
# OPTIONS - RANDINT, ROLL A DICE & HEAD AND TAIL
# ==============================================================================


class DDice(QDialog):
    def __init__(self, parent):
        super(DDice, self).__init__(parent)

        layout = QVBoxLayout(self)
        self._widdice = WDice(parent=self)
        layout.addWidget(self._widdice)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Dice roller"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        if self._widdice.ui.pushButton_start.isEnabled():
            QMessageBox.warning(
                self, le2mtrans(u"Warning"),
                le2mtrans(u"You must roll the dice"))
            return
        self.accept()

    def get_dicevalue(self):
        return self._widdice.get_dicevalue()


class DRandint(QDialog):
    def __init__(self, parent):
        super(DRandint, self).__init__(parent)

        layout = QVBoxLayout(self)
        self._widrandint = WRandint(parent=self)
        layout.addWidget(self._widrandint)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Random number"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        if self._widrandint.ui.pushButton_start.isEnabled():
            QMessageBox.warning(
                self, le2mtrans(u"Warning"),
                le2mtrans(u"You must drawn a random number"))
            return
        self.accept()

    def get_value(self):
        return self._widrandint.get_value()


class DHeadtail(QDialog):
    def __init__(self, parent):
        super(DHeadtail, self).__init__(parent)

        layout = QVBoxLayout(self)
        self._widheadtail = WHeadtail(parent=self)
        layout.addWidget(self._widheadtail)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Head and Tail"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        if self._widheadtail.ui.pushButton_start.isEnabled():
            QMessageBox.warning(
                self, le2mtrans(u"Warning"),
                le2mtrans(u"You must play"))
            return
        self.accept()

    def get_value(self):
        return self._widheadtail.get_value()


# ==============================================================================
# DISPLAY IMAGES AND VIDEOS
# ==============================================================================


class DDisplayImages(QDialog):
    def __init__(self, le2msrv, directory):
        QDialog.__init__(self)

        self.le2msrv = le2msrv
        self.directory = directory
        self.images = [i for i in os.listdir(self.directory) if
                       i.endswith(".jpg") or i.endswith(".png")]
        self.images.sort()
        logger.debug("Images: {}".format(self.images))

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label_image_path = QLabel()
        layout.addWidget(self.label_image_path)

        self.label_image = QLabel()
        layout.addWidget(self.label_image)
        if self.images:
            self._display_image(self.images[0])

        layout_buttons = QHBoxLayout()
        self.button_previous = QPushButton(le2mtrans(u"Previous"))
        self.button_next = QPushButton(le2mtrans(u"Next"))
        self.button_send = QPushButton(le2mtrans(u"Display on clients' screen"))
        self.button_close = QPushButton(le2mtrans(u"Close clients' screen"))
        layout_buttons.addWidget(self.button_previous)
        layout_buttons.addWidget(self.button_next)
        layout_buttons.addWidget(self.button_send)
        layout_buttons.addWidget(self.button_close)
        layout_buttons.addSpacerItem(
            QSpacerItem(2, 20, QSizePolicy.Fixed,
                              QSizePolicy.Expanding))
        layout.addLayout(layout_buttons)
        self.button_previous.clicked.connect(self._display_previous)
        self.button_next.clicked.connect(self._display_next)
        self.button_send.clicked.connect(self._display_on_clients)
        self.button_close.clicked.connect(self._close_clients_screen)

    def _display_image(self, image):
        self.current_image = image
        self.current_image_path = os.path.join(self.directory, self.current_image)
        self.label_image_path.setText(os.path.join(self.directory, self.images[0]))
        self.label_image.setPixmap(QPixmap(self.current_image_path))

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


class DDisplayVideo(QDialog):
    def __init__(self, le2msrv, video_file):
        QDialog.__init__(self)

        self.le2msrv = le2msrv
        self.video_file = video_file

        layout = QVBoxLayout()
        self.setLayout(layout)

        label_video_path = QLabel(str(self.video_file) + " " +
                                        le2mtrans(u"is ready to be played"))
        layout.addWidget(label_video_path)

        self.video_widget = Phonon.VideoWidget()
        layout.addWidget(self.video_widget)

        layout_buttons = QHBoxLayout()
        self.pushbutton_play = QPushButton(le2mtrans(u"Play"))
        self.pushbutton_play_on_clients = QPushButton(
            le2mtrans(u"Play on the server and on clients' screen"))
        layout_buttons.addWidget(self.pushbutton_play)
        layout_buttons.addWidget(self.pushbutton_play_on_clients)
        layout_buttons.addSpacerItem(
            QSpacerItem(20, 5, QSizePolicy.Expanding,
                              QSizePolicy.Fixed))
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
