# coding: utf-8

from PyQt4 import QtGui, QtCore
import random
from datetime import timedelta
from util.utiltools import CompteARebours
try:
    from util.utili18n import le2mtrans
except AttributeError:
    le2mtrans = lambda x: x
from cltguisrc.cltguisrcwid import widExplication, widPeriod, widCombo, \
    widSpinbox, widRadio, widListDrag, widTableview, widCompterebours, \
    widChat, widSlider, widLabel, widLineEdit
from configuration.configvar import YES_NO
import logging


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
        super(WPeriod, self).__init__(parent)
        self.ui = widPeriod.Ui_Form()
        self.ui.setupUi(self)

        self.set_period(period)
        self.ui.pushButton_historique.setText(le2mtrans(u"History"))
        if ecran_historique:
            self.ui.pushButton_historique.clicked.connect(ecran_historique.show)

    def set_period(self, period):
        self.ui.label_period.setText(
            le2mtrans(u"Period") + u" {}".format(period))


class WExplication(QtGui.QWidget):
    def __init__(self, text=None, parent=None, size=(450, 80), html=True):
        super(WExplication, self).__init__(parent)
        self.ui = widExplication.Ui_Form()
        self.ui.setupUi(self)
        if html:
            self.set_html(text or u"")
        else:
            self.set_text(text or u"")
        self.set_size(size)
        self.adjustSize()

    def set_size(self, size):
        self.ui.textEdit.setFixedSize(size[0], size[1])
        self.adjustSize()

    def set_text(self, text):
        self.ui.textEdit.setText(text)

    def set_html(self, html):
        self.ui.textEdit.setHtml(html)

    def get_text(self):
        return self.ui.textEdit.toPlainText()


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
                 automatique=False, parent=None, autotime=500):
        super(WSpinbox, self).__init__(parent)
        self.ui = widSpinbox.Ui_Form()
        self.ui.setupUi(self)
        self._minimum = minimum
        self._maximum = maximum
        self._interval = interval

        self.ui.label.setText(label)
        self.ui.spinBox.setMinimum(self._minimum)
        self.ui.spinBox.setMaximum(self._maximum)
        self.ui.spinBox.setSingleStep(self._interval)
        self.ui.spinBox.setValue(self._minimum)

        if automatique:
            self._timer = QtCore.QTimer()
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(self._changevalue)
            self._timer.start(autotime)

    def _changevalue(self):
        self.ui.spinBox.setValue(
                    random.randrange(self._minimum, self._maximum + 1,
                                     self._interval))

    def get_value(self):
        return self.ui.spinBox.value()


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