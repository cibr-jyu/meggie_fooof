# coding: utf-8

import logging
import os

import matplotlib.pyplot as plt

from meggie.utilities.filemanager import create_timestamped_folder
from meggie.utilities.filemanager import save_csv
from meggie.utilities.formats import format_float
from meggie.utilities.formats import format_floats
from meggie.utilities.plotting import color_cycle
from meggie.utilities.channels import iterate_topography


def plot_topo_fit(experiment, report_item):
    """ Plot topography where by clicking subplots you can check the fit parameters
    of specific channels """

    subject = experiment.active_subject

    reports = report_item.content
    ch_names = report_item.params['ch_names']
    freqs = list(reports.values())[0].freqs

    colors = color_cycle(len(reports))

    raw = subject.get_raw()
    info = raw.info

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
                    "R squred: " + format_float(fooof.r_squared_) + "\n" +
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

    fig.legend(handles=handles)
    fig.canvas.set_window_title(report_item.name)
    fig.suptitle(report_item.name)

    plt.show()


def save_all_channels(experiment, selected_name):
    """ Saves peak params and aperiodic params to a csv file for every 
    subject and channel and condition """
    row_descs = []
    csv_data = []

    column_names = ['CF', 'Amp', 'BW', 
                    'Aperiodic offset', 'Aperiodic exponent']

    for subject in experiment.subjects.values():
        fooof_item = subject.fooof_report.get(selected_name)
        if not fooof_item:
            continue
        for key, report in fooof_item.content.items():
            for ch_idx, ch_name in enumerate(fooof_item.params['ch_names']):
                ch_report = report.get_fooof(ch_idx)
                for peak in ch_report.peak_params_:
                    csv_data.append([format_float(peak[0]),
                                     format_float(peak[1]),
                                     format_float(peak[2]), 
                                     '', ''])
                    row_descs.append((subject.name, key, ch_name))
                aparams = ch_report.aperiodic_params_
                csv_data.append(['', '', '',
                                 format_float(aparams[0]),
                                 format_float(aparams[1])])

                row_descs.append((subject.name, key, ch_name))

    # Save the resulting csv into a output folder 'meggie way'
    folder = create_timestamped_folder(experiment)
    fname = selected_name + '_all_subject_all_channels_fooof.csv'
    path = os.path.join(folder, fname)

    save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)

