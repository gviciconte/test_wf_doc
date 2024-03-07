"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""
# You can directly use or subclass aiida.orm.data.Data
# or any other data type liste
from aiida.orm import List

class AspherixParameters(List):
    def __init__(self, shape=None,
                       convex_particle=None, 
                       domain=None,
                       mat_prop=None,
                       meshes_list=None,
                       part_temp_dict=None,
                       particle_distribution=None,
                       folder_mesh=None,
                       insertion_par=None,
                       **kwargs):
        super(AspherixParameters, self).__init__(
            list=[shape,
                  convex_particle, 
                  domain,
                  mat_prop,
                  meshes_list,
                  part_temp_dict,
                  particle_distribution,
                  folder_mesh,
                  insertion_par
                  ], **kwargs)

        self._shape = shape if shape is not None else 'not_set'
        self._domain = domain if domain is not None else 'not_set'
        self._mat_prop = mat_prop if mat_prop is not None else 'not_set'
        self._convex_particle = convex_particle if convex_particle is not None else 'not_set'
        self._meshes_list = meshes_list if meshes_list is not None else 'not_set'
        self._part_temp_dict = part_temp_dict if part_temp_dict is not None else 'not_set'
        self._particle_distribution = particle_distribution if particle_distribution is not None else 'not_set'
        self._folder_mesh = folder_mesh if folder_mesh is not None else 'not_set'
        self._insertion_par= insertion_par if insertion_par is not None else 'not_set'

    @property
    def shape(self):
        return self._shape

    @property
    def domain(self):
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
    def convex_particle(self):
        self._convex_particle

    @property
    def particle_distribution(self):
        self._particle_distribution

    @property
    def folder_mesh(self):
        self._folder_mesh
    
    @property
    def insertion_par(self):
        self._insertion_par