# coding: utf-8

import matplotlib.pyplot as plt
import mne
import numpy as np

from meggie.utilities.formats import format_float
from meggie.utilities.formats import format_floats
from meggie.utilities.plotting import color_cycle
from meggie.utilities.plotting import set_figure_title
from meggie.utilities.plotting import create_channel_average_plot
from meggie.utilities.channels import filter_info
from meggie.utilities.channels import iterate_topography
from meggie.utilities.channels import get_channels_by_type

from fooof import FOOOFGroup


def get_channel_averages(report_item, channels_by_type, channel_groups, ch_names):
    """Create channel averages using fooof's own averaging function"""

    reports = report_item.content

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

                if label not in averages:
                    averages[label] = []

                averages[label].append((key, avg_fooof))
    return averages


def plot_fit_averages(subject, channel_groups, name):
    """Plot channel averages of FOOOF items."""
    report_item = subject.fooof_report[name]
    ch_names = report_item.params["ch_names"]

    raw = subject.get_raw()
    info = raw.info

    channels_by_type = get_channels_by_type(info)
    averages = get_channel_averages(
        report_item, channels_by_type, channel_groups, ch_names
    )

    # Restructure averages to align with the condition-first loop strategy
    restructured_averages = {}
    for label, conditions in averages.items():
        ch_type, ch_group = label
        for fooof_key, fooof in conditions:
            restructured_averages.setdefault(fooof_key, {}).setdefault(ch_type, {})[
                ch_group
            ] = fooof

    # Plot averages with new loop order: conditions first, then channel groups
    fooof_keys = sorted(restructured_averages.keys())
    ch_types = sorted(set(label[0] for label in averages.keys()))

    for fooof_key in fooof_keys:
        for ch_type in ch_types:
            ch_groups = sorted(restructured_averages[fooof_key][ch_type].keys())

            def plot_fun(ax_idx, ax):
                fooof = restructured_averages[fooof_key][ch_type][ch_groups[ax_idx]]
                fooof.plot(
                    ax=ax,
                    plot_peaks="dot",
                    add_legend=False,
                )
                ax.set_title(ch_groups[ax_idx])

            title = f"{report_item.name} {ch_type} {fooof_key}"
            create_channel_average_plot(len(ch_groups), plot_fun, title)

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
            fooof.plot(
                ax=report_ax,
                plot_peaks="dot",
                add_legend=True,
            )

            text = "Condition: {}\n".format(report_key)
            text += "R squared: {}\nPeaks: \n".format(format_float(fooof.r_squared_))

            for peak_params in fooof.peak_params_:
                text += "{0} ({1}, {2})\n".format(*format_floats(peak_params))

            report_ax.set_title(text)

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
