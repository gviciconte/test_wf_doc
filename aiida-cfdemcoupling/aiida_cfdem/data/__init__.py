"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""
# You can directly use or subclass aiida.orm.data.Data
# or any other data type liste
from aiida.orm import List

class AspherixPositionsAndType(List):
    def __init__(self, positions, p_type,materials,part_template, **kwargs):
        super(AspherixPositionsAndType, self).__init__(list=[positions, p_type,materials,part_template], **kwargs)
        self._positions = positions
        self._p_type = p_type
        self._materials = materials
        self._part_template = part_template
    @property
    def positions(self):
        return self._positions

    @property
    def p_type(self):
        return self._p_type
    
    @property
    def materials(self):
        return self._materials

    @property
    def part_template(self):
        return self._part_template