# coding: utf-8

import matplotlib.pyplot as plt
import mne

from meggie.utilities.formats import format_float
from meggie.utilities.formats import format_floats
from meggie.utilities.plotting import color_cycle
from meggie.utilities.plotting import set_figure_title
from meggie.utilities.channels import filter_info
from meggie.utilities.channels import iterate_topography
from meggie.utilities.channels import get_channels_by_type

from fooof.objs.utils import average_fg

from fooof.bands import Bands


def plot_fooof_fit(fooof_ax, fooof, report_key):
    """ """
    fooof.plot(
        ax=fooof_ax,
        plot_peaks="dot",
        add_legend=False,
    )

    text = "Condition: {}\n".format(report_key)
    text += "R squared: {}\nPeaks: \n".format(format_float(fooof.r_squared_))

    for peak_params in fooof.peak_params_:
        text += "{0} ({1}, {2})\n".format(*format_floats(peak_params))

    fooof_ax.set_title(text)


def get_average_bands(bands):
    """ """
    if not bands:
        bands = [[0, 4], [4, 7], [7, 14], [14, 30], [30, 100]]
    bands = dict(
        [("band {0}".format(band_idx + 1), band) for band_idx, band in enumerate(bands)]
    )
    fooof_bands = Bands(bands)
    return fooof_bands


def get_channel_averages(
    reports, channels_by_type, channel_groups, fooof_bands, ch_names
):
    """Create channel averages using fooof's own averaging function"""

    averages = {}
    for key, fg in sorted(reports.items()):
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

                label = (ch_type, ch_group_key)

                idxs = [
                    ch_idx
                    for ch_idx, ch_name in enumerate(ch_names)
                    if ch_name in ch_type_group
                ]

                sub_fg = fg.get_group(idxs)
                avg_fg = average_fg(sub_fg, fooof_bands, avg_method="mean")

                if label not in averages:
                    averages[label] = []

                averages[label].append((key, avg_fg))
    return averages


def plot_fit_averages(subject, channel_groups, name, bands):
    """ """
    report_item = subject.fooof_report[name]
    reports = report_item.content
    ch_names = report_item.params["ch_names"]

    raw = subject.get_raw()
    info = raw.info

    channels_by_type = get_channels_by_type(info)

    fooof_bands = get_average_bands(bands)
    averages = get_channel_averages(
        reports, channels_by_type, channel_groups, fooof_bands, ch_names
    )

    # plot averages for each channel type separately
    ch_types = sorted(set([label[0] for label in averages.keys()]))
    for ch_type in ch_types:

        # ..and for each channel group
        ch_groups = sorted(
            [label[1] for label in averages.keys() if label[0] == ch_type]
        )
        for ch_group in ch_groups:

            # ..in a separate figure
            fig = plt.figure()

            for idx, (fooof_key, fooof) in enumerate(averages[(ch_type, ch_group)]):
                fooof_ax = fig.add_subplot(
                    1, len(averages[(ch_type, ch_group)]), idx + 1
                )
                plot_fooof_fit(fooof_ax, fooof, fooof_key)

            title = "{0} {1} {2}".format(report_item.name, ch_type, ch_group)
            fig.suptitle(title)
            set_figure_title(fig, title.replace(" ", "_"))

            fig.tight_layout()

    plt.show()


def plot_fit_topo(subject, name, ch_type):
    """Plot topography where by clicking subplots you can check the fit parameters
    of specific channels"""

    report_item = subject.fooof_report[name]
    reports = report_item.content
    ch_names = report_item.params["ch_names"]

    raw = subject.get_raw()
    info = raw.info

    if ch_type == "meg":
        picked_channels = [
            ch_name
            for ch_idx, ch_name in enumerate(info["ch_names"])
            if ch_idx in mne.pick_types(info, meg=True, eeg=False)
        ]
    else:
        picked_channels = [
            ch_name
            for ch_idx, ch_name in enumerate(info["ch_names"])
            if ch_idx in mne.pick_types(info, eeg=True, meg=False)
        ]
    info = filter_info(info, picked_channels)

    colors = color_cycle(len(reports))

    def on_pick(ax, info_idx, names_idx):
        """When a subplot representing a specific channel is clicked on the
        main topography plot, show a new figure containing FOOOF fit plot
        for every condition"""

        fig = ax.figure
        fig.delaxes(ax)

        for idx, (report_key, report) in enumerate(reports.items()):
            report_ax = fig.add_subplot(1, len(reports), idx + 1)
            fooof = report.get_fooof(names_idx)
            plot_fooof_fit(report_ax, fooof, report_key)

        fig.tight_layout()

    # Create a topography where one can inspect fits by clicking subplots
    fig = plt.figure()
    for ax, info_idx, names_idx in iterate_topography(fig, info, ch_names, on_pick):

        handles = []
        for color_idx, (key, report) in enumerate(reports.items()):
            curve = report.power_spectra[names_idx]
            handles.append(
                ax.plot(curve, color=colors[color_idx], linewidth=0.5, label=key)[0]
            )

    if not handles:
        return

    fig.legend(handles=handles)
    title = "{0}_{1}".format(report_item.name, ch_type)
    set_figure_title(fig, title)
    plt.show()
