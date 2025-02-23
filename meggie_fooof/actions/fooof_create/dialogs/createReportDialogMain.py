# coding: utf-8

import logging

from PyQt5 import QtWidgets

from meggie_fooof.actions.fooof_create.dialogs.createReportDialogUi import (
    Ui_CreateReportDialog,
)

from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget

from meggie.utilities.validators import validate_name
from meggie.utilities.messaging import exc_messagebox


class CreateReportDialog(QtWidgets.QDialog):
    """Implements functionalities for widgets defined in the corresponding UI-file."""

    def __init__(self, experiment, parent, selected_spectrum, default_name, handler):
        """ """
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
            geometry=self.ui.batchingWidgetPlaceholder.geometry(),
        )
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

        self.ui.lineEditName.setText(default_name)

    def experiment_getter(self):
        return self.experiment

    def accept(self):
        """Start item creation for current subject"""
        subject = self.experiment.active_subject
        selected_spectrum = self.selected_spectrum

        params = {}
        try:
            params["name"] = validate_name(self.ui.lineEditName.text())
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        params["peak_width_low"] = self.ui.doubleSpinBoxPeakWidthLow.value()
        params["peak_width_high"] = self.ui.doubleSpinBoxPeakWidthHigh.value()
        params["peak_threshold"] = self.ui.doubleSpinBoxPeakThreshold.value()
        params["max_n_peaks"] = self.ui.spinBoxMaxNPeaks.value()
        params["aperiodic_mode"] = self.ui.comboBoxAperiodicMode.currentText()
        params["minfreq"] = self.ui.doubleSpinBoxFreqMin.value()
        params["maxfreq"] = self.ui.doubleSpinBoxFreqMax.value()
        params["spectrum_name"] = selected_spectrum

        try:
            self.handler(subject, params)
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        # Update experiment file and the window
        self.parent.initialize_ui()

        self.close()

    def acceptBatch(self):
        """Start item creation of all subjects selected in the batching widget"""
        selected_spectrum = self.selected_spectrum

        params = {}
        try:
            params["name"] = validate_name(self.ui.lineEditName.text())
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        params["peak_width_low"] = self.ui.doubleSpinBoxPeakWidthLow.value()
        params["peak_width_high"] = self.ui.doubleSpinBoxPeakWidthHigh.value()
        params["peak_threshold"] = self.ui.doubleSpinBoxPeakThreshold.value()
        params["max_n_peaks"] = self.ui.spinBoxMaxNPeaks.value()
        params["aperiodic_mode"] = self.ui.comboBoxAperiodicMode.currentText()
        params["minfreq"] = self.ui.doubleSpinBoxFreqMin.value()
        params["maxfreq"] = self.ui.doubleSpinBoxFreqMax.value()
        params["spectrum_name"] = selected_spectrum

        selected_subject_names = self.batching_widget.selected_subjects

        # Loop through every subject creating items and collecting info from
        # failed cases
        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    self.handler(subject, params)
                    subject.release_memory()
                except Exception as exc:
                    self.batching_widget.failed_subjects.append((subject, str(exc)))
                    logging.getLogger("ui_logger").exception(str(exc))

        # if any fails, tell user about them
        self.batching_widget.cleanup()

        self.parent.initialize_ui()

        self.close()
