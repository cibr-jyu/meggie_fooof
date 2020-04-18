"""
"""
import logging

import matplotlib.pyplot as plt


from meggie.utilities.colors import color_cycle
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
        """
        """
        fig = ax.figure
        fig.delaxes(ax)

        for idx, (report_key, report) in enumerate(reports.items()):
            report_ax = fig.add_subplot(1, len(reports), idx+1)
            fooof = report.get_fooof(names_idx)

            fooof.plot(
                ax=report_ax,
                plot_peaks='dot',
                add_legend=False,
            )
            text = ("Condition: " + str(report_key) + "\n" +
                    "R squred: " + '{0:.2f}'.format(fooof.r_squared_) + "\n" +
                    "Peaks: \n")
            for peak_params in fooof.peak_params_:
                text = text + '{0:.2f} ({1:.2f}, {2:.2f})\n'.format(*peak_params)

            report_ax.set_title(text)

        fig.tight_layout()

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
    title = 'report_{0}'.format(report_item.name)
    fig.canvas.set_window_title(title)
    fig.suptitle(title)
    plt.show()

