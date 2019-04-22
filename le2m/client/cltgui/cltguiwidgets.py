# coding: utf-8

""" ============================================================================

This module contains a lot of useful custom widgets

============================================================================ """

# built-in
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, QTimer
import random
from datetime import time, timedelta

# le2m
from util.utiltools import CompteARebours
try:  # this way it is possible to load this module independently
    from util.utili18n import le2mtrans
except AttributeError:
    le2mtrans = lambda x: x
from cltguisrc.cltguisrcwid import widCombo, \
    widRadio, widListDrag, widTableview, \
    widChat, widSlider, widLabel, widLineEdit
from configuration.configvar import YES_NO
import logging
import numpy as np


logger = logging.getLogger("le2m")


class WLabel(QWidget):
    def __init__(self, text=None, parent=None):
        super(WLabel, self).__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(text or u"")
        layout.addWidget(self.label, 0, Qt.AlignCenter)

    def set_text(self, text):
        self.label.setText(text)


class WPeriod(QWidget):
    def __init__(self, period=1, ecran_historique=None, parent=None):
        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.label_period = QLabel()
        self.set_period(period)
        layout.addWidget(self.label_period, 0, Qt.AlignLeft)

        layout.addStretch()

        self.pushButton_history = QPushButton(le2mtrans(u"History"))
        layout.addWidget(self.pushButton_history, 0, Qt.AlignRight)

        if ecran_historique:
            self.pushButton_history.clicked.connect(ecran_historique.show)

    def set_period(self, period):
        self.label_period.setText(
            le2mtrans(u"Period") + u" {}".format(period))


class WExplication(QWidget):
    def __init__(self, text=None, parent=None, size=(450, 80), html=True):
        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setFixedSize(*size)
        layout.addWidget(self.textEdit, 0, Qt.AlignCenter)

        if html:
            self.set_html(text or u"")
        else:
            self.set_text(text or u"")
        self.adjustSize()

    def set_size(self, size):
        self.textEdit.setFixedSize(*size)
        self.adjustSize()

    def set_text(self, text):
        self.textEdit.setText(text)

    def set_html(self, html):
        self.textEdit.setHtml(html)

    def get_text(self):
        return self.textEdit.toPlainText()


class WCombo(QWidget):
    def __init__(self, label, items, automatique=False, parent=None):
        super(WCombo, self).__init__(parent)
        self._items = items

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addSpacerItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.label = QLabel(label)
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(self._items)
        layout.addWidget(self.combo)

        layout.addSpacerItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        if automatique:
            if self._items[0] == le2mtrans(u"Choose") or \
                            self._items[0] == u"Choisir":
                self.combo.setCurrentIndex(
                    random.randint(1, len(self._items) - 1))
            else:
                self.combo.setCurrentIndex(
                    random.randint(0, len(self._items) - 1))

    def get_currentindex(self):
        if self._items[0] == le2mtrans(u"Choose") and \
                        self.combo.currentIndex() == 0:
            raise ValueError(u"No index selected")
        return self.combo.currentIndex()


class WSpinbox(QWidget):
    def __init__(self, label, minimum=0, maximum=100, interval=1,
                 automatique=False, parent=None, width=50):
        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addSpacerItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        formlayout = QFormLayout()
        layout.addLayout(formlayout)

        self.label = QLabel(label)
        self.spinBox = QSpinBox()
        self.spinBox.setButtonSymbols(QSpinBox.NoButtons)
        self.spinBox.setMinimum(minimum)
        self.spinBox.setMaximum(maximum)
        self.spinBox.setSingleStep(interval)
        self.spinBox.setValue(minimum)
        self.spinBox.setFixedWidth(width)

        formlayout.addRow(self.label, self.spinBox)

        layout.addSpacerItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        if automatique:
            self.spinBox.setValue(
                random.randrange(minimum, maximum + 1, interval))

        self.adjustSize()

    def get_value(self):
        return self.spinBox.value()


class WRadio(QWidget):
    def __init__(self, label,
                 texts=tuple([v for k, v in sorted(YES_NO.viewitems())]),
                 automatique=False, parent=None):
        super(WRadio, self).__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addSpacerItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.label = QLabel(label)
        layout.addWidget(self.label)

        self.radios = list()
        self.button_group = QButtonGroup()
        for num, txt in enumerate(texts):
            self.radios.append(QRadioButton(txt))
            self.button_group.addButton(self.radios[-1], num)
            layout.addWidget(self.radios[-1])

        layout.addSpacerItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        if automatique:
            selected = random.choice(self.radios)
            selected.setChecked(True)

    def get_checkedbutton(self):
        checked = self.button_group.checkedId()
        if checked == -1:
            raise ValueError(le2mtrans(u"No item selected"))
        return checked


class WListDrag(QWidget):
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
            Qt.CustomContextMenu)
        self.ui.listWidget_right.customContextMenuRequested.connect(
            self._rightclick)
        self.ui.listWidget_right.setToolTip(
            le2mtrans(u"Right click to move up, down or delete an item"))

        self._menu = QMenu(le2mtrans(u"Menu"), self)

        self._action_moveup = QAction(le2mtrans(u"Move up"), self._menu)
        self._action_moveup.triggered.connect(self._moveup)
        self._menu.addAction(self._action_moveup)

        self._action_movedown = QAction(le2mtrans(u"Move down"), self._menu)
        self._action_movedown.triggered.connect(self._movedown)
        self._menu.addAction(self._action_movedown)

        self._action_delete = QAction(le2mtrans(u"Delete"), self._menu)
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


class WTableview(QWidget):
    def __init__(self, parent, tablemodel, size=(600, 600)):
        super(WTableview, self).__init__(parent)

        self.ui = widTableview.Ui_Form()
        self.ui.setupUi(self)
        self.ui.tableView.setModel(tablemodel)
        self.ui.tableView.setFixedSize(size[0], size[1])
        self.ui.tableView.horizontalHeader().setResizeMode(
            QHeaderView.Stretch)
        self.adjustSize()


class WCompterebours(QWidget):
    """

    # """
    def __init__(self, parent, temps, actionfin):
        """
        :param parent:
        :param temps: datetime.time(0, 2, 0)  # hours, minutes, seconds
        :type temps: datetime.time or timedelta
        :param actionfin:
        :return:
        """
        super(WCompterebours, self).__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addStretch()

        self._label = QLabel(le2mtrans(u"Remaining time:"))
        layout.addWidget(self._label, 0, Qt.AlignCenter)

        self._label_timer = QLabel()
        if type(temps) is time:
            self.tps = timedelta(hours=temps.hour, minutes=temps.minute,
                            seconds=temps.second).total_seconds()
        elif type(temps) is timedelta:
            self.tps = temps.total_seconds()
        else:
            raise TypeError (
                u"temps has to be either a datetime.time or datetime.timedelta")
        layout.addWidget(self._label_timer, 0, Qt.AlignCenter)

        layout.addStretch()

        self.compterebours = CompteARebours(self.tps)
        self.compterebours.changetime[str].connect(self._label_timer.setText)
        self.compterebours.endoftime.connect(actionfin)
        self.compterebours.start()

        self.adjustSize()

    def stop(self):
        self.compterebours.stop()

    def is_running(self):
        return self.compterebours.is_running()

    def restart(self):
        self.compterebours.set_time(self.tps)
        self.compterebours.start()


class WChat(QWidget):
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


class WSlider(QWidget):
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
            self._timer = QTimer()
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(self._changevalue)
            self._timer.start(autotime)

    def _changevalue(self):
        self.ui.horizontalSlider.setValue(
            random.randrange(self._minimum, self._maximum, self._interval))

    def get_value(self):
        return self.ui.horizontalSlider.value()


class WLineEdit(QWidget):
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
            self._timer = QTimer()
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


class WGrid(QWidget):
    def __init__(self, grille, automatique):
        QWidget.__init__(self)
        self._grille = grille
        self._grille = grille
        self._is_ok = False

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget_grid = QWidget()
        widget_grid.setStyleSheet("background-color: white; "
                                  "border: 1px solid #D8D8D8;")
        layout.addWidget(widget_grid)
        gridlayout = QGridLayout()
        for row, l in enumerate(self._grille):
            for col, c in enumerate(l):
                gridlayout.addWidget(QLabel(str(c)), row, col)
        widget_grid.setLayout(gridlayout)

        layout2 = QHBoxLayout()
        layout.addLayout(layout2)

        layout2.addWidget(QLabel(le2mtrans(u"Number of 1: ")))

        self._spin_grille =QSpinBox()
        self._spin_grille.setMinimum(0)
        self._spin_grille.setMaximum(100)
        self._spin_grille.setSingleStep(1)
        self._spin_grille.setButtonSymbols(QSpinBox.NoButtons)
        self._spin_grille.setFixedWidth(40)
        layout2.addWidget(self._spin_grille)

        self._pushButton_ok = QPushButton(u"Ok")
        self._pushButton_ok.setFixedWidth(40)
        self._pushButton_ok.clicked.connect(self._check)
        layout2.addWidget(self._pushButton_ok)

        self._label_result = QLabel((u"?"))
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


class WDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, nb_decimals=2, min_val=0, max_val=100, width=50):
        QDoubleSpinBox.__init__(self)
        self.setDecimals(nb_decimals)
        self.setMinimum(min_val)
        self.setMaximum(max_val)
        self.setButtonSymbols(QSpinBox.NoButtons)
        self.setMaximumWidth(width)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_win = WCompterebours(None, timedelta(seconds=10), lambda : None)
    my_win.show()
    sys.exit(app.exec_())