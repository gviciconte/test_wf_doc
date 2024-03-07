"""
Calculations provided by aiida_diff.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""
from aiida.common import datastructures
from aiida.engine import CalcJob
from aiida.orm import SinglefileData, Float,Int,FolderData,Dict
from aiida.plugins import DataFactory
AsxParameters=DataFactory("aspherix.parameters")
import pdb

class Calibration(CalcJob):
    """
    AiiDA calculation plugin wrapping the diff executable.

    Simple AiiDA plugin wrapper for 'diffing' two files.
    """
    _FILE_NAME="calibration.py"
    _cmdline_params = _FILE_NAME
    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        super().define(spec)

        # set default values for AiiDA options
        spec.inputs["metadata"]["options"]["resources"].default = {
            "num_machines": 1,
            "num_mpiprocs_per_machine": 1,
        }
        #spec.inputs["metadata"]["options"]["parser_name"].default = "aspherix"

        # new ports
        spec.input(
            "metadata.options.output_filename", valid_type=str, default="log.out"
        )
        spec.input(
            "metadata.options.aspherix_simulation_pvd", valid_type=str, default="micro/post/aspherix_simulation.pvd"
        )
        spec.input(
            "metadata.options.aspherix_restart_file", valid_type=str, default="micro/restart/restart.latest"
        )
        spec.input(
            "metadata.options.aspherix_simulation_post", valid_type=str, default="post"
        )
        spec.input(
        "metadata.options.aspherix_simulation_name", valid_type=str, default="aspherix_simulation.pvd"
        )
        spec.input("quantity_obj", valid_type=Float, help=" quantity used to calibrate")
        spec.input("max_iter", valid_type=Int, help=" max iteration optimization")
        spec.input(
            "restart_file_micro", valid_type=SinglefileData, help="restart file micro.",required=False
        )
        spec.input(
            "restart_file_macro", valid_type=SinglefileData, help="restart file macro.",required=False
        )
        spec.input(
            "convex_particle", valid_type=SinglefileData, help="convex particle stl file.",required=False
        )
        spec.input('AsxParametersMicro', valid_type=AsxParameters,required=False)
        spec.input('AsxParametersMacro', valid_type=AsxParameters,required=False)

        spec.output(
            "log",
            valid_type=SinglefileData,
            help="log file.",
        )
        spec.output(
            "restart_file",
            valid_type=SinglefileData,
            help="aspherix restart file.",
        )
        spec.output(
            "calibrated_variables",
            valid_type=Dict,
            help="calibrated variables dict.",
        )
        spec.output(
            "aspherix_points_info",
            valid_type=DataFactory("porosity"),
            help="info about points positions and type",
        )
        spec.exit_code(
            300,
            "ERROR_MISSING_OUTPUT_FILES",
            message="Calculation did not produce all expected output files.",
        )


    
    def create_aspherix_input_content(self,tmp):
        raise NotImplementedError
    
    @staticmethod
    def create_calibration_script(porosity_obj,max_iter):
        raise NotImplementedError


    def prepare_for_submission(self, folder):
        """
        Create input files.
        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files
            needed by the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        tmp=folder.get_abs_path('')
        self.create_aspherix_input_content(tmp)
        input_txt =self.create_calibration_script(self.inputs.quantity_obj.value,self.inputs.max_iter.value)

        input_filename = folder.get_abs_path(self._FILE_NAME)

        with open(input_filename, "w") as infile:
            infile.write(input_txt)


        
        codeinfo = datastructures.CodeInfo()
        codeinfo.cmdline_params = [self._cmdline_params]
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.stdout_name = self.metadata.options.output_filename
        codeinfo.withmpi = self.inputs.metadata.options.withmpi

        

        # Prepare a `CalcInfo` to be returned to the engine
        calcinfo = datastructures.CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = []
        if "restart_file_micro" in self.inputs:
            calcinfo.retrieve_list = [self.metadata.options.output_filename,
                                      self.metadata.options.aspherix_simulation_pvd
                                     ]
            calcinfo.local_copy_list = [
            (
                self.inputs.restart_file_micro.uuid,
                self.inputs.restart_file_micro.filename,
                "restart_micro.latest",
            ),
            (
                self.inputs.restart_file_macro.uuid,
                self.inputs.restart_file_macro.filename,
                "restart_macro.latest",
            ),
            (
                self.inputs.convex_particle.uuid,
                self.inputs.convex_particle.filename,
                self.inputs.convex_particle.filename,
            ),
                            ]
        else:

            calcinfo.retrieve_list = [self.metadata.options.output_filename,
                        self.metadata.options.aspherix_simulation_pvd,
                        self.metadata.options.aspherix_restart_file]

        calcinfo.retrieve_temporary_list = ['./micro/post',"commonData"]

        return calcinfo
