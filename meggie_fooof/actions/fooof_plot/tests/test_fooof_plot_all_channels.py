from meggie_fooof.utilities.testing import BaseFooofTestAction
from meggie_fooof.actions.fooof_plot import PlotFooof
from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class TestFooofPlotAllChannels(BaseFooofTestAction):
    def test_fooof_plot_all_channels(self):

        data = {"outputs": {"fooof_report": ["Report"]}}

        self.run_action(
            action_name="fooof_plot",
            handler=PlotFooof,
            data=data,
            patch_paths=["meggie_fooof.actions.fooof_plot"],
        )
        dialog = self.find_dialog(OutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(False)
        dialog.accept()
