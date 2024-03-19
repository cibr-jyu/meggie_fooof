from meggie_fooof.utilities.testing import BaseFooofTestAction
from meggie_fooof.actions.fooof_create import CreateFooof
from meggie_fooof.actions.fooof_create.dialogs.createReportDialogMain import (
    CreateReportDialog,
)


class TestFooofCreate(BaseFooofTestAction):
    def test_fooof_create(self):

        data = {"inputs": {"spectrum": ["Spectrum"]}}

        self.run_action(
            action_name="fooof_create",
            handler=CreateFooof,
            data=data,
            patch_paths=[
                "meggie_fooof.actions.fooof_create.dialogs.createReportDialogMain"
            ],
        )
        dialog = self.find_dialog(CreateReportDialog)
        dialog.accept()
