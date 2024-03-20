from meggie_fooof.utilities.testing import BaseFooofTestAction
from meggie_fooof.actions.fooof_delete import DeleteFooof


class TestFooofDelete(BaseFooofTestAction):
    def test_fooof_delete(self):

        data = {"outputs": {"fooof_report": ["Report"]}}

        self.run_action(
            action_name="fooof_delete",
            handler=DeleteFooof,
            data=data,
            patch_paths=["meggie_fooof.actions.fooof_delete"],
        )
