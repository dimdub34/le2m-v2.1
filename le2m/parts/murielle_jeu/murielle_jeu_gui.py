# -*- coding: utf-8 -*-

# built-in
from __future__ import division

import logging
import sys
from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
from PyQt4.QtCore import Qt, QTimer, QTime
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from twisted.internet import defer
from twisted.internet.defer import AlreadyCalledError

# controlOptimal
import murielle_jeu_params as pms
import murielle_jeu_texts as texts_CO
from client.cltgui.cltguiwidgets import (WExplication, WCompterebours)
from murielle_jeu_texts import trans_GA
# le2m
from util.utili18n import le2mtrans
from util.utiltools import timedelta_to_time

logger = logging.getLogger("le2m")


# ==============================================================================
# WIDGETS
# ==============================================================================


class MySlider(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.current_value = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.lcd_layout = QHBoxLayout()
        self.lcd = QLCDNumber(5)
        self.lcd.setMode(QLCDNumber.Dec)
        self.lcd.setSmallDecimalPoint(True)
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.setFixedSize(100, 50)
        self.lcd_layout.addWidget(self.lcd, 0, Qt.AlignCenter)
        self.grid_layout.addLayout(self.lcd_layout, 0, 1)

        self.label_min = QLabel(str(pms.DECISION_MIN))
        self.grid_layout.addWidget(self.label_min, 1, 0, Qt.AlignLeft)
        self.label_max = QLabel(str(pms.DECISION_MAX))
        self.grid_layout.addWidget(self.label_max, 1, 2, Qt.AlignRight)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(pms.DECISION_MIN)
        self.slider.setMaximum(pms.DECISION_MAX * int(1 / pms.DECISION_STEP))
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(QSlider.TicksAbove)
        self.slider.valueChanged.connect(self.display)
        self.grid_layout.addWidget(self.slider, 2, 0, 1, 3)

        self.layout.addStretch()

    def display(self, value):
        self.lcd.display(value / int(1 / pms.DECISION_STEP))

    def value(self):
        return self.slider.value() / int(1 / pms.DECISION_STEP)

    def setValue(self, the_value):
        self.slider.setValue(the_value * (1 / pms.DECISION_STEP))


class PlotExtraction(QWidget):
    """
    This widget plot the individual extractions
    """

    def __init__(self, extractions):
        QWidget.__init__(self)

        self.extractions = extractions

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.graph = self.fig.add_subplot(111,
                                          position=[0.15, 0.15, 0.75, 0.75])

        curve_marker = ""
        if pms.DYNAMIC_TYPE == pms.DISCRETE:
            self.graph.set_xlim(-1, pms.NOMBRE_PERIODES + 1)
            self.graph.set_xlabel(trans_GA(u"Periods"))
            self.graph.set_xticks(range(0, pms.NOMBRE_PERIODES + 1), 5)
            curve_marker = "."

        elif pms.DYNAMIC_TYPE == pms.CONTINUOUS:
            self.graph.set_xlim(
                -5, pms.CONTINUOUS_TIME_DURATION.total_seconds() + 5)
            self.graph.set_xticks(
                range(0, int(pms.CONTINUOUS_TIME_DURATION.total_seconds()) + 1,
                      30))
            self.graph.set_xlabel(trans_GA(u"Time (seconds)"))
            curve_marker = ""

        # curves
        if self.extractions.curve is None:
            self.extractions.curve, = self.graph.plot(self.extractions.xdata, self.extractions.ydata, "-k",
                                                      marker=curve_marker)
        self.graph.set_ylim(-0.1, pms.DECISION_MAX + 0.1)
        self.graph.set_yticks(np.arange(0, pms.DECISION_MAX + 0.1, 0.2))
        self.graph.set_ylabel("")
        self.graph.set_title(trans_GA(u"Extraction"))
        self.graph.grid()
        self.canvas.draw()


class PlotResource(QWidget):
    """
    Display the curves with the total extraction of the group and the curve of
    the stock of resource
    """

    def __init__(self, resource):
        QWidget.__init__(self)

        self.resource = resource

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.graph = self.fig.add_subplot(111,
                                          position=[0.15, 0.15, 0.75, 0.75])

        curve_marker = ""
        if pms.DYNAMIC_TYPE == pms.DISCRETE:
            self.graph.set_xlim(-1, pms.NOMBRE_PERIODES + 1)
            self.graph.set_xlabel(trans_GA(u"Periods"))
            self.graph.set_xticks(range(0, pms.NOMBRE_PERIODES + 1), 5)
            curve_marker = "."

        elif pms.DYNAMIC_TYPE == pms.CONTINUOUS:
            self.graph.set_xlim(
                -5, pms.CONTINUOUS_TIME_DURATION.total_seconds() + 5)
            self.graph.set_xticks(
                range(0, int(pms.CONTINUOUS_TIME_DURATION.total_seconds()) + 1,
                      30))
            self.graph.set_xlabel(trans_GA(u"Time (seconds)"))
            curve_marker = ""

        if self.resource.curve is None:
            self.resource.curve, = self.graph.plot(
                self.resource.xdata, self.resource.ydata,
                "-k", marker=curve_marker)

        self.graph.set_ylim(0, pms.RESOURCE_INITIAL_STOCK * 3)
        self.graph.set_yticks(range(0, pms.RESOURCE_INITIAL_STOCK * 3 + 1, 5))
        self.graph.set_ylabel("")
        self.graph.set_title(trans_GA(u"Available resource"))
        self.graph.grid()
        self.canvas.draw()


class PlotPayoff(QWidget):
    def __init__(self, payoffs):
        super(PlotPayoff, self).__init__()

        self.payoffs = payoffs

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.graph = self.fig.add_subplot(111, position=[0.15, 0.15, 0.75, 0.75])
        curve_marker = ""

        if pms.DYNAMIC_TYPE == pms.DISCRETE:
            self.graph.set_xlim(-1, pms.NOMBRE_PERIODES + 1)
            self.graph.set_xlabel(trans_GA(u"Periods"))
            self.graph.set_xticks(range(0, pms.NOMBRE_PERIODES + 1, 5))
            curve_marker = "."

        elif pms.DYNAMIC_TYPE == pms.CONTINUOUS:
            self.graph.set_xlim(-5, pms.CONTINUOUS_TIME_DURATION.total_seconds() + 5)
            self.graph.set_xticks(range(0, int(pms.CONTINUOUS_TIME_DURATION.total_seconds()) + 1, 30))
            self.graph.set_xlabel(trans_GA(u"Time (seconds)"))

        if self.payoffs.curve is None:
            self.payoffs.curve, = self.graph.plot(self.payoffs.xdata, self.payoffs.ydata, "-k", marker=curve_marker)

        self.graph.set_ylim(0, 250)
        self.graph.set_yticks(range(0, 251, 25))
        self.graph.set_ylabel("")
        self.graph.set_title(trans_GA(u"Part payoff"))
        self.graph.grid()
        self.canvas.draw()


class GuiInitialExtraction(QDialog):
    def __init__(self, remote, defered):
        QDialog.__init__(self, remote.le2mclt.screen)

        self.remote = remote
        self.defered = defered

        layout = QVBoxLayout()
        self.setLayout(layout)

        explanation_area = WExplication(parent=self, text=texts_CO.INITIAL_EXTRACTION)
        layout.addWidget(explanation_area)

        self.slider_area = MySlider()
        layout.addWidget(self.slider_area)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle("Decision")
        self.adjustSize()
        self.setFixedSize(self.size())

        if self.remote.le2mclt.automatique:
            if self.remote.simulation_extraction == 0:
                self.slider_area.setValue(pms.get_extraction_my(self.remote.current_instant))
            elif self.remote.simulation_extraction == 1:
                self.slider_area.setValue(pms.get_extraction_os(self.remote.current_instant))
            elif self.remote.simulation_extraction == 2:
                self.slider_area.setValue(pms.get_extraction_feed(self.remote.current_instant))
            else:
                self.slider_area.setValue(pms.get_extraction_aleatoire(self.remote.current_instant))
            self.timer_automatique = QTimer()
            self.timer_automatique.timeout.connect(buttons.button(QDialogButtonBox.Ok).click)
            self.timer_automatique.start(3000)

    def _accept(self):
        try:
            self.timer_automatique.stop()
        except AttributeError:
            pass
        val = self.slider_area.value()
        if not self.remote.le2mclt.automatique:
            confirmation = QMessageBox.question(self, "Confirmation", trans_GA(u"Do you confirm your choice?"),
                                                QMessageBox.No | QMessageBox.Yes)
            if confirmation != QMessageBox.Yes:
                return
        self.accept()
        logger.info("send {}".format(val))
        self.defered.callback(val)

    def reject(self):
        pass


class GuiDecision(QDialog):
    def __init__(self, remote, defered):
        super(GuiDecision, self).__init__(remote.le2mclt.screen)
        # main attributes
        self.remote = remote
        self.defered = defered

        layout = QVBoxLayout(self)

        # ----------------------------------------------------------------------
        # HEAD AREA
        # ----------------------------------------------------------------------
        layout_head = QHBoxLayout()
        layout.addLayout(layout_head, 0)

        if pms.DYNAMIC_TYPE == pms.DISCRETE:
            self.label_period = QLabel(le2mtrans(u"Period") + u" {}".format(self.remote.current_instant))
            layout_head.addWidget(self.label_period, 0, Qt.AlignLeft)

        self.compte_rebours = None
        if pms.DYNAMIC_TYPE == pms.CONTINUOUS:
            self.compte_rebours = WCompterebours(self, pms.CONTINUOUS_TIME_DURATION, lambda: None)
        elif pms.DYNAMIC_TYPE == pms.DISCRETE:
            self.compte_rebours = WCompterebours(self, pms.DISCRETE_DECISION_TIME, self.send_extrac)
        layout_head.addWidget(self.compte_rebours, 0, Qt.AlignLeft)
        layout_head.addStretch()

        # ----------------------------------------------------------------------
        # GRAPHICAL AREA
        # ----------------------------------------------------------------------

        self.plot_layout = QGridLayout()
        layout.addLayout(self.plot_layout)
        # extraction
        self.plot_extraction = PlotExtraction(self.remote.extractions)
        self.plot_layout.addWidget(self.plot_extraction, 0, 0)
        # part payoff
        self.plot_payoff = PlotPayoff(
            self.remote.payoff_part)
        self.plot_layout.addWidget(self.plot_payoff, 0, 1)
        # available resource
        self.plot_resource = PlotResource(self.remote.resource)
        self.plot_layout.addWidget(self.plot_resource, 1, 0)
        # value in text mode
        widget_infos = QWidget()
        widget_infos.setLayout(QVBoxLayout())
        self.textEdit_infos = QTextEdit()
        self.textEdit_infos.setReadOnly(True)
        self.textEdit_infos.setHtml(self.remote.text_infos)
        widget_infos.layout().addWidget(self.textEdit_infos)
        self.plot_layout.addWidget(widget_infos, 1, 1)
        self.plot_layout.setColumnStretch(0, 1)
        self.plot_layout.setColumnStretch(1, 1)

        # ----------------------------------------------------------------------
        # DECISION AREA
        # ----------------------------------------------------------------------

        self.extract_dec = MySlider()
        player_extrac = self.remote.extractions.ydata[-1]
        self.extract_dec.setValue(player_extrac)
        self.extract_dec.lcd.display(player_extrac)
        layout.addWidget(self.extract_dec)

        # ----------------------------------------------------------------------
        # FOOT AREA
        # ----------------------------------------------------------------------

        self.setWindowTitle(trans_GA(u"Decision"))

        if pms.DYNAMIC_TYPE == pms.CONTINUOUS:
            self.extract_dec.slider.sliderReleased.connect(self.send_extrac)
            if self.remote.le2mclt.automatique:
                self.extract_dec.slider.valueChanged.connect(self.send_extrac)
            self.timer_continuous = QTimer()
            self.timer_continuous.timeout.connect(self.update_data_and_graphs)
            self.timer_continuous.start(int(pms.TIMER_UPDATE.total_seconds()) * 1000)

        if pms.DYNAMIC_TYPE == pms.DISCRETE and self.remote.le2mclt.automatique:
            if self.remote.simulation_extraction == 0:
                self.extract_dec.setValue(pms.get_extraction_my(self.remote.current_instant))
            elif self.remote.simulation_extraction == 1:
                self.extract_dec.setValue(pms.get_extraction_os(self.remote.current_instant))
            elif self.remote.simulation_extraction == 2:
                self.extract_dec.setValue(pms.get_extraction_feed(self.remote.current_instant))
            else:
                self.extract_dec.setValue(pms.get_extraction_aleatoire(self.remote.current_instant))

        self.remote.end_of_time.connect(self.end_of_time)

    def reject(self):
        pass

    def send_extrac(self):
        dec = self.extract_dec.value()
        logger.info("{} send {}".format(self.remote.le2mclt, dec))
        if pms.DYNAMIC_TYPE == pms.CONTINUOUS:
            self.remote.server_part.callRemote("new_extraction", dec)
        elif pms.DYNAMIC_TYPE == pms.DISCRETE:
            self.defered.callback(dec)

    def update_data_and_graphs(self):
        if self.remote.le2mclt.automatique:
            if self.remote.simulation_extraction == 0:
                self.extract_dec.setValue(pms.get_extraction_my(self.remote.current_instant))
            elif self.remote.simulation_extraction == 1:
                self.extract_dec.setValue(pms.get_extraction_os(self.remote.current_instant))
            elif self.remote.simulation_extraction == 2:
                self.extract_dec.setValue(pms.get_extraction_feed(self.remote.current_instant))
            else:
                self.extract_dec.setValue(pms.get_extraction_aleatoire(self.remote.current_instant))
        self.plot_extraction.canvas.draw()
        self.plot_resource.canvas.draw()
        self.plot_payoff.canvas.draw()
        self.textEdit_infos.setHtml(self.remote.text_infos)
        if pms.DYNAMIC_TYPE == pms.DISCRETE:
            self.label_period.setText(u"Période {}".format(self.remote.current_instant))
            self.compte_rebours.restart()

    def end_of_time(self):
        try:
            self.timer_continuous.stop()
        except AttributeError:  # if dynamic == discrete
            pass
        # if pms.DYNAMIC_TYPE == pms.CONTINUOUS:
        try:
            self.defered.callback(None)
        except AlreadyCalledError as m:
            logger.warning(m.message)
        super(GuiDecision, self).accept()


class GuiSummary(QDialog):
    def __init__(self, remote, defered, the_text=""):
        super(GuiSummary, self).__init__(remote.le2mclt.screen)

        self.remote = remote
        self.defered = defered

        layout = QVBoxLayout(self)

        # ----------------------------------------------------------------------
        # GRAPHICAL AREA
        # ----------------------------------------------------------------------
        self.remote.extractions.curve = None
        self.remote.resource.curve = None
        self.remote.payoff_part.curve = None

        self.plot_layout = QGridLayout()
        layout.addLayout(self.plot_layout)

        # extractions (indiv + group)
        self.plot_extraction = PlotExtraction(self.remote.extractions)
        self.plot_layout.addWidget(self.plot_extraction, 0, 0)

        # payoff indiv
        self.plot_payoff = PlotPayoff(
            self.remote.payoff_part)
        self.plot_layout.addWidget(self.plot_payoff, 0, 1)

        # resource
        self.plot_resource = PlotResource(self.remote.resource)
        self.plot_layout.addWidget(self.plot_resource, 1, 0)

        # value in text mode
        widget_infos = QWidget()
        widget_infos.setLayout(QVBoxLayout())
        self.textEdit_infos = QTextEdit()
        self.textEdit_infos.setReadOnly(True)
        self.textEdit_infos.setText(the_text)
        widget_infos.layout().addWidget(self.textEdit_infos)
        self.plot_layout.addWidget(widget_infos, 1, 1)
        self.plot_layout.setColumnStretch(0, 1)
        self.plot_layout.setColumnStretch(1, 1)

        # ----------------------------------------------------------------------
        # FINALIZE THE DIALOG
        # ----------------------------------------------------------------------

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        # auto
        if self.remote.le2mclt.automatique:
            self.timer_automatique = QTimer()
            self.timer_automatique.timeout.connect(
                buttons.button(QDialogButtonBox.Ok).click)
            self.timer_automatique.start(7000)

        # title and size
        self.setWindowTitle(le2mtrans(u"Summary"))

    def _accept(self):
        try:
            self.timer_automatique.stop()
        except AttributeError:
            pass
        # ----------------------------------------------------------------------
        # we send back the different individual curves
        # ----------------------------------------------------------------------
        data_indiv = {
            "extractions": self.remote.extractions.get_curve(),
            "payoffs": self.remote.payoff_part.get_curve(),
            # "cost": self.remote.cost.get_curve(),
            "resource": self.remote.resource.get_curve()
        }
        logger.debug("{} send curves ({})".format(self.remote.le2mclt, data_indiv.keys()))
        self.defered.callback(data_indiv)
        self.accept()

    def reject(self):
        pass


# ==============================================================================
# CONFIGURATION SCREEN
# ==============================================================================


class DConfigure(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        form = QFormLayout()
        layout.addLayout(form)

        # ----------------------------------------------------------------------
        # dynamic
        # ----------------------------------------------------------------------
        self.combo_dynamic = QComboBox()
        self.combo_dynamic.addItems(["CONTINUOUS", "DISCRETE"])
        self.combo_dynamic.setCurrentIndex(pms.DYNAMIC_TYPE)
        form.addRow(QLabel("Dynamic"), self.combo_dynamic)

        # ----------------------------------------------------------------------
        # trial part
        # ----------------------------------------------------------------------
        self.checkbox_essai = QCheckBox()
        self.checkbox_essai.setChecked(pms.PARTIE_ESSAI)
        form.addRow(QLabel(u"Trial part"), self.checkbox_essai)

        # ----------------------------------------------------------------------
        # periods
        # ----------------------------------------------------------------------
        self.spin_periods = QSpinBox()
        self.spin_periods.setMinimum(0)
        self.spin_periods.setMaximum(100)
        self.spin_periods.setSingleStep(1)
        self.spin_periods.setValue(pms.NOMBRE_PERIODES)
        self.spin_periods.setButtonSymbols(QSpinBox.NoButtons)
        self.spin_periods.setMaximumWidth(50)
        form.addRow(QLabel(u"Number of periods"), self.spin_periods)

        # ----------------------------------------------------------------------
        # continuous time duration
        # ----------------------------------------------------------------------
        self.timeEdit_continuous_duration = QTimeEdit()
        self.timeEdit_continuous_duration.setDisplayFormat("hh:mm:ss")
        time_duration = timedelta_to_time(pms.CONTINUOUS_TIME_DURATION)
        self.timeEdit_continuous_duration.setTime(
            QTime(time_duration.hour, time_duration.minute,
                  time_duration.second))
        self.timeEdit_continuous_duration.setMaximumWidth(100)
        form.addRow(QLabel(u"Continuous time duration"),
                    self.timeEdit_continuous_duration)

        # ----------------------------------------------------------------------
        # discrete time decision
        # ----------------------------------------------------------------------
        self.timeEdit_discrete_duration = QTimeEdit()
        self.timeEdit_discrete_duration.setDisplayFormat("hh:mm:ss")
        time_duration = timedelta_to_time(pms.DISCRETE_DECISION_TIME)
        self.timeEdit_discrete_duration.setTime(
            QTime(time_duration.hour, time_duration.minute,
                  time_duration.second))
        self.timeEdit_discrete_duration.setMaximumWidth(100)
        form.addRow(QLabel(u"Discrete decision time"),
                    self.timeEdit_discrete_duration)

        # ----------------------------------------------------------------------
        # buttons
        # ----------------------------------------------------------------------
        button = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button.accepted.connect(self._accept)
        button.rejected.connect(self.reject)
        layout.addWidget(button)

        self.setWindowTitle(u"Configure")
        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        pms.PARTIE_ESSAI = self.checkbox_essai.isChecked()
        pms.DYNAMIC_TYPE = self.combo_dynamic.currentIndex()
        pms.param_tau = pms.tau = pms.tau_continu if pms.DYNAMIC_TYPE == pms.CONTINUOUS else pms.tau_discret
        pms.NOMBRE_PERIODES = self.spin_periods.value()
        time_continuous = self.timeEdit_continuous_duration.time().toPyTime()
        pms.CONTINUOUS_TIME_DURATION = timedelta(
            hours=time_continuous.hour, minutes=time_continuous.minute,
            seconds=time_continuous.second)
        time_discrete = self.timeEdit_discrete_duration.time().toPyTime()
        pms.DISCRETE_DECISION_TIME = timedelta(
            hours=time_discrete.hour, minutes=time_discrete.minute,
            seconds=time_discrete.second)
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    slider = MySlider()
    slider.setGeometry(300, 300, 300, 200)
    slider.show()
    sys.exit(app.exec_())
