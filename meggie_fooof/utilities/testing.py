from fooof import FOOOFGroup

from meggie_fooof.datatypes.fooof_report.fooof_report import FOOOFReport

from meggie.utilities.testing import BaseTestAction
from meggie.utilities.testing import create_test_experiment


def create_fooof_experiment(experiment_folder, experiment_name, n_subjects=2):
    """Generate experiment with data for testing."""

    experiment = create_test_experiment(
        experiment_folder, experiment_name, n_subjects=n_subjects
    )

    # create trivial content
    for subject in experiment.subjects.values():

        # use some basic params
        report_name = "Report"
        spectrum_name = "Spectrum"
        peak_width_low = 0.5
        peak_width_high = 12.0
        peak_threshold = 2.0
        max_n_peaks = 6
        aperiodic_mode = "fixed"
        minfreq = 1.17
        maxfreq = 39.88
        spectrum = subject.spectrum.get(spectrum_name)
        peak_width_limits = [peak_width_low, peak_width_high]
        peak_threshold = peak_threshold
        max_n_peaks = max_n_peaks
        aperiodic_mode = aperiodic_mode
        freq_range = [minfreq, maxfreq]
        report_content = {}
        for key, data in spectrum.content.items():
            fg = FOOOFGroup(
                peak_width_limits=peak_width_limits,
                peak_threshold=peak_threshold,
                max_n_peaks=max_n_peaks,
                aperiodic_mode=aperiodic_mode,
                verbose=False,
            )
            fg.fit(spectrum.freqs, data, freq_range)
            report_content[key] = fg

        params = {}
        params["spectrum_name"] = spectrum_name
        params["conditions"] = list(spectrum.content.keys())
        params["ch_names"] = spectrum.ch_names
        fooof_directory = subject.fooof_report_directory
        report = FOOOFReport(report_name, fooof_directory, params, report_content)
        subject.add(report, "fooof_report")

    return experiment


class BaseFooofTestAction(BaseTestAction):

    def setup_experiment(self):
        self.experiment = create_fooof_experiment(self.dirpath, "test_experiment")
        self.experiment.activate_subject("sample_01-raw")
