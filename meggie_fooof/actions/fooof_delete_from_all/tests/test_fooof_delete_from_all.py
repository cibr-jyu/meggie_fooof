from meggie_fooof.utilities.testing import BaseFooofTestAction
from meggie_fooof.actions.fooof_delete_from_all import DeleteFooofFromAll


class TestFooofDeleteFromAll(BaseFooofTestAction):
    def test_fooof_delete_from_all(self):

        data = {"outputs": {"fooof_report": ["Report"]}}

        self.run_action(
            action_name="fooof_delete_from_all",
            handler=DeleteFooofFromAll,
            data=data,
            patch_paths=["meggie_fooof.actions.fooof_delete_from_all"],
        )
