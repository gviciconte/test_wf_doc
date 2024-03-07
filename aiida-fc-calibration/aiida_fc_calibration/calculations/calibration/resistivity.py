from aiida.plugins import DataFactory

from aiida_fc_calibration.calculations.calibration import Calibration
from aiida_fc_calibration.common.functions import *
from aiida_fc_calibration.common.mkfile import *
from aiida_fc_calibration.common.mkfile_macro import *


class Calibration(Calibration):
    @classmethod
    def define(cls, spec):
        super(Calibration, cls).define(spec)

        spec.input(
            "metadata.options.parser_name",
            valid_type=str,
            default="calibration_res",
        )


    @staticmethod
    def create_input_electric_micro(asx):
        aspherix_input_file = "particle_shape sphere \n"
        aspherix_input_file +="variable pathCommon string ../commonData\n"
        aspherix_input_file +="read file ../restart_micro.latest\n"

        aspherix_input_file +="boundary_conditions x periodic y periodic\n"
        aspherix_input_file += simulation_domain(asx._domain)
        aspherix_input_file +="simulation_timestep 1e-7\n"
        aspherix_input_file +="write_output_timestep 1e-4\n"
        aspherix_input_file +="write_to_terminal_timestep 1e-5\n"
        aspherix_input_file +="include potentials_info.dat\n"

        aspherix_input_file += material_properties(asx._mat_prop)
        aspherix_input_file +="particle_contact_model normal hertz tangential history cohesion off rolling_friction off settings\n"
        aspherix_input_file +="wall_contact_model normal hertz tangential history settings\n"
        aspherix_input_file +="mesh_module servo center_of_mass ( 5e-3, 5e-3, 5e-3 ) ctrlPV force maximum_velocity 50 target_val 1 axis ( 0, 0, -1 ) mode auto ratio 0.01 id servo\n"
        

        aspherix_input_file += define_mesh(asx._meshes_list)
        aspherix_input_file += particles_templates(asx._part_temp_dict)
        aspherix_input_file +="enable_electrical_conductivity meshes { bottom, top } potentials { 0, ${DeltaV} } id ee1 enable_electric_heating yes\n"

        aspherix_input_file +="enable_heat_conduction initial_particle_temperature 300 area_correction no\n"
        aspherix_input_file +="compute cpgl all pair/gran/local pos ids force contactArea electricCurrent electricConductance \n"
        aspherix_input_file +="compute cwgl all wall/gran/local pos ids force contactArea electricCurrent electricConductance \n"

        aspherix_input_file +="wall/gran/local id wgl_lid_current interaction_with_mesh top electricCurrent\n"
        aspherix_input_file +="reduce id lid_current sum c_wgl_lid_current[1]\n"
        aspherix_input_file +="wall/gran/local id wgl_floor_current interaction_with_mesh bottom electricCurrent\n"
        aspherix_input_file +="reduce id floor_current sum c_wgl_floor_current[1]\n"

        aspherix_input_file +="variable I_top equal c_lid_current\n"
        aspherix_input_file +="variable I_bot equal c_floor_current\n"
        aspherix_input_file +="variable delta_I equal v_I_bot-v_I_top\n"
        aspherix_input_file +="variable I_mean equal 0.5*(v_I_top+v_I_bot)\n"


        aspherix_input_file +="compute t1 all reduce ave id_Temp\n"

        aspherix_input_file +="check_timestep\n"
        aspherix_input_file +="enable_gravity \n"
        aspherix_input_file +="write_to_file file postCo/conductivity_data.txt string \"id_time ${I_mean} ${delta_I} id_t1\" write_every_time 1e-3\n"
 
        aspherix_input_file +="calculate wall_contact_network properties {pos,ids,electricConductance,electricCurrent} id cal1\n"
        aspherix_input_file +="output_settings write_particle_contact_network yes write_wall_contact_network yes wall_network_command_id cal1\n"
        aspherix_input_file +="integrator disable yes\n"
        aspherix_input_file +="simulate time ${timeSim} \n"


        return aspherix_input_file


    @staticmethod
    def create_input_electric_macro(asx):
        aspherix_input_file = "particle_shape convex \n"
        aspherix_input_file +="variable pathCommon string ../commonData\n"
        aspherix_input_file +="read file ../restart_macro.latest\n"

        aspherix_input_file +="boundary_conditions x periodic y periodic\n"
        aspherix_input_file += simulation_domain(asx._domain)
        aspherix_input_file +="simulation_timestep 1e-7\n"
        aspherix_input_file +="write_output_timestep 1e-4\n"
        aspherix_input_file +="write_to_terminal_timestep 1e-5\n"
        aspherix_input_file +="include potentials_info.dat\n"

        aspherix_input_file +="include ${pathCommon}/variablesMacro\n"
        aspherix_input_file += material_properties(asx._mat_prop)
        aspherix_input_file +="particle_contact_model normal hertz tangential history cohesion off rolling_friction off settings\n"
        aspherix_input_file +="wall_contact_model normal hertz tangential history settings\n"
        aspherix_input_file +="mesh_module servo center_of_mass ( 5e-3, 5e-3, 5e-3 ) ctrlPV force maximum_velocity 50 target_val 1 axis ( 0, 0, -1 ) mode auto ratio 0.01 id servo\n"
        

        aspherix_input_file += define_mesh(asx._meshes_list)
        aspherix_input_file += particles_templates(asx._part_temp_dict)
        aspherix_input_file +="enable_electrical_conductivity meshes { bottom, top } potentials { 0, ${DeltaV} } \n"
        aspherix_input_file +="enable_heat_conduction initial_particle_temperature 300 area_correction yes contact_area convex \n"

        
        aspherix_input_file +="compute cpgl all pair/gran/local pos ids force contactArea electricCurrent electricConductance \n"
        aspherix_input_file +="compute cwgl all wall/gran/local pos ids force contactArea electricCurrent electricConductance \n"

        aspherix_input_file +="wall/gran/local id wgl_lid_current interaction_with_mesh top electricCurrent\n"
        aspherix_input_file +="reduce id lid_current sum c_wgl_lid_current[1]\n"
        aspherix_input_file +="wall/gran/local id wgl_floor_current interaction_with_mesh bottom electricCurrent\n"
        aspherix_input_file +="reduce id floor_current sum c_wgl_floor_current[1]\n"

        aspherix_input_file +="variable I_top equal c_lid_current\n"
        aspherix_input_file +="variable I_bot equal c_floor_current\n"
        aspherix_input_file +="variable delta_I equal v_I_bot-v_I_top\n"
        aspherix_input_file +="variable I_mean equal 0.5*(v_I_top+v_I_bot)\n"


        aspherix_input_file +="compute t1 all reduce ave id_Temp\n"

        aspherix_input_file +="check_timestep\n"
        aspherix_input_file +="enable_gravity \n"
        aspherix_input_file +="write_to_file file postCo/conductivity_data.txt string \"id_time ${I_mean} ${delta_I} id_t1\" write_every_time 1e-3\n"
 
        aspherix_input_file +="calculate wall_contact_network properties {pos,ids,electricConductance,electricCurrent} id cal1\n"
        aspherix_input_file +="output_settings write_particle_contact_network yes write_wall_contact_network yes wall_network_command_id cal1\n"
        aspherix_input_file +="integrator disable yes\n"
        aspherix_input_file +="simulate time ${timeSim} \n"


        return aspherix_input_file


    @staticmethod
    def create_run_dem():
        runDem="#!/bin/bash\n"
        runDem+="cd ${0%/*} || exit 1    # run from this directory\n"
        runDem+="rm -rf restart post\n"
        runDem+="cp ../fiber.stl .\n"
        runDem+="mpirun -np 4 aspherix -in input.asx\n"
        return runDem

    @staticmethod
    def write_common_file(commonDataFolder,radius,pores):
        write_variablesMicro(commonDataFolder,radius,pores)
        write_variablesMacro(commonDataFolder)

        return 




    def create_aspherix_input_content(self,tmp):

        insertion_micro=tmp+'/micro'
        os.makedirs(insertion_micro)
        write_variablesPotential(insertion_micro)

        asxDataMicro=self.inputs.AsxParametersMicro
        write_bottom(insertion_micro,asxDataMicro._domain)
        write_plate(insertion_micro,asxDataMicro._domain)
        insertion_txt =self.create_input_electric_micro(asxDataMicro)
        input_filename =insertion_micro+ '/input.asx'
        with open(input_filename, "w") as infile:
            infile.write(insertion_txt)

        insertion_txt =self.create_run_dem()
        input_filename =insertion_micro+ '/RunDEM'
        with open(input_filename, "w") as infile:
            infile.write(insertion_txt)
        os.system("chmod +x "+input_filename)
        
        asxDataMacro=self.inputs.AsxParametersMacro
        insertion_macro=tmp+'macro'
        os.makedirs(insertion_macro)
        write_bottom(insertion_macro,asxDataMacro._domain)
        write_plate(insertion_macro,asxDataMacro._domain)
 
        write_variablesPotential(insertion_macro)

        insertion_txt =self.create_input_electric_macro(asxDataMacro)
        input_filename =insertion_macro+ '/input.asx'
        with open(input_filename, "w") as infile:
            infile.write(insertion_txt)

        insertion_txt =self.create_run_dem()
        input_filename =insertion_macro+ '/RunDEM'
        with open(input_filename, "w") as infile:
            infile.write(insertion_txt)
        os.system("chmod +x "+input_filename)


        commonDataFolder=tmp+'commonData'
        os.makedirs(commonDataFolder)     
        self.write_common_file(commonDataFolder,asxDataMicro._part_temp_dict["part"]["radius"],asxDataMicro._part_temp_dict["pore"]["radius"])

    @staticmethod
    def create_calibration_script(resistivity_obj,iterMax):
        runPorosity="from fc_material_calibration_OM.resistivity import Calibration as CalibrationResitivity\n"
        runPorosity+="import os\n"
        runPorosity+="folderFC=os.getcwd()\n"
        runPorosity+="case_folders=['micro','macro']\n"
        runPorosity+=f"CalibrationResitivity({resistivity_obj},folderFC,'commonData',case_folders,{iterMax})\n"
        return runPorosity