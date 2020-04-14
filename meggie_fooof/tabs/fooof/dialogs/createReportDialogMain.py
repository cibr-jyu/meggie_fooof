# coding: utf-8

"""
"""

import logging

import numpy as np

from PyQt5 import QtWidgets

from meggie_fooof.tabs.fooof.dialogs.createReportDialogUi import Ui_CreateReportDialog

from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget

from meggie_fooof.datatypes.fooof_report.fooof_report import FOOOFReport

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

        # report = ... selected_spectrum ...
        from meggie.utilities.debug import debug_trace;
        debug_trace()

        report.save_content()
        subject.add(report, 'report')

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
