# coding: utf-8

import logging

import numpy as np

from meggie.utilities.filemanager import save_csv
from meggie.utilities.channels import get_channels_by_type
from meggie.utilities.formats import format_float
from meggie.utilities.threading import threaded

from fooof import FOOOFGroup


COLUMN_NAMES = [
    "CF",
    "Amp",
    "BW",
    "Aperiodic offset",
    "Aperiodic exponent",
    "R squared",
    "Mean Absolute Error",
]


@threaded
def save_all_channels(experiment, selected_name, path):
    """Saves peak params and aperiodic params to a csv file for every
    subject and channel and condition"""
    row_descs = []
    csv_data = []

    for subject in experiment.subjects.values():
        fooof_item = subject.fooof_report.get(selected_name)
        if not fooof_item:
            continue
        for key, report in fooof_item.content.items():
            for ch_idx, ch_name in enumerate(fooof_item.params["ch_names"]):
                ch_report = report.get_fooof(ch_idx)
                for peak in ch_report.peak_params_:
                    csv_data.append(
                        [
                            format_float(peak[0]),
                            format_float(peak[1]),
                            format_float(peak[2]),
                            "",
                            "",
                            "",
                            "",
                        ]
                    )
                    row_descs.append((subject.name, key, ch_name))
                aparams = ch_report.aperiodic_params_
                rsquared = ch_report.r_squared_
                mae = ch_report.error_
                csv_data.append(
                    [
                        "",
                        "",
                        "",
                        format_float(aparams[0]),
                        format_float(aparams[1]),
                        format_float(rsquared),
                        format_float(mae),
                    ]
                )

                row_descs.append((subject.name, key, ch_name))

    save_csv(path, csv_data, COLUMN_NAMES, row_descs)
    logging.getLogger("ui_logger").info("Saved the csv file to " + path)


@threaded
def save_channel_averages(experiment, selected_name, channel_groups, path):
    """ """
    row_descs = []
    csv_data = []

    # for each subject
    for subject in experiment.subjects.values():
        fooof_item = subject.fooof_report.get(selected_name)
        if not fooof_item:
            continue

        info = subject.get_raw().info
        channels_by_type = get_channels_by_type(info)

        # .. and each report
        for key, report in fooof_item.content.items():

            ch_names = fooof_item.params["ch_names"]

            # .. compute channel averages
            for ch_type in ["eeg", "mag", "grad"]:
                if ch_type not in channels_by_type:
                    continue

                if ch_type in ["grad", "mag"]:
                    ch_groups = channel_groups["meg"]
                else:
                    ch_groups = channel_groups["eeg"]

                for ch_group_key, ch_group in ch_groups.items():

                    ch_type_group = [
                        ch_name
                        for ch_name in ch_group
                        if ch_name in channels_by_type.get(ch_type)
                    ]

                    idxs = [
                        ch_idx
                        for ch_idx, ch_name in enumerate(ch_names)
                        if ch_name in ch_type_group
                    ]

                    sub_fg = report.get_group(idxs)

                    # average across the original spectra
                    data = np.mean(10**sub_fg.power_spectra, axis=0)[np.newaxis, :]

                    # and fit a new fooof
                    avg_fg = FOOOFGroup(
                        peak_width_limits=sub_fg.peak_width_limits,
                        peak_threshold=sub_fg.peak_threshold,
                        max_n_peaks=sub_fg.max_n_peaks,
                        aperiodic_mode=sub_fg.aperiodic_mode,
                        verbose=False,
                    )
                    avg_fg.fit(sub_fg.freqs, data, sub_fg.freq_range)
                    avg_fooof = avg_fg.get_fooof(0)

                    # .. and create entries for them
                    for peak in avg_fooof.peak_params_:
                        csv_data.append(
                            [
                                format_float(peak[0]),
                                format_float(peak[1]),
                                format_float(peak[2]),
                                "",
                                "",
                                "",
                                "",
                            ]
                        )
                        row_descs.append((subject.name, key, ch_type, ch_group_key))

                    aparams = avg_fooof.aperiodic_params_
                    rsquared = avg_fooof.r_squared_
                    mae = avg_fooof.error_
                    csv_data.append(
                        [
                            "",
                            "",
                            "",
                            format_float(aparams[0]),
                            format_float(aparams[1]),
                            format_float(rsquared),
                            format_float(mae),
                        ]
                    )

                    row_descs.append((subject.name, key, ch_type, ch_group_key))

    save_csv(path, csv_data, COLUMN_NAMES, row_descs)
    logging.getLogger("ui_logger").info("Saved the csv file to " + path)
