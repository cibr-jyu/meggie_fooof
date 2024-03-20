from meggie_fooof.utilities.testing import BaseFooofTestAction
from meggie_fooof.actions.fooof_plot import PlotFooof
from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class TestFooofPlotChannelAverages(BaseFooofTestAction):
    def test_fooof_plot_channel_averages(self):

        data = {"outputs": {"fooof_report": ["Report"]}}

        self.run_action(
            action_name="fooof_plot",
            handler=PlotFooof,
            data=data,
            patch_paths=["meggie_fooof.actions.fooof_plot"],
        )
        dialog = self.find_dialog(OutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(True)
        dialog.accept()
