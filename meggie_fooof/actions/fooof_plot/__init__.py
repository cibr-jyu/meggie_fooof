""" Contains implementation for fooof plot
"""
import logging

import matplotlib.pyplot as plt
import numpy as np

from meggie.utilities.messaging import exc_messagebox

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie_fooof.actions.fooof_plot.controller.fooof import plot_topo_fit


class PlotFooof(Action):
    """ Plots a FOOOF topography
    """

    def run(self):

        try:
            selected_name = self.data['outputs']['fooof_report'][0]
        except IndexError as exc:
            return

        subject = self.experiment.active_subject
        try:
            self.handler(subject, {'name': selected_name})
        except Exception as exc:
            exc_messagebox(self.window, exc)


    @subject_action
    def handler(self, subject, params):
        report_item = subject.fooof_report[params['name']]
        plot_topo_fit(subject, report_item)
        