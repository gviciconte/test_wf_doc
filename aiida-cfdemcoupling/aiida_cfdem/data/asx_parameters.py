"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""
# You can directly use or subclass aiida.orm.data.Data
# or any other data type liste
from aiida.orm import List

class AspherixParameters(List):
    def __init__(self, shape, 
                       domain,
                       mat_prop,
                       meshes_list,
                       part_temp_dict,
                       particle_distribution,
                       insertion_region,
                       insertion_par,

                       **kwargs):
        super(AspherixParameters, self).__init__(
            list=[shape, 
                  domain,
                  mat_prop,
                  meshes_list,
                  part_temp_dict,
                  particle_distribution,
                  insertion_region,
                  insertion_par
                  ], **kwargs)

        self._shape = shape
        self._domain = domain
        self._mat_prop = mat_prop
        self._meshes_list = meshes_list
        self._part_temp_dict = part_temp_dict
        self._particle_distribution = particle_distribution
        self._insertion_region = insertion_region
        self._insertion_par= insertion_par

    @property
    def shape(self):
        return self._shape

    @property
    def domai(self):
        return self._domain

    @property
    def mat_prop(self):
        self._mat_prop

    @property
    def meshes_list(self):
        self._meshes_list
    
    @property
    def temp_dict(self):
        self._part_temp_dict
    
    @property
    def particle_distribution(self):
        self._particle_distribution

    @property
    def insertion_region(self):
        self._insertion_region
    
    @property
    def insertion_par(self):
        self._insertion_par