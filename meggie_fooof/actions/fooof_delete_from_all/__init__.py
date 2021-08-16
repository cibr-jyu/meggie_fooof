""" Contains implementation for delete fooof from all
"""
import logging

import numpy as np

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class DeleteFooofFromAll(Action):
    """ Delete a FOOOF item from all subjects.
    """

    def run(self):

        try:
            selected_name = self.data['outputs']['fooof_report'][0]
        except IndexError as exc:
            return

        for subject in self.experiment.subjects.values():
            if selected_name in subject.fooof_report:
                try:
                    self.handler(subject, {'name': selected_name})
                except Exception as exc:
                    logging.getLogger('ui_logger').exception('')
                    logging.getLogger('ui_logger').warning(
                        'Could not remove FOOOF report for ' +
                        subject.name)

        try:
            self.experiment.save_experiment_settings()
        except Exception as exc:
            exc_messagebox(self.window, exc)

        self.window.initialize_ui()

    @subject_action
    def handler(self, subject, params):
        subject.remove(params['name'], 'fooof_report')


