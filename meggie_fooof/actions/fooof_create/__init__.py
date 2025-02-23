"""Contains create fooof action handling."""

from meggie.utilities.names import next_available_name

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie_fooof.actions.fooof_create.dialogs.createReportDialogMain import (
    CreateReportDialog,
)
from meggie_fooof.actions.fooof_create.controller.fooof import create_report


class CreateFooof(Action):
    """Creates FOOOF from existing spectrum."""

    def run(self, params={}):

        subject = self.experiment.active_subject

        try:
            selected_name = self.data["inputs"]["spectrum"][0]
        except Exception:
            return

        default_name = next_available_name(subject.fooof_report.keys(), selected_name)

        dialog = CreateReportDialog(
            self.experiment,
            self.window,
            selected_name,
            default_name,
            handler=self.handler,
        )
        dialog.show()

    @subject_action
    def handler(self, subject, params):
        """ """
        create_report(subject, params, do_meanwhile=self.window.update_ui)
        self.experiment.save_experiment_settings()
