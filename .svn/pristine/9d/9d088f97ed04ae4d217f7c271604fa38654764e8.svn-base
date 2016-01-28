# -*- coding: utf-8 -*-
__author__ = "Dimitri DUBOIS"

from PyQt4 import QtGui
from collections import namedtuple
from creatorutil import creatortrans
from creatorui import creatorscreen


class GuiCreator(QtGui.QDialog):
    """
    Screen that allows to set the parameters for the new part
    """

    Configuration = namedtuple(
        "Configuration",
        ["expe_name", "expe_shortname", "expe_menu", "groups_size",
         "groups_eachperiod", "periods", "currency"])

    def __init__(self, parent=None):
        super(GuiCreator, self).__init__(parent)

        self.ui = creatorscreen.Ui_Dialog()
        self.ui.setupUi(self)

        self._configuration = None

        self.ui.label_experimentname.setText(
            creatortrans(u"Part name (without spaces or caps, ex: publicGood)")
        )
        self.ui.label_experimentshortname.setText(
            creatortrans(u"Short part name (ex. PG for Public Good")
        )
        self.ui.label_experimentmenu.setText(
            creatortrans(u"Name for the menu in the main application "
                         u"(ex: Public Good)")
        )
        self.ui.label_groupsize.setText(
            creatortrans(u"Group size (0 = no group)")
        )
        self.ui.spinBox_groupsize.setValue(0)
        self.ui.label_groupseachperiod.setText(
            creatortrans(u"Do groups have to be formed each period?")
        )
        self.ui.comboBox_groupseachperiod.addItems(
            [creatortrans(u"No"), creatortrans(u"Yes")]
        )
        self.ui.label_periods.setText(
            creatortrans(u"Number of periods (0 = one-shot game)")
        )
        self.ui.spinBox_periods.setValue(0)
        self.ui.label_currency.setText(
            creatortrans(u"Experimental currency unit (empty if the "
                         u"same that the local currency)")
        )
        self.ui.lineEdit_currency.setText(
            creatortrans(u"ecu")
        )

        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.setWindowTitle(
            creatortrans(u"Configuration of a new part"))

    def _accept(self):
        """
        check if all the fields are filled in and if the data are consistents
        """
        try:

            expe_name = unicode(
                self.ui.lineEdit_experimentname.text().toUtf8(), "utf-8")
            expe_shortname = unicode(
                self.ui.lineEdit_experimentshortname.text().toUtf8(),
                "utf-8").upper()
            expe_menu = unicode(
                self.ui.lineEdit_experimentmenu.text().toUtf8(), "utf-8")
            periods = str(self.ui.spinBox_periods.value())
            groups_size = str(self.ui.spinBox_groupsize.value())
            groups_eachperiod = \
                str(bool(self.ui.comboBox_groupseachperiod.currentIndex()))
            currency = unicode(
                self.ui.lineEdit_currency.text().toUtf8(), "utf-8"
            ) or str(None)
            if not (expe_name and expe_shortname and expe_menu):
                raise ValueError(
                    creatortrans(u"All the text field are required"))

        except ValueError as e:
            QtGui.QMessageBox.warning(
                self, creatortrans(u"Warning"), e.message)
            return

        else:
            self._configuration = self.Configuration(
                expe_name, expe_shortname, expe_menu, groups_size,
                groups_eachperiod, periods, currency)

            confirmation = QtGui.QMessageBox.question(
                self, creatortrans(u"Confirmation"),
                creatortrans(u"Apply the following configuration?\n{}".format(
                    self._configuration)),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes:
                return
            self._directory = \
                str(
                    QtGui.QFileDialog.getExistingDirectory(
                        self,
                        creatortrans(u"Select the target directory "
                                     u"(to be loaded by LE2M the files must "
                                     u"be in le2m/parts directory)")))
            if not self._directory:
                return
            self.accept()

    def get_configuration(self):
        return self._directory, self._configuration
