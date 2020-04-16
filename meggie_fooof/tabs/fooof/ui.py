"""
"""
import logging


from meggie.utilities.names import next_available_name
from meggie.utilities.messaging import messagebox

from meggie_fooof.tabs.fooof.controller.fooof import plot_topo_fit

from meggie_fooof.tabs.fooof.dialogs.createReportDialogMain import CreateReportDialog


def create_report(experiment, data, window):
    """
    """
    try:
        selected_name = data['inputs']['spectrum'][0]
    except Exception as exc:
        return

    default_name = next_available_name(
        experiment.active_subject.fooof_report.keys(), 
        selected_name)

    dialog = CreateReportDialog(experiment, window, selected_name, 
                                default_name)
    dialog.show()


def plot_topo(experiment, data, window):
    """ Plot topography from report
    """
    subject = experiment.active_subject
    
    try:
        selected_name = data['outputs']['fooof_report'][0]
    except Exception as exc:
        return

    report_item = subject.fooof_report[selected_name]

    plot_topo_fit(experiment, report_item)


def delete(experiment, data, window):
    """ Delete selected fooof item for active subject
    """
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['fooof_report'][0]
    except IndexError as exc:
        return

    subject.remove(selected_name, 'fooof_report')
    experiment.save_experiment_settings()
    window.initialize_ui()


def delete_from_all(experiment, data, window):
    """ Delete selected fooof item from all subjects
    """
    try:
        selected_name = data['outputs']['fooof_report'][0]
    except IndexError as exc:
        return
    
    for subject in experiment.subjects.values():
        if selected_name in subject.fooof_report:
            try:
                subject.remove(selected_name, "fooof_report")
            except Exception as exc:
                logging.getLogger('ui_logger').warning(
                    'Could not remove FOOOF report for ' +
                    subject.name)
    experiment.save_experiment_settings()
    window.initialize_ui()

