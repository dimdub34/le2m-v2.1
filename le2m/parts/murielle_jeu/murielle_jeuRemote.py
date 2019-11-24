# -*- coding: utf-8 -*-

# built-in
import logging
import random

from PyQt4.QtCore import QTimer, pyqtSignal, QObject
from twisted.internet import defer

import murielle_jeu_params as pms
import murielle_jeu_texts as texts_CO
from client.cltremote import IRemote
from murielle_jeu_gui import GuiDecision, GuiInitialExtraction, GuiSummary

logger = logging.getLogger("le2m")


class RemoteGA(IRemote, QObject):
    end_of_time = pyqtSignal()

    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)
        QObject.__init__(self)

    def _init_vars(self):
        self.current_instant = 0
        self.extractions = PlotData()
        self.payoff_instant = PlotData()
        self.payoff_part = PlotData()
        self.resource = PlotData()
        self.text_infos = u""
        self.decision_screen = None
        self.simulation_extraction = int(self.le2mclt.uid.split("_")[2]) % 2  # 0 = myope, 1 = optimum social

    def remote_configure(self, params, server_part):
        logger.info(u"{} configure".format(self.le2mclt))
        self.server_part = server_part
        for k, v in params.items():
            setattr(pms, k, v)
        self._init_vars()

    def remote_set_initial_extraction(self):
        if self.le2mclt.simulation:
            if self.simulation_extraction:
                extraction = pms.get_extraction_os(0)
            else:
                extraction = pms.get_extraction_my(0)
            logger.info(u"{} Send {}".format(self.le2mclt, extraction))
            return extraction
        else:
            defered = defer.Deferred()
            screen = GuiInitialExtraction(self, defered)
            screen.show()
            return defered

    @defer.inlineCallbacks
    def send_simulation(self):
        if self.simulation_extraction:
            extraction = pms.get_extraction_os(self.current_instant)
        else:
            extraction = pms.get_extraction_my(self.current_instant)
        logger.info(u"{} Send {}".format(self._le2mclt.uid, extraction))
        yield(self.server_part.callRemote("new_extraction", extraction))

    def remote_display_decision(self, the_n):
        self.current_instant = the_n
        # simulation ---------------------------------------------------------------------------------------------------
        if self._le2mclt.simulation:
            # continuous
            if pms.DYNAMIC_TYPE == pms.CONTINUOUS:
                self.continuous_simulation_defered = defer.Deferred()
                self.continuous_simulation_timer = QTimer()
                self.continuous_simulation_timer.setInterval(1000)
                self.continuous_simulation_timer.timeout.connect(self.send_simulation)
                self.continuous_simulation_timer.start()
                return self.continuous_simulation_defered

            # discrete
            elif pms.DYNAMIC_TYPE == pms.DISCRETE:
                if self.simulation_extraction:
                    extraction = pms.get_extraction_os(self.current_instant)
                else:
                    extraction = pms.get_extraction_my(self.current_instant)
                logger.info(u"{} Send {}".format(self.le2mclt, extraction))
                return extraction

        # manual or auto -----------------------------------------------------------------------------------------------
        else:
            defered = defer.Deferred()
            if self.decision_screen is None:
                self.decision_screen = GuiDecision(self, defered)
                self.decision_screen.showFullScreen()
            else:
                self.decision_screen.defered = defered
                self.decision_screen.update_data_and_graphs()
            return defered

    def remote_update_data(self, instant_infos):
        self.current_instant = instant_infos["CO_instant"]
        # extraction
        self.extractions.add_x(self.current_instant)
        self.extractions.add_y(instant_infos["CO_extraction"])
        # resource
        self.resource.add_x(self.current_instant)
        self.resource.add_y(instant_infos["CO_resource"])
        # instant payoff
        self.payoff_instant.add_x(self.current_instant)
        self.payoff_instant.add_y(instant_infos["CO_instant_payoff"])
        # part payoff
        self.payoff_part.add_x(self.current_instant)
        self.payoff_part.add_y(instant_infos["CO_part_payoff"])

        # update curves
        try:
            self.extractions.update_curve()
            self.resource.update_curve()
            self.payoff_part.update_curve()
        except AttributeError:  # if period==0
            pass

        # text information
        old = self.text_infos
        the_time_str = texts_CO.trans_CO(u"Instant") if \
            pms.DYNAMIC_TYPE == pms.CONTINUOUS else \
            texts_CO.trans_CO(u"Period")
        self.text_infos = the_time_str + u": {}".format(self.current_instant) + \
                          u"<br>" + texts_CO.trans_CO(u"Extraction") + \
                          u": {:.2f}".format(self.extractions.ydata[-1]) + \
                          u"<br>" + texts_CO.trans_CO(u"Available resource") + \
                          u": {:.2f}".format(self.resource.ydata[-1]) + \
                          u"<br>" + texts_CO.trans_CO(u"Instant payoff") + \
                          u": {:.2f}".format(self.payoff_instant.ydata[-1]) + \
                          u"<br>" + texts_CO.trans_CO(u"Part payoff") + \
                          u": {:.2f}".format(self.payoff_part.ydata[-1])
        self.text_infos += u"<br>{}<br>{}".format(20 * "-", old)

        # log
        logger.debug("{} update data - instant {} - extraction {:.2f} - resource: {:.2f} - payoff: {:.2f}".format(
            self.le2mclt, self.current_instant, self.extractions.ydata[-1], self.resource.ydata[-1], self.payoff_part.ydata[-1]))

    def remote_end_update_data(self):
        logger.debug("{}: call of remote_end_data".format(self.le2mclt))
        if self.le2mclt.simulation and pms.DYNAMIC_TYPE == pms.CONTINUOUS:
            self.continuous_simulation_timer.stop()
            self.continuous_simulation_defered.callback(None)
        self.end_of_time.emit()

    def remote_display_summary(self, period_content):
        logger.info(u"{} Summary".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            curves = {"extractions": self.extractions.get_curve(), "payoffs": self.payoff_part.get_curve(),
                      "resource": self.resource.get_curve()}
            logger.info("{} send curves ({})".format(self.le2mclt, curves.keys()))
            return curves
        else:
            defered = defer.Deferred()
            summary_screen = GuiSummary(self, defered, texts_CO.get_text_summary(self.payoff_part.ydata[-1]))
            summary_screen.showFullScreen()
            return defered


class PlotData():
    def __init__(self):
        self.xdata = []
        self.ydata = []
        self.curve = None

    def add_x(self, val):
        self.xdata.append(int(val))

    def add_y(self, val):
        self.ydata.append(float(val))

    def update_curve(self):
        self.curve.set_data(self.xdata, self.ydata)

    def get_curve(self):
        return zip(self.xdata, self.ydata)
