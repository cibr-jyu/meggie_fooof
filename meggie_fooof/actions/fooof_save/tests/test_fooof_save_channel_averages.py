from meggie_fooof.utilities.testing import BaseFooofTestAction
from meggie_fooof.actions.fooof_save import SaveFooof
from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class TestFooofSaveChannelAverages(BaseFooofTestAction):
    def test_fooof_save_channel_averages(self):

        data = {"outputs": {"fooof_report": ["Report"]}}

        self.run_action(
            action_name="fooof_save",
            handler=SaveFooof,
            data=data,
            patch_paths=["meggie_fooof.actions.fooof_save"],
        )
        dialog = self.find_dialog(OutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(True)
        dialog.accept()
