from meggie_fooof.utilities.testing import BaseFooofTestAction
from meggie_fooof.actions.fooof_save import SaveFooof
from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class TestFooofSaveAllChannels(BaseFooofTestAction):
    def test_fooof_save_all_channels(self):

        data = {"outputs": {"fooof_report": ["Report"]}}

        self.run_action(
            action_name="fooof_save",
            handler=SaveFooof,
            data=data,
            patch_paths=["meggie_fooof.actions.fooof_save"],
        )
        dialog = self.find_dialog(OutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(False)
        dialog.accept()
