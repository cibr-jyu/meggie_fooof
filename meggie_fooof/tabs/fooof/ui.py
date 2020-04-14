"""
"""
import logging


from meggie.utilities.names import next_available_name

from meggie_fooof.tabs.fooof.dialogs.createReportDialogMain import CreateReportDialog


def create_report(experiment, data, window):
    """
    """
    selected_names = data['inputs']['spectrum']

    if not selected_names:
        return

    # take first
    selected = selected_names[0]

    default_name = next_available_name(
        experiment.active_subject.spectrum.keys(), selected)

    dialog = CreateReportDialog(experiment, window, selected, default_name)
    dialog.show()


def save(experiment, data, window):
    """
    """
    logging.getLogger('ui_logger').info('Save clicked!')


def plot(experiment, data, window):
    """
    """
    logging.getLogger('ui_logger').info('Plot clicked!')

