# coding: utf-8

import logging
import os

from meggie.utilities.filemanager import create_timestamped_folder
from meggie.utilities.filemanager import save_csv
from meggie.utilities.channels import get_channels_by_type
from meggie.utilities.formats import format_float
from meggie.utilities.threading import threaded

from fooof.objs.utils import average_fg

from fooof.bands import Bands


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
def save_all_channels(experiment, selected_name):
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

    # Save the resulting csv into a output folder 'meggie way'
    folder = create_timestamped_folder(experiment)
    fname = selected_name + "_all_subjects_all_channels_fooof.csv"
    path = os.path.join(folder, fname)

    save_csv(path, csv_data, COLUMN_NAMES, row_descs)
    logging.getLogger("ui_logger").info("Saved the csv file to " + path)


@threaded
def save_channel_averages(experiment, selected_name, channel_groups, bands):
    """ """
    row_descs = []
    csv_data = []

    # set up bands
    if not bands:
        bands = [[0, 4], [4, 7], [7, 14], [14, 30], [30, 100]]
    bands = dict(
        [("band {0}".format(band_idx + 1), band) for band_idx, band in enumerate(bands)]
    )
    fooof_bands = Bands(bands)

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
                    avg_fg = average_fg(sub_fg, fooof_bands, avg_method="mean")

                    # .. and create entries for them
                    for peak in avg_fg.peak_params_:
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

                    aparams = avg_fg.aperiodic_params_
                    rsquared = avg_fg.r_squared_
                    mae = avg_fg.error_
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

    # Save the resulting csv into a output folder 'meggie way'
    folder = create_timestamped_folder(experiment)
    fname = selected_name + "_all_subjects_channel_averages_fooof.csv"
    path = os.path.join(folder, fname)

    save_csv(path, csv_data, COLUMN_NAMES, row_descs)
    logging.getLogger("ui_logger").info("Saved the csv file to " + path)
