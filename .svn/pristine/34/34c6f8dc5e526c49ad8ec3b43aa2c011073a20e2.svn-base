# -*- coding: utf-8 -*-
__author__ = "Dimitri DUBOIS"
from PyQt4.QtCore import QObject, pyqtSignal
from xml.etree import ElementTree
from twisted.spread import pb
import logging
from questcomputil import qctrans


logger = logging.getLogger("questcomp")


class Question(object):
    def __init__(self):
        self._number = 0
        self._text = u""
        self._proposals = []
        self._goodanswers = []
        self._explanation = u""

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, num):
        self._number = num

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, txt):
        self._text = txt

    @property
    def proposals(self):
        return self._proposals

    @proposals.setter
    def proposals(self, proplist):
        self._proposals = proplist

    @property
    def goodanswers(self):
        return self._goodanswers

    @goodanswers.setter
    def goodanswers(self, galist):
        self._goodanswers = galist

    @property
    def explanation(self):
        return self._explanation

    @explanation.setter
    def explanation(self, expl):
        self._explanation = expl

    def __repr__(self):
        txt = qctrans(u"Number {num}").format(num=self.number)
        txt += qctrans(u"\nText: {txt}").format(txt=self.text)
        txt += qctrans(u"\nProposals: {p}").format(p=" | ".join(self.proposals))
        txt += qctrans(u"\nGood answers: {ga}").format(
            ga=" | ".join(self.goodanswers))
        txt += qctrans(u"\nExplanation: {exp}").format(exp=self.explanation)
        return txt

    def __str__(self):
        return self.__repr__()

    def tohtml(self):
        txt = u"<p><b>"
        txt += qctrans(u"Question {num}").format(num=self.number)
        txt += u"</b><br /><i>"
        txt += qctrans(u"Text")
        txt += u"</i>: {}<br /><i>".format(self.text)
        txt += qctrans(u"Proposals")
        txt += u"</i>:<ul>"
        for p in self.proposals:
            txt += u"<li>{}</li>".format(p)
        txt += u"</ul><i>"
        txt += qctrans(u"Good answers")
        txt += u"</i>:<ul>"
        for b in self.goodanswers:
            txt += u"<li>{}</li>".format(b)
        txt += u"</ul><i>"
        txt += qctrans(u"Explanation")
        txt += u"</i>: {}</p>".format(self.explanation)
        return txt


class CopyQuestion(Question, pb.Copyable):
    """
    This class is instanciated in place of question in order to be send
    to the remote
    """
    pass


class Questionnaire(QObject):

    valuechanged = pyqtSignal()

    def __init__(self):
        super(Questionnaire, self).__init__()
        self._questions = []
        self._file = None

    def add_question(self, quest):
        self._questions.append(quest)
        self.refresh()

    def set_questions(self, questions):
        if not questions:
            return

        for q in questions:
            self.add_question(q)

    def clear(self):
        del self._questions[:]

    def get_question(self, num):
        for q in self.get_questions():
            if q.number == num:
                return q
        return None

    def get_questions(self):
        return self._questions

    def isempty(self):
        return len(self._questions) == 0

    def refresh(self):
        self._questions.sort(key=lambda q: q.number)
        for q in self._questions:
            q.number = self._questions.index(q) + 1
        self.valuechanged.emit()

    def hasnumber(self, num):
        if self.isempty():
            return False

        for q in self.get_questions():
            if q.number == num:
                return True

        return False

    def delete(self, quest):
        self._questions.remove(quest)
        self.refresh()

    def size(self):
        return len(self._questions)

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, xmlfile):
        self._file = xmlfile

    def tohtml(self):
        """
        return an html text with the questions
        :return:str
        """
        if self.isempty():
            return

        html = u""
        html += u"<html><title>"
        html += qctrans(u"Understanding questionnaire")
        html += u"</title><body><h2>"
        html += qctrans(u"Understanding questionnaire")
        html += u"</h2>"
        for q in self.get_questions():
            html += q.tohtml()
        html += u"</body></html>"

        return html

    def toxml(self):
        """
        Return an xml string with the questions inside
        :return: str
        """
        if self.isempty():
            return

        questr = ElementTree.Element(u"questionnaire")

        for q in self.get_questions():
            quest = ElementTree.SubElement(questr, u"question")
            ennonce = ElementTree.SubElement(quest, u"ennonce")
            ennonce.text = u"{}".format(q.text)
            for p in q.proposals:
                proposition = ElementTree.SubElement(quest, u"proposition")
                proposition.text = u"{}".format(p)
            for b in q.goodanswers:
                bonrep = ElementTree.SubElement(quest, u'bonneReponse')
                bonrep.text = u"{}".format(b)
            explication = ElementTree.SubElement(quest, u"explication")
            explication.text = u"{}".format(q.explanation)

        logger.debug(qctrans(u"Generated xml: {xmlgen}").format(
            xmlgen=ElementTree.dump(questr)))

        return questr


def get_questions(xmlfile):
    """
    Return the questions
    :param xmlfile:
    :return: list
    """
    questions = []
    try:
        questionnaire = ElementTree.parse(xmlfile)
        logger.debug(qctrans(u"Questionnaire: {q}".format(q=questionnaire)))
        logger.info(qctrans(u"The questionnaire has {nb} questions").format(
            nb=len(questionnaire.findall("question"))))
        compteur = 1

        for q in questionnaire.iter("question"):
            question = CopyQuestion()  # the copy for sending through the netw
            question.number = compteur
            question.text = q.find("ennonce").text
            question.proposals = [p.text for p in q.findall("proposition")]
            question.goodanswers = [g.text for g in q.findall("bonneReponse")]
            question.explanation = q.find("explication").text

            logger.info(qctrans(u"Add question: {quest}").format(
                quest=question))
            questions.append(question)
            compteur += 1

    except ElementTree.ParseError as e:
        logger.critical(e.message)

    finally:
        return questions
