"""
"""

import os
import re
import logging

from fooof import FOOOFGroup


class FOOOFReport(object):
    """ Container for FOOOF report data that can be handled by meggie
    """

    def __init__(self, name, fooof_directory, params, content=None):
        """
        """
        self._name = name
        self._content = {}

        # on item creation, content is passed and is set here
        if content is not None:
            self._content = content
        
        self._path = fooof_directory
        self._params = params

    @property
    def content(self):
        """ Return report data if already in memory, otherwise read from fs. 
        Content is assumed to be a dictionary with conditions as keys 
        and reports as values """
        if self._content:
            return self._content

        template = self.name + '_' + r'([a-zA-Z1-9_]+)\.json'
        for fname in os.listdir(self._path):
            match = re.match(template, fname)
            if match:
                try:
                    key = str(match.group(1))
                except Exception as exc:
                    raise Exception("Unknown file name format.")

                if 'conditions' in self._params:
                    if key not in [str(elem) for elem 
                                   in self._params['conditions']]:
                        continue

                logging.getLogger('ui_logger').debug(
                        'Reading FOOOF file: ' + str(fname))

                fg = FOOOFGroup()
                fg.load(fname, self._path)
                self._content[key] = fg
        return self._content

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params

    def save_content(self):
        """ Save dictionary containing reports to fs
        """
        try:
            # if exists, delete first
            self.delete_content()

            for key, report in self._content.items():
                fname = self._name + '_' + str(key) + '.json'
                report.save(fname, self._path, save_results=True, 
                            save_settings=True, save_data=True)

        except Exception as exc:
            raise IOError('Writing FOOOF report failed')

    def delete_content(self):
        """ Delete report data from the fs
        """
        template = self.name + '_' + r'([a-zA-Z1-9_]+)\.json'
        for fname in os.listdir(self._path):
            match = re.match(template, fname)
            if match:
                try:
                    key = str(match.group(1))
                except Exception as exc:
                    continue

                if 'conditions' in self._params:
                    if key not in [str(elem) for elem 
                                   in self._params['conditions']]:
                        continue

                logging.getLogger('ui_logger').debug(
                        'Removing existing fooof file: ' + str(fname))

                os.remove(os.path.join(self._path, fname))

