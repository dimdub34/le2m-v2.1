# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from twisted.internet.defer import AlreadyCalledError
import random
import logging
from datetime import datetime
from configuration import configparam as params
from client import clttexts as textes
from configuration import configvar
from client.cltgui.cltguisrc import cltguiwelc, cltguifinal, cltguiquestfinal
from util.utili18n import le2mtrans
from cltguitablemodels import TableModelHistorique
from cltguiwidgets import WExplication, WTableview, WPeriod, WSpinbox, WCombo, \
    WRadio

logger = logging.getLogger("le2m")


class GuiAccueil(QtGui.QDialog):
    """
    L'écran d'accueil. Un bouton permet d'informer l'expérimentateur que
    le sujet a fini de lire les instructions
    """
    def __init__(self, defered, automatique, parent):
        super(GuiAccueil, self).__init__(parent)

        # variables
        self._defered = defered
        self._automatique = automatique

        # creation gui
        self.ui = cltguiwelc.Ui_Dialog()
        self.ui.setupUi(self)

        # centre écran avec image labo
        welcfont = self.ui.label_welcome.font()
        welcfont.setPointSize(20)
        welcfont.setBold(True)
        self.ui.label_welcome.setText(u"<font color='blue'>{}</font>".format(
            textes.ACCUEIL_label_welcome))
        try:
            img_labo_pix = QtGui.QPixmap(params.getp("WELCOMEPICTURE"))
            self.ui.label_image_accueil.setPixmap(img_labo_pix)
        except IOError:
            self.ui.label_image_accueil.setText(
                textes.ACCUEIL_label_image_accueil)

        self.ui.label_instructions.setText(
            le2mtrans(u"Please read the instructions that stand beside the "
                      u"computer. You are asked to click on the button below "
                      u"when you have finished."))

        # bouton
        self.ui.pushButton_valider.setText(le2mtrans(u"Instructions read"))
        self.ui.pushButton_valider.clicked.connect(self._accept)
        
        self.setWindowTitle(textes.ACCUEIL_titre)
        self.setFixedSize(900, 575)
    
        if self._automatique: 
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(self._accept)
            self._timer.start(7000)

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass
        self.ui.pushButton_valider.setEnabled(False)
        logger.info(u"Welcome callback: 1")
        self._defered.callback(1)
        self.accept()
        
    def reject(self):
        pass


class GuiHistorique(QtGui.QDialog):
    def __init__(self, parent, historique, size=(600, 500)):
        super(GuiHistorique, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)

        # table model: either historique or a new (empty) one
        self.tablemodel = TableModelHistorique(historique or [[], []])
        self.widtableview = WTableview(self, self.tablemodel, size=size)
        layout.addWidget(self.widtableview)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setWindowTitle(textes.le2mtrans(u"History"))
        self.adjustSize()
        self.setFixedSize(self.size())
        
    def reject(self):
        pass
        

class GuiRecapitulatif(QtGui.QDialog):
    """
    Dialog for the summary, for repeated game or one-shot.
    If ecran_historique is set if replace the default GuiHistorique
    """
    def __init__(self, defered, automatique, parent, periode, historique,
                 texte_recap, ecran_historique=None, size_histo=(500, 90)):
        """

        :param defered:
        :param automatique:
        :param parent:
        :param periode:
        :param historique:
        :param texte_recap:
        :param ecran_historique:
        :param size_histo: the size of the history table. The width of the
        explanation area will be the same than the width of the history table
        :return:
        """
        super(GuiRecapitulatif, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique
        self.ecran_historique = \
            ecran_historique or GuiHistorique(self, historique,
                                              size=(size_histo[0], 500))

        layout = QtGui.QVBoxLayout(self)

        if periode:
            self.widperiod = WPeriod(
                period=periode, ecran_historique=self.ecran_historique,
                parent=self)
            layout.addWidget(self.widperiod)

        self.widexplication = WExplication(text=texte_recap, parent=self,
                                           size=(size_histo[0], 80))
        layout.addWidget(self.widexplication)

        # ligne historique (entêtes et dernière ligne de l'historique)
        histo_recap = [historique[0], historique[-1]]
        self.tablemodel = TableModelHistorique(histo_recap)
        self.widtableview = WTableview(parent=self, tablemodel=self.tablemodel,
                                       size=size_histo)
        self.widtableview.ui.tableView.verticalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch)
        layout.addWidget(self.widtableview)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        # automatique
        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)

        # taille et titre
        self.setWindowTitle(le2mtrans(u"Summary"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        """
        :return:
        """
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        logger.info(u"callback: Ok summary")
        self._defered.callback(1)
        self.accept()
        
    def reject(self):
        pass


class GuiPopup(QtGui.QDialog):
    def __init__(self, defered, txt, temps=7000, parent=None, html=True,
                 size=(300, 100)):
        QtGui.QDialog.__init__(self, parent)

        self._defered = defered

        layout = QtGui.QVBoxLayout(self)

        wexplanation = WExplication(
            text=txt, parent=self, html=html, size=(size[0], size[1]))
        layout.addWidget(wexplanation)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Information"))
        self.adjustSize()
        self.setFixedSize(self.size())

        if temps > 0:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer.start(temps)

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass
        self.accept()
        self._defered.callback(1)

    def reject(self):
        pass
    

class GuiFinal(QtGui.QDialog):
    """
    The final screen. Displays the final payoff and allows the subject to
    make comments
    """
    def __init__(self, defered, auto, parent, txt):
        super(GuiFinal, self).__init__(parent)

        self.ui = cltguifinal.Ui_Dialog()
        self.ui.setupUi(self)

        self._defered = defered
        self._automatique = auto

        self.ui.textEdit_explication.setText(txt)

        self.ui.label_merci.setText(
            le2mtrans(u"The experiment is over, thank you for your participation"))

        self.ui.label_commentaires.setText(
            u"<html><body><p>" +
            le2mtrans(u"You can write comments about the experiment in the "
                      u"area just below") + u"<br />" +
            le2mtrans(u"Click on the \"save\" button once finished.") +
            u"</p></body></html>")

        self.ui.pushButton_valider.setText(le2mtrans(u"Save"))
        self.ui.pushButton_valider.clicked.connect(self._save)

        if self._automatique:
            self.ui.textEdit_commentaires.setText(
                le2mtrans(u"This is an automatic sentence"))
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(self._save)
            self._timer.start(7000)

        self.setWindowTitle(le2mtrans(u"End of the experiment"))

    def _save(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass
        self.ui.pushButton_valider.setEnabled(False)
        self.ui.textEdit_commentaires.setEnabled(False)
        commentaires = unicode(
            self.ui.textEdit_commentaires.toPlainText().toUtf8(), "utf-8")
        # suppression des ; car exportation csv
        commentaires = commentaires.replace(";", ",")
        try:
            self._defered.callback(commentaires)
        except AlreadyCalledError:
            pass

    def reject(self):
        self._save()
        super(GuiFinal, self).reject()

    def close(self):
        self._save()
        super(GuiFinal, self).close()


class DQuestFinal(QtGui.QDialog):
    def __init__(self, defered, automatique, parent):
        super(DQuestFinal, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        wexplanation = WExplication(
            text=le2mtrans(u"Please fill in the questionnaire below. This "
                           u"questionnaire is anonymous so please be sincere "
                           u"in your responses."),
            parent=self, size=(600, 60))
        layout.addWidget(wexplanation)

        self._gridlayout = QtGui.QGridLayout()
        layout.addLayout(self._gridlayout)

        # first line: year of birth and nationality-----------------------------
        currentyear = datetime.now().year
        self._birth = WSpinbox(label=le2mtrans(u"Year of birth"), parent=self,
                                minimum=currentyear-100, maximum=currentyear,
                                interval=1, automatique=self._automatique)
        if not self._automatique:
            self._birth.spinBox.setValue(currentyear)
        else:
            self._birth.spinBox.setValue(
                random.randint(currentyear-100, currentyear-15))
        self._gridlayout.addWidget(self._birth, 0, 0)

        countries = [v for k, v in sorted(configvar.COUNTRIES.viewitems())]
        countries.insert(0, le2mtrans(u"Choose"))
        countries.append(le2mtrans(u"Not in list above"))
        self._nationality = WCombo(
            parent=self, automatique=self._automatique,
            label=le2mtrans(u"Nationality"), items=countries)
        self._gridlayout.addWidget(self._nationality, 0, 1)

        # second line: gender and couple ---------------------------------------
        self._gender = WRadio(
            parent=self, automatique=self._automatique,
            label=le2mtrans(u"Gender"),
            texts=(le2mtrans(u"Male"), le2mtrans(u"Female")))
        self._gridlayout.addWidget(self._gender, 1, 0)

        self._couple = WRadio(
            parent=self, automatique=self._automatique,
            label=le2mtrans(u"Do you live in couple?"))
        self._gridlayout.addWidget(self._couple, 1, 1)

        # third line: student, discipline and level ---------------------------
        self._study = WRadio(parent=self, automatique=self._automatique,
                               label=le2mtrans(u"Are you a student?"))
        self._gridlayout.addWidget(self._study, 2, 0)

        study_topic = [v for k, v in sorted(configvar.ETUDES_DISCIPLINES.viewitems())]
        study_topic.insert(0, le2mtrans(u"Choose"))
        study_topic.append(le2mtrans(u"Not in the list above"))
        self._study_topic = WCombo(parent=self, automatique=self._automatique,
                                  label=le2mtrans(u"What topic do you study?"),
                                  items=study_topic)
        self._gridlayout.addWidget(self._study_topic, 2, 1)

        study_levels = [v for k, v in sorted(configvar.ETUDES_ANNEES.viewitems())]
        study_levels.insert(0, le2mtrans(u"Choose"))
        study_levels.append(le2mtrans(u"Not in the list above"))
        self._study_level = WCombo(parent=self, automatique=self._automatique,
                                   label=le2mtrans(u"Select the level"),
                                   items=study_levels)
        self._gridlayout.addWidget(self._study_level, 2, 2)

        # fourth line; brothers and sisters ------------------------------------
        self._brothers = WSpinbox(
            parent=self, automatique=self._automatique,
            label=le2mtrans(u"How much brother or sister do you have "
                            u"(half counts)?"), minimum=0, maximum=30)
        self._gridlayout.addWidget(self._brothers, 3, 0)

        self._brothers_rank = WSpinbox(
            parent=self, automatique=self._automatique,
            label=le2mtrans(u"What is your rank in your brotherhood?"),
            minimum=0, maximum=30)
        self._gridlayout.addWidget(self._brothers_rank, 3, 1)

        # sport ----------------------------------------------------------------
        self._sport = WRadio(parent=self, automatique=self._automatique,
                             label=le2mtrans(u"Do you practice sport?"))
        self._gridlayout.addWidget(self._sport, 4, 0)

        self._sport_individuel = WRadio(
            parent=self, automatique=self._automatique,
            label=le2mtrans(u"Kind of sport"),
            texts=(le2mtrans(u"Individual"), le2mtrans(u"Collective")))
        self._gridlayout.addWidget(self._sport_individuel, 4, 1)

        self._sport_competition = WRadio(
            parent=self, automatique=self._automatique,
            label=le2mtrans(u"Do you participate to competitions?"))
        self._gridlayout.addWidget(self._sport_competition, 4, 2)

        # religion -------------------------------------------------------------
        religion_important = [v for k, v in sorted(configvar.IMPORTANT_LEVELS.viewitems())]
        religion_important.insert(0, le2mtrans(u"Choose"))
        self._religion_place = WCombo(
            parent=self, automatique=self._automatique,
            label=le2mtrans(u"Is religion important in your life?"),
            items=religion_important)
        self._gridlayout.addWidget(self._religion_place, 5, 0)

        religions_names = [v for k, v in sorted(configvar.RELIGION_NAMES.viewitems())]
        religions_names.insert(0, le2mtrans(u"Choose"))
        religions_names.append(le2mtrans(u"Not in the list above"))
        self._religion_name = WCombo(
            parent=self, automatique=self._automatique,
            label=le2mtrans(u"What is your religion?"), items=religions_names)
        self._gridlayout.addWidget(self._religion_name, 5, 1)

        beliefs = [v for k, v in sorted(configvar.RELIGION_BELIEFS.viewitems())]
        beliefs.insert(0, le2mtrans(u"Choose"))
        self._religion_belief = WCombo(
            parent=self, automatique=self._automatique,
            label=le2mtrans(u"In general you would say that you are"),
            items=beliefs)
        self._gridlayout.addWidget(self._religion_belief, 5, 2)

        # expe -----------------------------------------------------------------
        self._expe = WRadio(
            parent=self, automatique=self._automatique,
            label=le2mtrans(u"Did you already partipate to an economic experiment?"))
        self._gridlayout.addWidget(self._expe, 6, 0)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        # enable and connections
        self._finalize()

        self.setWindowTitle(le2mtrans(u"Questionnaire"))
        self.adjustSize()
        self.setFixedSize(self.size())

        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)

    def _finalize(self):
        # study
        self._study_topic.setEnabled(False)
        self._study_level.setEnabled(False)
        self._study.radios[0].toggled.connect(
            lambda _: self._enable_widgets(
                self._study.get_checkedbutton() == 0, self._study_level,
                self._study_topic))

        # sport
        self._sport_individuel.setEnabled(False)
        self._sport_competition.setEnabled(False)
        self._sport.radios[0].toggled.connect(
            lambda _: self._enable_widgets(
                self._sport.get_checkedbutton() == 0,
                self._sport_individuel, self._sport_competition))

    def _enable_widgets(self, yes_or_no, *which):
        for w in which:
            w.setEnabled(yes_or_no)

    def reject(self):
        pass

    def _get_inputs(self):
        inputs = {}
        try:

            birth = self._birth.get_value()
            if birth == datetime.now().year:
                raise ValueError(le2mtrans(u"Please enter your year of birth"))
            else:
                inputs['naissance'] = birth
            inputs["nationalite"] = self._nationality.get_currentindex()
            inputs["genre"] = self._gender.get_checkedbutton()
            inputs['couple'] = self._couple.get_checkedbutton()
            inputs['experiences'] = self._expe.get_checkedbutton()

            # student
            inputs['etudiant'] = self._study.get_checkedbutton()
            if inputs['etudiant'] == 0:
                inputs['etudiant_discipline'] = self._study_topic.get_currentindex()
                inputs['etudiant_niveau'] = self._study_level.get_currentindex()

            # brotherhood
            inputs["fratrie_nombre"] = self._brothers.get_value()
            if inputs["fratrie_nombre"] > 0:
                inputs["fratrie_rang"] = self._brothers_rank.get_value()
            else:
                inputs["fratrie_rang"] = 0

            # sport
            inputs["sportif"] = self._sport.get_checkedbutton()
            if inputs["sportif"] == 0:
                inputs["sportif_type"] = self._sport_individuel.get_checkedbutton()
                inputs["sportif_competition"] = self._sport_competition.get_checkedbutton()

            # religion
            inputs['religion_place'] = self._religion_place.get_currentindex()
            inputs['religion_croyance'] = self._religion_belief.get_currentindex()
            inputs['religion_nom'] = self._religion_name.get_currentindex()

        except ValueError as e:
            QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"),
                le2mtrans(u"You must answer to all the questions"))
            return None

        return inputs

    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass

        inputs = self._get_inputs()

        if inputs:
            if not self._automatique:
                confirm = QtGui.QMessageBox.question(
                    self, le2mtrans(u"Confirmation"),
                    le2mtrans(u"Do you confirm your answers?"),
                    QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
                if confirm != QtGui.QMessageBox.Yes:
                    return

            logger.info(u"Send back: {}".format(inputs))
            self.accept()
            self._defered.callback(inputs)
        else:
            return


class DDisplayImages(QtGui.QDialog):
    def __init__(self, image):
        QtGui.QDialog.__init__(self)

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        self.label_image = QtGui.QLabel()
        layout.addWidget(self.label_image)
        self._display_image(image)

    def _display_image(self, image):
        self.current_image = image
        self.label_image.setPixmap(QtGui.QPixmap(self.current_image))

    def reject(self):
        pass

