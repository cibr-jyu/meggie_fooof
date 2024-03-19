import pkg_resources

import os
import json

from meggie.utilities.testing import BaseTestAction


class BaseFooofTestAction(BaseTestAction):

    def load_action_spec(self, action_name):
        action_path = pkg_resources.resource_filename("meggie_fooof", "actions")
        config_path = os.path.join(action_path, action_name, "configuration.json")
        with open(config_path, "r") as f:
            action_spec = json.load(f)
        return action_spec
