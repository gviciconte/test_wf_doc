from aiida.plugins import DataFactory

from aiida_aspherix.calculations.aspherix import AspherixCalculation
from aiida_aspherix.common.functions import *

class AspherixInsertion(AspherixCalculation):
    @classmethod
    def define(cls, spec):
        super(AspherixInsertion, cls).define(spec)

        spec.input(
            "metadata.options.parser_name",
            valid_type=str,
            default="aspherix",
        )




    @staticmethod
    def create_main_input_content(mat_param,domain,particle_template_par,shape,ins_par,part_dist,**kwargs):
        mesh_list=kwargs.get('mesh_list',None)
        aspherix_input_file = f"particle_shape {shape} \n"
        aspherix_input_file += simulation_domain(domain)
        aspherix_input_file += "simulation_timestep 5e-5 \n"
        aspherix_input_file += "write_output_timestep 0.05 \n"
        aspherix_input_file += "write_to_terminal_timestep 0.01 \n"
         

        aspherix_input_file += material_properties(mat_param)

        aspherix_input_file += "particle_contact_model normal hertz tangential history cohesion off rolling_friction off settings \n"
        aspherix_input_file += "wall_contact_model normal hertz tangential history settings \n"
        if mesh_list:
            aspherix_input_file += define_mesh(mesh_list)
        aspherix_input_file += particles_templates(particle_template_par)
        aspherix_input_file += particles_distribution(part_dist)
        aspherix_input_file += "enable_heat_conduction initial_particle_temperature 300 area_correction yes \n"
        aspherix_input_file += insertion_parameters(ins_par)
        aspherix_input_file += "check_timestep \n"
        aspherix_input_file += "enable_gravity \n"
        aspherix_input_file += "output_settings\n"
        aspherix_input_file += "simulate time 0.1\n"
        aspherix_input_file += "write_restart restart/restart.latest\n"



        return aspherix_input_file