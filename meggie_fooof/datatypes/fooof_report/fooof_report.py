"""
"""

import os


class FOOOFReport(object):
    """
    """

    def __init__(self, name, fooof_directory, params, content=None):
        """
        """
        self._name = name
        self._content = content
        
        # set ext correctly here!!!!!!!!!!!!!!!!!!!!!!!!!
        self._path = os.path.join(fooof_directory, name + '.XXDDD')
        self._params = params

    @property
    def content(self):
        """
        """
        if self._content:
            return self._content

        # read content here from file
        # self._content = ..

        return self._content

    @property
    def name(self):
        """
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        """
        self._name = name

    @property
    def params(self):
        """
        """
        return self._params

    @params.setter
    def params(self, params):
        """
        """
        self._params = params

    def save_content(self):
        """
        """
        try:
            # write fooof_report...
            pass
        except Exception as exc:
            raise IOError('Writing FOOOF report failed')

    def delete_content(self):
        os.remove(self._path)
