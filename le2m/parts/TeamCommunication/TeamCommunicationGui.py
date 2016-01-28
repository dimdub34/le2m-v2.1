# -*- coding: utf-8 -*-
"""
Ce module contient les boites de dialogue du programme.
"""

import logging
import random
import datetime
import pickle
from PyQt4 import QtGui, QtCore
from client.cltgui.cltguiwidgets import WExplication, WCompterebours, WChat, \
    WSpinbox, WSlider
import TeamCommunicationParams as pms
import TeamCommunicationTexts as texts
from TeamCommunicationGuiSrc import TeamCommunicationConfiguration, \
    TeamCommunicationWlist, TeamCommunicationCellule, TC_widGrilles, \
    TC_widDisplayer
from util.utiltools import get_pluriel
from server.servgui.servguidialogs import GuiPayoffs
from twisted.internet import defer

logger = logging.getLogger("le2m")


def _get_html(numero, grille):
    html = "<p>Grille {}<br />".format(numero)
    html += "<table style='width: 150px;'>"
    for l in grille:
        html += "<tr>"
        for c in l:
            html += "<td style='width: 15px;'>{}</td>".format(c)
        html += "</tr>"
    html += "</table>"
    return html


class WCell(QtGui.QWidget):
    def __init__(self, numero, displayer, tcremote):
        super(WCell, self).__init__()
        self.ui = TeamCommunicationCellule.Ui_Form()
        self.ui.setupUi(self)

        self._numero = numero
        self._displayer = displayer
        self._tcremote = tcremote

        self.ui.pushButton.setText("{}".format(numero))
        self.ui.pushButton.setFixedSize(45, 25)
        self.ui.pushButton.setStyleSheet(
            'QPushButton {border: 1px ridge gray;}')
        self.ui.spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.ui.spinBox.setFixedSize(45, 25)

        self.ui.pushButton.clicked.connect(lambda _: self._displayer.setText(
            _get_html(self._numero, pms.GRILLES[self._numero]["grille"])))
        self.ui.pushButton.clicked.connect(lambda _: self._send_look())
        self.ui.spinBox.valueChanged.connect(lambda _: self._send_try())

        self.setFixedSize(55, 75)

    def set_value(self, val):
        """
        Used in automatic and simulation modes
        :param val:
        :return:
        """
        self.ui.spinBox.setValue(val)

    @defer.inlineCallbacks
    def _send_look(self):
        try:
            yield (self._tcremote.send_look(self._numero))
        except Exception as e:
            logger.error(e.message)
        defer.returnValue(None)

    @defer.inlineCallbacks
    def _send_try(self):
        try:
            yield (self._tcremote.send_try(
                self._numero, self.ui.spinBox.value()))
        except Exception as e:
            logger.error(e.message)
        defer.returnValue(None)


class WGrilles(QtGui.QWidget):
    def __init__(self, parent, displayer, tcremote):
        super(WGrilles, self).__init__(parent)
        self.ui = TC_widGrilles.Ui_Form()
        self.ui.setupUi(self)

        for i in range(4):
            for j in range(25):
                num = 25 * i + j
                setattr(self, "grille_{}".format(num),
                        WCell(numero=num, displayer=displayer,
                              tcremote=tcremote))
                self.ui.gridLayout.addWidget(
                    getattr(self, "grille_{}".format(num)), i, j)

    def set_value(self, grille, value):
        getattr(self, "grille_{}".format(grille)).set_value(value)

    def get_values(self):
        values = {}
        for i in range(100):
            values[i] = getattr(
                self, "grille_{}".format(i)).ui.spinBox.value()
        return values


class WDisplayer(QtGui.QWidget):
    def __init__(self, parent):
        super(WDisplayer, self).__init__(parent)
        self.ui = TC_widDisplayer.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label.setText(
            u"Cliquer sur un numéro \npour voir la grille correspondante")
        font_grille = QtGui.QFont()
        font_grille.setPointSize(14)
        font_grille.setBold(True)
        self.ui.label.setFont(font_grille)


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, tcremote):
        super(GuiDecision, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique
        self._tcremote = tcremote

        layout = QtGui.QVBoxLayout(self)

        self._widexplication = WExplication(
            text=u"", parent=self, size=(400, 50))
        layout.addWidget(self._widexplication)

        self._widcompterebours = WCompterebours(
            parent=self, temps=pms.TEMPS_PARTIE, actionfin=self._accept)
        layout.addWidget(self._widcompterebours)

        self._widdisplayer = WDisplayer(parent=self)
        self._widdisplayer.ui.label.setFixedSize(400, 300)
        self._widgrilles = WGrilles(
            parent=self, displayer=self._widdisplayer.ui.label,
            tcremote=self._tcremote)
        self._widgrilles.setFixedSize(1250, 350)
        layout.addWidget(self._widgrilles)

        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(self._widdisplayer)
        hlayout.addSpacerItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        self.widchat = WChat(parent=self, action_send=self._send_message)
        hlayout.addWidget(self.widchat)
        layout.addLayout(hlayout)

        if pms.TREATMENT == pms.SANS_COMMUNICATION:
            self.widchat.setVisible(False)

        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(self._handle_automatic)
            self._timer.start(random.randint(1000, 15000))

        self.setWindowTitle(u"Décisions")
        self.adjustSize()
        self.setFixedSize(self.size())

    @defer.inlineCallbacks
    def _handle_automatic(self):
        if not self._widcompterebours.compterebours.isRunning():
            self._timer.stop()
        grille = random.randint(0, 99)
        try:
            yield (self._tcremote.send_look(grille))
        except Exception as e:
            logger.error(e.message)
        if random.random() >= 0.25:  # on fait un essai
            if random.randint(0, 1):  # on donne la bonne réponse
                nbun = pms.GRILLES[grille]["count"]
            else:
                nbun = random.randint(0, 100)
            self._widgrilles.set_value(grille, nbun)
            try:
                yield (self._tcremote.send_try(grille, nbun))
            except Exception as e:
                logger.error(e.message)

        if pms.TREATMENT == pms.AVEC_COMMUNICATION:
            if random.random() >= 0.60:  # on envoit un message
                self.widchat.write(u"Message automatique")
                self.widchat.ui.pushButton.click()
        defer.returnValue(None)

    def reject(self):
        pass

    def _accept(self):
        answers = self._widgrilles.get_values()
        logger.debug(u"Renvoi {}".format(answers))
        self._defered.callback(answers)
        self.accept()

    @defer.inlineCallbacks
    def _send_message(self, msg):
        try:
            yield (self._tcremote.send_message(msg))
        except Exception as e:
            logger.error(e.message)
        self.add_message(u"Vous: {}".format(msg))
        self.widchat.clear_writespace()
        defer.returnValue(None)

    def add_message(self, msg):
        self.widchat.add_text(msg)


class DConfiguration(QtGui.QDialog):
    def __init__(self, parent):
        super(DConfiguration, self).__init__(parent)
        self.ui = TeamCommunicationConfiguration.Ui_Dialog()
        self.ui.setupUi(self)

        treatmentscles = pms.treatmentcodes.keys()
        treatmentscles.sort()
        self.ui.comboBox_communication.addItems(
            [pms.treatmentcodes[t] for t in treatmentscles])
        self.ui.comboBox_communication.setCurrentIndex(pms.TREATMENT)
        self.ui.timeEdit_tempspartie.setTime(QtCore.QTime(
            pms.TEMPS_PARTIE.hour, pms.TEMPS_PARTIE.minute,
            pms.TEMPS_PARTIE.second))

        self.setWindowTitle(u"Configuration")
        self.setFixedSize(280, 150)

        self.ui.pushButton_grilles.clicked.connect(self._load_grilles)
        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def _accept(self):
        self._communication = self.ui.comboBox_communication.currentIndex()
        tpspart = self.ui.timeEdit_tempspartie.time()
        self._tempspartie = datetime.time(
            tpspart.hour(), tpspart.minute(), tpspart.second())
        if not self._tempspartie:
            QtGui.QMessageBox.critical(
                self, u"Attention", u"Il faut un temps de partie positif")
            return
        if not hasattr(self, "_grilles"):
            QtGui.QMessageBox.critical(
                self, u"Attention", u"Il faut charger les grilles")
            return

    def _load_grilles(self):
        fichier = str(QtGui.QFileDialog.getOpenFileName(
            self, u"Choisir le fichier de grilles", "",
            u"Fichier pickle (*.pck)"))
        with open(fichier, "rb") as f:
            self._grilles = pickle.load(f)
            self.ui.label_grilles_nb.setText(
                get_pluriel(len(self._grilles), u"grille"))
        logger.info(u"Grilles loaded")

    def get_config(self):
        return self._tempspartie, self._communication, self._grilles


class Wlist(QtGui.QWidget):
    def __init__(self):
        super(Wlist, self).__init__()
        self.ui = TeamCommunicationWlist.Ui_Form()
        self.ui.setupUi(self)

    def clear(self):
        self.ui.listWidget.clear()

    def add(self, texte):
        txt = texte or u""
        self.ui.listWidget.addItem(txt)


class DGains(GuiPayoffs):
    def __init__(self, le2mserver, gains_txt, textes_finaux, gains):
        GuiPayoffs.__init__(self, le2mserver, "TeamCommunication", gains_txt)

        self._textes_finaux = textes_finaux
        self._gains = gains
        self._le2mserv = le2mserver
        self.ui.pushButton_afficher.clicked.disconnect(self._display_onremotes)
        self.ui.pushButton_afficher.clicked.connect(
            lambda _: self._display_onremotes2())

    @defer.inlineCallbacks
    def _display_onremotes2(self):
        if not self._textes_finaux:
            return
        confirm = self._le2mserv.gestionnaire_graphique.question(
            u"Afficher les gains sur les postes?")
        if not confirm:
            return
        for j in self._le2mserv.gestionnaire_joueurs.get_players("base"):
            yield (j.display_information(self._textes_finaux[j.joueur]))

    def _add_tofinalpayoffs(self):
        if not self._gains:
            return
        for k, v in self._gains.iteritems():
            k.get_part("base").paiementFinal += float(v)
        self._le2mserv.gestionnaire_base.enregistrer()
        self._le2mserv.gestionnaire_graphique.infoserv(
            u"Gains de TeamCommunication ajoutés aux gains finaux", fg="red")


class DAdditionnalquestions(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, nbanswers):
        super(DAdditionnalquestions, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique
        self._nbanswers = nbanswers

        layout = QtGui.QVBoxLayout(self)

        self._widanswers = WSpinbox(
            label=texts.get_text_reponses(nbanswers),
            minimum=0, maximum=nbanswers, automatique=self._automatique,
            parent=self)
        layout.addWidget(self._widanswers)

        if pms.TREATMENT == pms.AVEC_COMMUNICATION:
            self._widinfosatisfaction = WSlider(
                label=texts.get_text_infosatisfaction(),
                minimum=1, maximum=7, automatique=self._automatique,
                parent=self)
            layout.addWidget(self._widinfosatisfaction)

        self._widjobsatisfaction = WSlider(
            label=texts.get_text_jobsatisfaction(),
            minimum=1, maximum=7, automatique=self._automatique,
            parent=self)
        layout.addWidget(self._widjobsatisfaction)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer.start(7000)

        self.setWindowTitle(u"Questions supplémentaires")
        self.adjustSize()
        self.setFixedSize(self.size())

    def reject(self):
        pass

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass
        rep = {"TC_confidence": self._widanswers.get_value(),
               "TC_jobsatisfaction": self._widjobsatisfaction.get_value()}
        if pms.TREATMENT == pms.AVEC_COMMUNICATION:
            rep["TC_infosatisfaction"] = self._widinfosatisfaction.get_value()
        if not self._automatique:
            confirm = QtGui.QMessageBox.question(
                self, u"Confirmation", u"Vous confirmez vos réponses?",
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirm != QtGui.QMessageBox.Yes:
                return
        logger.info(u"Renvoi {}".format(rep))
        self.accept()
        self._defered.callback(rep)


class DQuestionDictator(QtGui.QDialog):
    def __init__(self, defered, automatique, parent):
        super(DQuestionDictator, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        self._widPrediction = WSpinbox(
            label=texts.get_textpredictiondictator(), minimum=0, maximum=10,
            automatique=self._automatique, parent=self)
        layout.addWidget(self._widPrediction)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer.start(7000)

        self.setWindowTitle(u"Prédiction")
        self.adjustSize()
        self.setFixedSize(self.size())

    def reject(self):
        pass

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass

        if not self._automatique:
            confirm = QtGui.QMessageBox.question(
                self, u"Confirmation", u"Vous confirmez votre choix?",
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirm != QtGui.QMessageBox.Yes:
                return
            dec = self._widPrediction.get_value()
            logger.info(u"Send back {}".format(dec))
            self.accept()
            self._defered.callback(dec)
