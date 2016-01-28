# -*- coding: utf-8 -*-
"""
Ce module contient les boites de dialogue du programme.
"""

from PyQt4 import QtGui, QtCore
import logging
import voteMajoriteParams as pms
from client.cltgui.cltguiwidgets import WExplication, WListDrag, WRadio, \
    WTableview
from voteMajoriteGuiSrc import widTable
from client.cltgui.cltguitablemodels import TableModelHistorique
from util.utiltools import get_pluriel

logger = logging.getLogger("le2m")


class WTable(QtGui.QWidget):
    def __init__(self, parent, valeurs, period):
        super(WTable, self).__init__(parent)
        self.ui = widTable.Ui_Form()
        self.ui.setupUi(self)

        for i in range(4):
            getattr(self.ui, "label_pol_{}".format(i)).setText(
                u"Politique {}".format(i+1))
            getattr(self.ui, "label_val_{}".format(i)).setText(str(valeurs[i]))
        if period > 0:
            font = getattr(self.ui, "label_pol_{}".format(period-1)).font()
            font.setBold(True)
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
            labpol = getattr(self.ui, "label_pol_{}".format(period-1))
            labpol.setFont(font)
            labpol.setPalette(palette)
            labval = getattr(self.ui, "label_val_{}".format(period-1))
            labval.setFont(font)
            labval.setPalette(palette)


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, period, valeurs):
        super(GuiDecision, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        self._widexplication = WExplication(
                parent=self,
                text=u"Politique {}.\nLa mise en application de la politique "
                     u"vous coûte {}.\nVous devez voter pour ou contre.".format(
                        period, get_pluriel(pms.COUT, u"ecu")),
                size=(400, 80))
        layout.addWidget(self._widexplication)

        self._widpolitiques = WTable(self, valeurs, period)
        layout.addWidget(self._widpolitiques)

        self._widradio = WRadio(
            label=u"Vous votez", texts=pms.RADIOS,
            automatique=self._automatique, parent=self)
        layout.addWidget(self._widradio)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)

        self.setWindowTitle(u"Décision")
        self.adjustSize()
        self.setFixedSize(self.size())

    def reject(self):
        pass
    
    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        try:
            dec = self._widradio.get_checkedbutton()
        except ValueError as e:
            QtGui.QMessageBox.warning(
                self, u"Attention", e.message)
            return
        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, u"Confirmation", u"Vous confirmez votre choix?",
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes: 
                return
        logger.info(u"Renvoi {}".format(dec))
        self._defered.callback(dec)
        self.accept()


class DConfigure(QtGui.QDialog):
    def __init__(self, parent):
        super(DConfigure, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)

        self._widexplication = WExplication(
                parent=self,
                text=u"Choisir les profils à appliquer dans la session",
                size=(220, 50))
        layout.addWidget(self._widexplication)

        self._widlistdrag = WListDrag(parent=self, size=(100, 150))
        self._widlistdrag.ui.listWidget_left.addItems(
            sorted(list(pms.PROFILS.viewkeys())))
        layout.addWidget(self._widlistdrag)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok,
            QtCore.Qt.Horizontal)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(u"Configuration")
        self.adjustSize()

    def _accept(self):
        self._profils = self._widlistdrag.get_rightitems()
        self.accept()

    def get_infos(self):
        return self._profils


class DSummary(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, texte, historique,
                 valeurs):
        super(DSummary, self).__init__(parent)
        self._defered = defered

        layout = QtGui.QVBoxLayout(self)

        self._widexplication = WExplication(text=texte, parent=self,
                                            size=(550, 120))
        layout.addWidget(self._widexplication)

        self._widpolitiques = WTable(self, valeurs, 0)
        layout.addWidget(self._widpolitiques)

        self.tablemodel = TableModelHistorique(historique)
        self._widtableview = WTableview(self, self.tablemodel, size=(550, 150))
        self._widtableview.ui.tableView.verticalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch)
        layout.addWidget(self._widtableview)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        buttons.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self._accept)
        layout.addWidget(buttons)

        if automatique:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer.start(7000)

        self.setWindowTitle(u"Récapitulatif")
        self.adjustSize()
        self.setFixedSize(self.size())

    def reject(self):
        pass

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass
        self.accept()
        self._defered.callback(1)
