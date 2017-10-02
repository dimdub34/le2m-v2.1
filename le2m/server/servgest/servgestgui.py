# -*- coding: utf-8 -*-
"""
Ce module contient uniquement la classe GestionnaireGraphique du serveur
Cet objet, instancié une seule fois, gère toute la partie graphique du serveur.
"""
import os
from PyQt4 import QtGui
import logging
from util.utili18n import le2mtrans
from server.servgui.servguiwindows import GuiServeur
from server.servgui.servguidialogs import GuiInformation, DDisplayImages, DDisplayVideo


logger = logging.getLogger("le2m.{}".format(__name__))


class GestionnaireGraphique():
    """
    Cette classe fait le lien entre la couche métier du serveur et l'IHM.
    Si on change d'interface graphique il suffit de changer/modifier ce 
    gestionnaire.
    Elle gère toute la partie visuelle de l'écran serveur.
    """

    def __init__(self, le2mserv):
        self._le2mserv = le2mserv
        self._screen = GuiServeur(self._le2mserv)

    @property
    def screen(self):
        return self._screen

    def infoclt(self, texte, **kwargs):
        """
        Affiche le texte sur la liste client.
        Parmi les arguments de kwargs il peut y avoir le fb et bg
        """
        if isinstance(texte, list):
            for l in texte:
                self._screen.add_clientlist(l, **kwargs)
        else:
            self._screen.add_clientlist(texte, **kwargs)

    def infoserv(self, texte, **kwargs):
        """
        Affiche le texte sur la liste serveur.
        Parmi les arguments de kwargs il peut y avoir le fb et bg
        """
        if isinstance(texte, list):
            for l in texte:
                self._screen.add_serverlist(l, **kwargs)
        else:
            self._screen.add_serverlist(texte, **kwargs)

    def set_waitmode(self, liste_joueurs):
        """
        Ajoute visuellement tous les joueurs de liste en mode attente,
        cad qu'on attend une réponse de leur part. Visuellement ils sont 
        affichés dans l'onglet gestion de l'expérience et dans la partie 
        droite, avec l'identifiant du poste et la petite bulle rouge.
        """
        self._screen.set_wait_mode(liste_joueurs)

    def remove_waitmode(self, liste_joueurs):
        """
        Enlève visuellement le joueur de la liste des joueurs en mode
        attente. Visuellement la bulle du joueur passe verte.
        """
        self._screen.remove_wait_mode(liste_joueurs)

    def display_statusbar(self, message, temps=10000):
        """
        Affiche le message dans la barre de statut de l'écran serveur.
        """
        self._screen.ui.statusbar.showMessage(message, temps)

    def display_error(self, message):
        """
        Affiche une boite de dialogue d'erreur sur l'écran serveur.
        """
        QtGui.QMessageBox.critical(self._screen, "Erreur", message)

    def display_warning(self, message):
        """
        Affiche une boite de dialogue d'avertissement sur l'screen serveur.
        """
        QtGui.QMessageBox.warning(self._screen, "Attention", message)

    def display_information(self, message):
        """
        Affiche une boite de dialogue d'information sur l'écran serveur.
        :param message: the message to display
        """
        QtGui.QMessageBox.information(self._screen, "Information", message)

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
            titre=titre, text=text, parent=self._screen, size=size, html=html)
        ecran.exec_()

    def question(self, message, parent=None):
        """
        Affiche une boite de dialogue question sur l'écran serveur,
        avec uniquement les boutons oui|non. 
        Renvoie le choix effectué (oui ou non).
        """
        reponse = QtGui.QMessageBox.question(
            parent or self._screen, le2mtrans(u"Question"), message,
            QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
        return reponse == QtGui.QMessageBox.Yes

    def add_topartmenu(self, menuname, ordered_dict_actions):
        """
        Add a submenu to the "part" menu
        """
        menu = QtGui.QMenu(menuname, self._screen)
        for nom, methode in ordered_dict_actions.iteritems():
            action = QtGui.QAction(nom, self._screen)
            action.triggered.connect(methode)
            menu.addAction(action)
        self._screen.menu_parts.addMenu(menu)

    def display_images(self, directory):
        self.dialog_display_images = DDisplayImages(self._le2mserv, directory)
        self.dialog_display_images.show()

    def display_video(self, video_file):
        self.dialog_display_video = DDisplayVideo(self._le2mserv, video_file)
        self.dialog_display_video.show()