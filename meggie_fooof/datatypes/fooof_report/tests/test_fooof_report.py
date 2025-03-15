import tempfile
import os

import mne

from fooof import FOOOFGroup

from meggie.datatypes.spectrum.spectrum import Spectrum
from meggie.utilities.filemanager import ensure_folders

from meggie_fooof.datatypes.fooof_report.fooof_report import FOOOFReport


def test_fooof_report():
    with tempfile.TemporaryDirectory() as dirpath:

        # Create dummy spectrum data
        sample_folder = mne.datasets.sample.data_path()
        sample_fname = os.path.join(
            sample_folder, "MEG", "sample", "sample_audvis_raw.fif"
        )
        raw = mne.io.read_raw_fif(sample_fname, preload=True)
        mne_spectrum = raw.compute_psd(fmin=1, fmax=40, tmin=1, tmax=10)
        psds = mne_spectrum.get_data()
        freqs = mne_spectrum.freqs

        # Create a dummy Spectrum object
        spectrum_name = "TestSpectrum"
        cond_name = "1"
        spectrum_dir = os.path.join(dirpath, "spectrums")
        content = {cond_name: psds}
        params = {"conditions": [cond_name]}
        spectrum = Spectrum(
            spectrum_name,
            spectrum_dir,
            params,
            content=content,
            freqs=freqs,
            info=raw.info,
        )
        ensure_folders([spectrum_dir])
        spectrum.save_content()

        # Mimic parameters from the action
        peak_width_low = 2
        peak_width_high = 20
        peak_threshold = 0.01
        max_n_peaks = 10
        aperiodic_mode = "fixed"  # Explicitly set aperiodic_mode
        minfreq = 1
        maxfreq = 40

        # Generate FOOOF content based on Spectrum object
        report_content = {}
        for key, data in spectrum.content.items():
            fg = FOOOFGroup(
                peak_width_limits=[peak_width_low, peak_width_high],
                peak_threshold=peak_threshold,
                max_n_peaks=max_n_peaks,
                aperiodic_mode=aperiodic_mode,
                verbose=False,
            )
            fg.fit(freqs, psds, [minfreq, maxfreq])
            report_content[key] = fg

        # Create the meggie FOOOF object
        report_name = "TestFOOOFReport"
        report_params = {
            "name": report_name,
            "spectrum_name": spectrum_name,
            "peak_width_low": peak_width_low,
            "peak_width_high": peak_width_high,
            "peak_threshold": peak_threshold,
            "max_n_peaks": max_n_peaks,
            "aperiodic_mode": aperiodic_mode,
            "minfreq": 1,
            "maxfreq": 40,
            "conditions": list(report_content.keys()),
            "ch_names": spectrum.ch_names,
        }
        fooof_dir = os.path.join(dirpath, "fooofs")
        report = FOOOFReport(report_name, fooof_dir, report_params, report_content)
        ensure_folders([fooof_dir])
        report.save_content()

        # Load the FOOOFReport
        loaded_report = FOOOFReport(report_name, fooof_dir, report_params)

        # Verify that the report content is not empty and contains the FOOOF object
        assert isinstance(loaded_report.content, dict)
        assert len(loaded_report.content) > 0
        assert isinstance(list(loaded_report.content.values())[0], FOOOFGroup)
