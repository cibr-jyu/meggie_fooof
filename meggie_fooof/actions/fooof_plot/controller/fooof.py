# coding: utf-8

import matplotlib.pyplot as plt
import mne

from meggie.utilities.formats import format_float
from meggie.utilities.formats import format_floats
from meggie.utilities.plotting import color_cycle
from meggie.utilities.plotting import set_figure_title
from meggie.utilities.channels import average_to_channel_groups
from meggie.utilities.channels import filter_info
from meggie.utilities.channels import iterate_topography


def plot_fit_averages(subject, channel_groups, name):
    """
    """


def plot_fit_topo(subject, name, ch_type):
    """ Plot topography where by clicking subplots you can check the fit parameters
    of specific channels """

    report_item = subject.fooof_report[name]
    reports = report_item.content
    ch_names = report_item.params['ch_names']
    freqs = list(reports.values())[0].freqs

    raw = subject.get_raw()
    info = raw.info

    if ch_type == 'meg':
        picked_channels = [ch_name for ch_idx, ch_name in enumerate(info['ch_names'])
                           if ch_idx in mne.pick_types(info, meg=True, eeg=False)]
    else:
        picked_channels = [ch_name for ch_idx, ch_name in enumerate(info['ch_names'])
                           if ch_idx in mne.pick_types(info, eeg=True, meg=False)]
    info = filter_info(info, picked_channels)

    colors = color_cycle(len(reports))

    def on_pick(ax, info_idx, names_idx):
        """ When a subplot representing a specific channel is clicked on the 
        main topography plot, show a new figure containing FOOOF fit plot
        for every condition """

        fig = ax.figure
        fig.delaxes(ax)

        for idx, (report_key, report) in enumerate(reports.items()):
            report_ax = fig.add_subplot(1, len(reports), idx+1)
            fooof = report.get_fooof(names_idx)

            # Use plot function from fooof
            fooof.plot(
                ax=report_ax,
                plot_peaks='dot',
                add_legend=False,
            )
            # Add information about the fit to the axis title
            text = ("Condition: " + str(report_key) + "\n" +
                    "R squared: " + format_float(fooof.r_squared_) + "\n" +
                    "Peaks: \n")
            for peak_params in fooof.peak_params_:
                text = text + '{0} ({1}, {2})\n'.format(*format_floats(peak_params))

            report_ax.set_title(text)

        fig.tight_layout()

    # Create a topography where one can inspect fits by clicking subplots
    fig = plt.figure()
    for ax, info_idx, names_idx in iterate_topography(
            fig, info, ch_names, on_pick):

        handles = []
        for color_idx, (key, report) in enumerate(reports.items()):
            curve = report.power_spectra[names_idx]
            handles.append(
                ax.plot(curve, color=colors[color_idx],
                        linewidth=0.5, label=key)[0])

    if not handles:
        return

    fig.legend(handles=handles)
    title = '{0}_{1}'.format(report_item.name, ch_type)
    set_figure_title(fig, title)
    plt.show()

