# -*- coding: utf-8 -*-

""" ============================================================================

This module contains the server screen.

============================================================================ """

# built-in
import sys
import os
from PyQt4 import QtGui, QtCore
import logging
import platform

# le2m
from util import utiltools
from util.utili18n import le2mtrans
from configuration import configparam as params
from configuration.configconst import HOMME, FEMME, PILE, FACE
from server.servparties import Partie
from server.servplayers import Joueur
from servguisrc import servguimain
from servguitablemodels import TableModelJoueurs
from servguidialogs import (GuiPartLoad, GuiPartsPlayed,
    GuiGenres, DDice, DRandint, DHeadtail, DWebview, GuiInformation,
    DUnderstandingVisual, DEditGroups, DDisplayImages, DDisplayVideo)
from creator import creator
from extractor import extractor
from questcomp import questcomp


logger = logging.getLogger("le2m")


# ==============================================================================
# MENUS
# ==============================================================================


class MenuFile(QtGui.QMenu):
    def __init__(self):
        super(MenuFile, self).__init__()

        self.setTitle(le2mtrans(u"File"))

        # ----------------------------------------------------------------------
        # load
        # ----------------------------------------------------------------------
        self.action_load = QtGui.QAction(le2mtrans(u"Load a part"), self)
        self.action_load.setShortcut(QtGui.QKeySequence("Ctrl+o"))
        self.action_load.setToolTip(
            le2mtrans(u"Open a dialog box with a list of parts you can load"))
        self.addAction(self.action_load)

        # ----------------------------------------------------------------------
        # quit
        # ----------------------------------------------------------------------
        self.action_quit = QtGui.QAction(le2mtrans(u"Quit"), self)
        self.action_quit.setShortcut(QtGui.QKeySequence("Ctrl+q"))
        self.action_quit.setToolTip(le2mtrans(u"Exit the application"))
        self.addAction(self.action_quit)


class MenuExperiment(QtGui.QMenu):
    def __init__(self):
        super(MenuExperiment, self).__init__()

        self.setTitle(le2mtrans(u"Experiment"))

        # ----------------------------------------------------------------------
        # welcome
        # ----------------------------------------------------------------------
        self.action_welcome = QtGui.QAction(
            le2mtrans(u"Display welcome screen"), self)
        self.action_welcome.setToolTip(
            le2mtrans(u"Display the welcome screen on participants' screen"))
        self.addAction(self.action_welcome)

        # ----------------------------------------------------------------------
        # understanding questionnaire
        # ----------------------------------------------------------------------
        self.action_understand_load = QtGui.QAction(
            le2mtrans(u"Load an understanding questionnaire"), self)
        self.action_understand_load.setToolTip(
            le2mtrans(u"Open a dialog box to select an understanding "
                      u"questionnaire (xml file)"))
        self.addAction(self.action_understand_load)

        self.action_understand_run = QtGui.QAction(
            le2mtrans(u"Start the loaded understanding questionnaire"), self)
        self.action_understand_run.setToolTip(
            le2mtrans(u"Start the loaded understanding questionnaire"))
        self.addAction(self.action_understand_run)

        # ----------------------------------------------------------------------
        # final questionnaire
        # ----------------------------------------------------------------------
        self.action_finalquest = QtGui.QAction(
            le2mtrans(u"Display the final questionnaire"), self)
        self.action_finalquest.setToolTip(
            le2mtrans(u"Display the final questionnaire on participants' "
                      u"screen"))
        self.addAction(self.action_finalquest)

        # ----------------------------------------------------------------------
        # final questionnaire
        # ----------------------------------------------------------------------
        self.action_payoffs = QtGui.QAction(le2mtrans(u"Payoffs"), self)
        self.action_payoffs.setToolTip(
            le2mtrans(u"Display a dialog box with the payoffs of each player"))
        self.addAction(self.action_payoffs)


class MenuPart(QtGui.QMenu):
    def __init__(self):
        super(MenuPart, self).__init__()

        self.setTitle(le2mtrans(u"Part"))


class MenuEdit(QtGui.QMenu):
    def __init__(self):
        super(MenuEdit, self).__init__()
        
        self.setTitle(le2mtrans(u"Edit"))
        
        self.action_clear_server_list = QtGui.QAction(
            le2mtrans(u"Clear the server list"), self)
        self.action_clear_server_list.setToolTip(
            le2mtrans(u"Clear the server list"))
        self.addAction(self.action_clear_server_list)
        
        self.action_clear_client_list = QtGui.QAction(
            le2mtrans(u"Clear the client list"), self)
        self.action_clear_client_list.setToolTip(
            le2mtrans(u"Clear the client list"))
        self.addAction(self.action_clear_client_list)


class MenuOptions(QtGui.QMenu):
    def __init__(self):
        super(MenuOptions, self).__init__()

        self.setTitle(u"Options")

        self.action_stop_repetitions = QtGui.QAction(
            le2mtrans(u"Stop after this period"), self)
        self.action_stop_repetitions.setToolTip(
            le2mtrans(u"Clic on this menu to stop the part after this period"))
        self.action_stop_repetitions.setCheckable(True)
        self.addAction(self.action_stop_repetitions)

        self.action_edit_groups = QtGui.QAction(
            le2mtrans(u"Edit groups"), self)
        self.addAction(self.action_edit_groups)

        self.action_gender = QtGui.QAction(
            le2mtrans(u"Set participants gender in the application"), self)
        self.action_gender.setToolTip(
            le2mtrans(u"Display a dialog box that allows to set the gender of "
                      u"each remote (participant)"))
        self.addAction(self.action_gender)


class MenuTools(QtGui.QMenu):
    def __init__(self):
        super(MenuTools, self).__init__()

        self.setTitle(le2mtrans(u"Tools"))

        # ----------------------------------------------------------------------
        # creator
        # ----------------------------------------------------------------------
        self.action_creator = QtGui.QAction(
            le2mtrans(u"Create a new part"), self)
        self.action_creator.setToolTip(
            le2mtrans(u"Display a dialog box in which you can configure the "
                      u"part to create"))
        self.action_creator.triggered.connect(creator.creator)
        self.addAction(self.action_creator)

        # ----------------------------------------------------------------------
        # extractor
        # ----------------------------------------------------------------------
        self.action_extractor = QtGui.QAction(
            le2mtrans(u"Extract some experimental data"), self)
        self.action_extractor.setToolTip(
            le2mtrans(u"Open a dialog box for selection an sqlite file to "
                      u"extract"))
        self.action_extractor.triggered.connect(extractor.extractor)
        self.addAction(self.action_extractor)

        # ----------------------------------------------------------------------
        # understanding questionnaire creation
        # ----------------------------------------------------------------------
        self.action_questcomp = QtGui.QAction(
            le2mtrans(u"Create/Edit an understanding questionnaire"),
            self)
        self.action_questcomp.setToolTip(
            le2mtrans(u"Open a dialog box that allows to create or edit an "
                      u"understanding questionnaire"))
        self.action_questcomp.triggered.connect(questcomp.questcomp)
        self.addAction(self.action_questcomp)

        self.action_display_image = QtGui.QAction(
            le2mtrans(u"Display images on clients' screen"), self)
        self.action_display_image.setToolTip(
            le2mtrans(u"You have to select a directory with images and it will "
                      u"display it on client's screen. Be careful the "
                      u"directory has to been accessible by client through the "
                      u"network"))
        self.addAction(self.action_display_image)

        self.action_display_video = QtGui.QAction(
            le2mtrans(u"Display a video on clients' screen"), self)
        self.action_display_video.setToolTip(le2mtrans(
            u"Select a video and a dialog will open. You will be able to "
            u"display the video either on your screen or on the clients' "
            u"screen. Be careful the video file has to be accessible by the "
            u"clients through the network."))
        self.addAction(self.action_display_video)

        # ----------------------------------------------------------------------
        # random draws: dice, head and tail, number
        # ----------------------------------------------------------------------
        self.action_dice = QtGui.QAction(le2mtrans(u"Dice roller"), self)
        self.action_dice.setToolTip(le2mtrans(u"Roll a dice"))
        self.addAction(self.action_dice)

        self.action_randint = QtGui.QAction(le2mtrans(u"Random number"), self)
        self.action_randint.setToolTip(le2mtrans(u"Drawn a random number"))
        self.addAction(self.action_randint)

        self.action_head_and_tail = QtGui.QAction(
            le2mtrans(u"Head and Tail"), self)
        self.action_head_and_tail.setToolTip(le2mtrans(u"Play head and tail"))
        self.addAction(self.action_head_and_tail)


class MenuHelp(QtGui.QMenu):
    def __init__(self):
        super(MenuHelp, self).__init__()

        self.setTitle(le2mtrans(u"About"))

        self.action_help = QtGui.QAction(le2mtrans(u"Help"), self)
        self.action_help.setToolTip(
            le2mtrans(u"Display a window with a text of help"))
        self.addAction(self.action_help)

        self.action_about = QtGui.QAction(le2mtrans(u"About"), self)
        self.addAction(self.action_about)


# ==============================================================================
# TABS
# ==============================================================================


class TabInformations(QtGui.QWidget):
    def __init__(self):
        super(TabInformations, self).__init__()

        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        self.label_soft = QtGui.QLabel("LE2M")
        self.label_soft.setStyleSheet("color: brown; font-weight: bold;font-size:40px;")
        self.layout.addWidget(self.label_soft)

        self.layout.addSpacerItem(
            QtGui.QSpacerItem(5, 20, QtGui.QSizePolicy.Fixed,
                              QtGui.QSizePolicy.Expanding))

        self.img_layout = QtGui.QHBoxLayout()
        self.img_layout.addSpacerItem(
            QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Fixed))
        self.img = QtGui.QPixmap()
        self.img.load(params.getp("LABPICTURE"))
        self.img_label = QtGui.QLabel()
        self.img_label.setPixmap(self.img)
        self.img_layout.addWidget(self.img_label)
        self.img_layout.addSpacerItem(
            QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Fixed))
        self.layout.addLayout(self.img_layout)

        self.layout.addSpacerItem(
            QtGui.QSpacerItem(5, 20, QtGui.QSizePolicy.Fixed,
                              QtGui.QSizePolicy.Expanding))

        self.label_infos = QtGui.QLabel()
        self.label_infos.setText(
            "OS: {} {} | Python version: {}".format(
                platform.uname()[0], platform.uname()[2],
                sys.version.split()[0]))
        self.layout.addWidget(self.label_infos)


class TabClients(QtGui.QWidget):
    def __init__(self):
        super(TabClients, self).__init__()

        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        self.label_connected = QtGui.QLabel(
            le2mtrans(u"Nb. connected") + u": 0")
        self.layout.addWidget(self.label_connected)

        self.clients_table = QtGui.QTableView()
        self.layout.addWidget(self.clients_table)
        self.clients_table_model = TableModelJoueurs()
        self.clients_table.setModel(self.clients_table_model)
        self.clients_table.horizontalHeader().\
            setResizeMode(QtGui.QHeaderView.Stretch)
        self.clients_table.horizontalHeader().setClickable(True)
        self.clients_table.horizontalHeader().sectionClicked[int]. \
            connect(self.clients_table_model.inverse)


class TabLists(QtGui.QWidget):
    def __init__(self):
        super(TabLists, self).__init__()
        
        self.layout = QtGui.QHBoxLayout()
        self.setLayout(self.layout)
        
        # ----------------------------------------------------------------------
        # server
        # ----------------------------------------------------------------------
        self.list_server_layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.list_server_layout)
        self.label_list_server = QtGui.QLabel(le2mtrans(u"Server"))
        self.list_server_layout.addWidget(self.label_list_server)
        self.list_server = QtGui.QListWidget()
        self.list_server_layout.addWidget(self.list_server)
        
        # ----------------------------------------------------------------------
        # client
        # ----------------------------------------------------------------------
        self.list_client_layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.list_client_layout)
        self.label_list_client = QtGui.QLabel(le2mtrans(u"Client"))
        self.list_client_layout.addWidget(self.label_list_client)
        self.list_client = QtGui.QListWidget()
        self.list_client_layout.addWidget(self.list_client)

        # ----------------------------------------------------------------------
        # wait
        # ----------------------------------------------------------------------
        self.list_wait_layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.list_wait_layout)
        self.label_list_wait = QtGui.QLabel(le2mtrans(u"Wait"))
        self.list_wait_layout.addWidget(self.label_list_wait)
        self.list_wait = QtGui.QListWidget()
        self.list_wait.setMaximumWidth(350)
        self.list_wait_layout.addWidget(self.list_wait)


# ==============================================================================
# MAIN WINDOW
# ==============================================================================


class MainWindow(QtGui.QMainWindow):
    def __init__(self, le2msrv):
        super(MainWindow, self).__init__()

        self.le2msrv = le2msrv
        self.red_icon = QtGui.QIcon(os.path.join(params.getp("IMGDIR"), "red.png"))
        self.green_icon = QtGui.QIcon(os.path.join(params.getp("IMGDIR"), "green.png"))
        self.players_wait = list()

        # ----------------------------------------------------------------------
        # menus
        # ----------------------------------------------------------------------
        self.menu_bar = self.menuBar()
        self.menu_file = MenuFile()
        self.menu_bar.addMenu(self.menu_file)
        self.menu_experiment = MenuExperiment()
        self.menu_bar.addMenu(self.menu_experiment)
        self.menu_part = MenuPart()
        self.menu_bar.addMenu(self.menu_part)
        self.menu_edit = MenuEdit()
        self.menu_bar.addMenu(self.menu_edit)
        self.menu_options = MenuOptions()
        self.menu_bar.addMenu(self.menu_options)
        self.menu_tools = MenuTools()
        self.menu_bar.addMenu(self.menu_tools)
        self.menu_help = MenuHelp()
        self.menu_bar.addMenu(self.menu_help)

        # ----------------------------------------------------------------------
        # main widget
        # ----------------------------------------------------------------------
        self.main_widget = QtGui.QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QtGui.QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # ----------------------------------------------------------------------
        # tabs
        # ----------------------------------------------------------------------
        self.tab_widget = QtGui.QTabWidget()
        self.layout.addWidget(self.tab_widget)
        self.tab_infos = TabInformations()
        self.tab_infos.label_infos.setText(
            self.tab_infos.label_infos.text() +
            u" | Hostname: {} | IP: {}".format(
                self.le2msrv.hostname, self.le2msrv.ip))
        self.tab_widget.addTab(self.tab_infos, le2mtrans(u"Informations"))
        self.tab_clients = TabClients()
        self.tab_widget.addTab(self.tab_clients, le2mtrans(u"Clients"))
        self.tab_lists = TabLists()
        self.tab_widget.addTab(self.tab_lists, le2mtrans(u"Lists"))

        # ----------------------------------------------------------------------
        # connections
        # ----------------------------------------------------------------------
        # menu_file
        self.menu_file.action_load.triggered.connect(self.load_parts)
        self.menu_file.action_quit.triggered.connect(self.close)

        # menu_experiment
        self.menu_experiment.action_welcome.triggered.connect(
            self.display_welcome)
        self.menu_experiment.action_understand_load.triggered.connect(
            self.load_questcomp)
        self.menu_experiment.action_understand_run.triggered.connect(
            self.start_questcomp)
        self.menu_experiment.action_finalquest.triggered.connect(
            self.display_final_questionnaire)
        self.menu_experiment.action_payoffs.triggered.connect(
            lambda _: self.le2msrv.gestionnaire_experience.
                display_payoffs_onserver("base"))

        # menu_edit
        self.menu_edit.action_clear_server_list.triggered.connect(
            self.tab_lists.list_server.clear)
        self.menu_edit.action_clear_client_list.triggered.connect(
            self.tab_lists.list_client.clear)

        # menu_options
        self.menu_options.action_gender.triggered.connect(self.edit_genders)
        self.menu_options.action_edit_groups.triggered.connect(self.edit_groups)
        self.menu_options.action_stop_repetitions.triggered.connect(
            self.stop_repetitions)

        # menu_tools
        self.menu_tools.action_display_image.triggered.connect(self.display_images)
        self.menu_tools.action_display_video.triggered.connect(self.display_video)
        self.menu_tools.action_dice.triggered.connect(self.roll_dice)
        self.menu_tools.action_randint.triggered.connect(self.randint)
        self.menu_tools.action_head_and_tail.triggered.connect(self.head_and_tail)

        # menu_help
        self.menu_help.action_help.triggered.connect(self.display_help)
        self.menu_help.action_about.triggered.connect(self.display_about)

        # signals
        self.le2msrv.gestionnaire_joueurs.playeradded[object, int].connect(
            self.add_player_to_tab_clients)
        self.le2msrv.gestionnaire_joueurs.playerremoved[object, int].connect(
            self.remove_player_from_tab_clients)

    # --------------------------------------------------------------------------
    # slots
    # --------------------------------------------------------------------------
    # menu_file
    @QtCore.pyqtSlot()
    def load_parts(self):
        if self.le2msrv.gestionnaire_base.is_created():
            QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"),
                le2mtrans(u"The database is already created, you therefore "
                          u"cannot load another part. If you want to, you need "
                          u"to restart the application"))
            return
        screen_parts = GuiPartLoad(self)
        if screen_parts.exec_():
            self.le2msrv.gestionnaire_experience.load_experiment(
                screen_parts.get_expeinfos())
        else:
            return

    # menu_experiment
    @QtCore.pyqtSlot()
    def display_welcome(self):
        """
        Display the welcome screen on remotes
        """
        reply = QtGui.QMessageBox.question(
            self,
            le2mtrans(u'Confirmation'),
            le2mtrans(u"Display the welcome screen on remotes?"),
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
        )
        if reply != QtGui.QMessageBox.Yes:
            return
        self.le2msrv.gestionnaire_experience.display_welcome()

    @QtCore.pyqtSlot()
    def load_questcomp(self):
        """
        Récupère le fichier xml de questionnaire de compréhension et le
        traite
        :return:
        """
        xmlfile = str(
            QtGui.QFileDialog.getOpenFileName(
                self,
                le2mtrans(u"Select the understanding questionnaire to load"),
                "", le2mtrans(u"xml file (*.xml)")))
        if not xmlfile:
            return
        else:
            self.questcomp = questcomp.get_questions(xmlfile)
            if not self.questcomp:
                return

            txt = u""
            for q in self.questcomp:
                txt += u"{}\n\n".format(q)
            screen = DUnderstandingVisual(txt)
            screen.exec_()
            self.add_list_server(
                le2mtrans(u"Understanding questionnaire loaded "
                          u"({} questions)").format(len(self.questcomp)))

    @QtCore.pyqtSlot()
    def start_questcomp(self):
        """
        Start the understanding questionnaire
        """
        if not self.questcomp:
            QtGui.QMessageBox.warning(
                self,
                le2mtrans(u"Warning"),
                le2mtrans(u"Please load an understanding questionnaire"))
            return
        if not self.le2msrv.gestionnaire_base.is_created():
            QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"),
                le2mtrans(u"The understanding questionnaire cannot be started "
                          u"before the database is created. You first has to "
                          u"load at least one part."))
            return
        reply = QtGui.QMessageBox.question(
            self,
            le2mtrans(u'Confirmation'),
            le2mtrans(u"Please confirm you want to start the understanding "
                      u"questionnaire?"),
            QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
        if reply != QtGui.QMessageBox.Yes:
            return
        self.le2msrv.gestionnaire_experience.start_questcomp(self._questcomp)

    @QtCore.pyqtSlot()
    def display_final_questionnaire(self):
        """
        Display the final questionnaire on remotes
        """
        if not self.le2msrv.gestionnaire_base.is_created():
            QtGui.QMessageBox.warning(
                self,
                le2mtrans(u"Warning"),
                le2mtrans(u"There is no database yet. You first need to "
                          u"load at least one part."))
            return
        confirmation = QtGui.QMessageBox.question(
            self,
            le2mtrans(u"Confirmation"),
            le2mtrans(u"Start the final questionnaire?"),
            QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
        if confirmation != QtGui.QMessageBox.Ok:
            return
        self.le2msrv.gestionnaire_experience.display_finalquestionnaire()

    # menu_options
    @QtCore.pyqtSlot()
    def edit_genders(self):
        """
        Display a dialog for setting the gender of each subject (by remote)
        """
        players = self.le2msrv.gestionnaire_joueurs.get_players()
        gender_screen = GuiGenres(players, self)
        if gender_screen.exec_():
            self.le2msrv.gestionnaire_graphique.infoserv(
                [le2mtrans(u"Genders"), le2mtrans(u"Men")])
            self.le2msrv.gestionnaire_graphique.infoserv(
                map(str, [p for p in players if p.gender == HOMME]))
            self.le2msrv.gestionnaire_graphique.infoserv(le2mtrans(u"Women"))
            self.le2msrv.gestionnaire_graphique.infoserv(
                map(str, [p for p in players if p.gender == FEMME]))

    @QtCore.pyqtSlot()
    def edit_groups(self):
        joueurs = self._le2mserv.gestionnaire_joueurs.get_players()
        if not joueurs:
            QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"),
                le2mtrans(u"There is no player connected"))
            return
        dialog_edit_groups = DEditGroups(
            self.le2msrv,joueurs)
        dialog_edit_groups.exec_()

    # menu_tools
    @QtCore.pyqtSlot()
    def display_images(self):
        directory = QtGui.QFileDialog.getExistingDirectory(
            self, le2mtrans(u"Select the directory that contains the images "
                            u"to display"), "", QtGui.QFileDialog.ShowDirsOnly)
        if directory is None or str(directory) == '':
            return
        directory = str(directory)
        logger.debug("_display_images: directory: {}".format(directory))
        self.dialog_display_images = DDisplayImages(self.le2msrv, directory)
        self.dialog_display_images.show()

    @QtCore.pyqtSlot()
    def display_video(self):
        video_file = str(QtGui.QFileDialog.getOpenFileName(
            self, le2mtrans(u"Select a video file")))
        if video_file:
            self.dialog_display_video = DDisplayVideo(self.le2msrv, video_file)
            self.dialog_display_video.show()

    @QtCore.pyqtSlot()
    def roll_dice(self):
        screen = DDice(self)
        if screen.exec_():
            self.le2msrv.gestionnaire_graphique.infoserv(
                le2mtrans(u"Dice value: {}".format(screen.get_dicevalue())))

    @QtCore.pyqtSlot()
    def randint(self):
        screen = DRandint(self)
        if screen.exec_():
            self.le2msrv.gestionnaire_graphique.infoserv(
                le2mtrans(u"Random number: {}".format(screen.get_value())))

    @QtCore.pyqtSlot()
    def head_and_tail(self):
        screen = DHeadtail(self)
        if screen.exec_():
            self.le2msrv.gestionnaire_graphique.infoserv(
                le2mtrans(u"Head and tail: {}".format(
                    le2mtrans(u"Head") if screen.get_value() == FACE else
                    le2mtrans(u"Tail"))))

    # menu_help
    @QtCore.pyqtSlot()
    def display_help(self):
        """
        Display a dialog with some help on le2m
        """
        help_file = os.path.join(params.getp("HTMLDIR"),
                                    "le2m_aide.html")
        webscreen = DWebview(
            help_file, title=le2mtrans(u"Help"), parent=self)
        webscreen.show()

    @QtCore.pyqtSlot()
    def display_about(self):
        """
        Display a dialog with some infos about the authors of le2m
        """
        the_file = os.path.join(
            params.getp("HTMLDIR"), "le2m_auteurs.html")
        screen = GuiInformation(
            parent=self, titre=le2mtrans(u"Developers"), size=(450, 180),
            html=True, text=utiltools.get_contenu_fichier(the_file))
        screen.show()

    # signals
    @QtCore.pyqtSlot(object, int)
    def add_player_to_tab_clients(self, player, nbplayers):
        self.tab_clients.clients_table_model.ajouter_joueur(player)
        self.tab_clients.label_connected.setText(
            le2mtrans(le2mtrans(u"Nb. connected") + u": {}".format(nbplayers)))

    @QtCore.pyqtSlot(object, int)
    def remove_player_from_tab_clients(self, player, nbplayers):
        self.tab_clients.clients_table_model.enlever_joueur(player)
        self.tab_clients.label_connected.setText(
            le2mtrans(le2mtrans(u"Nb. connected") + u": {}".format(nbplayers)))

    @QtCore.pyqtSlot()
    def stop_repetitions(self):
        if self.menu_options.action_stop_repetitions.isChecked():
            self.le2msrv.gestionnaire_experience.stop_repetitions = True
            self.menu_options.action_stop_repetitions.setText(
                le2mtrans(u"The part will stop after this period"))
        else:
            self.le2msrv.gestionnaire_experience.stop_repetitions = False
            self.menu_options.action_stop_repetitions.setText(
                le2mtrans(u"Stop the part after this period "))

    # --------------------------------------------------------------------------
    # methods
    # --------------------------------------------------------------------------

    def closeEvent(self, event):
        """
        Ask a confirmation before closing
        """
        reply = QtGui.QMessageBox.question(
            self,
            le2mtrans(u'Confirmation'),
            le2mtrans(u"Are you sure you want to exit?"),
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.le2msrv.arreter()
            event.accept()
        else:
            event.ignore()

    def add_list_server(self, txt, **kwargs):
        if txt:
            logger.info(txt)
        try:
            item = QtGui.QListWidgetItem(QtCore.QString(txt))
        except TypeError:
            item = QtGui.QListWidgetItem(QtCore.QString(u""))
        if txt and kwargs:
            item.setForeground(QtGui.QColor(kwargs.get("fg", "black")))
            item.setBackground(QtGui.QColor(kwargs.get("bg", "white")))
        self.tab_lists.list_server.addItem(item)

    def add_list_client(self, txt, **kwargs):
        if txt:
            logger.info(txt)
        try:
            item = QtGui.QListWidgetItem(QtCore.QString(txt))
        except TypeError:
            item = QtGui.QListWidgetItem(QtCore.QString(u""))
        if txt and kwargs:
            item.setForeground(QtGui.QColor(kwargs.get("fg", "black")))
            item.setBackground(QtGui.QColor(kwargs.get("bg", "white")))
        self.tab_lists.list_client.addItem(item)

    def set_wait_mode(self, list_players):
        """
        Display a colored icon beside the hostname to see whether the remote
        has a decided or not yet
        :param list_players: either a list of players (or parts) or only one
         element (player or part)
        """
        self.tab_lists.list_wait.clear()
        del self.players_wait[:]
        # if the argument is a list
        if isinstance(list_players, list):
            for p in list_players:
                e = QtGui.QListWidgetItem(self.red_icon, u"")
                if isinstance(p, Partie):
                    self.players_wait.append(p.joueur)
                    e.setText(repr(p.joueur))
                elif isinstance(p, Joueur):
                    self.players_wait.append(p)
                    e.setText(repr(p))
                self.tab_lists.list_wait.addItem(e)
        # if the argument is only one object
        else:
            e = QtGui.QListWidgetItem(self.red_icon, u"")
            if isinstance(list_players, Partie):
                self.players_wait.append(list_players.joueur)
                e.setText(repr(list_players.joueur))
            elif isinstance(list_players, Joueur):
                self.players_wait.append(list_players)
                e.setText(repr(list_players))
            self.tab_lists.list_wait.addItem(e)

    def remove_wait_mode(self, list_players):
        """
        Change the icon color to green, meaning that the remote has taken
        his decision
        :param list_players: either a list of players (or parts) or only one
         element (player or part)
        """
        if isinstance(list_players, list):
            for p in list_players:
                try:
                    index = self.players_wait.index(p)
                except ValueError as e:
                    logger.warning(
                        le2mtrans(u"Problem with remove_waitmode: "
                                  u"{msg}").format(e.message))
                else:
                    self.tab_lists.list_wait.item(index).setIcon(
                        self.green_icon)
        else:
            try:
                index = self.players_wait.index(list_players)
            except ValueError as e:
                logger.warning(
                    le2mtrans(u"Problem with remove_waitmode: "
                              u"{msg}").format(e.message))
            else:
                self.tab_lists.list_wait.item(index).setIcon(self.green_icon)

# ==============================================================================
# OLD
# ==============================================================================
# def _add_list(txt, the_list, **kwargs):
#         if txt:
#             logger.info(txt)
#         item = QtGui.QListWidgetItem(QtCore.QString(txt))
#         if txt and kwargs:
#             item.setForeground(QtGui.QColor(kwargs.get("fg", "black")))
#             item.setBackground(QtGui.QColor(kwargs.get("bg", "white")))
#         the_list.addItem(item)


# class GuiServeur(QtGui.QMainWindow):
#
#     def __init__(self, le2mserv):
#         super(GuiServeur, self).__init__()
#
#         self._le2mserv = le2mserv
#         self._questcomp = None
#
#         self.ui = servguimain.Ui_EcranServeur()
#         self.ui.setupUi(self)
#         self._create_menus()
#
#         self.ui.label_le2m.setText(
#             le2mtrans(u"LE2M\nExperimental Economics Software of Montpellier"))
#         self.ui.label_le2m.setStyleSheet("color: brown;")
#
#         # tabs
#         self.ui.onglets.setTabText(self.ui.onglets.indexOf(self.ui.tabInfos),
#                                    le2mtrans(u"Informations"))
#         self.ui.onglets.setTabText(self.ui.onglets.indexOf(self.ui.tabClients),
#                                    le2mtrans(u"Remotes"))
#         self.ui.onglets.setTabText(self.ui.onglets.indexOf(
#             self.ui.tabExperience), le2mtrans(u"Experiment"))
#
#         # picture on the first tab ---------------------------------------------
#         # try:
#         #     img_labo_pix = QtGui.QPixmap(params.getp("LABLOGO"))
#         #     self.ui.label_logo_laboratoire.setPixmap(img_labo_pix)
#         # except IOError:
#         #     logger.warning(u"Error while loading LABLOGO picture")
#         #     self.ui.label_logo_laboratoire.setText(
#         #         le2mtrans(u"Here the logo of the lab"))
#         try:
#             img_leem_pix = QtGui.QPixmap(params.getp("LABPICTURE"))
#             img_leem_pix.scaledToWidth(500)
#             self.ui.label_image_centre.setPixmap(img_leem_pix)
#         except IOError:
#             logger.warning(u"Error while loading LABPICTURE picture")
#             self.ui.label_image_centre.setText(
#                 le2mtrans(u"Here the main picture"))
#
#         # icons for the waiting mode -------------------------------------------
#         self._icon_rouge = QtGui.QIcon(
#             os.path.join(params.getp("IMGDIR"), "red.png"))
#         self._icon_vert = QtGui.QIcon(
#             os.path.join(params.getp("IMGDIR"), "green.png"))
#         self.ui.label_attente.setText(le2mtrans(u"Decisions"))
#         self._players_wait_mode = list()
#
#         # server infos ---------------------------------------------------------
#         self.ui.label_infos_serveur.setText(
#             u"OS: {} {} | Python version: {} | Hostname: {} | IP: {}".format(
#                 platform.uname()[0], platform.uname()[2],
#                 sys.version.split()[0], self._le2mserv.hostname,
#                 self._le2mserv.ip))
#
#         # table on the second tab with connected remotes -----------------------
#         # handle automatic and simulation modes as well as remotes' deconnection
#         self.ui.label_connectedremotes.setText(
#             le2mtrans(u"Connected remotes: 0"))
#         self.tableJoueurs = TableModelJoueurs()
#         self.ui.tv_clients_connectes.setModel(self.tableJoueurs)
#         self.ui.tv_clients_connectes.horizontalHeader().\
#             setResizeMode(QtGui.QHeaderView.Stretch)
#         self.ui.tv_clients_connectes.horizontalHeader().setClickable(True)
#         self.ui.tv_clients_connectes.horizontalHeader().sectionClicked[int]. \
#             connect(self.tableJoueurs.inverse)
#         self.ui.onglets.setCurrentIndex(0)
#
#         self.setWindowTitle(le2mtrans(u"LE2M"))
#
#     def _create_menus(self):
#         # file -----------------------------------------------------------------
#         self.menu_file = QtGui.QMenu(le2mtrans(u"File"), self.ui.menubar)
#         self.ui.menubar.addMenu(self.menu_file)
#         self.action_loadpart = QtGui.QAction(
#             le2mtrans(u"Load a part"), self.menu_file)
#         self.action_loadpart.setShortcut(QtGui.QKeySequence("Ctrl+o"))
#         self.action_loadpart.setToolTip(
#             le2mtrans(u"Open a dialog box with a list of parts you can load"))
#         self.action_loadpart.triggered.connect(self._load_parts)
#         self.menu_file.addAction(self.action_loadpart)
#
#         self.menu_file.addSeparator()
#
#         self.action_quit = QtGui.QAction(le2mtrans(u"Quit"), self.menu_file)
#         self.action_quit.setShortcut(QtGui.QKeySequence("Ctrl+q"))
#         self.action_quit.setToolTip(le2mtrans(u"Quit the application"))
#         self.action_quit.triggered.connect(self.close)
#         self.menu_file.addAction(self.action_quit)
#
#         # experiment -----------------------------------------------------------
#         self.menu_experiment = QtGui.QMenu(
#             le2mtrans(u"Experiment"), self.ui.menubar)
#         self.ui.menubar.addMenu(self.menu_experiment)
#         self.action_welcome = QtGui.QAction(
#             le2mtrans(u"Display welcome screen"), self.menu_experiment)
#         self.action_welcome.setToolTip(
#             le2mtrans(u"Display the welcome screen on participants' screen"))
#         self.action_welcome.triggered.connect(lambda _: self._display_welcome())
#         self.menu_experiment.addAction(self.action_welcome)
#
#         self.menu_experiment.addSeparator()
#
#         self.action_loadquestcomp = QtGui.QAction(
#             le2mtrans(u"Load an understanding questionnaire"),
#             self.menu_experiment)
#         self.action_loadquestcomp.setToolTip(
#             le2mtrans(u"Open a dialog box for selecting an understanding "
#                       u"questionnaire (xml file)"))
#         self.action_loadquestcomp.triggered.connect(self._load_questcomp)
#         self.menu_experiment.addAction(self.action_loadquestcomp)
#         self.action_startquestcomp = QtGui.QAction(
#             le2mtrans(u"Start the understanding questionnaire"),
#             self.menu_experiment)
#         self.action_startquestcomp.setToolTip(
#             le2mtrans(u"Start the loaded understanding questionnaire"))
#         self.action_startquestcomp.triggered.connect(self._start_questcomp)
#         self.menu_experiment.addAction(self.action_startquestcomp)
#
#         self.menu_experiment.addSeparator()
#
#         self.action_finalquest = QtGui.QAction(
#             le2mtrans(u"Display final questionnaire"), self.menu_experiment)
#         self.action_finalquest.setToolTip(
#             le2mtrans(u"Display the final questionnaire on participants' "
#                       u"screen"))
#         self.action_finalquest.triggered.connect(self._display_finalquest)
#         self.menu_experiment.addAction(self.action_finalquest)
#         self.action_payoffs = QtGui.QAction(
#             le2mtrans(u"Payoffs"), self.menu_experiment)
#         self.action_payoffs.setToolTip(
#             le2mtrans(u"Display a dialog box with the payoffs of each player"))
#         self.action_payoffs.triggered.connect(
#             lambda _: self._le2mserv.gestionnaire_experience.display_payoffs_onserver(
#                 "base"))
#         self.menu_experiment.addAction(self.action_payoffs)
#
#         # parts ----------------------------------------------------------------
#         self.menu_parts = QtGui.QMenu(le2mtrans(u"Parts"), self.ui.menubar)
#         self.ui.menubar.addMenu(self.menu_parts)
#
#         # edit -----------------------------------------------------------------
#         self.menu_edit = QtGui.QMenu(le2mtrans(u"Edit"), self.ui.menubar)
#         self.ui.menubar.addMenu(self.menu_edit)
#         self.action_clearsrv = QtGui.QAction(
#             le2mtrans(u"Clear server list"), self.menu_edit)
#         self.action_clearsrv.setToolTip(le2mtrans(u"Clear the server list"))
#         self.action_clearsrv.triggered.connect(self.ui.list_server.clear)
#         self.menu_edit.addAction(self.action_clearsrv)
#         self.action_clearclt = QtGui.QAction(
#             le2mtrans(u"Clear client list"), self.menu_edit)
#         self.action_clearclt.setToolTip(le2mtrans(u"Clear the client list"))
#         self.action_clearclt.triggered.connect(self.ui.list_client.clear)
#         self.menu_edit.addAction(self.action_clearclt)
#
#         # options --------------------------------------------------------------
#         self.menu_options = QtGui.QMenu(le2mtrans(u"Options"), self.ui.menubar)
#         self.ui.menubar.addMenu(self.menu_options)
#
#         self.action_stoprepetitions = QtGui.QAction(
#             le2mtrans(u"Stop the part after this period"), self.menu_options)
#         self.action_stoprepetitions.setToolTip(
#             le2mtrans(u"Clic on this menu to stop the part after this period"))
#         self.action_stoprepetitions.triggered.connect(self._stoprep)
#         self.action_stoprepetitions.setCheckable(True)
#         self.menu_options.addAction(self.action_stoprepetitions)
#
#         self.action_edit_groups = QtGui.QAction(
#             le2mtrans(u"Edit groups"), self.menu_options)
#         self.action_edit_groups.triggered.connect(self.edit_groups)
#         self.menu_options.addAction(self.action_edit_groups)
#
#         self.action_gender = QtGui.QAction(
#             le2mtrans(u"Set participants gender in the application"),
#             self.menu_options)
#         self.action_gender.setToolTip(
#             le2mtrans(u"Display a dialog box that allows to set the gender of "
#                       u"each remote (participant)"))
#         self.action_gender.triggered.connect(self._edit_genders)
#         self.menu_options.addAction(self.action_gender)
#
#         self.menu_experiment.addSeparator()
#
#         self.action_drawpart = QtGui.QAction(
#             le2mtrans(u"Draw a part among those played"), self.menu_experiment)
#         self.action_drawpart.triggered.connect(self._draw_part)
#         self.menu_options.addAction(self.action_drawpart)
#         self.action_displaypartspayoffs = QtGui.QAction(
#             le2mtrans(u"Display the payoffs of each part"),
#             self.menu_experiment)
#         self.action_displaypartspayoffs.setToolTip(
#             le2mtrans(u"Display a dialog box where you can choose for which "
#                       u"part you want to inform the participants about their "
#                       u"payoff"))
#         self.action_displaypartspayoffs.triggered.connect(
#             self._display_payoffs_partsSelection)
#         self.menu_options.addAction(self.action_displaypartspayoffs)
#
#         # tools ----------------------------------------------------------------
#         self.menu_tools = QtGui.QMenu(le2mtrans(u"Tools"), self.ui.menubar)
#         self.ui.menubar.addMenu(self.menu_tools)
#         self.action_creator = QtGui.QAction(
#             le2mtrans(u"Create a new part"), self.menu_tools)
#         self.action_creator.setToolTip(
#             le2mtrans(u"Display a dialog box in which you can configure the "
#                       u"part to create"))
#         self.action_creator.triggered.connect(creator.creator)
#         self.menu_tools.addAction(self.action_creator)
#         self.action_questcomp = QtGui.QAction(
#             le2mtrans(u"Create/Edit an understanding questionnaire"),
#             self.menu_tools)
#         self.action_questcomp.setToolTip(
#             le2mtrans(u"Open a dialog box that allows to create or edit an "
#                       u"understanding questionnaire"))
#         self.action_questcomp.triggered.connect(questcomp.questcomp)
#         self.menu_tools.addAction(self.action_questcomp)
#         self.action_extractor = QtGui.QAction(
#             le2mtrans(u"Extract some experimental data"), self.menu_tools)
#         self.action_extractor.setToolTip(
#             le2mtrans(u"Open a dialog box for selection an sqlite file to "
#                       u"extract"))
#         self.action_extractor.triggered.connect(extractor.extractor)
#         self.menu_tools.addAction(self.action_extractor)
#         self.action_display_image = QtGui.QAction(
#             le2mtrans(u"Display images on clients' screen"), self.menu_tools)
#         self.action_display_image.setToolTip(
#             le2mtrans(u"You have to select a directory with images and it will "
#                       u"display it on client's screen. Be careful the "
#                       u"directory has to been accessible by client through the "
#                       u"network"))
#         self.action_display_image.triggered.connect(self._display_images)
#         self.menu_tools.addAction(self.action_display_image)
#         self.action_display_video = QtGui.QAction(
#             le2mtrans(u"Display a video on clients' screen"), self.menu_tools)
#         self.action_display_video.setToolTip(le2mtrans(
#             u"Select a video and a dialog will open. You will be able to "
#             u"display the video either on your screen or on the clients' "
#             u"screen. Be careful the video file has to be accessible by the "
#             u"clients through the network."))
#         self.action_display_video.triggered.connect(self._display_video)
#         self.menu_tools.addAction(self.action_display_video)
#
#         self.menu_tools.addSeparator()
#
#         # random draws: dice, head and tail, number
#         self.action_dice = QtGui.QAction(
#             le2mtrans(u"Dice roller"), self.menu_tools)
#         self.action_dice.setToolTip(le2mtrans(u"Roll a dice"))
#         self.action_dice.triggered.connect(self._rolldice)
#         self.menu_tools.addAction(self.action_dice)
#
#         self.action_randint = QtGui.QAction(
#             le2mtrans(u"Random number"), self.menu_tools)
#         self.action_randint.setToolTip(le2mtrans(u"Drawn a random number"))
#         self.action_randint.triggered.connect(self._randint)
#         self.menu_tools.addAction(self.action_randint)
#
#         self.action_headtail = QtGui.QAction(
#             le2mtrans(u"Head and Tail"), self.menu_tools)
#         self.action_headtail.setToolTip(le2mtrans(u"Play head and tail"))
#         self.action_headtail.triggered.connect(self._headtail)
#         self.menu_tools.addAction(self.action_headtail)
#
#         # help -----------------------------------------------------------------
#         self.menu_help = QtGui.QMenu(le2mtrans(u"Help"), self.ui.menubar)
#         self.ui.menubar.addMenu(self.menu_help)
#         self.action_help = QtGui.QAction(le2mtrans(u"Help"), self.menu_help)
#         self.action_help.setToolTip(
#             le2mtrans(u"Display a window with a text of help"))
#         self.action_help.triggered.connect(self._display_help)
#         self.menu_help.addAction(self.action_help)
#         self.action_about = QtGui.QAction(le2mtrans(u"About"), self.menu_help)
#         self.action_about.triggered.connect(self._display_about)
#         self.menu_help.addAction(self.action_about)
#
#     def connect_slots(self):
#         self._le2mserv.gestionnaire_joueurs.playeradded[object, int].connect(
#             self._addplayer)
#         self._le2mserv.gestionnaire_joueurs.playerremoved[object, int].connect(
#             self._removeplayer)
#         self._le2mserv.gestionnaire_experience.stoprepetitions[bool].connect(
#             self._stoprepetitions)
#
#     def _load_parts(self):
#         if self._le2mserv.gestionnaire_base.is_created():
#             QtGui.QMessageBox.warning(
#                 self, le2mtrans(u"Warning"),
#                 le2mtrans(u"The database is already created, you therefore "
#                           u"cannot load another part. If you want to, you need "
#                           u"to restart the application"))
#             return
#         screenparts = GuiPartLoad(self)
#         if screenparts.exec_():
#             self._le2mserv.gestionnaire_experience.load_experiment(
#                 screenparts.get_expeinfos())
#         else:
#             return
#
#     def add_serverlist(self, texte, **kwargs):
#         _add_list(texte if texte else u"", self.ui.list_server, **kwargs)
#
#     def add_clientlist(self, texte, **kwargs):
#         _add_list(texte if texte else u"", self.ui.list_client, **kwargs)
#
#     def _display_welcome(self):
#         """
#         Display the welcome screen on remotes
#         """
#         reply = QtGui.QMessageBox.question(
#             self,
#             le2mtrans(u'Confirmation'),
#             le2mtrans(u"Display the welcome screen on remotes?"),
#             QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
#         )
#         if reply != QtGui.QMessageBox.Yes:
#             return
#         self._le2mserv.gestionnaire_experience.display_welcome()
#
#     def _display_images(self):
#         directory = QtGui.QFileDialog.getExistingDirectory(
#             self, le2mtrans(u"Select the directory that contains the images "
#                             u"to display"), "", QtGui.QFileDialog.ShowDirsOnly)
#         if directory is None or str(directory) == '':
#             return
#         directory = str(directory)
#         logger.debug("_display_images: directory: {}".format(directory))
#         self._le2mserv.gestionnaire_graphique.display_images(directory)
#
#     def _display_video(self):
#         video_file = str(QtGui.QFileDialog.getOpenFileName(self, le2mtrans(u"Select a video file")))
#         if video_file:
#             self._le2mserv.gestionnaire_graphique.display_video(video_file)
#
#     def closeEvent(self, event):
#         """
#         Parce qu'on demande confirmation avant de quitter
#         """
#         reply = QtGui.QMessageBox.question(
#             self,
#             le2mtrans(u'Confirmation'),
#             le2mtrans(u"Are you sure you want to exit LE2M?"),
#             QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
#         if reply == QtGui.QMessageBox.Yes:
#             self._le2mserv.arreter()
#             event.accept()
#         else:
#             event.ignore()
#
#     def _edit_genders(self):
#         """
#         Display a dialog for setting the gender of each subject (by remote)
#         """
#         players = self._le2mserv.gestionnaire_joueurs.get_players()
#         ecran_genres = GuiGenres(players, self)
#         if ecran_genres.exec_():
#             self._le2mserv.gestionnaire_graphique.infoserv(
#                 [le2mtrans(u"Genders"), le2mtrans(u"Men")])
#             self._le2mserv.gestionnaire_graphique.infoserv(
#                 map(str, [p for p in players if p.gender == HOMME]))
#             self._le2mserv.gestionnaire_graphique.infoserv(le2mtrans(u"Women"))
#             self._le2mserv.gestionnaire_graphique.infoserv(
#                 map(str, [p for p in players if p.gender == FEMME]))
#
#     def edit_groups(self):
#         joueurs = self._le2mserv.gestionnaire_joueurs.get_players()
#         if not joueurs:
#             QtGui.QMessageBox.warning(
#                 self, le2mtrans(u"Warning"),
#                 le2mtrans(u"There is no player connected"))
#             return
#         dialog_edit_groups = DEditGroups(
#             self._le2mserv,joueurs)
#         dialog_edit_groups.exec_()
#
#     def _display_finalquest(self):
#         """
#         Display the final questionnaire on remotes
#         """
#         if not self._le2mserv.gestionnaire_base.is_created():
#             QtGui.QMessageBox.warning(
#                 self,
#                 le2mtrans(u"Warning"),
#                 le2mtrans(u"There is no database yet. You first need to "
#                           u"load at least one part."))
#             return
#         confirmation = QtGui.QMessageBox.question(
#             self,
#             le2mtrans(u"Confirmation"),
#             le2mtrans(u"Start the final questionnaire?"),
#             QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
#         if confirmation != QtGui.QMessageBox.Ok:
#             return
#         self._le2mserv.gestionnaire_experience.display_finalquestionnaire()
#
#     def _display_help(self):
#         """
#         Display a dialog with some help on le2m
#         """
#         help_file = os.path.join(params.getp("HTMLDIR"),
#                                     "le2m_aide.html")
#         webscreen = DWebview(
#             help_file, title=le2mtrans(u"Help"), parent=self)
#         webscreen.show()
#
#     def _display_about(self):
#         """
#         Display a dialog with some infos about the authors of le2m
#         """
#         fichier_auteurs = os.path.join(
#             params.getp("HTMLDIR"), "le2m_auteurs.html")
#         screen = GuiInformation(
#             parent=self, titre=le2mtrans(u"Developers"), size=(450, 180),
#             html=True, text=utiltools.get_contenu_fichier(fichier_auteurs))
#         screen.show()
#
#     def _draw_part(self):
#         """
#         Display a dialog with the list of played part.
#         The experimenter select the parts among which he/she wants to do
#         a random draw for paiements for example
#         :return:
#         """
#         parties_jouees = self._le2mserv.gestionnaire_experience. \
#             get_parts()
#         ecran_parties = GuiPartsPlayed(parties_jouees, self)
#         if ecran_parties.exec_():
#             parties_selectionnees = ecran_parties.get_parties_selectionnees()
#             if not parties_selectionnees:
#                 return
#             self._le2mserv.gestionnaire_experience.draw_part(
#                 parties_selectionnees)
#         else:
#             return
#
#     def _display_payoffs_partsSelection(self):
#         """
#         Open a dialog box with the list of parts that have been played.
#         The experimenter chooses which part he/she wants to be displayed
#         on the remotes
#         :return:
#         """
#         parts = self._le2mserv.gestionnaire_experience.get_parts()
#         screen = GuiPartsPlayed(parts, self)
#         if screen.exec_():
#             choices = screen.get_parties_selectionnees()
#             if choices:
#                 confirmation = self._le2mserv.gestionnaire_graphique.question(
#                     le2mtrans(u"Display the details of the selected parts "
#                               u"on remotes?\n{}").format(choices))
#                 if not confirmation:
#                     return
#
#                 self._le2mserv.gestionnaire_experience.display_payoffs_onremotes(
#                     choices)
#
#     def _stoprep(self):
#         """
#         Change the value of the stop_repetitions variable. This method is
#         called by the stop_repetitions method (just above) but also by the
#         server of each part, at the beginning of the part in order to reset
#         the value to False
#         """
#         if self._le2mserv.gestionnaire_experience.stop_repetitions:
#             self._le2mserv.gestionnaire_experience.stop_repetitions = False
#         else:
#             self._le2mserv.gestionnaire_experience.stop_repetitions = True
#
#     def set_wait_mode(self, list_players):
#         """
#         Display a colored icon beside the hostname to see whether the remote
#         has a decided or not yet
#         :param list_players: either a list of players (or parts) or only one
#          element (player or part)
#         """
#         self.ui.listWidget_attente.clear()
#         del self._players_wait_mode[:]
#         # if the argument is a list
#         if isinstance(list_players, list):
#             for p in list_players:
#                 e = QtGui.QListWidgetItem(self._icon_rouge, u"")
#                 if isinstance(p, Partie):
#                     self._players_wait_mode.append(p.joueur)
#                     e.setText(repr(p.joueur))
#                 elif isinstance(p, Joueur):
#                     self._players_wait_mode.append(p)
#                     e.setText(repr(p))
#                 self.ui.listWidget_attente.addItem(e)
#         # if the argument is only one object
#         else:
#             e = QtGui.QListWidgetItem(self._icon_rouge, u"")
#             if isinstance(list_players, Partie):
#                 self._players_wait_mode.append(list_players.joueur)
#                 e.setText(repr(list_players.joueur))
#             elif isinstance(list_players, Joueur):
#                 self._players_wait_mode.append(list_players)
#                 e.setText(repr(list_players))
#             self.ui.listWidget_attente.addItem(e)
#
#     def remove_wait_mode(self, list_players):
#         """
#         Change the icon color to green, meaning that the remote has taken
#         his decision
#         :param list_players: either a list of players (or parts) or only one
#          element (player or part)
#         """
#         if isinstance(list_players, list):
#             for p in list_players:
#                 try:
#                     index = self._players_wait_mode.index(p)
#                 except ValueError as e:
#                     logger.warning(
#                         le2mtrans(u"Problem with remove_waitmode: "
#                                   u"{msg}").format(e.message)
#                     )
#                 else:
#                     self.ui.listWidget_attente.item(index).setIcon(
#                         self._icon_vert)
#         else:
#             try:
#                 index = self._players_wait_mode.index(list_players)
#             except ValueError as e:
#                 logger.warning(
#                     le2mtrans(u"Problem with remove_waitmode: "
#                               u"{msg}").format(e.message)
#                 )
#             else:
#                 self.ui.listWidget_attente.item(index).setIcon(self._icon_vert)
#
#     @QtCore.pyqtSlot(object, int)
#     def _addplayer(self, player, nbplayers):
#         self.tableJoueurs.ajouter_joueur(player)
#         self.ui.label_connectedremotes.setText(
#             le2mtrans(u"Connected remotes: {num}").format(num=nbplayers))
#
#     @QtCore.pyqtSlot(object, int)
#     def _removeplayer(self, player, nbplayers):
#         self.tableJoueurs.enlever_joueur(player)
#         self.ui.label_connectedremotes.setText(
#             le2mtrans(u"Connected remotes: {num}").format(num=nbplayers))
#
#     @QtCore.pyqtSlot(bool)
#     def _stoprepetitions(self, yes_or_no):
#         if yes_or_no:
#             self.action_stoprepetitions.setText(
#                 le2mtrans(u"The part will stop after this period"))
#         else:
#             self.action_stoprepetitions.setText(
#                 le2mtrans(u"Stop the part after this period "))
#
#     def _rolldice(self):
#         screen = DDice(self)
#         if screen.exec_():
#             self._le2mserv.gestionnaire_graphique.infoserv(
#                 le2mtrans(u"Dice value: {}".format(screen.get_dicevalue())))
#
#     def _randint(self):
#         screen = DRandint(self)
#         if screen.exec_():
#             self._le2mserv.gestionnaire_graphique.infoserv(
#                 le2mtrans(u"Random number: {}".format(screen.get_value())))
#
#     def _headtail(self):
#         screen = DHeadtail(self)
#         if screen.exec_():
#             self._le2mserv.gestionnaire_graphique.infoserv(
#                 le2mtrans(u"Head and tail: {}".format(
#                     le2mtrans(u"Head") if screen.get_value() == FACE else
#                     le2mtrans(u"Tail"))))
#
#     @QtCore.pyqtSlot()
#     def _load_questcomp(self):
#         """
#         Récupère le fichier xml de questionnaire de compréhension et le
#         traite
#         :return:
#         """
#         xmlfile = str(
#             QtGui.QFileDialog.getOpenFileName(
#                 self,
#                 le2mtrans(u"Select the understanding questionnaire to load"),
#                 "", le2mtrans(u"xml file (*.xml)")))
#         if not xmlfile:
#             return
#         else:
#             self.questcomp = questcomp.get_questions(xmlfile)
#             if not self.questcomp:
#                 return
#
#             txt = u""
#             for q in self.questcomp:
#                 txt += u"{}\n\n".format(q)
#             screen = DUnderstandingVisual(txt)
#             screen.exec_()
#             self.add_list_server(
#                 le2mtrans(u"Understanding questionnaire loaded "
#                           u"({} questions)").format(len(self.questcomp)))
#
#     @QtCore.pyqtSlot()
#     def _start_questcomp(self):
#         """
#         Start the understanding questionnaire
#         """
#         if not self.questcomp:
#             QtGui.QMessageBox.warning(
#                 self,
#                 le2mtrans(u"Warning"),
#                 le2mtrans(u"Please load an understanding questionnaire"))
#             return
#         if not self.le2msrv.gestionnaire_base.is_created():
#             QtGui.QMessageBox.warning(
#                 self, le2mtrans(u"Warning"),
#                 le2mtrans(u"The understanding questionnaire cannot be started "
#                           u"before the database is created. You first has to "
#                           u"load at least one part."))
#             return
#         reply = QtGui.QMessageBox.question(
#             self,
#             le2mtrans(u'Confirmation'),
#             le2mtrans(u"Please confirm you want to start the understanding "
#                       u"questionnaire?"),
#             QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
#         if reply != QtGui.QMessageBox.Yes:
#             return
#         self.le2msrv.gestionnaire_experience.start_questcomp(self._questcomp)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    params.setp_appdir("/home/dimitri/Documents/travail/programmes/le2m-v2.1/le2m")
    win = MainWindow(None)
    win.add_list_server("text on server list")
    win.add_list_client("text on client list")
    win.show()
    sys.exit(app.exec_())