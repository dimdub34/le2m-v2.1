# -*- coding: utf-8 -*-
"""
Ce module contient les boites de dialogue du programme.
"""

from PyQt4 import QtGui, QtCore
import logging
from client.cltgui.cltguidialogs import GuiHistorique
import PublicGoodGameGenderParams as pms
import PublicGoodGameGenderTexts as textes
from PublicGoodGameGenderGuiSrc import PublicGoodGameGenderConfigure, \
    P3G_widIcones
from client.cltgui.cltguiwidgets import WPeriod, WExplication, WSpinbox

logger = logging.getLogger("le2m")


class WIcones(QtGui.QWidget):
    def __init__(self, parent, grouptype):
        super(WIcones, self).__init__(parent)
        self.ui = P3G_widIcones.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_grouptype.setText(u"Composition de votre groupe")
        imgf = QtGui.QPixmap(pms.get_icone("F"))
        imgh = QtGui.QPixmap(pms.get_icone("H"))
        for i in range(1, 5):
            getattr(self.ui, "label_icon_{}".format(i)).setPixmap(imgf)
        for i in range(1, 1 + grouptype):
            getattr(self.ui, "label_icon_{}".format(i)).setPixmap(imgh)


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, periode, historique,
                 grouptype):
        super(GuiDecision, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique
        self._historique = GuiHistorique(self, historique)

        layout = QtGui.QVBoxLayout(self)

        self._widperiod = WPeriod(
            period=periode, ecran_historique=self._historique, parent=self)
        layout.addWidget(self._widperiod)

        self._widexplication = WExplication(
            text=textes.DECISION_explication, parent=self, size=(450, 60))
        layout.addWidget(self._widexplication)

        if pms.TRAITEMENT == pms.ICONES:
            self._widicones = WIcones(parent=self, grouptype=grouptype)
            layout.addWidget(self._widicones)

        self._widdecision = WSpinbox(
            label=textes.DECISION_label, minimum=pms.DECISION_MIN,
            maximum=pms.DECISION_MAX, interval=pms.DECISION_STEP,
            automatique=self._automatique, parent=self)
        layout.addWidget(self._widdecision)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)

        # title and size
        self.setWindowTitle(textes.DECISION_titre)
        self.adjustSize()
        self.setFixedSize(self.size())

    def reject(self):
        pass
    
    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        decision = self._widdecision.get_value()
        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, textes.DECISION_confirmation.titre,
                textes.DECISION_confirmation.message,
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes: 
                return
        logger.info(u"Decision callback {}".format(decision))
        self._defered.callback(decision)
        self.accept()


class DConfigure(QtGui.QDialog):
    def __init__(self, parent):
        super(DConfigure, self).__init__(parent)
        self.ui = PublicGoodGameGenderConfigure.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.label_treatment.setText(u"Treatment")
        treatments = pms.get_treatments()
        self.ui.comboBox_treatment.addItems(
            [treatments[k] for k in sorted(treatments.viewkeys())])
        self.ui.comboBox_treatment.setCurrentIndex(pms.TRAITEMENT)

        self.ui.label_hommes.setText(u"Nombre d'hommes")
        self.ui.spinBox_hommes.setValue(pms.NB_HOMMES)
        for i in range (5):
            getattr(self.ui, "label_{}".format(i)).setText(
                u"Nombre de groupe avec {} homme".format(i))
            getattr(self.ui, "spinBox_{}".format(i)).setValue(pms.GROUPES[i])

        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.setWindowTitle(u"Configuration")
        self.setFixedSize(300, 280)

    def _accept(self):
        self._treatment = self.ui.comboBox_treatment.currentIndex()
        self._nbhommes = self.ui.spinBox_hommes.value()
        self._groupes = {}
        for i in range(5):
            self._groupes[i] = getattr(self.ui, "spinBox_{}".format(i)).value()

        nbhtemp = 0
        for k, v in self._groupes.iteritems():
            nbhtemp += k * v
        if nbhtemp != self._nbhommes:
            QtGui.QMessageBox.critical(
                self, u"Attention", u"Le nombre d'hommes et les groupes ne "
                                    u"correspondent pas")
            return
        self.accept()

    def get_infos(self):
        return self._treatment, self._nbhommes, self._groupes
