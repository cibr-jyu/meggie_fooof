""" Contains implementation for fooof plot
"""

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.channels import get_channels_by_type

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie_fooof.actions.fooof_plot.controller.fooof import plot_fit_topo
from meggie_fooof.actions.fooof_plot.controller.fooof import plot_fit_averages

from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class PlotFooof(Action):
    """Plots a FOOOF topography"""

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
            plot_fit_averages(
                subject, params["channel_groups"], params["name"], params["bands"]
            )
        else:
            info = subject.get_raw().info
            chs = list(get_channels_by_type(info).keys())
            if "eeg" in chs:
                plot_fit_topo(subject, params["name"], ch_type="eeg")
            if "grad" in chs or "mag" in chs:
                plot_fit_topo(subject, params["name"], ch_type="meg")
