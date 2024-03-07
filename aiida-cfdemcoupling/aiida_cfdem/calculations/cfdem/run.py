

from aiida_cfdem.calculations.cfdem import CfdemCalculation
from aiida_cfdem.common.functions import *
from aiida_cfdem.common.cfdem_files import *
from aiida_cfdem.common.cfdem_functions import *
from aiida_cfdem.common.zero_files import *
import os
import pdb
system_dict={
"fvSchemes":fvSchemes,
"fvSolution":fvSolution,
"topoSetDict":topoSetDict,
"createPatchDict":createPatchDict
}

constant_dict={"couplingProperties":couplingProperties,
"phaseProperties":phaseProperties,
"g":gravity,
"thermophysicalProperties.gas":thermoProp_gas,
"thermophysicalProperties.vapor":thermoProp_vapor,
"momentumTransport.gas":momentumTransport_gas,
"momentumTransport.vapor":momentumTransport_vapor}

zero_files_dict={"alpha.gas": alpha_gas,
"alpha.vapor":alpha_vapor,
"N2.gas":N2_gas,
"O2.gas":O2_gas,
"p":p,
"p_rgh":p_rgh,
"T.gas":T_gas,
"T.vapor":T_vapor,
"U.gas":U_gas,
"U.vapor":U_vapor,
"voidfraction":voidfraction,
"Ydefault":Y_default
}


class CfdemRun(CfdemCalculation):
    @classmethod
    def define(cls, spec):
        super(CfdemRun, cls).define(spec)

        spec.input(
            "metadata.options.parser_name",
            valid_type=str,
            default="cfdem",
        )

    @staticmethod
    def create_cfd_folders_and_files(tmp,domain,solver_in):

        DEM_folder=f"{tmp}/DEM"
        CFD_folder=f"{tmp}/CFD"
        CFD_system=f"{CFD_folder}/system"
        CFD_constant=f"{CFD_folder}/constant"
        CFD_0=f"{CFD_folder}/0"
        xmin_a=domain["low"][0]
        ymin_a=domain["low"][1]
        zmin_a=domain["low"][2]

        xmax_a=domain["high"][0]
        ymax_a=domain["high"][1]
        zmax_a=domain["high"][2]

        system_dict.update({"controlDict":f"{controlDict}".format(solver=solver_in)}),
                    
        system_dict.update({"blockMeshDict":f"{blockMeshDict}".format(xmin=xmin_a,
                                                                xmax=xmax_a,
                                                                ymin=ymin_a,
                                                                ymax=ymax_a,
                                                                zmin=zmin_a,
                                                                zmax=zmax_a
                                                                )})
                    
        os.makedirs(DEM_folder)
        os.makedirs(CFD_system)
        os.makedirs(CFD_constant)
        os.makedirs(CFD_0)
        
        create_OF_dicts(CFD_constant,constant_dict)
        create_OF_dicts(CFD_system,system_dict)
        create_OF_dicts(CFD_0,zero_files_dict)




    @staticmethod
    def create_aspherix_input_content(mat_param,domain,particle_template_par,shape,part_dist,mesh_list,DeltaV):
        
        aspherix_input_file = f"particle_shape {shape} \n"
        aspherix_input_file += "read file ../restart.latest \n"
        aspherix_input_file += simulation_domain(domain)
        aspherix_input_file += "simulation_timestep 1e-5 \n"
        aspherix_input_file += "write_output_timestep 0.05 \n"
        aspherix_input_file += "write_to_terminal_timestep 0.01 \n"
         

        aspherix_input_file += material_properties(mat_param)

        aspherix_input_file += "particle_contact_model normal hertz tangential history cohesion off rolling_friction off settings \n"
        aspherix_input_file += "wall_contact_model normal hertz tangential history settings \n"
        aspherix_input_file += "mesh_module servo center_of_mass ( 5e-3, 5e-3, 30e-3 ) ctrlPV force maximum_velocity 5 target_val 1 axis ( 0, 0, -1 ) mode auto ratio 0.01 id servo\n"

        aspherix_input_file += define_mesh(mesh_list)

        
        aspherix_input_file += particles_templates(particle_template_par)

        aspherix_input_file +=f"enable_electrical_conductivity meshes {{ bottom, top }} potentials {{ 0, {DeltaV} }} id ee1 enable_electric_heating yes\n"
        aspherix_input_file += "enable_heat_conduction initial_particle_temperature 300 area_correction yes #contact_area convex \n"

        aspherix_input_file += "check_timestep \n"
        aspherix_input_file += "enable_gravity \n"
        aspherix_input_file += "output_settings\n"
        aspherix_input_file += "integrator disable yes\n"
        aspherix_input_file += "modify_command id top old_style yes servo/integrate stop\n"
        aspherix_input_file += "enable_cfd_coupling  heat_transfer yes\n"

        aspherix_input_file += "write_restart restart/restart.latest\n"



        return aspherix_input_file
    
    @staticmethod
    def parCFDDEMrun():
        a="""
        . ~/.bashrc
casePath="$(dirname "$(readlink -f ${BASH_SOURCE[0]})")"

separateDEM="run.asx"

# check if mesh was built
if [ -f "$casePath/CFD/constant/polyMesh/points" ]; then
    echo "mesh was built before - using old mesh"
else
    echo "mesh needs to be built"
    cd $casePath/CFD
    blockMesh
    topoSet
    createPatch -overwrite
fi
#- include functions
source $CFDEM_SRC_DIR/lagrangian/cfdemParticle/etc/functions.sh
cd ..
#--------------------------------------------------------------------------------#
#- define variables
casePath="$(dirname "$(readlink -f ${BASH_SOURCE[0]})")"
logpath=$casePath
headerText="run_parallel_cfdemSolverIB_CFDDEM"
logfileName="log_$headerText"
solverName="cfdemSolverMultiPhaseEuler"
nrProcs=1
machineFileName="none"   # yourMachinefileName | none
debugMode="off"          # on | off| strict
separateDEM="run.asx"
#--------------------------------------------------------------------------------#

#- call function to run a parallel CFD-DEM case
parCFDDEMrun $logpath $logfileName $casePath $headerText $solverName $nrProcs $machineFileName $debugMode $separateDEM
        """
        return a