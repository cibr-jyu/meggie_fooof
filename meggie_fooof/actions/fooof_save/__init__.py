"""Contains implementation for fooof save"""

import os

from PyQt5 import QtWidgets

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.filemanager import homepath

from meggie.mainwindow.dynamic import Action

from meggie_fooof.actions.fooof_save.controller.fooof import save_all_channels
from meggie_fooof.actions.fooof_save.controller.fooof import save_channel_averages

from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class SaveFooof(Action):
    """Saves FOOOF to a csv."""

    def run(self, params={}):

        try:
            selected_name = self.data["outputs"]["fooof_report"][0]
        except IndexError:
            return

        def option_handler(selected_option):
            default_filename = (
                selected_name + "_all_subjects_channel_averages_fooof.csv"
                if selected_option == "channel_averages"
                else selected_name + "_all_subjects_all_channels_fooof.csv"
            )
            filepath, _ = QtWidgets.QFileDialog.getSaveFileName(
                self.window,
                "Save FOOOF to CSV",
                os.path.join(homepath(), default_filename),
                "CSV Files (*.csv);;All Files (*)",
            )
            if not filepath:
                return

            params = {
                "name": selected_name,
                "output_option": selected_option,
                "channel_groups": self.experiment.channel_groups,
                "filepath": filepath,
            }

            try:
                self.handler(self.experiment.active_subject, params)
            except Exception as exc:
                exc_messagebox(self.window, exc)

        dialog = OutputOptions(self.window, handler=option_handler)
        dialog.show()

    def handler(self, subject, params):
        if params["output_option"] == "channel_averages":
            save_channel_averages(
                self.experiment,
                params["name"],
                params["channel_groups"],
                params["filepath"],
                do_meanwhile=self.window.update_ui,
            )
        else:
            save_all_channels(
                self.experiment,
                params["name"],
                params["filepath"],
                do_meanwhile=self.window.update_ui,
            )
