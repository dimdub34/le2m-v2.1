# -*- coding: utf-8 -*-
__author__ = "Dimitri DUBOIS"

from PyQt4 import QtGui, QtCore
import logging
from extractorui import extractorscreen
from extractorutil import extrans


logger = logging.getLogger("extractor.{}".format(__name__))


class GuiExtractor(QtGui.QDialog):
    def __init__(self, parts):
        super(GuiExtractor, self).__init__()

        self.ui = extractorscreen.Ui_Dialog()
        self.ui.setupUi(self)

        self._selectedparts = []

        self.ui.label.setText(extrans(u"Select the parts you want to extract"))
        self._model = QtGui.QStandardItemModel()
        self.ui.listView.setModel(self._model)
        self.ui.listView.setFixedSize(500, 400)

        for p in parts:
            item = QtGui.QStandardItem('{}'.format(p))
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            item.setEditable(False)
            self._model.appendRow(item)

        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self._checkbox = []

        self.setWindowTitle(extrans(u"Data extraction"))

    def _accept(self):
        for ligne in range(self._model.rowCount()):
            item = self._model.item(ligne)
            if item.checkState() == QtCore.Qt.Checked:
                self._selectedparts.append(str(item.text()))

        if not self._selectedparts:
            QtGui.QMessageBox.critical(
                self, extrans(u"Error"),
                extrans(u"At least one part should be selected for extraction")
            )
            return

        self._dirout = str(QtGui.QFileDialog.getExistingDirectory(
            self, extrans(u"Please select the directory in which to extract "
                          u"the data"))
        )
        if not self._dirout:
            return

        self.accept()

    def get_extractinfos(self):
        return self._dirout, self._selectedparts