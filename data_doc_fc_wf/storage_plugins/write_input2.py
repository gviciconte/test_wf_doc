"""Dedicated storage plugin for Aspherix input
"""
import dlite
from dlite.options import Options

import yaml
from pathlib import Path



class write_input2(dlite.DLiteStorageBase):  # pylint: disable=invalid-name
    """DLite storage plugin for Aspherix input.
    """


    def open(self, uri, options=None):
        """Opens `uri`."""
        # pylint: disable=attribute-defined-outside-init
        self.options = Options(options)
        self.uri = uri

    def save(self,inst):

        #data = dict(data_input=inst.properties)
        with open(self.uri, "w", encoding="utf8") as handle:
            yaml.dump(inst.properties, handle, default_flow_style=False)

        return inst
       
