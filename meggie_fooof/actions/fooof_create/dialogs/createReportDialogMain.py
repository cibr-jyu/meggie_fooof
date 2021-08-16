# coding: utf-8

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


class CreateReportDialog(QtWidgets.QDialog):
    """ Implements functionalities for widgets defined in the corresponding UI-file.
    """

    def __init__(self, experiment, parent, selected_spectrum, default_name, handler):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_CreateReportDialog()
        self.ui.setupUi(self)

        self.parent = parent
        self.experiment = experiment
        self.handler = handler
        self.selected_spectrum = selected_spectrum

        # initialize frequency limits from spectrum data
        spectrum_item = experiment.active_subject.spectrum[selected_spectrum]
        minfreq = spectrum_item.freqs[0]
        maxfreq = spectrum_item.freqs[-1]
        self.ui.doubleSpinBoxFreqMin.setValue(minfreq)
        self.ui.doubleSpinBoxFreqMax.setValue(maxfreq)

        # add a general batching widget to dialog
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
        """ Collect parameters from the dialog and creates an FOOOFReport item
        """

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

        # As meggie spectrum items can contain data for multiple conditions,
        # reports are also created for all those conditions, and dict is used.
        report_content = {}

        for key, data in spectrum.content.items():

            fg = FOOOFGroup(peak_width_limits=peak_width_limits,
			    peak_threshold=peak_threshold,
			    max_n_peaks=max_n_peaks,
                            aperiodic_mode=aperiodic_mode,
			    verbose=False)

            @threaded
            def fit(**kwargs):
                """ Run fitting in a separate thread so that UI stays responsive
                """
                fg.fit(spectrum.freqs, data, freq_range)

            fit(do_meanwhile=self.parent.update_ui)

            logging.getLogger('ui_logger').info('FOOOF results for ' +
                                                subject.name + ', ' +
                                                'condition: ' + key)
            # Log the textual report
            logging.getLogger('ui_logger').info(
                gen_results_fg_str(fg, concise=True))

            report_content[key] = fg

        params = {
            'conditions': list(spectrum.content.keys()),
            'based_on': selected_spectrum,
            'ch_names': spectrum.ch_names,
        }

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

    def accept(self):
        """ Start item creation for current subject
        """
        subject = self.experiment.active_subject
        selected_spectrum = self.selected_spectrum

        params = {}
        try:
            params['name'] = validate_name(self.ui.lineEditName.text())
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        params['peak_width_low'] = self.ui.doubleSpinBoxPeakWidthLow.value()
        params['peak_width_high'] = self.ui.doubleSpinBoxPeakWidthHigh.value()
        params['peak_threshold'] = self.ui.doubleSpinBoxPeakThreshold.value()
        params['max_n_peaks'] = self.ui.spinBoxMaxNPeaks.value()
        params['aperiodic_mode'] = self.ui.comboBoxAperiodicMode.currentText()
        params['minfreq'] = self.ui.doubleSpinBoxFreqMin.value()
        params['maxfreq'] = self.ui.doubleSpinBoxFreqMax.value()

        try:
            self.handler(subject, params)
            self.experiment.save_experiment_settings()
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        # Update experiment file and the window
        self.parent.initialize_ui()

        self.close()

    def acceptBatch(self):
        """ Start item creation of all subjects selected in the batching widget
        """
        selected_spectrum = self.selected_spectrum
        experiment = self.experiment

        params = {}
        try:
            params['name'] = validate_name(self.ui.lineEditName.text())
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        params['peak_width_low'] = self.ui.doubleSpinBoxPeakWidthLow.value()
        params['peak_width_high'] = self.ui.doubleSpinBoxPeakWidthHigh.value()
        params['peak_threshold'] = self.ui.doubleSpinBoxPeakThreshold.value()
        params['max_n_peaks'] = self.ui.spinBoxMaxNPeaks.value()
        params['aperiodic_mode'] = self.ui.comboBoxAperiodicMode.currentText()
        params['minfreq'] = self.ui.doubleSpinBoxFreqMin.value()
        params['maxfreq'] = self.ui.doubleSpinBoxFreqMax.value()

        selected_subject_names = self.batching_widget.selected_subjects

        # Loop through every subject creating items and collecting info from
        # failed cases
        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    self.handler(subject, params)
                    subject.release_memory()
                except Exception as exc:
                    self.batching_widget.failed_subjects.append(
                        (subject, str(exc)))
                    logging.getLogger('ui_logger').exception(str(exc))

        # if any fails, tell user about them
        self.batching_widget.cleanup()

        # and update experiment file and the UI
        try:
            self.experiment.save_experiment_settings()
        except Exception as exc:
            exc_messagebox(self.parent, exc)

        self.parent.initialize_ui()

        self.close()
