# coding: utf-8

from PyQt4 import QtGui, QtCore
import random
from datetime import timedelta
from util.utiltools import CompteARebours
try:  # this way it is possible to load this module independently
    from util.utili18n import le2mtrans
except AttributeError:
    le2mtrans = lambda x: x
from cltguisrc.cltguisrcwid import widPeriod, widCombo, \
    widSpinbox, widRadio, widListDrag, widTableview, widCompterebours, \
    widChat, widSlider, widLabel, widLineEdit
from configuration.configvar import YES_NO
import logging
import numpy as np


logger = logging.getLogger("le2m")


class WLabel(QtGui.QWidget):
    def __init__(self, text=None, parent=None):
        super(WLabel, self).__init__(parent)
        self.ui = widLabel.Ui_Form()
        self.ui.setupUi(self)
        self.set_text(text or u"")

    def set_text(self, text):
        self.ui.label.setText(text)


class WPeriod(QtGui.QWidget):
    def __init__(self, period=1, ecran_historique=None, parent=None):
        QtGui.QWidget.__init__(self, parent)

        layout = QtGui.QHBoxLayout()
        self.setLayout(layout)

        self._label_period = QtGui.QLabel()
        self.set_period(period)
        layout.addWidget(self._label_period)

        layout.addSpacerItem(QtGui.QSpacerItem(
            20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))

        self._pushButton_history = QtGui.QPushButton(le2mtrans(u"History"))
        layout.addWidget(self._pushButton_history)
        if ecran_historique:
            self._pushButton_history.clicked.connect(ecran_historique.show)

    def set_period(self, period):
        self._label_period.setText(
            le2mtrans(u"Period") + u" {}".format(period))


class WExplication(QtGui.QWidget):
    def __init__(self, text=None, parent=None, size=(450, 80), html=True):
        QtGui.QWidget.__init__(self, parent)

        layout = QtGui.QHBoxLayout()
        self.setLayout(layout)

        self._textEdit = QtGui.QTextEdit()
        self._textEdit.setReadOnly(True)
        self._textEdit.setFixedSize(*size)
        layout.addWidget(self._textEdit)

        if html:
            self.set_html(text or u"")
        else:
            self.set_text(text or u"")
        self.adjustSize()

    def set_size(self, size):
        self._textEdit.setFixedSize(*size)
        self.adjustSize()

    def set_text(self, text):
        self._textEdit.setText(text)

    def set_html(self, html):
        self._textEdit.setHtml(html)

    def get_text(self):
        return self._textEdit.toPlainText()


class WCombo(QtGui.QWidget):
    def __init__(self, label, items, automatique=False, parent=None,
                 autotime=500):
        super(WCombo, self).__init__(parent)
        self.ui = widCombo.Ui_Form()
        self.ui.setupUi(self)
        self._items = items
        self.ui.label.setText(label)
        self.ui.comboBox.addItems(self._items)
        if automatique:
            self._timer = QtCore.QTimer()
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(self._changeindex)
            self._timer.start(autotime)

    def _changeindex(self):
        if self._items[0] == le2mtrans(u"Choose") or \
                        self._items[0] == u"Choisir":
            self.ui.comboBox.setCurrentIndex(
                random.randint(1, len(self._items)-1))
        else:
            self.ui.comboBox.setCurrentIndex(
                random.randint(0, len(self._items)-1))

    def get_currentindex(self):
        if self._items[0] == le2mtrans(u"Choose") and \
                        self.ui.comboBox.currentIndex() == 0:
            raise ValueError(u"No index selected")
        return self.ui.comboBox.currentIndex()


class WSpinbox(QtGui.QWidget):
    def __init__(self, label, minimum=0, maximum=100, interval=1,
                 automatique=False, parent=None, autotime=500, width=50):
        QtGui.QWidget.__init__(self, parent)

        self._minimum = minimum
        self._maximum = maximum
        self._interval = interval

        layout = QtGui.QHBoxLayout()
        self.setLayout(layout)

        formlayout = QtGui.QFormLayout()
        layout.addLayout(formlayout)

        self._label = QtGui.QLabel(label)
        self._spinBox = QtGui.QSpinBox()
        self._spinBox.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        self._spinBox.setMinimum(self._minimum)
        self._spinBox.setMaximum(self._maximum)
        self._spinBox.setSingleStep(self._interval)
        self._spinBox.setValue(self._minimum)
        self._spinBox.setFixedWidth(50)

        formlayout.addRow(self._label, self._spinBox)

        if automatique:
            self._timer = QtCore.QTimer()
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(self._changevalue)
            self._timer.start(autotime)

    def _changevalue(self):
        self._spinBox.setValue(
                    random.randrange(self._minimum, self._maximum + 1,
                                     self._interval))

    def get_value(self):
        return self._spinBox.value()


class WRadio(QtGui.QWidget):
    def __init__(self, label,
                 texts=tuple([v for k, v in sorted(YES_NO.viewitems())]),
                 automatique=False, parent=None, autotime=500):
        super(WRadio, self).__init__(parent)
        self.ui = widRadio.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label.setText(label)
        self.ui.radioButton_0.setText(texts[0])
        self.ui.radioButton_1.setText(texts[1])
        if len(texts) > 2:
            for i in range(2, len(texts)):
                setattr(self.ui, "radioButton_{}".format(i),
                        QtGui.QRadioButton())
                getattr(self.ui, "radioButton_{}".format(i)).setText(texts[i])
                self.ui.buttonGroup.addButton(
                    getattr(self.ui, "radioButton_{}".format(i)))
                self.ui.horizontalLayout_radios.addWidget(
                    getattr(self.ui, "radioButton_{}".format(i)))

        if automatique:
            self._timer = QtCore.QTimer()
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(self._checkbutton)
            self._timer.start(autotime)

    def _checkbutton(self):
        radios = [v for k, v in self.ui.__dict__.viewitems() if "radioButton" in k]
        selected = random.choice(radios)
        selected.setChecked(True)

    def get_checkedbutton(self):
        """
        Return the index of the checked radioButton in the list
        :return: Integer
        """
        radios = [v for k, v in sorted(self.ui.__dict__.viewitems()) if
                  "radioButton" in k]
        checked = None
        for i, r in enumerate(radios):
            if r.isChecked():
                checked = i
                break
        if checked is None:
            raise ValueError(le2mtrans(u"No item selected"))
        return checked


class WListDrag(QtGui.QWidget):
    """
    This widget allows to move some elements from the list on the left side to
    the list on the right side.
    """
    def __init__(self, parent, size=(80, 100)):
        super(WListDrag, self).__init__(parent)
        self.ui = widListDrag.Ui_Form()
        self.ui.setupUi(self)

        self.ui.listWidget_left.setFixedSize(size[0], size[1])
        self.ui.listWidget_left.setToolTip(
            le2mtrans(u"Drag one or several item(s) from this list to the "
                      u"list on the right side"))
        self.ui.listWidget_right.setFixedSize(size[0], size[1])
        self.ui.listWidget_right.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.listWidget_right.customContextMenuRequested.connect(
            self._rightclick)
        self.ui.listWidget_right.setToolTip(
            le2mtrans(u"Right click to move up, down or delete an item"))

        self._menu = QtGui.QMenu(le2mtrans(u"Menu"), self)

        self._action_moveup = QtGui.QAction(le2mtrans(u"Move up"), self._menu)
        self._action_moveup.triggered.connect(self._moveup)
        self._menu.addAction(self._action_moveup)

        self._action_movedown = QtGui.QAction(le2mtrans(u"Move down"), self._menu)
        self._action_movedown.triggered.connect(self._movedown)
        self._menu.addAction(self._action_movedown)

        self._action_delete = QtGui.QAction(le2mtrans(u"Delete"), self._menu)
        self._action_delete.triggered.connect(self._delete)
        self._menu.addAction(self._action_delete)

    def _rightclick(self, point):
        self._menu.exec_(self.ui.listWidget_right.mapToGlobal(point))

    def _delete(self):
        currentrow = self.ui.listWidget_right.currentRow()
        self.ui.listWidget_right.takeItem(currentrow)

    def _moveup(self):
        currentrow = self.ui.listWidget_right.currentRow()
        currentitem = self.ui.listWidget_right.takeItem(currentrow)
        self.ui.listWidget_right.insertItem(currentrow - 1, currentitem)

    def _movedown(self):
        currentrow = self.ui.listWidget_right.currentRow()
        currentitem = self.ui.listWidget_right.takeItem(currentrow)
        self.ui.listWidget_right.insertItem(currentrow + 1, currentitem)

    def get_rightitems(self):
        items = []
        for i in range(self.ui.listWidget_right.count()):
            items.append(str(self.ui.listWidget_right.item(i).text()))
        return items


class WTableview(QtGui.QWidget):
    def __init__(self, parent, tablemodel, size=(600, 600)):
        super(WTableview, self).__init__(parent)

        self.ui = widTableview.Ui_Form()
        self.ui.setupUi(self)
        self.ui.tableView.setModel(tablemodel)
        self.ui.tableView.setFixedSize(size[0], size[1])
        self.ui.tableView.horizontalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch)
        self.adjustSize()


class WCompterebours(QtGui.QWidget):
    """

    """
    def __init__(self, parent, temps, actionfin):
        """
        :param parent:
        :param temps: datetime.time(0, 2, 0)  # heures, minutes, secondes
        :param actionfin:
        :return:
        """
        super(WCompterebours, self).__init__(parent)
        self.ui = widCompterebours.Ui_Form()
        self.ui.setupUi(self)

        self.ui.label.setText(le2mtrans(u"Remaining time:"))
        tps = timedelta(hours=temps.hour, minutes=temps.minute,
                        seconds=temps.second).seconds
        self.compterebours = CompteARebours(tps)
        self.compterebours.changetime[str].connect(self.ui.label_timer.setText)
        self.compterebours.endoftime.connect(actionfin)
        self.compterebours.start()

    def stop(self):
        self.compterebours.stop()

    def is_running(self):
        return self.compterebours.isRunning()


class WChat(QtGui.QWidget):
    def __init__(self, parent, action_send, size_read=(450, 150),
                 size_write=(450, 60)):
        super(WChat, self).__init__(parent)
        self.ui = widChat.Ui_Form()
        self.ui.setupUi(self)

        self.ui.label_read.setText(le2mtrans(u"Instant messaging"))
        self.ui.textEdit_read.setFixedSize(size_read[0], size_read[1])
        self.ui.label_write.setText(le2mtrans(u"Write your message below"))
        self.ui.textEdit_read.setReadOnly(True)
        self.ui.textEdit_write.setFixedSize(size_write[0], size_write[1])

        self.ui.pushButton.setText(le2mtrans(u"Send the message"))
        self.ui.pushButton.clicked.connect(
            lambda _: action_send(
                unicode(
                    self.ui.textEdit_write.toPlainText().toUtf8(), "utf-8")))

    def add_text(self, text):
        self.ui.textEdit_read.insertPlainText(text)
        if text[:-1] != '\n':
            self.ui.textEdit_read.insertPlainText('\n')
        bar = self.ui.textEdit_read.verticalScrollBar()
        bar.setValue(bar.maximum())

    def clear_writespace(self):
        self.ui.textEdit_write.clear()

    def write(self, msg):
        self.ui.textEdit_write.setText(msg)


class WSlider(QtGui.QWidget):
    def __init__(self, label, minimum=0, maximum=10, interval=1,
                 automatique=False, autotime=500, parent=None):
        super(WSlider, self).__init__(parent)

        self._minimum = minimum
        self._maximum = maximum
        self._interval = interval

        self.ui = widSlider.Ui_Form()
        self.ui.setupUi(self)

        self.ui.label.setText(label)
        self.ui.horizontalSlider.setMinimum(minimum)
        self.ui.horizontalSlider.setMaximum(maximum)
        self.ui.horizontalSlider.setSingleStep(interval)
        self.ui.horizontalSlider.setValue(minimum)
        self.ui.lcdNumber.display(self.ui.horizontalSlider.value())

        if automatique:
            self._timer = QtCore.QTimer()
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(self._changevalue)
            self._timer.start(autotime)

    def _changevalue(self):
        self.ui.horizontalSlider.setValue(
            random.randrange(self._minimum, self._maximum, self._interval))

    def get_value(self):
        return self.ui.horizontalSlider.value()


class WLineEdit(QtGui.QWidget):
    def __init__(self, parent, label, automatique=False,
                 list_of_possible_values=[u"val {}".format(i) for i in range(5)],
                 autotime=1000):
        super(WLineEdit, self).__init__(parent)

        self._automatique = automatique
        self._autotime = autotime

        self.ui = widLineEdit.Ui_Form()
        self.ui.setupUi(self)

        self.ui.label.setText(label)

        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(
                lambda: self.ui.lineEdit.setText(
                    random.choice(list_of_possible_values)))
            self._timer.start(self._autotime)

    def get_text(self):
        text = unicode(self.ui.lineEdit.text().toUtf8(), encoding='utf-8')
        logger.debug(text)
        if not text:
            raise ValueError(le2mtrans(u"You must complete the text area") +
                             u" ({})".format(self.ui.label.text()))
        return text


class WGrid(QtGui.QWidget):
    def __init__(self, grille, automatique):
        QtGui.QWidget.__init__(self)
        self._grille = grille
        self._grille = grille
        self._is_ok = False

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        widget_grid = QtGui.QWidget()
        widget_grid.setStyleSheet("background-color: white; "
                                  "border: 1px solid #D8D8D8;")
        layout.addWidget(widget_grid)
        gridlayout = QtGui.QGridLayout()
        for row, l in enumerate(self._grille):
            for col, c in enumerate(l):
                gridlayout.addWidget(QtGui.QLabel(str(c)), row, col)
        widget_grid.setLayout(gridlayout)

        layout2 = QtGui.QHBoxLayout()
        layout.addLayout(layout2)

        layout2.addWidget(QtGui.QLabel(le2mtrans(u"Number of 1: ")))

        self._spin_grille =QtGui.QSpinBox()
        self._spin_grille.setMinimum(0)
        self._spin_grille.setMaximum(100)
        self._spin_grille.setSingleStep(1)
        self._spin_grille.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        self._spin_grille.setFixedWidth(40)
        layout2.addWidget(self._spin_grille)

        self._pushButton_ok = QtGui.QPushButton(u"Ok")
        self._pushButton_ok.setFixedWidth(40)
        self._pushButton_ok.clicked.connect(self._check)
        layout2.addWidget(self._pushButton_ok)

        self._label_result = QtGui.QLabel((u"?"))
        layout2.addWidget(self._label_result)

        if automatique:
            if random.randint(0, 1):
                self._spin_grille.setValue(np.sum(self._grille))
            else:
                grid_max_of_ones = np.product(np.shape(self._grille))
                self._spin_grille.setValue(random.randint(0, grid_max_of_ones))
            self._pushButton_ok.click()

    def _check(self):
        answer = self._spin_grille.value()
        if answer == np.sum(self._grille):
            self._is_ok = True
            self._label_result.setText("V")
            self._label_result.setStyleSheet("color: green; font-weight: bold;")
            self._spin_grille.setEnabled(False)
            self._pushButton_ok.setEnabled(False)
        else:
            self._is_ok = False
            self._label_result.setText("X")
            self._label_result.setStyleSheet("color: red; font-weight: bold;")

    def is_ok(self):
        return self._is_ok
