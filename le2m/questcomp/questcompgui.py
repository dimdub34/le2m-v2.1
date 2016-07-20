# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import os
import logging
import random
from xml.etree import ElementTree
import questcomputil
from questcompui import questcompquest, questcompquestedit, \
    questcompscreen
from questcomputil import qctrans
import questcompmod


logger = None


class GuiQuestComp(QtGui.QMainWindow):
    def __init__(self):
        super(GuiQuestComp, self).__init__()

        global logger
        questcomputil.create_logger()
        logger = logging.getLogger("questcomp")

        self.ui = questcompscreen.Ui_MainWindow()
        self.ui.setupUi(self)

        self._questionnaire = questcompmod.Questionnaire()
        self._questionnaire.valuechanged.connect(self._displayquestionnaire)

        # menus ----------------------------------------------------------------
        # file
        menu_file = QtGui.QMenu(qctrans(u"File"), self.ui.menubar)
        self.ui.menubar.addMenu(menu_file)
        submenu_filenew = QtGui.QMenu(qctrans(u"New"), menu_file)
        menu_file.addMenu(submenu_filenew)
        action_newquestionnaire = QtGui.QAction(
            qctrans(u"Questionnaire"), submenu_filenew)
        action_newquestionnaire.triggered.connect(self._newquestionnaire)
        submenu_filenew.addAction(action_newquestionnaire)
        action_newquestion = QtGui.QAction(
            qctrans(u"Question"), submenu_filenew)
        action_newquestion.triggered.connect(self._newquest)
        action_newquestion.setShortcut(QtGui.QKeySequence("Ctrl+n"))
        submenu_filenew.addAction(action_newquestion)
        menu_file.addSeparator()
        action_open = QtGui.QAction(qctrans(u"Open"), menu_file)
        action_open.triggered.connect(self._open)
        action_open.setShortcut(QtGui.QKeySequence("Ctrl+o"))
        menu_file.addAction(action_open)
        action_save = QtGui.QAction(qctrans(u"Save"), menu_file)
        action_save.triggered.connect(self._save)
        action_save.setShortcut(QtGui.QKeySequence("Ctrl+s"))
        menu_file.addAction(action_save)
        action_saveas = QtGui.QAction(qctrans(u"Save as"), menu_file)
        action_saveas.triggered.connect(self._saveas)
        menu_file.addAction(action_saveas)
        menu_file.addSeparator()
        action_print = QtGui.QAction(qctrans(u"Print"), menu_file)
        action_print.triggered.connect(self._print)
        action_print.setShortcut(QtGui.QKeySequence("Ctrl+p"))
        menu_file.addAction(action_print)
        action_close = QtGui.QAction(qctrans(u"Quit"), menu_file)
        action_close.triggered.connect(self.close)
        action_close.setShortcut(QtGui.QKeySequence("Ctrl+q"))
        menu_file.addAction(action_close)

        # tools
        menu_tools = QtGui.QMenu(qctrans(u"Tools"), self.ui.menubar)
        self.ui.menubar.addMenu(menu_tools)
        action_test = QtGui.QAction(
            qctrans(u"Test the questionnaire"), menu_tools)
        action_test.triggered.connect(self._test)
        menu_tools.addAction(action_test)
        
        # contextual menu of the treeWidget_questionnaire
        self.ui.treeWidget_questionnaire.setHeaderItem(
            QtGui.QTreeWidgetItem([qctrans(u"Understanding questions")]))
        self.ui.treeWidget_questionnaire.header().setResizeMode(
            QtGui.QHeaderView.Stretch)
        self.ui.treeWidget_questionnaire.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.treeWidget_questionnaire. \
            customContextMenuRequested["QPoint"].connect(self._menucontexttree)

        self.setFixedSize(800, 600)
        frameg = self.frameGeometry()
        cent = QtGui.QDesktopWidget().availableGeometry().center()
        frameg.moveCenter(cent)
        self.move(frameg.topLeft())

    def _menucontexttree(self, point):
        """
        From the point we collect the question and then we propose to edit
        that question or to delete it
        """
        try:
            item = self.ui.treeWidget_questionnaire.itemAt(point)
            nom = unicode(item.text(0).toUtf8(), "utf-8")
            num = int(nom.split()[1])
            question = self._questionnaire.get_question(num)
            menu = QtGui.QMenu(self)
            action_modify = QtGui.QAction(qctrans(u"Modify"), menu)
            action_modify.triggered.connect(lambda _: self._editquest(question))
            menu.addAction(action_modify)
            action_delete = QtGui.QAction(qctrans(u"Delete"), menu)
            action_delete.triggered.connect(lambda _: self._deletequest(question))
            menu.addAction(action_delete)
            menu.exec_(QtGui.QCursor.pos())
        except (IndexError, AttributeError, ValueError):
            pass

    def _newquestionnaire(self):
        """
        Clear the current questionnaire (and the associated file) and
        create a (empty) new one
        """
        if not self._questionnaire.isempty():
            confirm = QtGui.QMessageBox.question(
                self, qctrans(u"Confirmation"),
                qctrans(u"An understanding questionnaire is loaded. Do you "
                        u"really want to close it and create a new one?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes
            )
            if confirm != QtGui.QMessageBox.Yes:
                return
        self._questionnaire.clear()
        self._questionnaire.file = None
        self.ui.treeWidget_questionnaire.clear()

    def _open(self):
        """
        Open an understanding questionnaire (xml file), get the questions
        that are inside the file and set them in the questionnaire
        """
        if not self._questionnaire.isempty():
            confirm = QtGui.QMessageBox.question(
                self, qctrans(u"Confirmation"),
                qctrans(u"An understanding questionnaire is loaded. Do you "
                        u"really want to close it and open a new one?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirm != QtGui.QMessageBox.Yes:
                return

        xmlfile = str(QtGui.QFileDialog.getOpenFileName(
            self, qctrans(u"Select the understanding questionnaire"), "",
            qctrans(u"xml file (*.xml)")))
        if not xmlfile:
            return

        self._questionnaire.file = xmlfile
        questions = questcompmod.get_questions(xmlfile)
        self._questionnaire.set_questions(questions)

    def _save(self):
        """
        Save the questionnaire.
        If the questionnaire has no file associated the call _saveas before
        """
        if not self._questionnaire.file:
            self._saveas()
            if not self._questionnaire.file:
                return  # _saveas has been canceled

        questxml = self._questionnaire.toxml()
        if questxml is None:
            return

        try:
            ElementTree.ElementTree(questxml).write(
                self._questionnaire.file, encoding="utf-8")
        except ElementTree.ParseError as e:
            logger.critical(
                qctrans(u"Error while saving the understanding questionnaire "
                        u"in the xml file: {msg}".format(msg=e.message)))
            return

        QtGui.QMessageBox.information(
            self, qctrans(u"File saved"),
            qctrans(u"Understanding questionnaire saved"))

    def _saveas(self):
        """
        """
        xmlfile = str(QtGui.QFileDialog.getSaveFileName(
            self, qctrans(u"xml file")))
        if not xmlfile:
            return

        if os.path.splitext(xmlfile)[1] != ".xml":
            xmlfile += ".xml"
        self._questionnaire.file = xmlfile
        self._save()

    def _print(self):
        html = self._questionnaire.tohtml()
        if not html:
            return

        printer = QtGui.QPrinter()
        doc = QtGui.QTextDocument()
        doc.setHtml(html)
        dialog = QtGui.QPrintDialog(printer)
        dialog.setModal(True)
        dialog.setWindowTitle(qctrans(u"Understanding questionnaire"))
        if dialog.exec_(): 
            doc.print_(printer)
            QtGui.QMessageBox.information(
                self, qctrans(u"Print"),
                qctrans(u"Understanding questionnaire successfully printed"))
    
    def _newquest(self):
        questedit = GuiQuestEdit(self, self._questionnaire)
        questedit.exec_()

    def _editquest(self, quest):
        questedit = GuiQuestEdit(self, self._questionnaire, quest)
        questedit.exec_()

    def _displayquestionnaire(self):
        """
        """
        self.ui.treeWidget_questionnaire.clear()
        for q in self._questionnaire.get_questions():
            self._displayquest(q)

    def _displayquest(self, quest):
        """
        """
        if not quest:
            return

        twi_question = QtGui.QTreeWidgetItem(
            [qctrans(u"Question {num}").format(num=quest.number)])
        self.ui.treeWidget_questionnaire.addTopLevelItem(twi_question)

        twi_ennonce = QtGui.QTreeWidgetItem([qctrans(u"Text")])
        twi_ennonce.addChild(QtGui.QTreeWidgetItem([quest.text]))
        twi_question.addChild(twi_ennonce)

        twi_propositions = QtGui.QTreeWidgetItem([qctrans(u"Proposals")])
        for p in quest.proposals:
            twi_propositions.addChild(QtGui.QTreeWidgetItem([p]))
        twi_question.addChild(twi_propositions)

        twi_bonnes_reponses = QtGui.QTreeWidgetItem(
            [qctrans(u"Good answers")])
        for b in quest.goodanswers:
            twi_bonnes_reponses.addChild(QtGui.QTreeWidgetItem([b]))
        twi_question.addChild(twi_bonnes_reponses)

        twi_explication = QtGui.QTreeWidgetItem([qctrans(u"Explanation")])
        twi_explication.addChild(
            QtGui.QTreeWidgetItem([quest.explanation]))
        twi_question.addChild(twi_explication)

    def _deletequest(self, quest):
        confirmation = QtGui.QMessageBox.question(
            self, qctrans(u"Confirmation"),
            qctrans(u"Delete {q}?").format(q=quest),
            QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
        if confirmation != QtGui.QMessageBox.Yes:
            return
        self._questionnaire.delete(quest)

    def closeEvent(self, event):
        confirmation = QtGui.QMessageBox.question(
            self, qctrans(u"Confirmation"),
            qctrans(u"Are you sure you want to quit?"),
            QtGui.QMessageBox.No | QtGui.QMessageBox.Yes
        )
        if confirmation != QtGui.QMessageBox.Yes: 
            event.ignore()
            return
        event.accept()
        
    def _test(self):
        if self._questionnaire.isempty():
            QtGui.QMessageBox.warning(
                self, qctrans(u"Warning"),
                qctrans(u"There is no questionnaire loaded"))
            return

        faults = []
        for c, q in enumerate(self._questionnaire.get_questions()):
            ecran = GuiQuestCompQuest(None, False, q, self)
            ecran.exec_()
            if ecran.iswrong():
                faults.append(c+1)
        QtGui.QMessageBox.information(
            self, qctrans(u"End"),
            qctrans(u"You've done {nbfaults} fault(s) {q}").format(
                nbfaults=len(faults),
                q=u"" if not faults else u"({})".format(faults)))


class GuiQuestEdit(QtGui.QDialog):
    """
    Screen for displaying, creating or editing a question
    """
    def __init__(self, parent, questionnaire, question=None):
        super(GuiQuestEdit, self).__init__(parent)
        
        self.ui = questcompquestedit.Ui_Dialog()
        self.ui.setupUi(self)

        self._questionnaire = questionnaire
        self._edit = True if question else False
        self._question = question or questcompmod.Question()

        self.ui.spinBox_numero.setToolTip(
            qctrans(u"This number is used to sort the list of questions"))
        if not self._edit:
            self.ui.spinBox_numero.setValue(self._questionnaire.size() + 1)
        else:
            self.ui.spinBox_numero.setValue(self._question.number)
        self.ui.textEdit_ennonce.setText(self._question.text)
        for c, p in enumerate(self._question.proposals):
            le = getattr(self.ui, "lineEdit_propositions_{}".format(c+1))
            le.setText(p)
            if p in self._question.goodanswers:
                ckb = getattr(self.ui, "checkBox_propositions_{}".format(c+1))
                ckb.setChecked(True)
        self.ui.textEdit_explication.setText(self._question.explanation)

        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        
    def _testcontent(self):
        """
        Test the content of fields
        If everything is ok return a question
        :return: Question
        """
        quest = None
        try:
            # num
            num = self.ui.spinBox_numero.value()
            if not self._edit or \
            (self._edit and num != self._question.number):
                if self._questionnaire.hasnumber(num):
                    raise ValueError(qctrans(u"This number already exists, "
                                             u"please choose another one"))

            text = unicode(self.ui.textEdit_ennonce.toPlainText().toUtf8(),
                           "utf-8")
            if not text:
                raise ValueError(qctrans(u"You need to provide a text"))

            proposals, goodanswers = [], []
            for i in xrange(1, 7):
                leprop = getattr(self.ui, "lineEdit_propositions_{}".format(i))
                txtprop = unicode(leprop.text().toUtf8(), "utf-8")
                if txtprop:
                    proposals.append(txtprop)
                    chkb= getattr(self.ui, "checkBox_propositions_{}".format(i))
                    if chkb.isChecked():
                        goodanswers.append(txtprop)

            if len(proposals) < 2:
                raise ValueError(qctrans(u"You must give at least 2 proposals"))
            if not goodanswers:
                raise ValueError(qctrans(u"You must give at least 1 good "
                                         u"answer"))

            explanation = unicode(
                self.ui.textEdit_explication.toPlainText().toUtf8(),
                "utf-8")
            if not explanation:
                raise ValueError(qctrans(u"You need to provide an explanation"))

            quest = questcompmod.Question()
            quest.number = num
            quest.text = text
            quest.proposals = proposals
            quest.goodanswers = goodanswers
            quest.explanation = explanation

        except ValueError as e:
            QtGui.QMessageBox.critical(
                self,  qctrans(u"Error"), e.message)

        finally:
            return quest
        
    def _accept(self):
        quest = self._testcontent()
        logger.debug(qctrans(u"Edited question: {q}").format(q=quest))
        if not quest:
            return

        if self._edit:
            confirmation = QtGui.QMessageBox.question(
                self,
                qctrans(u"Confirmation"),
                qctrans(u"Do you want to save changes for this question?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation == QtGui.QMessageBox.Yes:
                for att in ["number", "text", "proposals", "goodanswers",
                            "explanation"]:
                    setattr(self._question, att, getattr(quest, att))
                self._questionnaire.refresh()
        else:
            confirmation = QtGui.QMessageBox.question(
                self,
                qctrans(u"Confirmation"),
                qctrans(u"Do you want to add this question to the "
                        u"questionnaire?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes
            )
            if confirmation == QtGui.QMessageBox.Yes:
                self._questionnaire.add_question(quest)

        self.accept()


class GuiQuestCompQuest(QtGui.QDialog):
    def __init__(self, defered, automatique, question, parent=None):
        super(GuiQuestCompQuest, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique
        self._question = question

        self.ui = questcompquest.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.label_numeroQuestion.setText(qctrans(u"Question {num}").format(
            num=self._question.number))
        self.ui.textEdit_ennonce.setText(self._question.text)

        # proposals ------------------------------------------------------------
        espace_gauche = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ui.hl_propositions.addItem(espace_gauche)

        self._cases_decisions = []
        # boutons radio --------------------------------------------------------
        if len(self._question.goodanswers) == 1:
            for p in self._question.proposals:
                btn = QtGui.QRadioButton(p, self)
                self._cases_decisions.append(btn)
                self.ui.hl_propositions.addWidget(btn)
            if self._automatique:
                random.choice(self._cases_decisions).setChecked(True)
        # checkbox -------------------------------------------------------------
        else:
            for p in self._question.proposals:
                checkbox = QtGui.QCheckBox(p, self)
                self._cases_decisions.append(checkbox)
                self.ui.hl_propositions.addWidget(checkbox)
            if self._automatique:
                nb = random.randint(1, len(self._question.proposals) - 1)
                for i in range(1, nb + 1):
                    b = random.choice(self._cases_decisions)
                    if not b.isChecked():
                        b.setChecked(True)

        espace_droite = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ui.hl_propositions.addItem(espace_droite)

        self.ui.pushButton_valider.clicked.connect(self._accept)

        self.adjustSize()
        self.setFixedSize(self.size())

        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(self._accept)
            self._timer.start(7000)

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass

        textes_items_selectionnes = []
        for b in self._cases_decisions:
            if b.isChecked():
                textes_items_selectionnes.append(
                    unicode(b.text().toUtf8(), "utf-8"))
        if not textes_items_selectionnes:
            QtGui.QMessageBox.warning(
                self, qctrans(u'Warning'),
                qctrans(u"You must answer to the question"))
            return

        self._wrong = False
        for br in self._question.goodanswers:
            if br not in textes_items_selectionnes:
                self._wrong = True

        # si pas automatique on affiche l'explication de la réponse
        if not self._automatique:
            if len(self._question.goodanswers) > 1:
                texte = qctrans(u"The right answers were")
                texte += u": \n {}".format(
                    u"\n".join(self._question.goodanswers))
            else:
                texte = qctrans(u"The right answer was ")
                texte += u": {}".format(self._question.goodanswers[0])

            texte += u"\n\n{}".format(self._question.explanation)

            QtGui.QMessageBox.information(self, qctrans("Information"), texte)

        if self._defered:
            self._defered.callback(self._wrong)
        self.accept()

    def iswrong(self):
        return self._wrong

    def reject(self):
        pass  # on ne fait rien si le sujet clique sur la croix

