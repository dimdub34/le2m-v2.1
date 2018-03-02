# -*- coding: utf-8 -*-

""" ============================================================================

This modules contains only the class GestionnaireGraphique of the server.
This class handles the graphical part on the server side

============================================================================ """

# built-in
import os
from PyQt4 import QtGui
import logging

# le2m
from util.utili18n import le2mtrans
from server.servgui.servguiwindows import MainWindow  # , GuiServeur
from server.servgui.servguidialogs import GuiInformation, DDisplayImages, DDisplayVideo


logger = logging.getLogger("le2m")


class GestionnaireGraphique():
    """
    Cette classe fait le lien entre la couche métier du serveur et l'IHM.
    Si on change d'interface graphique il suffit de changer/modifier ce 
    gestionnaire.
    Elle gère toute la partie visuelle de l'écran serveur.
    """

    def __init__(self, le2mserv):
        self.le2mserv = le2mserv
        self.screen = MainWindow(self.le2mserv)

    def infoclt(self, texte, **kwargs):
        """
        Affiche le texte sur la liste client.
        Parmi les arguments de kwargs il peut y avoir le fb et bg
        """
        if isinstance(texte, list):
            for l in texte:
                self.screen.add_list_client(l, **kwargs)
        else:
            self.screen.add_list_client(texte, **kwargs)

    def infoserv(self, texte, **kwargs):
        """
        Affiche le texte sur la liste serveur.
        Parmi les arguments de kwargs il peut y avoir le fb et bg
        """
        if isinstance(texte, list):
            for l in texte:
                self.screen.add_list_server(l, **kwargs)
        else:
            self.screen.add_list_server(texte, **kwargs)

    def set_waitmode(self, liste_joueurs):
        """
        Ajoute visuellement tous les joueurs de liste en mode attente,
        cad qu'on attend une réponse de leur part. Visuellement ils sont 
        affichés dans l'onglet gestion de l'expérience et dans la partie 
        droite, avec l'identifiant du poste et la petite bulle rouge.
        """
        self.screen.set_wait_mode(liste_joueurs)

    def remove_waitmode(self, liste_joueurs):
        """
        Enlève visuellement le joueur de la liste des joueurs en mode
        attente. Visuellement la bulle du joueur passe verte.
        """
        self.screen.remove_wait_mode(liste_joueurs)

    def display_statusbar(self, message, temps=10000):
        """
        Affiche le message dans la barre de statut de l'écran serveur.
        """
        self.screen.ui.statusbar.showMessage(message, temps)

    def display_error(self, message):
        """
        Affiche une boite de dialogue d'erreur sur l'écran serveur.
        """
        QtGui.QMessageBox.critical(self.screen, "Erreur", message)

    def display_warning(self, message):
        """
        Affiche une boite de dialogue d'avertissement sur l'screen serveur.
        """
        QtGui.QMessageBox.warning(self.screen, "Attention", message)

    def display_information(self, message):
        """
        Affiche une boite de dialogue d'information sur l'écran serveur.
        :param message: the message to display
        """
        QtGui.QMessageBox.information(self.screen, "Information", message)

    def display_information2(self, text, titre=u"Information",
                             html=False, size=(450, 450)):
        """
        Affiche le texte dans une boite de dialogue, au sein d'un textEdit
        :param texte: le texte à afficher
        :param titre: le titre de la boite de dialogue
        :param html: affiche du html si vrai
        :param size: la taille de la boite: largeur, hauteur
        :return:
        """
        ecran = GuiInformation(
            titre=titre, text=text, parent=self.screen, size=size, html=html)
        ecran.exec_()

    def question(self, message, parent=None):
        """
        Affiche une boite de dialogue question sur l'écran serveur,
        avec uniquement les boutons oui|non. 
        Renvoie le choix effectué (oui ou non).
        """
        reponse = QtGui.QMessageBox.question(
            parent or self.screen, le2mtrans(u"Question"), message,
            QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
        return reponse == QtGui.QMessageBox.Yes

    def add_topartmenu(self, menuname, ordered_dict_actions):
        """
        Add a submenu to the "part" menu
        """
        menu = QtGui.QMenu(menuname, self.screen)
        for nom, methode in ordered_dict_actions.items():
            action = QtGui.QAction(nom, self.screen)
            action.triggered.connect(methode)
            menu.addAction(action)
        self.screen.menu_parts.addMenu(menu)

    # def display_images(self, directory):
    #     self.dialog_display_images = DDisplayImages(self.le2mserv, directory)
    #     self.dialog_display_images.show()

    # def display_video(self, video_file):
    #     self.dialog_display_video = DDisplayVideo(self.le2mserv, video_file)
    #     self.dialog_display_video.show()