""" Contains implementation for fooof info
"""
import os

from meggie.mainwindow.dynamic import InfoAction


class Info(InfoAction):
    """ Fills up fooof info box """

    def run(self):

        message = ""
        try:
            selected_name = self.data['outputs']['fooof_report'][0]
            fooof_item = self.experiment.active_subject.fooof_report[selected_name]
            params = fooof_item.params

            message += "Name: {0}\n\n".format(fooof_item.name)

            if 'spectrum_name' in params:
                message += "Based on: {0}\n".format(params['spectrum_name'])

        except Exception as exc:
            message = ""
        return message

