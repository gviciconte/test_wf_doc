"""
Parsers provided by aiida_Aspherix.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
from aiida.common import exceptions
from aiida.engine import ExitCode
from aiida.orm import SinglefileData, Dict
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory, DataFactory
import pdb
from aiida_fc_calibration.common.functions import getParticles
import re
from aiida_fc_calibration.data import AspherixPositions

import pathlib




class PorosityParser(Parser):
    """
    Parser class for parsing output of calculation.
    """

    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a DiffCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.nodes.process.process.ProcessNode`
        """
        super().__init__(node)


    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        
        output_filename = self.node.get_option("output_filename")
        pvd_filename = self.node.get_option("aspherix_simulation_name")
        # Check that folder content is as expected
        files_retrieved = self.retrieved.base.repository.list_object_names()
        
        #
        files_expected = [output_filename]
        # Note: set(A) <= set(B) checks whether A is a subset of B
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error(
                f"Found files '{files_retrieved}', expected to find '{files_expected}'"
            )
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        # add output file
        self.logger.info(f"Parsing '{output_filename}'")
        with self.retrieved.base.repository.open(output_filename, "rb") as handle:
            output_node = SinglefileData(file=handle)
        self.out("log", output_node)
        
        # add output file
        self.logger.info(f"Parsing '{pvd_filename}'")
        with self.retrieved.base.repository.open(pvd_filename, "rb") as handle:
            pvd_node = SinglefileData(file=handle)
            
        if "restart.latest" in files_retrieved:
            # add output file
            self.logger.info(f"Parsing '{pvd_filename}'")
            with self.retrieved.base.repository.open("restart.latest", "rb") as handle:
                restart_node = SinglefileData(file=handle)
            self.out("restart_file", restart_node)
        
        
        post_folder=None
        retrieved_temporary_folder = kwargs['retrieved_temporary_folder']
        if retrieved_temporary_folder is not None:
            retrieved_temporary_folder = pathlib.Path(retrieved_temporary_folder)  # Optional to use the modern `pathlib` module instead of `os`.
            for subpath in retrieved_temporary_folder.iterdir():
                #
                if subpath.name== self.node.get_option("aspherix_simulation_post"):
                    post_folder=str(subpath)
        if post_folder is  None:
            raise Exception("no post folder")


            
        points=self.parse_pvd(pvd_node,post_folder)
        points_info = AspherixPositions(positions=points)
        #
        self.out("aspherix_points_info", points_info)
        #pdb.set_trace()
        return ExitCode(0)

    def parse_pvd(self,pvd_node,post_folder):
        file=pvd_node.get_content()
        #pdb.set_trace()
        file_vtm = re.match(r'(?s).*file="(.*)"/>', file).group(1)
        readerVTM=getParticles(post_folder+"/"+file_vtm)
        points = readerVTM.GetPoints()
        type = readerVTM.GetPointData().GetAbstractArray("type")
        typeV=[]
        pointsV=[]
        for nta in range(0,type.GetNumberOfValues()): 
            typeV.append(type.GetValue(nta))
            pointsV.append(points.GetPoint(nta))
        return pointsV

def recover_variables(folder):
    match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
    varOut={}
    with open(f"{folder}/variablesMicro")  as file:
            data = file.readlines()
    variablesMi=["PrefactorRmicro","ThermalCondMicro"]
    for variable in variablesMi:
        for line in  data:
            if line.startswith(f"variable {variable}"):
                match=(re.findall(match_number, line))
                varOut[variable]=float(match[0])
    with open(f"{folder}/variablesMacro")  as file:
            data = file.readlines()
    variablesMi=["PrefactorRmacro","ThermalCondMacro"]
    for variable in variablesMi:
        for line in  data:
            if line.startswith(f"variable {variable}"):
                match=(re.findall(match_number, line))
                varOut[variable]=float(match[0])
    
    return varOut

class CalibrationParser(Parser):
    """
    Parser class for parsing output of calculation.
    """

    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a DiffCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.nodes.process.process.ProcessNode`
        """
        super().__init__(node)


    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        
        output_filename = self.node.get_option("output_filename")
        files_retrieved = self.retrieved.base.repository.list_object_names()
        
        files_expected = [output_filename]
        # Note: set(A) <= set(B) checks whether A is a subset of B
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error(
                f"Found files '{files_retrieved}', expected to find '{files_expected}'"
            )
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        # add output file
        self.logger.info(f"Parsing '{output_filename}'")
        with self.retrieved.base.repository.open(output_filename, "rb") as handle:
            output_node = SinglefileData(file=handle)
        self.out("log", output_node)
    
        
        data_folder=None
        retrieved_temporary_folder = kwargs['retrieved_temporary_folder']
        if retrieved_temporary_folder is not None:
            retrieved_temporary_folder = pathlib.Path(retrieved_temporary_folder)  # Optional to use the modern `pathlib` module instead of `os`.
            for subpath in retrieved_temporary_folder.iterdir():
                #
                if subpath.name== "commonData":
                    data_folder=str(subpath)
        if data_folder is  None:
            raise Exception("no commonData folder")

        var=recover_variables(data_folder)
        variables = Dict(var)
        #
        self.out("calibrated_variables", variables)

        return ExitCode(0)

                    

        
