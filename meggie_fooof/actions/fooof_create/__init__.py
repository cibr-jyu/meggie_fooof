""" Contains create fooof action handling.
"""
import os 

from meggie.utilities.names import next_available_name

from meggie.utilities.messaging import exc_messagebox

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie_fooof.actions.fooof_create.dialogs.createReportDialogMain import CreateReportDialog
from meggie_fooof.actions.fooof_create.controller.fooof import create_report


class CreateFooof(Action):
    """ Creates FOOOF from existing spectrum.
    """

    def run(self):

        subject = self.experiment.active_subject

        try:
            selected_name = self.data['inputs']['spectrum'][0]
        except Exception as exc:
            return

        default_name = next_available_name(subject.fooof_report.keys(), selected_name)

        def handle_subject(subject, params):
            params['spectrum_name'] = selected_name
            self.handler(subject, params)

        dialog = CreateReportDialog(self.experiment, self.window, selected_name,
                                    default_name, handler=handle_subject)
        dialog.show()


    @subject_action
    def handler(self, subject, params):
        """
        """
        create_report(subject, params, do_meanwhile=self.window.update_ui)

