# coding: utf-8

import logging
import os

import matplotlib.pyplot as plt

from meggie.utilities.filemanager import create_timestamped_folder
from meggie.utilities.filemanager import save_csv
from meggie.utilities.formats import format_float


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

