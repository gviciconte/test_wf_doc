"""
Calculations provided by aiida_diff.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""
from aiida.common import datastructures
from aiida.engine import CalcJob
from aiida.orm import SinglefileData, Dict,Str,FolderData,List
from aiida.plugins import DataFactory
from aiida_aspherix.data import AspherixPositionsAndType
from aiida_aspherix.common.functions import *
import pdb


class AspherixCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping the diff executable.

    Simple AiiDA plugin wrapper for 'diffing' two files.
    """
    _INPUT_FILE_NAME="input.asx"
    _cmdline_params = ("-in", _INPUT_FILE_NAME)
    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        super().define(spec)

        # set default values for AiiDA options
        spec.inputs["metadata"]["options"]["resources"].default = {
            "num_machines": 1,
            "num_mpiprocs_per_machine": 1,
        }
        spec.inputs["metadata"]["options"]["withmpi"].default = False

        # new ports
        spec.input(
            "metadata.options.output_filename", valid_type=str, default="asx.out"
        )
        spec.input(
            "metadata.options.aspherix_simulation_pvd", valid_type=str, default="post/aspherix_simulation.pvd"
        )
        spec.input(
            "metadata.options.aspherix_simulation_post", valid_type=str, default="post"
        )
        spec.input(
        "metadata.options.aspherix_simulation_name", valid_type=str, default="aspherix_simulation.pvd"
        )
        spec.input(
            "metadata.options.aspherix_restart_file", valid_type=str, default="restart/restart.latest"
        )

        spec.input("domain", valid_type=Dict, help="calculation domain")

        spec.input("materials_list", valid_type=Dict, help="material parameters")

        spec.input("insertion_parameters", valid_type=Dict, help="insertion parameters")

        spec.input("shape", valid_type=Str, help="shape")

        spec.input("mesh_list", valid_type=List, help="list of meshes dict",required=False)

        spec.input("particle_template_list", valid_type=Dict, help="dictionary containing particle template parameters")

        spec.input("particle_distribution", valid_type=Dict, help="dictionary containing particle distribution parameters")

        spec.input("folder_mesh", valid_type=FolderData, help="folder containing meshfile",required=False)

        spec.input(
            "convex_particle", valid_type=SinglefileData, help="convex particle stl file.",required=False
        )
        spec.output(
            "log",
            valid_type=SinglefileData,
            help="log file.",
        )
        spec.output(
            "aspherix_simulation_pvd",
            valid_type=SinglefileData,
            help="aspherix_simulation pvd file",
        )
        # spec.output(
        #     "aspherix_points_info",
        #     valid_type=AspherixPositionsAndType,
        #     help="info about points positions and type",
        # )
        spec.output(
            "aspherix_points_info",
            valid_type=Dict,
            help="info about points positions and type",
        )
        spec.output(
            "restart_file",
            valid_type=SinglefileData,
            help="aspherix restart file.",
        )
        spec.exit_code(
            300,
            "ERROR_MISSING_OUTPUT_FILES",
            message="Calculation did not produce all expected output files.",
        )


    @staticmethod
    def create_main_input_content(mat_param_list,domain,particle_template_list,shape,ins_par,**kwargs):
        raise NotImplementedError



    def prepare_for_submission(self, folder):
        """
        Create input files.
        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files
            needed by the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        #pdb.set_trace()
        if "mesh_list" in self.inputs:
             input_txt =self.create_main_input_content(self.inputs.materials_list.get_dict(),
                                        self.inputs.domain.get_dict(),
                                        self.inputs.particle_template_list.get_dict(),
                                        self.inputs.shape.value,
                                        self.inputs.insertion_parameters.get_dict(),
                                        self.inputs.particle_distribution.get_dict(),
                                        mesh_list=self.inputs.mesh_list.get_list())
        else:
            input_txt =self.create_main_input_content(self.inputs.materials_list.get_dict(),
                                                    self.inputs.domain.get_dict(),
                                                    self.inputs.particle_template_list.get_dict(),
                                                    self.inputs.shape.value,
                                                    self.inputs.insertion_parameters.get_dict(),
                                                    self.inputs.particle_distribution.get_dict()
                                                    )





        input_filename = folder.get_abs_path(self._INPUT_FILE_NAME)

        with open(input_filename, "w") as infile:
            infile.write(input_txt)

        write_bottom(folder.get_abs_path(""),self.inputs.domain.get_dict())
        write_plate(folder.get_abs_path(""),self.inputs.domain.get_dict())

        codeinfo = datastructures.CodeInfo()
        codeinfo.cmdline_params = list(self._cmdline_params)
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.stdout_name = self.metadata.options.output_filename
        codeinfo.withmpi = self.inputs.metadata.options.withmpi



        # Prepare a `CalcInfo` to be returned to the engine
        calcinfo = datastructures.CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.retrieve_list = [self.metadata.options.output_filename,
            self.metadata.options.aspherix_simulation_pvd,
            self.metadata.options.aspherix_restart_file]
        calcinfo.retrieve_temporary_list = ['./post']
        calcinfo.local_copy_list = []
        #pdb.set_trace()
        if "convex_particle" in self.inputs:
            calcinfo.local_copy_list = [
                (
                    self.inputs.convex_particle.uuid,
                    self.inputs.convex_particle.filename,
                    self.inputs.convex_particle.filename,
                ),
                ]

        if "folder_mesh" in self.inputs:
            def _get_local_file_info(filename):
                return (self.inputs.folder_mesh.uuid, filename, filename)

            for filename in self.inputs.folder_mesh.list_object_names():
                    calcinfo.local_copy_list.append(_get_local_file_info(filename))




        return calcinfo
