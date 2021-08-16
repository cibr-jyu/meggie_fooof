""" Contains functions for handling FOOOFs
"""

import logging

from PyQt5 import QtWidgets

from fooof import FOOOFGroup
from fooof.core.strings import gen_results_fg_str

from meggie_fooof.actions.fooof_create.dialogs.createReportDialogUi import Ui_CreateReportDialog

from meggie_fooof.datatypes.fooof_report.fooof_report import FOOOFReport

from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget

from meggie.utilities.threading import threaded
from meggie.utilities.validators import validate_name
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox


@threaded
def create_report(subject, params):
    """ Collect parameters from the dialog and creates an FOOOFReport item
    """

    report_name = params['name']
    spectrum_name = params['spectrum_name']

    peak_width_low = params['peak_width_low']
    peak_width_high = params['peak_width_high']
    peak_threshold = params['peak_threshold']
    max_n_peaks = params['max_n_peaks']
    aperiodic_mode = params['aperiodic_mode']
    minfreq = params['minfreq']
    maxfreq = params['maxfreq']

    spectrum = subject.spectrum.get(spectrum_name)

    peak_width_limits = [peak_width_low, peak_width_high]
    peak_threshold = peak_threshold
    max_n_peaks = max_n_peaks
    aperiodic_mode = aperiodic_mode
    freq_range = [minfreq, maxfreq]

    # As meggie spectrum items can contain data for multiple conditions,
    # reports are also created for all those conditions, and dict is used.
    report_content = {}

    for key, data in spectrum.content.items():

        fg = FOOOFGroup(peak_width_limits=peak_width_limits,
            peak_threshold=peak_threshold,
            max_n_peaks=max_n_peaks,
                        aperiodic_mode=aperiodic_mode,
            verbose=False)

        fg.fit(spectrum.freqs, data, freq_range)

        logging.getLogger('ui_logger').info('FOOOF results for ' +
                                            subject.name + ', ' +
                                            'condition: ' + key)
        # Log the textual report
        logging.getLogger('ui_logger').info(
            gen_results_fg_str(fg, concise=True))

        report_content[key] = fg

    params['conditions'] = list(spectrum.content.keys())
    params['ch_names'] = spectrum.ch_names

    fooof_directory = subject.fooof_report_directory

    # Create a container item that meggie understands, 
    # and which holds the report data
    report = FOOOFReport(report_name, 
                         fooof_directory,
                         params,
                         report_content)

    # save report data to fs
    report.save_content()

    # and add the report item to subject
    subject.add(report, 'fooof_report')
