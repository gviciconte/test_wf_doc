from aiida.plugins import DataFactory

from aiida_fc_calibration.calculations.calibration import Calibration
from aiida_fc_calibration.common.functions import *
from aiida_fc_calibration.common.mkfile import *
from aiida_fc_calibration.common.functions import *
import pdb
class Calibration(Calibration):
    @classmethod
    def define(cls, spec):
        super(Calibration, cls).define(spec)

        spec.input(
            "metadata.options.parser_name",
            valid_type=str,
            default="calibration",
        )


    @staticmethod
    def create_input_insertion(asx):
        aspherix_input_file = "particle_shape sphere \n"
        aspherix_input_file +="variable pathCommon string ../commonData\n"
        aspherix_input_file +="variable pathInfo string ./\n"
        aspherix_input_file +="boundary_conditions x periodic y periodic\n"
        aspherix_input_file += simulation_domain(asx._domain)
        aspherix_input_file +="simulation_timestep 1e-7\n"
        aspherix_input_file +="write_output_timestep 1e-4\n"
        aspherix_input_file +="write_to_terminal_timestep 1e-5\n"

        aspherix_input_file +="include ${pathCommon}/variablesMicro\n"
        aspherix_input_file += material_properties(asx._mat_prop)
        aspherix_input_file +="particle_contact_model normal hertz tangential history cohesion off rolling_friction off settings\n"
        aspherix_input_file +="wall_contact_model normal hertz tangential history settings\n"
        aspherix_input_file +="mesh_module servo center_of_mass ( 5e-3, 5e-3, 5e-3 ) ctrlPV force maximum_velocity 50 target_val 1 axis ( 0, 0, -1 ) mode auto ratio 0.01 id servo\n"
        

        aspherix_input_file += define_mesh(asx._meshes_list)
        aspherix_input_file += particles_templates(asx._part_temp_dict)
        aspherix_input_file +="include  ${pathCommon}/particlesMicro\n"

        aspherix_input_file +="insertion mode pack region simulation_domain_region_ insert_every_time 1e-4 target_particle_count 20000 &\n"
        aspherix_input_file +="                particle_distribution pd1 velocity constant ( 0, 0, -1 ) id ins1 disable_few_particles_error yes &\n"
        aspherix_input_file +="                packing_generator style batch batch_size 100\n"

        aspherix_input_file +="check_timestep\n"
        aspherix_input_file +="enable_gravity \n"
        aspherix_input_file +="enable_heat_conduction initial_particle_temperature 300\n"
        aspherix_input_file +="enable_loadbalancing\n"
        aspherix_input_file +="calculate wall_contact_network properties {pos,ids} id cal1\n"
        aspherix_input_file +="output_settings write_particle_contact_network yes write_wall_contact_network yes wall_network_command_id cal1\n"
        aspherix_input_file +="modify_command id top old_style yes servo/integrate stop\n"
        aspherix_input_file +="simulate time 10.1e-4\n"
        aspherix_input_file +="disable_command id ins1\n"
        aspherix_input_file +="modify_command id top old_style yes servo/integrate start\n"
        aspherix_input_file +="simulate time 10.1e-4\n"
        aspherix_input_file +="integrator disable yes\n"
        aspherix_input_file +="delete_particles every_time once material pore_mat\n"
        aspherix_input_file +="simulate time 1.1e-4\n"
        aspherix_input_file +="write_restart restart/restart.latest\n"

        return aspherix_input_file

    @staticmethod
    def create_run_dem():
        runDem="#!/bin/bash\n"
        runDem+="cd ${0%/*} || exit 1    # run from this directory\n"
        runDem+="rm -rf restart post\n"
        runDem+="mpirun -np 4 aspherix -in input.asx\n"

        return runDem

    @staticmethod
    def write_common_file(commonDataFolder,radius,pores):
        write_variablesMicro(commonDataFolder,radius,pores)
        write_partilclesMicro(commonDataFolder)
        

        return 




    def create_aspherix_input_content(self,tmp):
        

        insertion_micro=tmp+'micro'
        os.makedirs(insertion_micro)
        
        asxData=self.inputs.AsxParametersMicro
        write_bottom(insertion_micro,asxData._domain)
        write_plate(insertion_micro,asxData._domain)
        insertion_txt =self.create_input_insertion(asxData)
        input_filename =insertion_micro+ '/input.asx'
        with open(input_filename, "w") as infile:
            infile.write(insertion_txt)

        insertion_txt =self.create_run_dem()
        input_filename =insertion_micro+ '/RunDEM'
        with open(input_filename, "w") as infile:
            infile.write(insertion_txt)
        os.system("chmod +x "+input_filename)
        
        commonDataFolder=tmp+'commonData'
        os.makedirs(commonDataFolder)
    
        self.write_common_file(commonDataFolder,asxData._part_temp_dict["part"]["radius"],asxData._part_temp_dict["pore"]["radius"])

    @staticmethod
    def create_calibration_script(porosity_obj,iterMax):
        runPorosity="from fc_material_calibration_OM.porosity import Calibration as CalibrationPorosity\n"
        runPorosity+="import os\n"
        runPorosity+="folderFC=os.getcwd()\n"
        runPorosity+=f"CalibrationPorosity({porosity_obj},folderFC,'commonData',{iterMax})\n"
        return runPorosity