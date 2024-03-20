from meggie_fooof.utilities.testing import BaseFooofTestAction
from meggie_fooof.actions.fooof_info import Info


class TestFooofInfo(BaseFooofTestAction):
    def test_fooof_info(self):

        data = {"outputs": {"fooof_report": ["Report"]}}

        content = self.run_action(
            action_name="fooof_info",
            handler=Info,
            data=data,
            patch_paths=["meggie_fooof.actions.fooof_info"],
        )
        assert content
