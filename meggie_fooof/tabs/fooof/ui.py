import logging

from meggie.utilities.names import next_available_name
from meggie.utilities.messaging import exc_messagebox

from meggie_fooof.tabs.fooof.controller.fooof import plot_topo_fit
from meggie_fooof.tabs.fooof.controller.fooof import save_all_channels

from meggie_fooof.tabs.fooof.dialogs.createReportDialogMain import CreateReportDialog


def create_report(experiment, data, window):
    """ Opens dialog that can be used to create FOOOF reports
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
    """ Plot topography from report, than can be used to inspect fits
    """
    subject = experiment.active_subject
    
    try:
        selected_name = data['outputs']['fooof_report'][0]
    except Exception as exc:
        return

    report_item = subject.fooof_report[selected_name]

    try:
        plot_topo_fit(experiment, report_item)
    except Exception as exc:
        logging.getLogger('ui_logger').exception(str(exc))
        exc_messagebox(window, exc)


def save(experiment, data, window):
    """ Save periodic and aperiodic params from all channels and 
    subjects to csv """

    try:
        selected_name = data['outputs']['fooof_report'][0]
    except IndexError as exc:
        return

    try:
        save_all_channels(experiment, selected_name)
    except Exception as exc:
        logging.getLogger('ui_logger').exception(str(exc))
        exc_messagebox(window, exc)


def delete(experiment, data, window):
    """ Delete selected fooof item for active subject
    """
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['fooof_report'][0]
    except IndexError as exc:
        return

    try:
        subject.remove(selected_name, 'fooof_report')
    except Exception as exc:
        logging.getLogger('ui_logger').exception(str(exc))
        exc_messagebox(window, exc)

    experiment.save_experiment_settings()

    logging.getLogger('ui_logger').info('Deleted selected FOOOF item')

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
                logging.getLogger('ui_logger').exception(str(exc))
                logging.getLogger('ui_logger').warning(
                    'Could not remove FOOOF report for ' +
                    subject.name)

    experiment.save_experiment_settings()

    logging.getLogger('ui_logger').info('Deleted selected FOOOF item from all subjects.')

    window.initialize_ui()


def fooof_info(experiment, data, window):
    """ Fills info element on the FOOOF tab
    """
    try:
        selected_name = data['outputs']['fooof_report'][0]
        fooof_item = experiment.active_subject.fooof_report[selected_name]
        params = fooof_item.params

        message = ""

        if 'based_on' in params:
            message += "Based on: {0}\n".format(params['based_on'])

        return message
    except Exception as exc:
        return ""

