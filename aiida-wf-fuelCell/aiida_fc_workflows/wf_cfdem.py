"""Implementation of the MultiplyAddWorkChain for testing and demonstration purposes."""
from aiida.engine import ToContext, WorkChain
from aiida.orm import AbstractCode, Dict,List,FolderData,Str,Float,SinglefileData,Int
from aiida.plugins.factories import CalculationFactory,DataFactory
import pdb
PorosityCalibration = CalculationFactory('fc_calibration.porosity')
ResistivityCalibration = CalculationFactory('fc_calibration.resistivity')
ThConductivityCalibration = CalculationFactory('fc_calibration.th_conductivity')

AspherixInsertion = CalculationFactory('aspherix.insertion_compression')
CfdemCal=CalculationFactory("cfdem.run")
AsxParameters=DataFactory("aspherix.parameters")


class InsertionAndComputation(WorkChain):
    """WorkChain to multiply two numbers and add a third, for testing and demonstration purposes."""

    @classmethod
    def define(cls, spec):
        """Specify inputs and outputs."""
        super().define(spec)

        spec.input('CalcParameters', valid_type=AsxParameters)
        spec.input('CalcParametersMacro', valid_type=AsxParameters)

        spec.input('problemParameters', valid_type=Dict)
        spec.input('measured', valid_type=Dict)
        spec.input('asx', valid_type=AbstractCode)
        spec.input('cfdem', valid_type=AbstractCode)
        spec.input('py', valid_type=AbstractCode)

        spec.outline(
            cls.calibration_porosity,
            cls.insertion_macro,
            cls.calibration_resistivity,
            cls.calibration_th,
            cls.cfdem,
            cls.result,
        )
        spec.output('result', valid_type=SinglefileData)
        spec.exit_code(400, 'ERROR_NEGATIVE_NUMBER', message='The result is a negative number.')

    def calibration_porosity(self):
        asxData=self.inputs.CalcParameters
        porosityMeasured=self.inputs.measured["porosityMeasured"]
        inputs = {
            "code": self.inputs.py,
            "quantity_obj": Float(porosityMeasured),
            "max_iter": Int(2),
            "AsxParametersMicro": asxData,
            "metadata": {
                "description": "Test job submission with the aiida_aspherix plugin",
            },
        }
        future = self.submit(PorosityCalibration, **inputs)

        return ToContext(porosity=future)


    def insertion_macro(self):
        asxData=self.inputs.CalcParametersMacro

        inputs = {
            "code": self.inputs.asx,
            "folder_mesh":FolderData(tree=asxData._folder_mesh),
            "mesh_list":List(asxData._meshes_list),
            "shape":Str(asxData._shape),
            "convex_particle": SinglefileData(asxData._convex_particle),
            "particle_distribution":Dict(asxData._particle_distribution),
            "insertion_parameters":Dict(asxData._insertion_par),
            "domain": Dict(asxData._domain),
            "materials_list": Dict(asxData._mat_prop),
            "particle_template_list": Dict(asxData._part_temp_dict),
            "metadata": {
                "description": "Test job submission with the aiida_aspherix plugin",
            },
         }
        future = self.submit(AspherixInsertion, **inputs)

        return ToContext(insertion=future)



    def calibration_resistivity(self):
        aspherix_data_macro=self.inputs.CalcParametersMacro
        aspherix_data=self.inputs.CalcParameters
        restart_file_macro =  self.ctx.insertion.outputs.restart_file
        restart_file_micro =  self.ctx.porosity.outputs.restart_file

        resistivityMeasured=self.inputs.measured["resistivityMeasured"]
        inputs = {
            "code": self.inputs.py,
            "quantity_obj": Float(resistivityMeasured),
            "convex_particle": SinglefileData(file=aspherix_data_macro._convex_particle),
            "restart_file_micro": restart_file_micro,
            "restart_file_macro": restart_file_macro,
            "max_iter": Int(1),
            "AsxParametersMicro": aspherix_data,
            "AsxParametersMacro": aspherix_data_macro,
            "metadata": {
                "description": "Test job submission with the aiida_aspherix plugin",
            },
        }
        future = self.submit(ResistivityCalibration, **inputs)

        return ToContext(resistivity=future)

    def calibration_th(self):
        aspherix_data_macro=self.inputs.CalcParametersMacro
        aspherix_data=self.inputs.CalcParameters
        restart_file_macro =  self.ctx.insertion.outputs.restart_file
        restart_file_micro =  self.ctx.porosity.outputs.restart_file

        thConductivityMeasured=self.inputs.measured["thConductivityMeasured"]
        inputs = {
            "code": self.inputs.py,
            "quantity_obj": Float(thConductivityMeasured),
            "convex_particle": SinglefileData(file=aspherix_data_macro._convex_particle),
            "restart_file_micro": restart_file_micro,
            "restart_file_macro": restart_file_macro,
            "max_iter": Int(1),
            "AsxParametersMicro": aspherix_data,
            "AsxParametersMacro": aspherix_data_macro,
            "metadata": {
                "description": "Test job submission with the aiida_aspherix plugin",
            },
        }
        future = self.submit(ThConductivityCalibration, **inputs)

        return ToContext(th_conductivity=future)




    def cfdem(self):
        res_info=self.ctx.resistivity.outputs.calibrated_variables
        th_info=self.ctx.th_conductivity.outputs.calibrated_variables

        restart_file =  self.ctx.porosity.outputs.restart_file
        asxData = self.inputs.CalcParameters
        problemDict=self.inputs.problemParameters.get_dict()
        asxData._mat_prop["part_mat"]["contactResistancePrefactor"]=res_info["PrefactorRmicro"]
        asxData._mat_prop["part_mat"]["thermalConductivity"]=th_info["ThermalCondMicro"]

        inputs = {
            "code": self.inputs.cfdem,
            "restart_file":restart_file,
            "solver":Str(problemDict["solver"]),
            "deltaV":Float(problemDict["deltaV"]),
            "OxigenVelocity":List(problemDict["OxigenVelocity"]),
            "SteamVelocity":List(problemDict["SteamVelocity"]),
            "folder_mesh":FolderData(tree=asxData._folder_mesh),
            "mesh_list":List(asxData._meshes_list),
            "shape":Str(asxData._shape),
            "particle_distribution":Dict(asxData._particle_distribution),
            "insertion_parameters":Dict({}),
            "res_calibrated_variables":self.ctx.resistivity.outputs.calibrated_variables,
            "th_calibrated_variables":self.ctx.th_conductivity.outputs.calibrated_variables,
            "domain": Dict(asxData._domain),
            "materials_list": Dict(asxData._mat_prop),
            "particle_template_list": Dict(asxData._part_temp_dict),
            "metadata": {
                "description": "Test job submission with the aiida_aspherix plugin",
                    },
            }
        future = self.submit(CfdemCal, **inputs)

        return ToContext(cfdem=future)

    def result(self):
        """Add the result to the outputs."""
        self.out('result',self.ctx.cfdem.outputs.restart_file)
