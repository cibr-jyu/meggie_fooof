# coding: utf-8

"""
"""

import logging

import numpy as np

from fooof import FOOOFGroup

from PyQt5 import QtWidgets

from meggie_fooof.tabs.fooof.dialogs.createReportDialogUi import Ui_CreateReportDialog
from meggie_fooof.datatypes.fooof_report.fooof_report import FOOOFReport

from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget

from meggie.utilities.decorators import threaded
from meggie.utilities.validators import validate_name
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox


class CreateReportDialog(QtWidgets.QDialog):
    """
    """

    def __init__(self, experiment, parent, selected_spectrum, default_name):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_CreateReportDialog()
        self.ui.setupUi(self)

        self.parent = parent
        self.experiment = experiment

        self.selected_spectrum = selected_spectrum

        spectrum_item = experiment.active_subject.spectrum[selected_spectrum]
        minfreq = spectrum_item.freqs[0]
        maxfreq = spectrum_item.freqs[-1]

        self.ui.doubleSpinBoxFreqMin.setValue(minfreq)
        self.ui.doubleSpinBoxFreqMax.setValue(maxfreq)

        self.batching_widget = BatchingWidget(
            experiment_getter=self.experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

        self.ui.lineEditName.setText(default_name)

    def experiment_getter(self):
        return self.experiment

    def create_report(self, subject, selected_spectrum):

        report_name = validate_name(self.ui.lineEditName.text())

        spectrum = subject.spectrum.get(selected_spectrum)

        peak_width_low = self.ui.doubleSpinBoxPeakWidthLow.value()
        peak_width_high = self.ui.doubleSpinBoxPeakWidthHigh.value()
        peak_threshold = self.ui.doubleSpinBoxPeakThreshold.value()
        max_n_peaks = self.ui.spinBoxMaxNPeaks.value()
        aperiodic_mode = self.ui.comboBoxAperiodicMode.currentText()
        minfreq = self.ui.doubleSpinBoxFreqMin.value()
        maxfreq = self.ui.doubleSpinBoxFreqMax.value()

        peak_width_limits = [peak_width_low, peak_width_high]
        peak_threshold = peak_threshold
        max_n_peaks = max_n_peaks
        aperiodic_mode = aperiodic_mode
        freq_range = [minfreq, maxfreq]

        report_content = {}

        for key, data in spectrum.content.items():

            fg = FOOOFGroup(peak_width_limits=peak_width_limits,
			    peak_threshold=peak_threshold,
			    max_n_peaks=max_n_peaks,
                            aperiodic_mode=aperiodic_mode,
			    verbose=False)

            @threaded
            def fit(**kwargs):
                fg.fit(spectrum.freqs, data, freq_range)

            fit(do_meanwhile=self.parent.update_ui)


            report_content[key] = fg

        params = {
            'conditions': list(spectrum.content.keys()),
            'based_on': selected_spectrum,
            'ch_names': spectrum.ch_names,
        }

        fooof_directory = subject.fooof_report_directory
        report = FOOOFReport(report_name, 
                             fooof_directory,
                             params,
                             report_content)

        report.save_content()
        subject.add(report, 'fooof_report')

    def accept(self):
        subject = self.experiment.active_subject
        selected_spectrum = self.selected_spectrum

        try:
            self.create_report(subject, selected_spectrum)
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        self.experiment.save_experiment_settings()
        self.parent.initialize_ui()

        logging.getLogger('ui_logger').info('Finished.')

        self.close()


    def acceptBatch(self):
        selected_spectrum = self.selected_spectrum
        experiment = self.experiment

        selected_subject_names = self.batching_widget.selected_subjects

        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    self.create_report(subject, selected_spectrum)
                    subject.release_memory()
                except Exception as exc:
                    self.batching_widget.failed_subjects.append(
                        (subject, str(exc)))
                    logging.getLogger('ui_logger').exception(str(exc))

        self.batching_widget.cleanup()
        self.experiment.save_experiment_settings()
        self.parent.initialize_ui()

        logging.getLogger('ui_logger').info('Finished.')

        self.close()
