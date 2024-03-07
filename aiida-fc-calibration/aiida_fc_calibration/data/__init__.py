"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""
# You can directly use or subclass aiida.orm.data.Data
# or any other data type liste
from aiida.orm import List

class AspherixPositions(List):
    def __init__(self, positions, **kwargs):
        super(AspherixPositions, self).__init__(list=[positions], **kwargs)
        self._positions = positions

    @property
    def positions(self):
        return self._positions

