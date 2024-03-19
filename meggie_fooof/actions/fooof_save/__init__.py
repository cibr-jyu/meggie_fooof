""" Contains implementation for fooof save
"""

from meggie.utilities.messaging import exc_messagebox

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie_fooof.actions.fooof_save.controller.fooof import save_all_channels
from meggie_fooof.actions.fooof_save.controller.fooof import save_channel_averages

from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class SaveFooof(Action):
    """Saves FOOOF to a csv."""

    def run(self):

        try:
            selected_name = self.data["outputs"]["fooof_report"][0]
        except IndexError:
            return

        config = self.window.prefs.read_config()
        try:

            def to_tuple(val):
                return [float(x) for x in val.strip("[").strip("]").split("-")]

            band_entry = config.get("meggie_fooof", "bands")
            bands = [to_tuple(val) for val in band_entry.split(",")]
        except Exception:
            bands = None

        def option_handler(selected_option):
            params = {
                "name": selected_name,
                "output_option": selected_option,
                "channel_groups": self.experiment.channel_groups,
                "bands": bands,
            }
            try:
                self.handler(self.experiment.active_subject, params)
            except Exception as exc:
                exc_messagebox(self.window, exc)

        dialog = OutputOptions(self.window, handler=option_handler)
        dialog.show()

    @subject_action
    def handler(self, subject, params):
        if params["output_option"] == "channel_averages":
            save_channel_averages(
                self.experiment,
                params["name"],
                params["channel_groups"],
                params["bands"],
                do_meanwhile=self.window.update_ui,
            )
        else:
            save_all_channels(
                self.experiment, params["name"], do_meanwhile=self.window.update_ui
            )
